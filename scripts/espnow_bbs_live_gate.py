#!/usr/bin/env python3
"""Gated ESP-NOW BBS live backup, build, and flash helper."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOSC_ROOT = Path("/mnt/h/dos-c")
DEFAULT_LIVE_ROOT = DEFAULT_DOSC_ROOT / "secrets" / "espnow-bbs"
DEFAULT_COORDINATOR_PORT = "/dev/ttyUSB0"
FLASH_ORDER = ["coordinator", "peer01", "peer02", "peer03"]
FORBIDDEN_FLASH_ARGS = {
    "--trust-flash-content",
    "--erase-all",
    "--force",
    "erase-flash",
    "erase_flash",
    "erase-region",
    "erase_region",
}

sys.path.insert(0, str(ROOT / "scripts"))
import live_bench_preflight as preflight  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_command(
    argv: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    try:
        result = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            errors="replace",
        )
    except FileNotFoundError as exc:
        return {
            "available": False,
            "argv": argv,
            "error": str(exc),
            "stdout": [],
            "stderr": [],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "available": True,
            "argv": argv,
            "timeoutSeconds": timeout,
            "error": str(exc),
            "stdout": (exc.stdout or "").splitlines(),
            "stderr": (exc.stderr or "").splitlines(),
        }
    return {
        "available": True,
        "argv": argv,
        "returncode": result.returncode,
        "stdout": result.stdout.splitlines(),
        "stderr": result.stderr.splitlines(),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def json_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def require_success(result: dict[str, Any], label: str) -> None:
    if result.get("returncode") == 0:
        return
    raise SystemExit(f"{label} failed: {json.dumps(result, indent=2)}")


def command_not_supported(result: dict[str, Any]) -> bool:
    text = "\n".join(result.get("stdout", []) + result.get("stderr", [])).lower()
    return "invalid choice" in text or "no such command" in text or "unknown command" in text


def run_esptool_with_spelling_fallback(
    argv_prefix: list[str],
    port: str,
    command: str,
    rest: list[str],
    *,
    timeout: float,
) -> dict[str, Any]:
    spellings = {
        "read-flash": ["read-flash", "read_flash"],
        "write-flash": ["write-flash", "write_flash"],
        "verify-flash": ["verify-flash", "verify_flash"],
    }.get(command, [command])
    first: dict[str, Any] | None = None
    for spelling in spellings:
        argv = argv_prefix + ["--port", port, spelling] + rest
        result = run_command(argv, timeout=timeout)
        if first is None:
            first = result
        if result.get("returncode") == 0:
            return result
        if not command_not_supported(result):
            return result
    return first or {"available": False, "argv": argv_prefix, "error": "no command attempted"}


def load_passing_preflight(path: Path) -> dict[str, Any]:
    record = json_load(path)
    preflight.validate_preflight_record(record)
    if not record.get("ok"):
        raise SystemExit(f"preflight is not passing: {record.get('failures', [])}")
    for role in FLASH_ORDER:
        if role == "coordinator":
            if not record.get("coordinatorMap", {}).get("mac"):
                raise SystemExit("preflight is missing coordinatorMap")
        elif role not in record.get("peerMap", {}):
            raise SystemExit(f"preflight is missing {role} in peerMap")
    return record


def device_plan(record: dict[str, Any]) -> dict[str, Any]:
    devices: dict[str, Any] = {}
    pi_target = record["piIdentity"]["target"]
    devices["coordinator"] = {
        "role": "coordinator",
        "kind": "pi",
        "target": pi_target,
        "port": record.get("coordinatorPort", DEFAULT_COORDINATOR_PORT),
        "mac": record["coordinatorMap"]["mac"],
        "chip": record["coordinatorMap"].get("chip"),
        "flashSize": record["coordinatorMap"].get("flashSize"),
    }
    for role, peer in record["peerMap"].items():
        identity = record["peerEsp32Identities"]["ports"][peer["windowsPort"]]
        devices[role] = {
            "role": role,
            "kind": "windows-peer",
            "windowsPort": peer["windowsPort"],
            "wslPort": peer["wslPort"],
            "port": identity["port"],
            "portKind": identity["portKind"],
            "tool": identity["tool"],
            "mac": peer["mac"],
            "chip": peer.get("chip"),
            "flashSize": peer.get("flashSize"),
        }
    return devices


def known_hosts_for_preflight(record: dict[str, Any], live_dir: Path) -> Path:
    keyscan_lines = record.get("piIdentity", {}).get("sshKeyscan", {}).get("stdout", [])
    if not keyscan_lines:
        raise SystemExit("preflight does not contain Pi ssh-keyscan output")
    known_hosts = live_dir / "known_hosts"
    known_hosts.write_text("\n".join(keyscan_lines) + "\n", encoding="utf-8")
    return known_hosts


def ssh_base(target: str, known_hosts: Path) -> list[str]:
    return [
        "ssh",
        "-o",
        f"UserKnownHostsFile={known_hosts}",
        "-o",
        "StrictHostKeyChecking=yes",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=8",
        target,
    ]


def backup_local_peer(device: dict[str, Any], backup_dir: Path) -> dict[str, Any]:
    target = backup_dir / f"{device['role']}-{device['windowsPort']}-full-flash.bin"
    if target.exists():
        raise SystemExit(f"refusing to overwrite backup: {target}")
    result = run_esptool_with_spelling_fallback(
        list(device["tool"]["argv"]),
        device["port"],
        "read-flash",
        ["0", "ALL", str(target)],
        timeout=600.0,
    )
    require_success(result, f"read-flash backup for {device['role']}")
    return {
        "path": str(target),
        "sha256": sha256_file(target),
        "bytes": target.stat().st_size,
        "command": result,
    }


def backup_remote_coordinator(
    device: dict[str, Any],
    backup_dir: Path,
    known_hosts: Path,
    stamp: str,
) -> dict[str, Any]:
    target = backup_dir / "coordinator-pi-ttyUSB0-full-flash.bin"
    if target.exists():
        raise SystemExit(f"refusing to overwrite backup: {target}")
    remote_path = f"/tmp/espnow-bbs-{stamp}-coordinator-full-flash.bin"
    remote_script = (
        "set -eu; "
        "if command -v esptool >/dev/null 2>&1; then ESPTOOL=esptool; "
        "elif command -v esptool.py >/dev/null 2>&1; then ESPTOOL=esptool.py; "
        "elif python3 -c 'import esptool' >/dev/null 2>&1; then ESPTOOL='python3 -m esptool'; "
        "else echo esptool-not-found >&2; exit 127; fi; "
        f"$ESPTOOL --no-stub --port {shlex.quote(device['port'])} "
        f"read_flash 0 ALL {shlex.quote(remote_path)}; "
        f"sha256sum {shlex.quote(remote_path)}"
    )
    read_result = run_command(
        ssh_base(device["target"], known_hosts) + [remote_script],
        timeout=700.0,
    )
    require_success(read_result, "coordinator read-flash backup")
    scp_result = run_command(
        [
            "scp",
            "-o",
            f"UserKnownHostsFile={known_hosts}",
            "-o",
            "StrictHostKeyChecking=yes",
            f"{device['target']}:{remote_path}",
            str(target),
        ],
        timeout=180.0,
    )
    cleanup_result = run_command(
        ssh_base(device["target"], known_hosts) + [f"rm -f {shlex.quote(remote_path)}"],
        timeout=30.0,
    )
    require_success(scp_result, "copy coordinator backup")
    return {
        "path": str(target),
        "sha256": sha256_file(target),
        "bytes": target.stat().st_size,
        "command": read_result,
        "copyCommand": scp_result,
        "cleanupCommand": cleanup_result,
    }


def run_live_config_generator(
    dosc_root: Path,
    live_dir: Path,
    devices: dict[str, Any],
    channel: int,
) -> dict[str, Any]:
    generator = dosc_root / "scripts" / "generate_espnow_bbs_live_config.py"
    argv = [
        "python3",
        str(generator),
        "--coordinator-mac",
        devices["coordinator"]["mac"],
        "--peer01-mac",
        devices["peer01"]["mac"],
        "--peer02-mac",
        devices["peer02"]["mac"],
        "--peer03-mac",
        devices["peer03"]["mac"],
        "--channel",
        str(channel),
        "--out-dir",
        str(live_dir),
    ]
    result = run_command(argv, cwd=dosc_root, timeout=30.0)
    require_success(result, "live config generation")
    return result


def build_role(
    dosc_root: Path,
    live_dir: Path,
    role: str,
) -> dict[str, Any]:
    if role == "coordinator":
        project = dosc_root / "firmware" / "espnow-bbs" / "coordinator"
        override = live_dir / "coordinator.sdkconfig.defaults"
    else:
        project = dosc_root / "firmware" / "espnow-bbs" / "peer"
        override = live_dir / f"{role}.sdkconfig.defaults"
    build_dir = live_dir / "builds" / role
    env = os.environ.copy()
    env["SDKCONFIG_DEFAULTS"] = f"sdkconfig.defaults;{override}"
    result = run_command(
        ["idf.py", "-C", str(project), "-B", str(build_dir), "build"],
        env=env,
        timeout=900.0,
    )
    require_success(result, f"ESP-IDF build for {role}")
    artifact = capture_build_artifacts(role, build_dir)
    artifact["buildCommand"] = result
    artifact["project"] = str(project)
    artifact["sdkconfigDefaults"] = env["SDKCONFIG_DEFAULTS"]
    return artifact


def capture_build_artifacts(role: str, build_dir: Path) -> dict[str, Any]:
    flasher_args_path = build_dir / "flasher_args.json"
    flash_project_args_path = build_dir / "flash_project_args"
    if not flasher_args_path.exists():
        raise SystemExit(f"missing flasher_args.json for {role}: {flasher_args_path}")
    if not flash_project_args_path.exists():
        raise SystemExit(f"missing flash_project_args for {role}: {flash_project_args_path}")
    flasher_args = json_load(flasher_args_path)
    write_args = list(flasher_args.get("write_flash_args", []))
    reject_forbidden_flash_args(write_args)
    files = []
    for offset, relative in sorted(flasher_args.get("flash_files", {}).items()):
        path = (build_dir / relative).resolve()
        if not path.exists():
            raise SystemExit(f"missing flash file for {role}: {path}")
        files.append(
            {
                "offset": offset,
                "path": str(path),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    build_digest = hashlib.sha256()
    for item in files:
        build_digest.update(item["offset"].encode("ascii"))
        build_digest.update(item["sha256"].encode("ascii"))
    return {
        "role": role,
        "buildDir": str(build_dir),
        "flasherArgsJson": str(flasher_args_path),
        "flashProjectArgs": str(flash_project_args_path),
        "flashSettings": flasher_args.get("flash_settings", {}),
        "writeFlashArgs": write_args,
        "files": files,
        "combinedSha256": build_digest.hexdigest(),
    }


def reject_forbidden_flash_args(args: list[str]) -> None:
    lowered = {arg.lower() for arg in args}
    forbidden = sorted(lowered & FORBIDDEN_FLASH_ARGS)
    if forbidden:
        raise SystemExit(f"forbidden flash arguments present: {forbidden}")


def validate_manifest_integrity(manifest: dict[str, Any]) -> None:
    preflight_path = Path(manifest["preflightPath"])
    if preflight_path.exists() and sha256_file(preflight_path) != manifest["preflightSha256"]:
        raise SystemExit("preflight JSON hash changed since prepare")
    for role, backup in manifest.get("backups", {}).items():
        path = Path(backup["path"])
        if not path.exists():
            raise SystemExit(f"missing backup for {role}: {path}")
        if sha256_file(path) != backup["sha256"]:
            raise SystemExit(f"backup hash mismatch for {role}: {path}")
    for role, build in manifest.get("builds", {}).items():
        reject_forbidden_flash_args(list(build.get("writeFlashArgs", [])))
        for item in build.get("files", []):
            path = Path(item["path"])
            if not path.exists():
                raise SystemExit(f"missing build file for {role}: {path}")
            if sha256_file(path) != item["sha256"]:
                raise SystemExit(f"build hash mismatch for {role}: {path}")


def verify_current_identities(manifest: dict[str, Any], known_hosts: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for role in ["peer01", "peer02", "peer03"]:
        device = manifest["devices"][role]
        selected = {"selected": device["tool"]}
        identity = preflight.collect_esp32_identity_for_port(
            selected,
            device["windowsPort"],
            device["wslPort"],
        )
        observed = identity.get("parsedIdentity", {}).get("mac")
        if not identity.get("ok") or observed != device["mac"]:
            raise SystemExit(
                f"current identity mismatch for {role}: expected {device['mac']} observed {observed}"
            )
        results[role] = identity

    coordinator = manifest["devices"]["coordinator"]
    remote_script = preflight.build_pi_remote_script(
        coordinator["port"],
        skip_coordinator=False,
    )
    ssh = run_command(
        ssh_base(coordinator["target"], known_hosts) + [remote_script],
        timeout=90.0,
    )
    require_success(ssh, "current coordinator identity")
    identity = preflight.parse_remote_coordinator_identity(
        ssh.get("stdout", []),
        coordinator["port"],
        skipped=False,
    )
    observed = identity.get("parsedIdentity", {}).get("mac")
    if not identity.get("ok") or observed != coordinator["mac"]:
        raise SystemExit(
            "current coordinator identity mismatch: "
            f"expected {coordinator['mac']} observed {observed}"
        )
    results["coordinator"] = identity
    return results


def write_flash_args(build: dict[str, Any], *, remote_dir: str | None = None) -> list[str]:
    args = list(build.get("writeFlashArgs", []))
    reject_forbidden_flash_args(args)
    for item in build["files"]:
        args.append(item["offset"])
        path = Path(item["path"])
        args.append(f"{remote_dir}/{path.name}" if remote_dir else str(path))
    return args


def verify_flash_args(build: dict[str, Any], *, remote_dir: str | None = None) -> list[str] | None:
    settings = build.get("flashSettings", {})
    if not all(settings.get(key) for key in ["flash_mode", "flash_size", "flash_freq"]):
        return None
    args = [
        "--flash-mode",
        settings["flash_mode"],
        "--flash-size",
        settings["flash_size"],
        "--flash-freq",
        settings["flash_freq"],
    ]
    for item in build["files"]:
        args.append(item["offset"])
        path = Path(item["path"])
        args.append(f"{remote_dir}/{path.name}" if remote_dir else str(path))
    return args


def flash_local_peer(device: dict[str, Any], build: dict[str, Any]) -> dict[str, Any]:
    write = run_esptool_with_spelling_fallback(
        list(device["tool"]["argv"]),
        device["port"],
        "write-flash",
        write_flash_args(build),
        timeout=700.0,
    )
    require_success(write, f"write-flash {device['role']}")
    record: dict[str, Any] = {"writeFlash": write}
    verify_args = verify_flash_args(build)
    if verify_args:
        verify = run_esptool_with_spelling_fallback(
            list(device["tool"]["argv"]),
            device["port"],
            "verify-flash",
            verify_args,
            timeout=700.0,
        )
        require_success(verify, f"verify-flash {device['role']}")
        record["verifyFlash"] = verify
    return record


def flash_remote_coordinator(
    device: dict[str, Any],
    build: dict[str, Any],
    known_hosts: Path,
    stamp: str,
) -> dict[str, Any]:
    remote_dir = f"/tmp/espnow-bbs-live-{stamp}-coordinator"
    mkdir = run_command(
        ssh_base(device["target"], known_hosts) + [f"mkdir -p {shlex.quote(remote_dir)}"],
        timeout=30.0,
    )
    require_success(mkdir, "create remote coordinator flash directory")
    copies = []
    for item in build["files"]:
        source = Path(item["path"])
        target = f"{device['target']}:{remote_dir}/{source.name}"
        copy = run_command(
            [
                "scp",
                "-o",
                f"UserKnownHostsFile={known_hosts}",
                "-o",
                "StrictHostKeyChecking=yes",
                str(source),
                target,
            ],
            timeout=180.0,
        )
        require_success(copy, f"copy coordinator flash file {source.name}")
        copies.append(copy)

    def remote_esptool(command: str, rest: list[str], timeout: float) -> dict[str, Any]:
        remote_script = (
            "set -eu; "
            "if command -v esptool >/dev/null 2>&1; then ESPTOOL=esptool; "
            "elif command -v esptool.py >/dev/null 2>&1; then ESPTOOL=esptool.py; "
            "elif python3 -c 'import esptool' >/dev/null 2>&1; then ESPTOOL='python3 -m esptool'; "
            "else echo esptool-not-found >&2; exit 127; fi; "
            "$ESPTOOL --no-stub --port "
            + shlex.quote(device["port"])
            + " "
            + shlex.join([command] + rest)
        )
        result = run_command(ssh_base(device["target"], known_hosts) + [remote_script], timeout=timeout)
        if result.get("returncode") != 0 and command_not_supported(result):
            fallback = command.replace("-", "_")
            if fallback != command:
                return remote_esptool(fallback, rest, timeout)
        return result

    write = remote_esptool(
        "write-flash",
        write_flash_args(build, remote_dir=remote_dir),
        700.0,
    )
    require_success(write, "write-flash coordinator")
    record: dict[str, Any] = {"mkdir": mkdir, "copies": copies, "writeFlash": write}
    verify_args = verify_flash_args(build, remote_dir=remote_dir)
    if verify_args:
        verify = remote_esptool("verify-flash", verify_args, 700.0)
        require_success(verify, "verify-flash coordinator")
        record["verifyFlash"] = verify
    cleanup = run_command(
        ssh_base(device["target"], known_hosts) + [f"rm -rf {shlex.quote(remote_dir)}"],
        timeout=30.0,
    )
    record["cleanup"] = cleanup
    return record


def command_prepare(args: argparse.Namespace) -> int:
    if not args.confirm_read_flash_backups:
        raise SystemExit("prepare requires --confirm-read-flash-backups")
    preflight_path = args.preflight.resolve()
    preflight_record = load_passing_preflight(preflight_path)
    devices = device_plan(preflight_record)
    stamp = utc_stamp()
    live_dir = args.live_dir or (args.dosc_root / "secrets" / "espnow-bbs" / f"live-{stamp}")
    if live_dir.exists() and any(live_dir.iterdir()):
        raise SystemExit(f"refusing to reuse non-empty live dir: {live_dir}")

    config_result = run_live_config_generator(args.dosc_root, live_dir, devices, args.channel)
    live_dir.mkdir(parents=True, exist_ok=True)
    backup_dir = live_dir / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    known_hosts = known_hosts_for_preflight(preflight_record, live_dir)
    backups: dict[str, Any] = {
        "coordinator": backup_remote_coordinator(devices["coordinator"], backup_dir, known_hosts, stamp)
    }
    for role in ["peer01", "peer02", "peer03"]:
        backups[role] = backup_local_peer(devices[role], backup_dir)

    builds = {}
    for role in FLASH_ORDER:
        builds[role] = build_role(args.dosc_root, live_dir, role)

    manifest = {
        "tool": "scripts/espnow_bbs_live_gate.py",
        "mode": "prepare",
        "generatedAt": utc_now(),
        "doscRoot": str(args.dosc_root),
        "liveDir": str(live_dir),
        "preflightPath": str(preflight_path),
        "preflightSha256": sha256_file(preflight_path),
        "preflightGeneratedAt": preflight_record.get("generatedAt"),
        "devices": devices,
        "knownHosts": str(known_hosts),
        "configGeneration": config_result,
        "backups": backups,
        "builds": builds,
        "recoveryCommands": recovery_commands(devices, backups),
        "flashGate": {
            "requiresManifestHashMatch": True,
            "requiresCurrentIdentityMatch": True,
            "requiresConfirmWriteFlash": True,
            "forbiddenArgs": sorted(FORBIDDEN_FLASH_ARGS),
            "flashOrder": FLASH_ORDER,
        },
    }
    manifest_path = live_dir / "manifest.json"
    json_write(manifest_path, manifest)
    print(json.dumps({"ok": True, "manifest": str(manifest_path)}, indent=2))
    return 0


def recovery_commands(devices: dict[str, Any], backups: dict[str, Any]) -> dict[str, str]:
    commands = {}
    for role in FLASH_ORDER:
        backup = backups[role]["path"]
        device = devices[role]
        if role == "coordinator":
            commands[role] = (
                f"copy {backup} to {device['target']} and run: "
                f"esptool --port {device['port']} write_flash 0x0 <backup-file>"
            )
        else:
            commands[role] = (
                f"{shlex.join(device['tool']['argv'])} --port {device['port']} "
                f"write-flash 0x0 {backup}"
            )
    return commands


def command_flash(args: argparse.Namespace) -> int:
    if not args.confirm_write_flash:
        raise SystemExit("flash requires --confirm-write-flash")
    manifest_path = args.manifest.resolve()
    manifest = json_load(manifest_path)
    validate_manifest_integrity(manifest)
    known_hosts = Path(manifest["knownHosts"])
    identities = verify_current_identities(manifest, known_hosts)
    stamp = utc_stamp()
    evidence: dict[str, Any] = {
        "tool": "scripts/espnow_bbs_live_gate.py",
        "mode": "flash",
        "generatedAt": utc_now(),
        "manifest": str(manifest_path),
        "identityChecks": identities,
        "flashOrder": FLASH_ORDER,
        "results": {},
    }
    for role in FLASH_ORDER:
        device = manifest["devices"][role]
        build = manifest["builds"][role]
        if role == "coordinator":
            result = flash_remote_coordinator(device, build, known_hosts, stamp)
        else:
            result = flash_local_peer(device, build)
        evidence["results"][role] = result
        evidence_path = manifest_path.parent / f"flash-evidence-{stamp}.json"
        json_write(evidence_path, evidence)
    evidence["ok"] = True
    evidence_path = manifest_path.parent / f"flash-evidence-{stamp}.json"
    json_write(evidence_path, evidence)
    print(json.dumps({"ok": True, "evidence": str(evidence_path)}, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_parser = sub.add_parser("prepare", help="Back up devices and create a flash manifest.")
    prepare_parser.add_argument("--preflight", type=Path, required=True)
    prepare_parser.add_argument("--dosc-root", type=Path, default=DEFAULT_DOSC_ROOT)
    prepare_parser.add_argument("--live-dir", type=Path)
    prepare_parser.add_argument("--channel", type=int, default=1)
    prepare_parser.add_argument("--confirm-read-flash-backups", action="store_true")
    prepare_parser.set_defaults(func=command_prepare)

    flash_parser = sub.add_parser("flash", help="Flash using a prepared manifest.")
    flash_parser.add_argument("--manifest", type=Path, required=True)
    flash_parser.add_argument("--confirm-write-flash", action="store_true")
    flash_parser.set_defaults(func=command_flash)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "prepare":
        args.dosc_root = args.dosc_root.resolve()
        if not args.dosc_root.exists():
            raise SystemExit(f"DOS-C root does not exist: {args.dosc_root}")
        if args.live_dir is not None:
            args.live_dir = args.live_dir.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
