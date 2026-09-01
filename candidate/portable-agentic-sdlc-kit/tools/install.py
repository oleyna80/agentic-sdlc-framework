#!/usr/bin/env python3
"""Fail-closed installer for the noncanonical Portable Agentic SDLC Kit.

The command deliberately has a small surface:

    python3 tools/install.py plan --target <repository>
    python3 tools/install.py apply --target <repository>

``plan`` never writes to the target.  ``apply`` rebuilds and compares the plan
immediately before staging or publishing any bytes.  This is compensating
rollback, not a claim of filesystem-wide transactional atomicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable


EXIT_INVALID = 2
MANIFEST_SCHEMA = 1
WINDOWS_RESERVED = re.compile(r"[<>:\"|?*]")
WINDOWS_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


class InstallerError(Exception):
    """A deterministic, safe failure that should be shown to the operator."""


class ManifestError(InstallerError):
    """The package manifest cannot safely describe an installation."""


@dataclass(frozen=True)
class PackageManifest:
    package_identity: str
    schema_version: int
    repository_revision: str
    payload_root: str
    approved_create_paths: tuple[str, ...]
    manifest_path: Path


@dataclass(frozen=True)
class PlanAction:
    path: str
    action: str
    source_sha256: str | None
    reason: str | None = None


@dataclass(frozen=True)
class InstallPlan:
    target_root: str
    manifest_digest: str
    plan_identity: str
    actions: tuple[PlanAction, ...]

    @property
    def blocking_actions(self) -> tuple[PlanAction, ...]:
        return tuple(action for action in self.actions if action.action in {"collision", "blocked"})

    def to_dict(self) -> dict[str, object]:
        return {
            "target_root": self.target_root,
            "manifest_digest": self.manifest_digest,
            "plan_identity": self.plan_identity,
            "actions": [asdict(action) for action in self.actions],
            "ready": not self.blocking_actions,
        }


@dataclass(frozen=True)
class ApplyResult:
    success: bool
    plan_identity: str
    created_paths: tuple[str, ...]
    skipped_paths: tuple[str, ...]
    collision_paths: tuple[str, ...]
    blocked_paths: tuple[str, ...]
    residual_paths: tuple[str, ...]
    diagnostic: str | None = None
    recovery_instructions: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "success": self.success,
            "plan_identity": self.plan_identity,
            "created_paths": list(self.created_paths),
            "skipped_paths": list(self.skipped_paths),
            "collision_paths": list(self.collision_paths),
            "blocked_paths": list(self.blocked_paths),
            "residual_paths": list(self.residual_paths),
            "diagnostic": self.diagnostic,
            "recovery_instructions": self.recovery_instructions,
        }


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _validate_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ManifestError("manifest path must be a non-empty string")
    if "\x00" in value:
        raise ManifestError(f"manifest path contains NUL: {value!r}")
    if "\\" in value:
        raise ManifestError(f"manifest path uses a non-portable backslash: {value!r}")
    if value.startswith("//") or value.startswith("\\\\"):
        raise ManifestError(f"manifest path is a network root: {value!r}")
    if re.match(r"^[A-Za-z]:", value):
        raise ManifestError(f"manifest path has a Windows drive prefix: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute():
        raise ManifestError(f"manifest path is absolute: {value!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ManifestError(f"manifest path is not normalized: {value!r}")
    if path.as_posix() != value:
        raise ManifestError(f"manifest path is not normalized: {value!r}")
    if any(WINDOWS_RESERVED.search(part) for part in path.parts):
        raise ManifestError(f"manifest path contains invalid platform characters: {value!r}")
    for component in path.parts:
        if component.rstrip(" .") != component:
            raise ManifestError(f"manifest path has a Windows-trimmed component: {value!r}")
        device_stem = component.split(".", 1)[0].upper()
        if device_stem in WINDOWS_DEVICE_NAMES:
            raise ManifestError(f"manifest path has a Windows reserved device component: {value!r}")
    return value


def load_manifest(manifest_path: Path | None = None) -> PackageManifest:
    """Load and validate the package's deterministic, explicit file manifest."""
    resolved_manifest = (manifest_path or Path(__file__).resolve().parent.parent / "package-manifest.json").resolve()
    try:
        raw = json.loads(resolved_manifest.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ManifestError(f"cannot read manifest: {resolved_manifest}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"manifest is not valid JSON: {exc.msg}") from exc

    if not isinstance(raw, dict):
        raise ManifestError("manifest root must be an object")
    if raw.get("manifest_schema") != MANIFEST_SCHEMA:
        raise ManifestError(f"unsupported manifest_schema: {raw.get('manifest_schema')!r}")
    package_identity = raw.get("package_identity")
    revision = raw.get("repository_revision")
    payload_root = raw.get("payload_root")
    approved = raw.get("approved_create_paths")
    if not isinstance(package_identity, str) or not package_identity:
        raise ManifestError("manifest package_identity must be a non-empty string")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ManifestError("manifest repository_revision must be a 40-character lowercase Git SHA")
    if payload_root != "template":
        raise ManifestError("manifest payload_root must be exactly 'template'")
    if not isinstance(approved, list) or not approved:
        raise ManifestError("manifest approved_create_paths must be a non-empty list")
    paths = tuple(_validate_relative_path(item) for item in approved)
    if tuple(sorted(paths)) != paths or len(set(paths)) != len(paths):
        raise ManifestError("manifest approved_create_paths must be unique and lexicographically sorted")
    if len({path.casefold() for path in paths}) != len(paths):
        raise ManifestError("manifest approved_create_paths must not collide under Windows case folding")
    return PackageManifest(package_identity, MANIFEST_SCHEMA, revision, payload_root, paths, resolved_manifest)


def _resolve_target(target: Path | str) -> Path:
    target_path = Path(target)
    try:
        resolved = target_path.resolve(strict=True)
    except OSError as exc:
        raise InstallerError(f"target root cannot be resolved: {target_path}") from exc
    if not resolved.is_dir():
        raise InstallerError(f"target root is not a directory: {resolved}")
    return resolved


def _source_path(manifest: PackageManifest, relative_path: str) -> Path:
    payload_root = (manifest.manifest_path.parent / manifest.payload_root).resolve(strict=True)
    source = manifest.manifest_path.parent / manifest.payload_root / relative_path
    try:
        resolved = source.resolve(strict=True)
    except OSError as exc:
        raise ManifestError(f"approved source is missing: {relative_path}") from exc
    if not _is_within(resolved, payload_root):
        raise ManifestError(f"approved source escapes payload root: {relative_path}")
    mode = resolved.stat().st_mode
    if not stat.S_ISREG(mode):
        raise ManifestError(f"approved source is not a regular file: {relative_path}")
    return resolved


def _destination_safety(target_root: Path, relative_path: str) -> tuple[Path, str | None]:
    destination = target_root.joinpath(*PurePosixPath(relative_path).parts)
    if not _is_within(destination, target_root):
        return destination, "destination escapes target root"
    current = target_root
    for component in PurePosixPath(relative_path).parts[:-1]:
        current = current / component
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode):
            return destination, f"destination parent is a symlink: {current.relative_to(target_root).as_posix()}"
        if not stat.S_ISDIR(info.st_mode):
            return destination, f"destination parent is not a directory: {current.relative_to(target_root).as_posix()}"
    return destination, None


def _classify_destination(target_root: Path, source: Path, relative_path: str) -> PlanAction:
    destination, unsafe = _destination_safety(target_root, relative_path)
    source_digest = _sha256_file(source)
    if unsafe:
        return PlanAction(relative_path, "blocked", source_digest, unsafe)
    try:
        info = destination.lstat()
    except FileNotFoundError:
        return PlanAction(relative_path, "create", source_digest)
    if stat.S_ISREG(info.st_mode):
        if _sha256_file(destination) == source_digest:
            return PlanAction(relative_path, "skip-identical", source_digest)
        return PlanAction(relative_path, "collision", source_digest, "destination file differs")
    if stat.S_ISLNK(info.st_mode):
        return PlanAction(relative_path, "collision", source_digest, "destination is a symlink")
    return PlanAction(relative_path, "collision", source_digest, "destination is not a regular file")


def build_plan(target: Path | str, manifest_path: Path | None = None) -> InstallPlan:
    """Create a complete non-mutating installation plan."""
    manifest = load_manifest(manifest_path)
    target_root = _resolve_target(target)
    actions = tuple(
        _classify_destination(target_root, _source_path(manifest, relative_path), relative_path)
        for relative_path in manifest.approved_create_paths
    )
    manifest_digest = _sha256_file(manifest.manifest_path)
    identity_input = {
        "manifest_digest": manifest_digest,
        "target_root": str(target_root),
        "actions": [asdict(action) for action in actions],
    }
    return InstallPlan(str(target_root), manifest_digest, _sha256_bytes(_canonical_json(identity_input)), actions)


def _result_from_plan(plan: InstallPlan, diagnostic: str) -> ApplyResult:
    return ApplyResult(
        success=False,
        plan_identity=plan.plan_identity,
        created_paths=(),
        skipped_paths=tuple(action.path for action in plan.actions if action.action == "skip-identical"),
        collision_paths=tuple(action.path for action in plan.actions if action.action == "collision"),
        blocked_paths=tuple(action.path for action in plan.actions if action.action == "blocked"),
        residual_paths=(),
        diagnostic=diagnostic,
    )


def _descriptor_publication_supported() -> bool:
    """Return whether this host can publish without following target symlinks."""
    required = (os.open, os.mkdir, os.stat, os.unlink)
    return hasattr(os, "O_NOFOLLOW") and all(operation in os.supports_dir_fd for operation in required)


def _open_target_fd(target_root: Path) -> int:
    if not _descriptor_publication_supported():
        raise OSError("safe descriptor-relative publication is unavailable on this platform")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    return os.open(target_root, flags)


def _open_destination_parent(
    target_fd: int,
    relative_path: str,
    created_dirs: list[str],
    *,
    create_missing: bool = True,
) -> tuple[int, str]:
    """Open a destination parent without following any path component.

    Each descent is relative to an already-open directory descriptor.  A
    directory swapped for a symlink after planning is therefore rejected rather
    than followed during publication.
    """
    parts = PurePosixPath(relative_path).parts
    current_fd = os.dup(target_fd)
    traversed: list[str] = []
    try:
        for component in parts[:-1]:
            traversed.append(component)
            try:
                info = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
            except FileNotFoundError:
                if not create_missing:
                    raise
                os.mkdir(component, dir_fd=current_fd)
                created_dirs.append("/".join(traversed))
                info = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise OSError(f"unsafe destination parent during publication: {'/'.join(traversed)}")
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current_fd)
            os.close(current_fd)
            current_fd = next_fd
        return current_fd, parts[-1]
    except BaseException:
        os.close(current_fd)
        raise


