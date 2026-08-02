#!/usr/bin/env python3
"""Offline fixtures for signed, committed Codex authorization envelopes."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LIFE = ROOT / "template/.codex/scripts/lifecycle.py"
NAMESPACE = "agentic-sdlc-authorization"
IDENTITY = "owner@agentic-sdlc"


def call(repo: Path, *args: str, signers: Path | None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if signers is None:
        env.pop("AGENTIC_SDLC_OWNER_SIGNERS", None)
    else:
        env["AGENTIC_SDLC_OWNER_SIGNERS"] = str(signers)
    return subprocess.run(
        [sys.executable, str(LIFE), "--root", str(repo), "--state", str(repo / ".agent/active-work-block.json"), *args],
        text=True, capture_output=True, env=env, check=False,
    )


def blocked(repo: Path, *args: str, signers: Path | None) -> None:
    result = call(repo, *args, signers=signers)
    assert result.returncode == 2 and "BLOCKED:" in result.stdout, result.stdout


def record(expiry: str | None = None, **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "work_block_id": "WB", "specification": {"path": "docs/spec.md", "revision": "1"},
        "spec_digest": "sha256:fixture", "write_set": ["x"],
        "expires_at": expiry or (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat(),
        "status": "APPROVED", "owner_evidence": "owner-record",
        "critic": {"status": "READY", "verdict": "APPROVE"},
        "signature": {"path": ".agent/authorizations/wb.json.sig"},
    }
    value.update(overrides)
    return value


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def sign(path: Path, key: Path) -> None:
    path.with_suffix(path.suffix + ".sig").unlink(missing_ok=True)
    subprocess.run(["ssh-keygen", "-Y", "sign", "-q", "-f", str(key), "-n", NAMESPACE, str(path)], check=True, capture_output=True)


def commit(repo: Path, path: Path, value: dict[str, object], key: Path, message: str = "authorization") -> None:
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    sign(path, key)
    git(repo, "add", str(path.relative_to(repo)), str(path.with_suffix(path.suffix + ".sig").relative_to(repo)))
    git(repo, "commit", "-qm", message)


def generate_key(directory: Path, name: str) -> Path:
    key = directory / name
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    return key


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        owner_key, attacker_key = generate_key(temp, "owner"), generate_key(temp, "attacker")
        signers = temp / "owner-signers"
        public = (owner_key.with_suffix(".pub")).read_text(encoding="utf-8").strip()
        signers.write_text(f"{IDENTITY} {public}\n", encoding="utf-8")
        repo = temp / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "a@b")
        git(repo, "config", "user.name", "a")
        (repo / ".agent/authorizations").mkdir(parents=True)
        (repo / "x").write_text("x", encoding="utf-8")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "base")
        path = repo / ".agent/authorizations/wb.json"
        auth = record()
        commit(repo, path, auth, owner_key)
        (repo / ".agent/active-work-block.json").write_text(json.dumps({"schema_version": 2, "write_gate": {"status": "BLOCKED"}}), encoding="utf-8")
        result = call(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)
        assert result.returncode == 0, result.stdout + result.stderr
        state = json.loads((repo / ".agent/active-work-block.json").read_text(encoding="utf-8"))
        assert state["authorization"]["blob_id"] and state["authorization"]["signature_blob_id"]

        blocked(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=None)
        modified = record(write_set=["x", "evil"])
        commit(repo, path, modified, owner_key, "modified-json")
        # The committed JSON now differs from its former signature only after restoring it below.
        path.write_text(json.dumps({**modified, "write_set": ["forged"]}) + "\n", encoding="utf-8")
        git(repo, "add", str(path.relative_to(repo)))
        git(repo, "commit", "-qm", "unsigned-json-change")
        blocked(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)

        commit(repo, path, record(), owner_key, "fresh-owner-record")
        signature = path.with_suffix(path.suffix + ".sig")
        signature.write_text(signature.read_text(encoding="utf-8").replace("BEGIN", "XEGIN", 1), encoding="utf-8")
        git(repo, "add", str(signature.relative_to(repo)))
        git(repo, "commit", "-qm", "modified-signature")
        blocked(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)

        commit(repo, path, record(owner_evidence="forged-local-record"), attacker_key, "attacker-signed-record")
        blocked(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)

        commit(repo, path, record(expiry=(dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat()), owner_key, "expired")
        blocked(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)
        commit(repo, path, record(owner_evidence=""), owner_key, "missing-owner-evidence")
        blocked(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)
        fresh = record()
        commit(repo, path, fresh, owner_key, "fresh-auth")
        result = call(repo, "open", "--authorization", ".agent/authorizations/wb.json", signers=signers)
        assert result.returncode == 0, result.stdout + result.stderr
        renewal = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30)).isoformat()
        assert call(repo, "renew", "--expires-at", renewal, signers=signers).returncode == 0
        baseline = (repo / ".agent/active-work-block.json").read_text(encoding="utf-8")

        def rejects_renewal(label: str, mutate) -> None:
            forged = json.loads(baseline)
            mutate(forged)
            before = json.dumps(forged, sort_keys=True) + "\n"
            (repo / ".agent/active-work-block.json").write_text(before, encoding="utf-8")
            result = call(repo, "renew", "--expires-at", renewal, signers=signers)
            assert result.returncode == 2 and "BLOCKED:" in result.stdout, f"{label}: {result.stdout}"
            assert (repo / ".agent/active-work-block.json").read_text(encoding="utf-8") == before, label

        rejects_renewal("tampered authorization JSON blob", lambda state: state["authorization"].update(blob_id="0" * 40))
        rejects_renewal("tampered authorization signature blob", lambda state: state["authorization"].update(signature_blob_id="0" * 40))
        rejects_renewal("widened write-set", lambda state: state["write_set"].append("evil/**"))
        rejects_renewal("tampered specification", lambda state: state["specification"].update(revision="forged"))
        rejects_renewal("tampered digest", lambda state: state.update(spec_digest="sha256:forged"))
        rejects_renewal("tampered Critic", lambda state: state["critic"].update(verdict="SUPPLEMENT"))
        rejects_renewal("tampered Work Block", lambda state: state.update(work_block_id="FORGED"))

        stale = json.loads(baseline)
        stale["base_commit"] = "deadbee"
        before = json.dumps(stale, sort_keys=True) + "\n"
        (repo / ".agent/active-work-block.json").write_text(before, encoding="utf-8")
        blocked(repo, "renew", "--expires-at", str(fresh["expires_at"]), signers=signers)
        assert (repo / ".agent/active-work-block.json").read_text(encoding="utf-8") == before
    print("Signed authorization lifecycle fixtures: OK")


if __name__ == "__main__":
    main()
