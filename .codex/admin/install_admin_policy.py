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
import shutil
import stat
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMIN_DIR = ROOT / ".codex" / "admin"
PROFILE_DIR = ADMIN_DIR / "profiles"
DEFAULT_PROFILE = "yolo-compatible"
DEFAULT_TARGET_DIR = Path("/etc/codex")
SOURCE_HOOK = ADMIN_DIR / "hooks" / "esp32_admin_policy.py"
SUPPORT_SOURCES = [
    ROOT / "scripts" / "agent_process_classifiers.py",
    ROOT / "scripts" / "agent_process_contracts.py",
]
YOLO_FORBIDDEN_KEYS = ("allowed_sandbox_modes", "allowed_approval_policies")


@dataclass(frozen=True)
class InstallEntry:
    label: str
    source: Path
    target: Path
    file_mode: str


@dataclass(frozen=True)
class TargetLayout:
    target_dir: Path
    hook_dir: Path
    backup_dir: Path
    requirements: Path
    hook: Path
    privileged: bool


def profile_requirements(profile: str) -> Path:
    if profile == DEFAULT_PROFILE:
        return PROFILE_DIR / DEFAULT_PROFILE / "requirements.toml"
    if profile == "admin-strict":
        return PROFILE_DIR / "admin-strict" / "requirements.toml"
    raise SystemExit(f"unknown profile: {profile}")


def is_system_target(target_dir: Path) -> bool:
    resolved = target_dir.resolve()
    system = DEFAULT_TARGET_DIR.resolve()
    return resolved == system or system in resolved.parents


def target_layout(target_dir: Path) -> TargetLayout:
    target_dir = target_dir.expanduser()
    hook_dir = target_dir / "hooks"
    return TargetLayout(
        target_dir=target_dir,
        hook_dir=hook_dir,
        backup_dir=target_dir / "backups",
        requirements=target_dir / "requirements.toml",
        hook=hook_dir / "esp32_admin_policy.py",
        privileged=is_system_target(target_dir) and os.geteuid() != 0,
    )


def install_entries(requirements: Path, layout: TargetLayout) -> list[InstallEntry]:
    return [
        InstallEntry("requirements", requirements, layout.requirements, "0644"),
        InstallEntry("hook", SOURCE_HOOK, layout.hook, "0755"),
        *[
            InstallEntry(f"support:{source.name}", source, layout.hook_dir / source.name, "0644")
            for source in SUPPORT_SOURCES
        ],
    ]


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


def run_command(args: list[str], privileged: bool) -> None:
    command = ["sudo", *args] if privileged else args
    subprocess.run(command, check=True)


def copy_with_mode(source: Path, target: Path, file_mode: str, layout: TargetLayout) -> None:
    if layout.privileged:
        run_command(["mkdir", "-p", str(target.parent)], privileged=True)
        run_command(["install", "-m", file_mode, "-o", "root", "-g", "root", str(source), str(target)], privileged=True)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    target.chmod(int(file_mode, 8))


def backup_existing(target: Path, label: str, layout: TargetLayout) -> Path | None:
    if not target.exists():
        return None
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = layout.backup_dir / f"{target.name}.{timestamp}.{label}.bak"
    if layout.privileged:
        run_command(["mkdir", "-p", str(layout.backup_dir)], privileged=True)
        run_command(["cp", "-p", str(target), str(backup)], privileged=True)
    else:
        layout.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
    return backup


def install_file(entry: InstallEntry, layout: TargetLayout) -> Path | None:
    backup = backup_existing(entry.target, sha256(entry.source)[:12], layout)
    copy_with_mode(entry.source, entry.target, entry.file_mode, layout)
    return backup


def remove_file(target: Path, layout: TargetLayout) -> Path | None:
    backup = backup_existing(target, "remove", layout)
    if target.exists():
        if layout.privileged:
            run_command(["rm", "-f", str(target)], privileged=True)
        else:
            target.unlink()
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
    for source in [SOURCE_HOOK, *SUPPORT_SOURCES]:
        if not source.exists():
            raise SystemExit(f"missing managed-hook source file: {source}")
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