def _unlink_created(target_fd: int, relative_path: str, is_directory: bool) -> None:
    """Remove a recorded artifact only through the original target descriptor.

    ``target_fd`` remains open from publication through rollback.  In
    particular, rollback must not reopen ``target_root`` by pathname: an
    operator may replace that directory after publication starts, and a
    pathname reopen could then remove an artifact owned by the replacement.
    """
    parent_fd = -1
    try:
        parent_fd, name = _open_destination_parent(target_fd, relative_path, [], create_missing=False)
        if is_directory:
            os.rmdir(name, dir_fd=parent_fd)
        else:
            os.unlink(name, dir_fd=parent_fd)
    finally:
        if parent_fd >= 0:
            os.close(parent_fd)


def _rollback(
    target_fd: int,
    target_root: Path,
    created_files: Iterable[str],
    created_dirs: Iterable[str],
    rollback_failure_injector: Callable[[Path], bool] | None,
) -> tuple[str, ...]:
    residuals: list[str] = []
    for relative_path in reversed(tuple(created_files)):
        path = target_root.joinpath(*PurePosixPath(relative_path).parts)
        try:
            if rollback_failure_injector and rollback_failure_injector(path):
                raise OSError("injected rollback failure")
            _unlink_created(target_fd, relative_path, is_directory=False)
        except OSError:
            residuals.append(str(path))
    for relative_path in reversed(tuple(created_dirs)):
        path = target_root.joinpath(*PurePosixPath(relative_path).parts)
        try:
            if rollback_failure_injector and rollback_failure_injector(path):
                raise OSError("injected rollback failure")
            _unlink_created(target_fd, relative_path, is_directory=True)
        except OSError:
            residuals.append(str(path))
    return tuple(residuals)


