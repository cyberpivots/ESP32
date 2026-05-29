#!/usr/bin/env python3
"""Install, validate, or remove ESP32 Codex managed-hook profiles.

Operator sovereignty rule: the default yolo-compatible profile must not
constrain `codex --yolo`. Tier 3 governance remains advisory in yolo mode.
The admin-strict profile is explicit opt-in only.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import stat
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_DIR = ROOT / ".codex" / "admin"
PROFILE_DIR = ADMIN_DIR / "profiles"
DEFAULT_PROFILE = "yolo-compatible"
SOURCE_HOOK = ADMIN_DIR / "hooks" / "esp32_admin_policy.py"
TARGET_DIR = Path("/etc/codex")
TARGET_HOOK_DIR = TARGET_DIR / "hooks"
BACKUP_DIR = TARGET_DIR / "backups"
TARGET_REQUIREMENTS = TARGET_DIR / "requirements.toml"
TARGET_HOOK = TARGET_HOOK_DIR / "esp32_admin_policy.py"
YOLO_FORBIDDEN_KEYS = ("allowed_sandbox_modes", "allowed_approval_policies")


def profile_requirements(profile: str) -> Path:
    if profile == DEFAULT_PROFILE:
        return PROFILE_DIR / DEFAULT_PROFILE / "requirements.toml"
    if profile == "admin-strict":
        return PROFILE_DIR / "admin-strict" / "requirements.toml"
    raise SystemExit(f"unknown profile: {profile}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mode(path: Path) -> str:
    return stat.filemode(path.stat().st_mode)


def owner(path: Path) -> str:
    st = path.stat()
    return f"{st.st_uid}:{st.st_gid}"


def parse_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def run_root(args: list[str]) -> None:
    command = args if os.geteuid() == 0 else ["sudo", *args]
    subprocess.run(command, check=True)


def backup_existing(target: Path, label: str) -> Path | None:
    if not target.exists():
        return None
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = BACKUP_DIR / f"{target.name}.{timestamp}.{label}.bak"
    run_root(["mkdir", "-p", str(BACKUP_DIR)])
    run_root(["cp", "-p", str(target), str(backup)])
    return backup


def install_file(source: Path, target: Path, file_mode: str) -> Path | None:
    backup = backup_existing(target, sha256(source)[:12])
    run_root(["mkdir", "-p", str(target.parent)])
    run_root(["install", "-m", file_mode, "-o", "root", "-g", "root", str(source), str(target)])
    return backup


def remove_file(target: Path) -> Path | None:
    backup = backup_existing(target, "remove")
    if target.exists():
        run_root(["rm", "-f", str(target)])
    return backup


def assert_yolo_compatible(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    data = parse_toml(path)
    failures: list[str] = []
    for marker in [*YOLO_FORBIDDEN_KEYS, "rules.prefix_rules"]:
        if marker in raw:
            failures.append(f"{path} must not contain {marker}")
    for key in YOLO_FORBIDDEN_KEYS:
        if key in data:
            failures.append(f"{path} must not set {key}")
    rules = data.get("rules")
    if isinstance(rules, dict) and "prefix_rules" in rules:
        failures.append(f"{path} must not set rules.prefix_rules")
    if failures:
        raise SystemExit("\n".join(failures))


def source_checks(profile: str) -> Path:
    requirements = profile_requirements(profile)
    if not requirements.exists():
        raise SystemExit(f"missing requirements profile: {requirements}")
    parse_toml(requirements)
    if profile == DEFAULT_PROFILE:
        assert_yolo_compatible(requirements)
        assert_yolo_compatible(ADMIN_DIR / "requirements.toml")
    if not SOURCE_HOOK.exists():
        raise SystemExit(f"missing hook template: {SOURCE_HOOK}")
    return requirements


def diff_text(source: Path, target: Path) -> str:
    if not target.exists():
        return f"target missing: {target}\n"
    src = source.read_text(encoding="utf-8").splitlines(keepends=True)
    dst = target.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    return "".join(difflib.unified_diff(dst, src, fromfile=str(target), tofile=str(source)))


def print_report(title: str, paths: list[Path]) -> None:
    print(title)
    for path in paths:
        if path.exists():
            print(f"- {path}: sha256={sha256(path)} mode={mode(path)} owner={owner(path)}")
        else:
            print(f"- {path}: missing")


def dry_run(profile: str) -> int:
    requirements = source_checks(profile)
    print(f"profile: {profile}")
    print_report("source files", [requirements, SOURCE_HOOK])
    print_report("target files", [TARGET_REQUIREMENTS, TARGET_HOOK])
    print("requirements diff:")
    print(diff_text(requirements, TARGET_REQUIREMENTS), end="")
    print("hook diff:")
    print(diff_text(SOURCE_HOOK, TARGET_HOOK), end="")
    print("planned backups:")
    for target in [TARGET_REQUIREMENTS, TARGET_HOOK]:
        if target.exists():
            print(f"- {target} -> {BACKUP_DIR}/{target.name}.<utc>.<label>.bak")
        else:
            print(f"- {target}: no backup needed; target missing")
    return 0


def install(profile: str) -> int:
    requirements = source_checks(profile)
    if profile == "admin-strict":
        print("WARNING: admin-strict blocks codex --yolo by design.")
    backups = [
        install_file(requirements, TARGET_REQUIREMENTS, "0644"),
        install_file(SOURCE_HOOK, TARGET_HOOK, "0755"),
    ]
    parse_toml(TARGET_REQUIREMENTS)
    print(f"installed profile: {profile}")
    print_report("installed files", [TARGET_REQUIREMENTS, TARGET_HOOK])
    print("backups:")
    for backup in backups:
        print(f"- {backup}" if backup else "- none")
    return 0


def validate(profile: str) -> int:
    requirements = source_checks(profile)
    missing = [str(path) for path in [TARGET_REQUIREMENTS, TARGET_HOOK] if not path.exists()]
    if missing:
        print("FAIL: missing installed files: " + ", ".join(missing))
        return 1
    parse_toml(TARGET_REQUIREMENTS)
    failures: list[str] = []
    if sha256(requirements) != sha256(TARGET_REQUIREMENTS):
        failures.append("requirements hash mismatch")
    if sha256(SOURCE_HOOK) != sha256(TARGET_HOOK):
        failures.append("hook hash mismatch")
    if oct(TARGET_REQUIREMENTS.stat().st_mode & 0o777) != "0o644":
        failures.append("requirements mode must be 0644")
    if oct(TARGET_HOOK.stat().st_mode & 0o777) != "0o755":
        failures.append("hook mode must be 0755")
    if profile == DEFAULT_PROFILE:
        try:
            assert_yolo_compatible(TARGET_REQUIREMENTS)
        except SystemExit as exc:
            failures.append(str(exc))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print_report("installed files", [TARGET_REQUIREMENTS, TARGET_HOOK])
        return 1
    print(f"validated profile: {profile}")
    print_report("validated installed files", [TARGET_REQUIREMENTS, TARGET_HOOK])
    return 0


def remove_system_requirements() -> int:
    backup = remove_file(TARGET_REQUIREMENTS)
    if TARGET_REQUIREMENTS.exists():
        print(f"FAIL: {TARGET_REQUIREMENTS} still exists")
        return 1
    print("removed system requirements; codex --yolo is no longer constrained by /etc/codex/requirements.toml")
    print(f"backup: {backup}" if backup else "backup: none; target missing")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--install", action="store_true")
    group.add_argument("--validate", action="store_true")
    group.add_argument("--remove-system-requirements", action="store_true")
    parser.add_argument(
        "--profile",
        choices=[DEFAULT_PROFILE, "admin-strict"],
        default=DEFAULT_PROFILE,
        help="requirements profile to use; admin-strict blocks codex --yolo",
    )
    args = parser.parse_args()
    if args.remove_system_requirements:
        return remove_system_requirements()
    if args.dry_run:
        return dry_run(args.profile)
    if args.install:
        return install(args.profile)
    if args.validate:
        return validate(args.profile)
    return 2


if __name__ == "__main__":
    sys.exit(main())
