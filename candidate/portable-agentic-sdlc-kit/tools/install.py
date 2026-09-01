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


@dataclass
class _PublishedArtifact:
    """An installer-created object bound to the descriptor that named it.

    The retained parent descriptor is deliberately part of the rollback proof.
    A relative pathname can be rebound by an operator after publication starts;
    that pathname must never be reopened to decide what rollback may remove.
    """

    relative_path: str
    parent_fd: int
    name: str
    is_directory: bool
    device: int
    inode: int


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
    created_dirs: list[_PublishedArtifact],
    parent_identities: dict[str, tuple[int, int] | None],
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
            parent_path = "/".join(traversed)
            expected_identity = parent_identities[parent_path]
            try:
                info = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
            except FileNotFoundError:
                if expected_identity is not None:
                    raise OSError(f"destination parent changed during publication: {parent_path}")
                if not create_missing:
                    raise
                os.mkdir(component, dir_fd=current_fd)
                info = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
                created_dirs.append(
                    _PublishedArtifact(
                        relative_path="/".join(traversed),
                        parent_fd=os.dup(current_fd),
                        name=component,
                        is_directory=True,
                        device=info.st_dev,
                        inode=info.st_ino,
                    )
                )
                parent_identities[parent_path] = (info.st_dev, info.st_ino)
            if expected_identity is None and parent_path in parent_identities:
                # A parent that was absent during pre-publication binding must
                # be created by this publication, never adopted after a swap.
                expected_identity = parent_identities[parent_path]
            if (
                stat.S_ISLNK(info.st_mode)
                or not stat.S_ISDIR(info.st_mode)
                or expected_identity != (info.st_dev, info.st_ino)
            ):
                raise OSError(f"unsafe destination parent during publication: {parent_path}")
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current_fd)
            opened = os.fstat(next_fd)
            if (opened.st_dev, opened.st_ino) != expected_identity:
                os.close(next_fd)
                raise OSError(f"destination parent changed during publication: {parent_path}")
            os.close(current_fd)
            current_fd = next_fd
        return current_fd, parts[-1]
    except BaseException:
        os.close(current_fd)
        raise


def _descriptor_path(directory_fd: int) -> Path | None:
    """Return a proven current pathname for an already-open directory."""
    try:
        descriptor_stat = os.fstat(directory_fd)
        descriptor_link = os.readlink(f"/proc/self/fd/{directory_fd}")
        if not os.path.isabs(descriptor_link) or descriptor_link.endswith(" (deleted)"):
            return None
        reported_directory = Path(descriptor_link)
        path_stat = reported_directory.stat()
    except OSError:
        return None
    if (path_stat.st_dev, path_stat.st_ino) != (descriptor_stat.st_dev, descriptor_stat.st_ino):
        return None
    return reported_directory


def _artifact_identity_matches(artifact: _PublishedArtifact) -> bool:
    try:
        info = os.stat(artifact.name, dir_fd=artifact.parent_fd, follow_symlinks=False)
    except OSError:
        return False
    expected_type = stat.S_ISDIR if artifact.is_directory else stat.S_ISREG
    return expected_type(info.st_mode) and (info.st_dev, info.st_ino) == (artifact.device, artifact.inode)


def _reported_artifact_path(artifact: _PublishedArtifact) -> str:
    parent_path = _descriptor_path(artifact.parent_fd)
    if parent_path is not None and _artifact_identity_matches(artifact):
        return str(parent_path / artifact.name)
    descriptor_stat = os.fstat(artifact.parent_fd)
    return (
        f"<unresolved created artifact dev={artifact.device} ino={artifact.inode} "
        f"parent-dev={descriptor_stat.st_dev} parent-ino={descriptor_stat.st_ino} "
        f"name={artifact.name!r}>"
    )


def _unlink_created(artifact: _PublishedArtifact) -> None:
    """Remove only the exact object created by this publication.

    The artifact's current directory entry must still have the recorded inode,
    device and type.  A replacement is an operator-owned object and causes a
    fail-closed rollback residual rather than an unlink/rmdir by pathname.
    """
    if not _artifact_identity_matches(artifact):
        raise OSError("created artifact identity cannot be proven during rollback")
    if artifact.is_directory:
        os.rmdir(artifact.name, dir_fd=artifact.parent_fd)
    else:
        os.unlink(artifact.name, dir_fd=artifact.parent_fd)