def _create_external_stage_dir(target_root: Path) -> Path:
    """Create staging outside the resolved target, even with hostile TMPDIR."""
    candidates = (Path(tempfile.gettempdir()), target_root.parent)
    for candidate in candidates:
        try:
            resolved_candidate = candidate.resolve(strict=True)
        except OSError:
            continue
        if not resolved_candidate.is_dir() or _is_within(resolved_candidate, target_root):
            continue
        try:
            stage_root = Path(tempfile.mkdtemp(prefix="portable-kit-stage-", dir=resolved_candidate))
            if _is_within(stage_root.resolve(strict=True), target_root):
                stage_root.rmdir()
                continue
            return stage_root
        except OSError:
            continue
    raise OSError("cannot create staging outside the resolved target root")


def apply_plan(
    plan: InstallPlan,
    manifest_path: Path | None = None,
    failure_injector: Callable[[Path], None] | None = None,
    rollback_failure_injector: Callable[[Path], bool] | None = None,
    before_publish_injector: Callable[[str], None] | None = None,
) -> ApplyResult:
    """Revalidate, stage, and publish a plan without touching pre-existing files.

    The two injectors are intentionally internal test seams.  The command-line
    interface never enables them; fixtures use them to exercise real publication
    and recovery code deterministically.
    """
    try:
        manifest = load_manifest(manifest_path)
        refreshed = build_plan(Path(plan.target_root), manifest.manifest_path)
    except InstallerError as exc:
        return _result_from_plan(plan, f"apply revalidation failed: {exc}")
    if refreshed != plan:
        return _result_from_plan(refreshed, "apply revalidation failed: plan changed before publication")
    if plan.blocking_actions:
        return _result_from_plan(plan, "apply blocked by collision or unsafe destination")

    target_root = Path(plan.target_root)
    create_actions = tuple(action for action in plan.actions if action.action == "create")
    skipped = tuple(action.path for action in plan.actions if action.action == "skip-identical")
    created_files: list[str] = []
    created_dirs: list[str] = []
    stage_root: Path | None = None
    target_fd = -1
    try:
        stage_root = _create_external_stage_dir(target_root)
        for action in create_actions:
            source = _source_path(manifest, action.path)
            staged = stage_root.joinpath(*PurePosixPath(action.path).parts)
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, staged)
            if _sha256_file(staged) != action.source_sha256:
                raise OSError(f"staged bytes changed for {action.path}")
        target_fd = _open_target_fd(target_root)
        for action in create_actions:
            if before_publish_injector:
                before_publish_injector(action.path)
            parent_fd = -1
            try:
                parent_fd, name = _open_destination_parent(target_fd, action.path, created_dirs)
                output_fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o666, dir_fd=parent_fd)
                destination = target_root.joinpath(*PurePosixPath(action.path).parts)
                source = stage_root.joinpath(*PurePosixPath(action.path).parts)
                with os.fdopen(output_fd, "wb") as output_handle, source.open("rb") as input_handle:
                    shutil.copyfileobj(input_handle, output_handle)
                created_files.append(action.path)
                if failure_injector:
                    failure_injector(destination)
            finally:
                if parent_fd >= 0:
                    os.close(parent_fd)
    except OSError as exc:
        residuals = _rollback(target_fd, target_root, created_files, created_dirs, rollback_failure_injector) if target_fd >= 0 else ()
        recovery = None
        if residuals:
            recovery = "Remove only these residual paths after inspection: " + ", ".join(residuals)
        return ApplyResult(
            success=False,
            plan_identity=plan.plan_identity,
            created_paths=tuple(
                str(target_root.joinpath(*PurePosixPath(path).parts))
                for path in created_files
                if str(target_root.joinpath(*PurePosixPath(path).parts)) not in residuals
            ),
            skipped_paths=skipped,
            collision_paths=(),
            blocked_paths=(),
            residual_paths=residuals,
            diagnostic=f"publication failed: {exc}",
            recovery_instructions=recovery,
        )
    finally:
        if target_fd >= 0:
            os.close(target_fd)
        if stage_root is not None:
            try:
                shutil.rmtree(stage_root)
            except OSError:
                # Staging is outside the target and an operator-visible failure
                # is preferable to reporting a successful publication with junk.
                pass
    return ApplyResult(
        success=True,
        plan_identity=plan.plan_identity,
        created_paths=tuple(str(target_root.joinpath(*PurePosixPath(action.path).parts)) for action in create_actions),
        skipped_paths=skipped,
        collision_paths=(),
        blocked_paths=(),
        residual_paths=(),
    )


def apply_target(target: Path | str, manifest_path: Path | None = None) -> ApplyResult:
    """Build and immediately revalidate a plan for the command-line apply mode."""
    try:
        plan = build_plan(target, manifest_path)
    except InstallerError as exc:
        return ApplyResult(False, "", (), (), (), (), (), f"plan failed: {exc}")
    return apply_plan(plan, manifest_path)


def _emit(value: dict[str, object]) -> None:
    print(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "apply"))
    parser.add_argument("--target", required=True, help="existing repository directory to receive candidate payload")
    args = parser.parse_args(argv)
    if args.command == "plan":
        try:
            plan = build_plan(args.target)
        except InstallerError as exc:
            _emit({"ready": False, "diagnostic": str(exc)})
            return EXIT_INVALID
        _emit(plan.to_dict())
        return 0 if not plan.blocking_actions else EXIT_INVALID
    result = apply_target(args.target)
    _emit(result.to_dict())
    return 0 if result.success else EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())