def dry_run(profile: str, target_dir: Path) -> int:
    requirements = source_checks(profile)
    layout = target_layout(target_dir)
    entries = install_entries(requirements, layout)
    print(f"profile: {profile}")
    print(f"target-dir: {layout.target_dir}")
    print_report("source files", [entry.source for entry in entries])
    print_report("target files", [entry.target for entry in entries])
    for entry in entries:
        print(f"{entry.label} diff:")
        print(diff_text(entry.source, entry.target), end="")
    print("planned backups:")
    for entry in entries:
        if entry.target.exists():
            print(f"- {entry.target} -> {layout.backup_dir}/{entry.target.name}.<utc>.<label>.bak")
        else:
            print(f"- {entry.target}: no backup needed; target missing")
    return 0


def install(profile: str, target_dir: Path) -> int:
    requirements = source_checks(profile)
    layout = target_layout(target_dir)
    entries = install_entries(requirements, layout)
    if profile == "admin-strict":
        print("WARNING: admin-strict blocks codex --yolo by design.")
    backups = [(entry.label, install_file(entry, layout)) for entry in entries]
    parse_toml(layout.requirements)
    print(f"installed profile: {profile}")
    print(f"target-dir: {layout.target_dir}")
    print_report("installed files", [entry.target for entry in entries])
    print("backups:")
    for label, backup in backups:
        print(f"- {label}: {backup}" if backup else f"- {label}: none")
    return 0


def validate(profile: str, target_dir: Path) -> int:
    requirements = source_checks(profile)
    layout = target_layout(target_dir)
    entries = install_entries(requirements, layout)
    missing = [str(entry.target) for entry in entries if not entry.target.exists()]
    if missing:
        print("FAIL: missing installed files: " + ", ".join(missing))
        return 1
    parse_toml(layout.requirements)
    failures: list[str] = []
    for entry in entries:
        if sha256(entry.source) != sha256(entry.target):
            failures.append(f"{entry.label} hash mismatch")
        actual_mode = entry.target.stat().st_mode & 0o777
        expected_mode = int(entry.file_mode, 8)
        if actual_mode != expected_mode:
            failures.append(f"{entry.label} mode must be {entry.file_mode}")
    if profile == DEFAULT_PROFILE:
        try:
            assert_yolo_compatible(layout.requirements)
        except SystemExit as exc:
            failures.append(str(exc))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print_report("installed files", [entry.target for entry in entries])
        return 1
    print(f"validated profile: {profile}")
    print(f"target-dir: {layout.target_dir}")
    print_report("validated installed files", [entry.target for entry in entries])
    return 0


def remove_system_requirements(target_dir: Path) -> int:
    layout = target_layout(target_dir)
    backup = remove_file(layout.requirements, layout)
    if layout.requirements.exists():
        print(f"FAIL: {layout.requirements} still exists")
        return 1
    if is_system_target(layout.target_dir):
        print("removed system requirements; codex --yolo is no longer constrained by requirements.toml")
    else:
        print("removed target requirements; temp target no longer has requirements.toml")
    print(f"target-dir: {layout.target_dir}")
    print(f"backup: {backup}" if backup else "backup: none; target missing")
    print_report("remaining managed hook files", [layout.hook, *[layout.hook_dir / source.name for source in SUPPORT_SOURCES]])
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
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=DEFAULT_TARGET_DIR,
        help="managed policy target directory; defaults to /etc/codex",
    )
    args = parser.parse_args()
    if args.remove_system_requirements:
        return remove_system_requirements(args.target_dir)
    if args.dry_run:
        return dry_run(args.profile, args.target_dir)
    if args.install:
        return install(args.profile, args.target_dir)
    if args.validate:
        return validate(args.profile, args.target_dir)
    return 2


if __name__ == "__main__":
    sys.exit(main())