def _rollback(
    created_files: Iterable[_PublishedArtifact],
    created_dirs: Iterable[_PublishedArtifact],
    rollback_failure_injector: Callable[[Path], bool] | None,
) -> tuple[str, ...]:
    residuals: list[str] = []
    for artifact in reversed(tuple(created_files)):
        path = _reported_artifact_path(artifact)
        try:
            if rollback_failure_injector and rollback_failure_injector(Path(path)):
                raise OSError("injected rollback failure")
            _unlink_created(artifact)
        except OSError:
            residuals.append(path)
    for artifact in reversed(tuple(created_dirs)):
        path = _reported_artifact_path(artifact)
        try:
            if rollback_failure_injector and rollback_failure_injector(Path(path)):
                raise OSError("injected rollback failure")
            _unlink_created(artifact)
        except OSError:
            residuals.append(path)
    return tuple(residuals)


def _close_artifacts(artifacts: Iterable[_PublishedArtifact]) -> None:
    for artifact in artifacts:
        try:
            os.close(artifact.parent_fd)
        except OSError:
            pass


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


def _bind_parent_identities(target_fd: int, actions: Iterable[PlanAction]) -> dict[str, tuple[int, int] | None]:
    """Bind every required parent to its pre-publication directory identity.

    Missing parents are recorded as absent.  Publication may create those exact
    missing components but must fail if another actor supplies a directory in
    their place after this binding step.
    """
    identities: dict[str, tuple[int, int] | None] = {}
    for action in actions:
        current_fd = os.dup(target_fd)
        traversed: list[str] = []
        try:
            for component in PurePosixPath(action.path).parts[:-1]:
                traversed.append(component)
                parent_path = "/".join(traversed)
                try:
                    info = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
                except FileNotFoundError:
                    identities.setdefault(parent_path, None)
                    # Every deeper component is necessarily absent too.
                    for remaining in PurePosixPath(action.path).parts[len(traversed):-1]:
                        traversed.append(remaining)
                        identities.setdefault("/".join(traversed), None)
                    break
                if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                    raise OSError(f"unsafe destination parent during publication: {parent_path}")
                identity = (info.st_dev, info.st_ino)
                previous = identities.setdefault(parent_path, identity)
                if previous != identity:
                    raise OSError(f"destination parent changed during publication: {parent_path}")
                next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current_fd)
                opened = os.fstat(next_fd)
                if (opened.st_dev, opened.st_ino) != identity:
                    os.close(next_fd)
                    raise OSError(f"destination parent changed during publication: {parent_path}")
                os.close(current_fd)
                current_fd = next_fd
        finally:
            os.close(current_fd)
    return identities


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
    created_files: list[_PublishedArtifact] = []
    created_dirs: list[_PublishedArtifact] = []
    parent_identities: dict[str, tuple[int, int] | None] = {}
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
        parent_identities = _bind_parent_identities(target_fd, create_actions)
        for action in create_actions:
            if before_publish_injector:
                before_publish_injector(action.path)
            parent_fd = -1
            try:
                parent_fd, name = _open_destination_parent(
                    target_fd, action.path, created_dirs, parent_identities
                )
                output_fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o666, dir_fd=parent_fd)
                destination = target_root.joinpath(*PurePosixPath(action.path).parts)
                source = stage_root.joinpath(*PurePosixPath(action.path).parts)
                with os.fdopen(output_fd, "wb") as output_handle, source.open("rb") as input_handle:
                    shutil.copyfileobj(input_handle, output_handle)
                info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                created_files.append(
                    _PublishedArtifact(
                        relative_path=action.path,
                        parent_fd=os.dup(parent_fd),
                        name=name,
                        is_directory=False,
                        device=info.st_dev,
                        inode=info.st_ino,
                    )
                )
                if failure_injector:
                    failure_injector(destination)
            finally:
                if parent_fd >= 0:
                    os.close(parent_fd)
    except OSError as exc:
        residuals = (
            _rollback(created_files, created_dirs, rollback_failure_injector)
            if target_fd >= 0
            else ()
        )
        recovery = None
        if residuals:
            recovery = (
                "Do not remove paths beneath the current target pathname unless each "
                "reported artifact identity is independently proven. Inspect only these "
                "descriptor-bound residual locations before manual cleanup: " + ", ".join(residuals)
            )
        return ApplyResult(
            success=False,
            plan_identity=plan.plan_identity,
            created_paths=tuple(
                _reported_artifact_path(artifact)
                for artifact in created_files
                if _artifact_identity_matches(artifact)
                and _reported_artifact_path(artifact) not in residuals
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
        _close_artifacts(created_files)
        _close_artifacts(created_dirs)
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
