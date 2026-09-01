#!/usr/bin/env python3
"""Deterministic disposable-fixture coverage for the portable kit installer."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
INSTALL_PATH = PACKAGE_ROOT / "tools" / "install.py"
SPEC = importlib.util.spec_from_file_location("portable_kit_install", INSTALL_PATH)
assert SPEC and SPEC.loader
install = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install
SPEC.loader.exec_module(install)


class InstallerFixtureTests(unittest.TestCase):
    def make_package(self, root: Path, paths: list[str]) -> Path:
        package = root / "package"
        payload = package / "template"
        for relative in paths:
            destination = payload.joinpath(*relative.split("/"))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(f"payload:{relative}\n", encoding="utf-8")
        manifest = {
            "manifest_schema": 1,
            "package_identity": "fixture-package",
            "payload_root": "template",
            "repository_revision": "a" * 40,
            "approved_create_paths": sorted(paths),
        }
        manifest_path = package / "package-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return manifest_path

    def test_manifest_is_explicit_and_matches_payload(self) -> None:
        manifest = install.load_manifest()
        actual_files = sorted(
            path.relative_to(PACKAGE_ROOT / "template").as_posix()
            for path in (PACKAGE_ROOT / "template").rglob("*")
            if path.is_file()
        )
        self.assertEqual(list(manifest.approved_create_paths), actual_files)
        self.assertEqual(manifest.package_identity, "portable-agentic-sdlc-kit-candidate")
        self.assertEqual(manifest.repository_revision, "be988807c38543eb90a728fcb4349bc97dd5695a")

    def test_plan_is_non_mutating_and_cli_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            sentinel = target / "existing.txt"
            sentinel.write_bytes(b"leave me unchanged")
            before = sentinel.read_bytes()
            plan = install.build_plan(target)
            self.assertFalse(plan.blocking_actions)
            self.assertTrue(all(action.action == "create" for action in plan.actions))
            self.assertEqual(sentinel.read_bytes(), before)
            completed = subprocess.run(
                [sys.executable, str(INSTALL_PATH), "plan", "--target", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["plan_identity"], plan.plan_identity)
            self.assertEqual(sentinel.read_bytes(), before)

    def test_apply_creates_then_skips_identical_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            first = install.apply_target(target)
            self.assertTrue(first.success, first.diagnostic)
            self.assertTrue(first.created_paths)
            self.assertTrue((target / "AGENTS.md").is_file())
            second = install.apply_target(target)
            self.assertTrue(second.success, second.diagnostic)
            self.assertFalse(second.created_paths)
            self.assertEqual(len(second.skipped_paths), len(install.load_manifest().approved_create_paths))

    def test_collision_preserves_existing_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            existing = target / "AGENTS.md"
            existing.write_bytes(b"operator-owned content")
            plan = install.build_plan(target)
            collision = next(action for action in plan.actions if action.path == "AGENTS.md")
            self.assertEqual(collision.action, "collision")
            result = install.apply_plan(plan)
            self.assertFalse(result.success)
            self.assertIn("AGENTS.md", result.collision_paths)
            self.assertEqual(existing.read_bytes(), b"operator-owned content")

    def test_invalid_and_windows_style_paths_fail_closed(self) -> None:
        invalid_paths = [
            "../escape.txt",
            "/absolute.txt",
            "C:\\drive.txt",
            "\\\\server\\share.txt",
            "safe\\mixed.txt",
            "CON",
            "aux.txt",
            "Com1.log",
            "nested/LpT9.md",
            "trailing-dot.",
            "trailing-space ",
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            for index, invalid in enumerate(invalid_paths):
                manifest = self.make_package(root / str(index), [invalid])
                with self.assertRaises(install.ManifestError, msg=invalid):
                    install.build_plan(target, manifest)

    def test_windows_casefold_destination_collisions_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            manifest = self.make_package(root, ["Guide.md", "guide.md"])
            with self.assertRaises(install.ManifestError):
                install.build_plan(target, manifest)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable on this platform")
    def test_symlink_parent_escape_is_blocked_without_target_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            outside = root / "outside"
            target.mkdir()
            outside.mkdir()
            os.symlink(outside, target / "agentic")
            plan = install.build_plan(target)
            blocked = [action for action in plan.actions if action.path.startswith("agentic/")]
            self.assertTrue(blocked)
            self.assertTrue(all(action.action == "blocked" for action in blocked))
            result = install.apply_plan(plan)
            self.assertFalse(result.success)
            self.assertEqual(list(outside.iterdir()), [])

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable on this platform")
    def test_parent_symlink_swap_after_plan_fails_closed_without_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            outside = root / "outside"
            target.mkdir()
            outside.mkdir()
            (target / "nested").mkdir()
            manifest = self.make_package(root, ["nested/item.txt"])
            plan = install.build_plan(target, manifest)

            def swap_parent(relative_path: str) -> None:
                self.assertEqual(relative_path, "nested/item.txt")
                (target / "nested").rmdir()
                os.symlink(outside, target / "nested")

            result = install.apply_plan(plan, manifest, before_publish_injector=swap_parent)
            self.assertFalse(result.success)
            self.assertIn("unsafe destination parent", result.diagnostic or "")
            self.assertFalse((outside / "item.txt").exists())
            self.assertTrue((target / "nested").is_symlink())

    def test_staging_remains_outside_target_when_tempdir_points_at_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt"])
            plan = install.build_plan(target, manifest)
            original_tempdir = tempfile.tempdir
            try:
                tempfile.tempdir = str(target)
                result = install.apply_plan(plan, manifest)
            finally:
                tempfile.tempdir = original_tempdir
            self.assertTrue(result.success, result.diagnostic)
            self.assertEqual((target / "one.txt").read_text(encoding="utf-8"), "payload:one.txt\n")
            self.assertFalse(any(path.name.startswith("portable-kit-stage-") for path in target.iterdir()))

    def test_apply_rejects_target_drift_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt", "two.txt"])
            plan = install.build_plan(target, manifest)
            (target / "one.txt").write_text("operator drift", encoding="utf-8")
            result = install.apply_plan(plan, manifest)
            self.assertFalse(result.success)
            self.assertEqual(result.diagnostic, "apply revalidation failed: plan changed before publication")
            self.assertEqual((target / "one.txt").read_text(encoding="utf-8"), "operator drift")
            self.assertFalse((target / "two.txt").exists())

    def test_staged_publication_failure_rolls_back_only_created_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            operator_file = target / "operator.txt"
            operator_file.write_text("preserve", encoding="utf-8")
            manifest = self.make_package(root, ["one.txt", "two.txt"])
            plan = install.build_plan(target, manifest)

            def fail_after_second(path: Path) -> None:
                if path.name == "two.txt":
                    raise OSError("injected publication failure")

            result = install.apply_plan(plan, manifest, failure_injector=fail_after_second)
            self.assertFalse(result.success)
            self.assertEqual(result.residual_paths, ())
            self.assertFalse((target / "one.txt").exists())
            self.assertFalse((target / "two.txt").exists())
            self.assertEqual(operator_file.read_text(encoding="utf-8"), "preserve")

    def test_rollback_preserves_operator_artifact_after_target_directory_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            original_target = root / "target-before-replacement"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt", "two.txt"])
            plan = install.build_plan(target, manifest)

            def replace_target_then_fail(path: Path) -> None:
                if path.name == "one.txt":
                    target.rename(original_target)
                    target.mkdir()
                    (target / "operator-owned.txt").write_text("preserve", encoding="utf-8")
                elif path.name == "two.txt":
                    raise OSError("injected publication failure after target replacement")

            result = install.apply_plan(plan, manifest, failure_injector=replace_target_then_fail)
            self.assertFalse(result.success)
            self.assertEqual(result.residual_paths, ())
            self.assertEqual((target / "operator-owned.txt").read_text(encoding="utf-8"), "preserve")
            self.assertFalse((target / "one.txt").exists())
            self.assertFalse((target / "two.txt").exists())
            self.assertFalse((original_target / "one.txt").exists())
            self.assertFalse((original_target / "two.txt").exists())

    def test_incomplete_rollback_reports_exact_residual_and_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt", "two.txt"])
            plan = install.build_plan(target, manifest)

            def fail_after_second(path: Path) -> None:
                if path.name == "two.txt":
                    raise OSError("injected publication failure")

            def fail_rollback(path: Path) -> bool:
                return path.name == "one.txt"

            result = install.apply_plan(
                plan,
                manifest,
                failure_injector=fail_after_second,
                rollback_failure_injector=fail_rollback,
            )
            residual = str(target / "one.txt")
            self.assertFalse(result.success)
            self.assertEqual(result.residual_paths, (residual,))
            self.assertIn(residual, result.recovery_instructions or "")
            self.assertTrue((target / "one.txt").is_file())
            self.assertFalse((target / "two.txt").exists())

    def test_incomplete_rollback_after_target_replacement_reports_actual_residual(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            prior_target = root / "target-before-replacement"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt", "two.txt"])
            plan = install.build_plan(target, manifest)

            def replace_target_then_fail(path: Path) -> None:
                if path.name == "one.txt":
                    target.rename(prior_target)
                    target.mkdir()
                    (target / "operator-owned.txt").write_text("preserve", encoding="utf-8")
                elif path.name == "two.txt":
                    raise OSError("injected publication failure after target replacement")

            def fail_rollback(path: Path) -> bool:
                return path.name == "one.txt"

            result = install.apply_plan(
                plan,
                manifest,
                failure_injector=replace_target_then_fail,
                rollback_failure_injector=fail_rollback,
            )
            actual_residual = str(prior_target / "one.txt")
            replacement_path = str(target / "one.txt")
            self.assertFalse(result.success)
            self.assertEqual(result.residual_paths, (actual_residual,))
            self.assertIn(actual_residual, result.recovery_instructions or "")
            self.assertNotIn(replacement_path, result.recovery_instructions or "")
            self.assertTrue((prior_target / "one.txt").is_file())
            self.assertFalse((prior_target / "two.txt").exists())
            self.assertEqual((target / "operator-owned.txt").read_text(encoding="utf-8"), "preserve")
            self.assertFalse((target / "one.txt").exists())

    def test_source_change_after_plan_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt"])
            plan = install.build_plan(target, manifest)
            (root / "package" / "template" / "one.txt").write_text("changed source", encoding="utf-8")
            result = install.apply_plan(plan, manifest)
            self.assertFalse(result.success)
            self.assertEqual(result.diagnostic, "apply revalidation failed: plan changed before publication")
            self.assertFalse((target / "one.txt").exists())

    def test_invalid_manifest_after_plan_is_rejected_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            manifest = self.make_package(root, ["one.txt"])
            plan = install.build_plan(target, manifest)
            manifest.write_text("not json", encoding="utf-8")
            result = install.apply_plan(plan, manifest)
            self.assertFalse(result.success)
            self.assertTrue((result.diagnostic or "").startswith("apply revalidation failed:"))
            self.assertFalse((target / "one.txt").exists())

    def test_root_control_plane_files_are_not_modified(self) -> None:
        repository_root = PACKAGE_ROOT.parents[1]
        controls = [repository_root / "FILE_REGISTRY.yml", repository_root / "PROJECT_MAP.md"]
        before = {path: path.read_bytes() for path in controls}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            self.assertTrue(install.apply_target(target).success)
        self.assertEqual({path: path.read_bytes() for path in controls}, before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
