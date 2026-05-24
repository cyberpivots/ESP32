#!/usr/bin/env python3
"""Gated ESP-NOW BBS live backup, build, and flash helper."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
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
REMOTE_ESPNOW_ESPTOOL = (
    "/home/dospi/dos-c/artifacts/runtime/esptool-venv-espnow-encrypted/bin/esptool.py"
)
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
COMPLETE_REQUIRED_TRANSCRIPT_TYPES = {
    "hello",
    "state_get",
    "peer_list",
    "diag_get",
    "fw_inventory",
    "msg_post",
    "msg_pull",
    "msg_search",
    "msg_ack",
    "download_list",
    "download_status",
    "otap_status",
    "otap_intent",
}
COMPLETE_REQUIRED_PEERS = {"peer01", "peer02", "peer03"}
COMPLETE_CLEANUP_CATEGORIES = {
    "dosbox": ("dosbox-x", "dosbox"),
    "modal": ("zenity", "modal", "warning"),
    "bridge": ("espnow_bbs_bridge.py", "bridge process"),
    "listeners": ("31331", "31332", "8080", "listener"),
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


def wsl_path_to_windows(path: Path) -> str:
    text = str(path)
    if text.startswith("/mnt/") and len(text) >= 7 and text[5].isalpha() and text[6] == "/":
        drive = text[5].upper()
        rest = text[7:].replace("/", "\\")
        return f"{drive}:\\{rest}" if rest else f"{drive}:\\"
    return text


def local_file_arg(device: dict[str, Any], path: Path) -> str:
    if device.get("portKind") == "windows":
        return wsl_path_to_windows(path)
    return str(path)


def remote_esptool_setup_script() -> str:
    """Select the coordinator-side esptool runtime used by proven Pi backups."""
    return (
        f"REMOTE_ESPNOW_ESPTOOL={shlex.quote(REMOTE_ESPNOW_ESPTOOL)}; "
        "ESPTOOL_KIND=path; "
        "ESPTOOL_STUB_ARGS=''; "
        "if [ -n \"${ESPNOW_BBS_ESPTOOL:-}\" ]; then "
        "if [ -x \"$ESPNOW_BBS_ESPTOOL\" ]; then "
        "ESPTOOL=\"$ESPNOW_BBS_ESPTOOL\"; ESPTOOL_LABEL=\"$ESPNOW_BBS_ESPTOOL\"; "
        "else echo espnow-bbs-esptool-env-not-executable >&2; exit 127; fi; "
        "elif [ -x \"$REMOTE_ESPNOW_ESPTOOL\" ]; then "
        "ESPTOOL=\"$REMOTE_ESPNOW_ESPTOOL\"; ESPTOOL_LABEL=\"$REMOTE_ESPNOW_ESPTOOL\"; "
        "elif command -v esptool >/dev/null 2>&1; then "
        "ESPTOOL=esptool; ESPTOOL_LABEL=$(command -v esptool); ESPTOOL_STUB_ARGS='--no-stub'; "
        "elif command -v esptool.py >/dev/null 2>&1; then "
        "ESPTOOL=esptool.py; ESPTOOL_LABEL=$(command -v esptool.py); ESPTOOL_STUB_ARGS='--no-stub'; "
        "elif python3 -c 'import esptool' >/dev/null 2>&1; then "
        "ESPTOOL_KIND=python_module; ESPTOOL_LABEL='python3 -m esptool'; "
        "ESPTOOL_STUB_ARGS='--no-stub'; "
        "else echo esptool-not-found >&2; exit 127; fi; "
        "echo \"__espnow_bbs_esptool__ ${ESPTOOL_LABEL} stub_args=${ESPTOOL_STUB_ARGS:-none}\"; "
        "run_esptool() { "
        "if [ \"$ESPTOOL_KIND\" = python_module ]; then python3 -m esptool \"$@\"; "
        "else \"$ESPTOOL\" \"$@\"; fi; "
        "}; "
    )


def remote_esptool_invocation(port: str, command: str, rest: list[str]) -> str:
    return (
        remote_esptool_setup_script()
        + "run_esptool $ESPTOOL_STUB_ARGS --port "
        + shlex.quote(port)
        + " "
        + shlex.join([command] + rest)
    )


def idf_py_command(env: dict[str, str]) -> list[str]:
    resolved = shutil.which("idf.py", path=env.get("PATH"))
    if resolved:
        return [resolved]
    idf_path = env.get("IDF_PATH")
    if idf_path:
        idf_script = Path(idf_path) / "tools" / "idf.py"
        if idf_script.exists():
            python_env = env.get("IDF_PYTHON_ENV_PATH")
            if python_env:
                python = Path(python_env) / "bin" / "python"
                if python.exists():
                    return [str(python), str(idf_script)]
            return [sys.executable, str(idf_script)]
    return ["idf.py"]


def idf_build_command(
    env: dict[str, str],
    project: Path,
    build_dir: Path,
    sdkconfig: Path,
) -> list[str]:
    return idf_py_command(env) + [
        "-C",
        str(project),
        "-B",
        str(build_dir),
        "-D",
        f"SDKCONFIG={sdkconfig}",
        "build",
    ]


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
    target_arg = local_file_arg(device, target)
    result = run_esptool_with_spelling_fallback(
        list(device["tool"]["argv"]),
        device["port"],
        "read-flash",
        ["0", "ALL", target_arg],
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
        + remote_esptool_invocation(device["port"], "read_flash", ["0", "ALL", remote_path])
        + "; "
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
    sdkconfig = live_dir / "sdkconfigs" / f"{role}.sdkconfig"
    sdkconfig.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SDKCONFIG_DEFAULTS"] = f"sdkconfig.defaults;{override}"
    env["SDKCONFIG"] = str(sdkconfig)
    result = run_command(
        idf_build_command(env, project, build_dir, sdkconfig),
        env=env,
        timeout=900.0,
    )
    require_success(result, f"ESP-IDF build for {role}")
    artifact = capture_build_artifacts(role, build_dir)
    artifact["buildCommand"] = result
    artifact["project"] = str(project)
    artifact["sdkconfigDefaults"] = env["SDKCONFIG_DEFAULTS"]
    artifact["sdkconfig"] = str(sdkconfig)
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


def build_file_arg(
    path: Path,
    *,
    remote_dir: str | None = None,
    path_arg: Any | None = None,
) -> str:
    if remote_dir:
        return f"{remote_dir}/{path.name}"
    if path_arg:
        return path_arg(path)
    return str(path)


def write_flash_args(
    build: dict[str, Any],
    *,
    remote_dir: str | None = None,
    path_arg: Any | None = None,
) -> list[str]:
    args = list(build.get("writeFlashArgs", []))
    reject_forbidden_flash_args(args)
    for item in build["files"]:
        args.append(item["offset"])
        path = Path(item["path"])
        args.append(build_file_arg(path, remote_dir=remote_dir, path_arg=path_arg))
    return args


def verify_flash_args(
    build: dict[str, Any],
    *,
    remote_dir: str | None = None,
    path_arg: Any | None = None,
) -> list[str] | None:
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
        args.append(build_file_arg(path, remote_dir=remote_dir, path_arg=path_arg))
    return args


def flash_local_peer(device: dict[str, Any], build: dict[str, Any]) -> dict[str, Any]:
    write = run_esptool_with_spelling_fallback(
        list(device["tool"]["argv"]),
        device["port"],
        "write-flash",
        write_flash_args(build, path_arg=lambda path: local_file_arg(device, path)),
        timeout=700.0,
    )
    require_success(write, f"write-flash {device['role']}")
    record: dict[str, Any] = {"writeFlash": write}
    verify_args = verify_flash_args(build, path_arg=lambda path: local_file_arg(device, path))
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
            + remote_esptool_invocation(device["port"], command, rest)
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
                f"{REMOTE_ESPNOW_ESPTOOL} --port {device['port']} "
                "write-flash 0x0 <backup-file>"
            )
        else:
            backup_arg = local_file_arg(device, Path(backup))
            commands[role] = (
                f"{shlex.join(device['tool']['argv'])} --port {device['port']} "
                f"write-flash 0x0 {backup_arg}"
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


def normalize_text(text: str) -> str:
    text = text.lower().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", text)


def load_json_or_text(path: Path) -> tuple[Any | None, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        return json.loads(text), text
    except json.JSONDecodeError:
        parsed_lines = []
        for line in text.splitlines():
            try:
                parsed_lines.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return (parsed_lines if parsed_lines else None), text


def iter_dicts(value: Any) -> Any:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for item in value:
            yield from iter_dicts(item)


def extract_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and re.fullmatch(r"-?\d+", value.strip()):
        return int(value.strip())
    return None


def collect_counter_triples(parsed: Any | None, text: str) -> list[tuple[int, int, int]]:
    triples: list[tuple[int, int, int]] = []
    for item in iter_dicts(parsed):
        lowered = {str(key).lower(): value for key, value in item.items()}
        rx = extract_int(lowered.get("rx"))
        tx = extract_int(lowered.get("tx"))
        ack = None
        for key in ("acks", "ack", "app_acks", "appacks"):
            ack = extract_int(lowered.get(key))
            if ack is not None:
                break
        if rx is not None and tx is not None and ack is not None:
            triples.append((rx, tx, ack))

    for match in re.finditer(
        r"rx[^0-9]{0,10}(\d+)[^a-z0-9]{1,10}tx[^0-9]{0,10}(\d+)"
        r"[^a-z0-9]{1,10}a(?:ck|cks)?[^0-9]{0,10}(\d+)",
        text,
        flags=re.IGNORECASE,
    ):
        triples.append(tuple(int(part) for part in match.groups()))
    for match in re.finditer(r"\b(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\b", text):
        triples.append(tuple(int(part) for part in match.groups()))
    return triples


def audit_bridge_transcript(path: Path) -> dict[str, Any]:
    parsed, text = load_json_or_text(path)
    normalized = normalize_text(text)
    failures: list[str] = []

    missing = sorted(
        request
        for request in COMPLETE_REQUIRED_TRANSCRIPT_TYPES
        if request.replace("_", " ") not in normalized
    )
    if missing:
        failures.append("missing_transcript_types:" + ",".join(missing))

    peer_ids = sorted(peer for peer in COMPLETE_REQUIRED_PEERS if peer in normalized.replace(" ", ""))
    espnow_count = normalized.count("espnow enc")
    if set(peer_ids) != COMPLETE_REQUIRED_PEERS or espnow_count < 3:
        failures.append("transcript_peer_mismatch")

    serial_errors: list[int] = []
    for item in iter_dicts(parsed):
        for key, value in item.items():
            lowered_key = str(key).lower()
            if "serial" in lowered_key and ("err" in lowered_key or "error" in lowered_key):
                parsed_int = extract_int(value)
                if parsed_int is not None:
                    serial_errors.append(parsed_int)
    for match in re.finditer(r"serial[^\n]{0,30}err(?:or|ors)?[^0-9]{0,10}(\d+)", text, re.I):
        serial_errors.append(int(match.group(1)))
    if not serial_errors:
        failures.append("missing_serial_error_evidence")
    elif any(value != 0 for value in serial_errors):
        failures.append("serial_errors_nonzero")

    triples = collect_counter_triples(parsed, text)
    moving = False
    if len(triples) >= 2:
        rx_values = [item[0] for item in triples]
        tx_values = [item[1] for item in triples]
        ack_values = [item[2] for item in triples]
        moving = (
            max(rx_values) > min(rx_values)
            and max(tx_values) > min(tx_values)
            and max(ack_values) > min(ack_values)
        )
    if not moving:
        failures.append("counters_not_moving")

    return {
        "ok": not failures,
        "path": str(path),
        "sha256": sha256_file(path),
        "requiredTypes": sorted(COMPLETE_REQUIRED_TRANSCRIPT_TYPES),
        "peerIds": peer_ids,
        "espnowEncMentions": espnow_count,
        "serialErrors": serial_errors,
        "counterTriples": triples,
        "failures": failures,
    }


def cleanup_line_is_clear(line: str) -> bool:
    normalized = normalize_text(line)
    padded = f" {normalized} "
    clear_markers = (
        " no ",
        "none",
        "not found",
        "absent",
        "closed",
        "cleanup ok",
        "pass",
        "0 process",
        "0 listener",
        "not listening",
    )
    return any(marker in padded for marker in clear_markers)


def audit_cleanup_proof(path: Path) -> dict[str, Any]:
    parsed, text = load_json_or_text(path)
    lines = text.splitlines() or [text]
    failures: list[str] = []
    categories: dict[str, Any] = {}
    for category, terms in COMPLETE_CLEANUP_CATEGORIES.items():
        matching = [
            line.strip()
            for line in lines
            if any(normalize_text(term) in normalize_text(line) for term in terms)
        ]
        clear = bool(matching) and all(cleanup_line_is_clear(line) for line in matching)
        categories[category] = {"ok": clear, "lines": matching}
        if not clear:
            failures.append(f"cleanup_{category}_not_clear")
    return {
        "ok": not failures,
        "path": str(path),
        "sha256": sha256_file(path),
        "categories": categories,
        "failures": failures,
        "jsonParsed": parsed is not None,
    }


def audit_completion_manifest(manifest: dict[str, Any], manifest_path: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    for section in ["devices", "backups", "builds"]:
        if not isinstance(manifest.get(section), dict):
            failures.append(f"manifest_missing_{section}")
            continue
        missing_roles = [role for role in FLASH_ORDER if role not in manifest[section]]
        if missing_roles:
            failures.append(f"manifest_{section}_missing_roles:" + ",".join(missing_roles))

    flash_gate = manifest.get("flashGate", {})
    if flash_gate.get("requiresConfirmWriteFlash") is not True:
        failures.append("manifest_flash_gate_missing_confirm_write")
    if flash_gate.get("flashOrder") != FLASH_ORDER:
        failures.append("manifest_flash_order_mismatch")

    for role, backup in manifest.get("backups", {}).items():
        if not backup.get("sha256") or not backup.get("bytes"):
            failures.append(f"manifest_backup_incomplete:{role}")
        path = Path(str(backup.get("path", "")))
        if path.exists() and sha256_file(path) != backup.get("sha256"):
            failures.append(f"manifest_backup_hash_mismatch:{role}")
        elif not path.exists():
            warnings.append(f"backup_not_rechecked:{role}")

    for role, build in manifest.get("builds", {}).items():
        try:
            reject_forbidden_flash_args(list(build.get("writeFlashArgs", [])))
        except SystemExit:
            failures.append(f"manifest_forbidden_flash_args:{role}")
        for item in build.get("files", []):
            if not item.get("sha256") or not item.get("bytes") or not item.get("offset"):
                failures.append(f"manifest_build_file_incomplete:{role}")
            path = Path(str(item.get("path", "")))
            if path.exists() and sha256_file(path) != item.get("sha256"):
                failures.append(f"manifest_build_hash_mismatch:{role}")
            elif not path.exists():
                warnings.append(f"build_not_rechecked:{role}:{path.name}")

    return {
        "ok": not failures,
        "path": str(manifest_path),
        "sha256": sha256_file(manifest_path),
        "failures": failures,
        "warnings": warnings,
    }


def audit_flash_evidence(evidence: dict[str, Any], evidence_path: Path, manifest_path: Path) -> dict[str, Any]:
    failures: list[str] = []
    if evidence.get("ok") is not True:
        failures.append("flash_evidence_not_ok")
    evidence_manifest = evidence.get("manifest")
    if evidence_manifest:
        try:
            if Path(evidence_manifest).resolve() != manifest_path.resolve():
                failures.append("flash_evidence_manifest_mismatch")
        except OSError:
            failures.append("flash_evidence_manifest_mismatch")
    else:
        failures.append("flash_evidence_missing_manifest")

    results = evidence.get("results", {})
    if not isinstance(results, dict):
        failures.append("flash_evidence_missing_results")
        results = {}
    for role in FLASH_ORDER:
        role_result = results.get(role)
        if not isinstance(role_result, dict):
            failures.append(f"flash_evidence_missing_role:{role}")
            continue
        for key in ["writeFlash", "verifyFlash"]:
            command = role_result.get(key)
            if not isinstance(command, dict) or command.get("returncode") != 0:
                failures.append(f"flash_evidence_{key}_failed:{role}")

    return {
        "ok": not failures,
        "path": str(evidence_path),
        "sha256": sha256_file(evidence_path),
        "failures": failures,
    }


def audit_vision_gate(path: Path) -> dict[str, Any]:
    payload = json_load(path)
    failures: list[str] = []
    if payload.get("ok") is not True or payload.get("status") != "pass":
        failures.append("vision_gate_not_pass")
    views = payload.get("views", {})
    if not isinstance(views, dict):
        failures.append("vision_gate_missing_views")
        views = {}
    for view, result in views.items():
        if isinstance(result, dict) and result.get("required") and not result.get("ok"):
            failures.append(f"vision_gate_missing_view:{view}")
    for section in ["transcript", "cleanup"]:
        result = payload.get(section)
        if not isinstance(result, dict) or result.get("ok") is not True:
            failures.append(f"vision_gate_{section}_not_ok")
    if not payload.get("screenshots"):
        failures.append("vision_gate_missing_screenshot_hashes")
    return {
        "ok": not failures,
        "path": str(path),
        "sha256": sha256_file(path),
        "status": payload.get("status"),
        "failures": failures,
    }


def command_complete(args: argparse.Namespace) -> int:
    manifest_path = args.manifest.resolve()
    flash_evidence_path = args.flash_evidence.resolve()
    bridge_transcript_path = args.bridge_transcript.resolve()
    cleanup_proof_path = args.cleanup_proof.resolve()
    vision_gate_path = args.vision_gate.resolve()

    manifest = json_load(manifest_path)
    flash_evidence = json_load(flash_evidence_path)
    manifest_audit = audit_completion_manifest(manifest, manifest_path)
    flash_audit = audit_flash_evidence(flash_evidence, flash_evidence_path, manifest_path)
    transcript_audit = audit_bridge_transcript(bridge_transcript_path)
    cleanup_audit = audit_cleanup_proof(cleanup_proof_path)
    vision_audit = audit_vision_gate(vision_gate_path)

    failures = []
    for audit in [manifest_audit, flash_audit, transcript_audit, cleanup_audit, vision_audit]:
        failures.extend(audit.get("failures", []))
    status = "pass" if not failures else "needs_manual_review"
    payload = {
        "ok": status == "pass",
        "status": status,
        "generatedAt": utc_now(),
        "tool": "scripts/espnow_bbs_live_gate.py complete",
        "inputs": {
            "manifest": str(manifest_path),
            "flashEvidence": str(flash_evidence_path),
            "bridgeTranscript": str(bridge_transcript_path),
            "cleanupProof": str(cleanup_proof_path),
            "visionGate": str(vision_gate_path),
        },
        "manifest": manifest_audit,
        "flashEvidence": flash_audit,
        "transcript": transcript_audit,
        "cleanup": cleanup_audit,
        "visionGate": vision_audit,
        "failures": failures,
    }
    out = args.out.resolve() if args.out else manifest_path.parent / f"completion-evidence-{utc_stamp()}.json"
    json_write(out, payload)
    print(json.dumps({"ok": payload["ok"], "status": status, "evidence": str(out)}, indent=2))
    return 0 if payload["ok"] else 2


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

    complete_parser = sub.add_parser("complete", help="Audit post-run transcript, cleanup, and vision evidence.")
    complete_parser.add_argument("--manifest", type=Path, required=True)
    complete_parser.add_argument("--flash-evidence", type=Path, required=True)
    complete_parser.add_argument("--bridge-transcript", type=Path, required=True)
    complete_parser.add_argument("--cleanup-proof", type=Path, required=True)
    complete_parser.add_argument("--vision-gate", type=Path, required=True)
    complete_parser.add_argument("--out", type=Path)
    complete_parser.set_defaults(func=command_complete)

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
