#!/usr/bin/env python3
"""Read-only live-bench preflight for the ESP-NOW BBS bench lane."""

from __future__ import annotations

import argparse
import getpass
import grp
import json
import os
import platform
import pwd
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "research" / "bench-records" / "live-bench"

DEFAULT_WINDOWS_PORTS = ["COM4", "COM5", "COM6"]
CURRENT_ACCEPTED_WINDOWS_PORTS = ["COM6", "COM10", "COM12"]
DEFAULT_PI_USER = "dospi"
DEFAULT_PI_HOST = "172.16.0.2"
ACCEPTED_PI_ACCESS_HOSTS = {DEFAULT_PI_HOST, "192.168.137.93", "192.168.137.105"}
DEFAULT_COORDINATOR_PORT = "/dev/ttyUSB0"
REMOTE_ESPNOW_ESPTOOL = (
    "/home/dospi/dos-c/artifacts/runtime/esptool-venv-espnow-encrypted/bin/esptool"
)
ACCEPTED_PEER_ROLE_MACS = {
    "peer01": "94:b9:7e:da:17:d0",
    "peer02": "78:e3:6d:0a:90:14",
    "peer03": "94:b9:7e:da:9a:50",
}

EXPECTED_USB = {
    "descriptionContains": "CP210x",
    "pnpDeviceIdContains": "VID_10C4&PID_EA60",
    "status": "OK",
}

EXPECTED_ESP32 = {
    "chipContains": "ESP32-D0WDQ6",
    "flashSize": "4MB",
}

EXPECTED_PI = {
    "hostname": "dos-pi4-poe",
    "model": "Raspberry Pi 4 Model B Rev 1.2",
    "serial": "10000000aaaa5b24",
    "rootSource": "/dev/mmcblk0p2",
    "eth0Address": "172.16.0.2/24",
    "closedTcpPorts": ["31331", "31332", "8080"],
    "sshFingerprints": {
        "RSA": "SHA256:ZA1lH2codkJpMkj3FpSIoHoqFmUbRUIHO6QpUDcBT50",
        "ECDSA": "SHA256:IaFCqHEYIHPW4vMmzYgpATf3PdDwZS25Qm62Ct6U5ek",
        "ED25519": "SHA256:3VldDFyssS+mO+xRhsc2SljowM0ijPXiYSBv/vwPubA",
    },
}

CURRENT_ESPTOOL_COMMANDS = ("chip-id", "read-mac", "flash-id")
LEGACY_ESPTOOL_COMMANDS = ("chip_id", "read_mac", "flash_id")
ESPTOOL_COMMAND_ALIASES = {
    "chip-id": ("chip-id", "chip_id"),
    "read-mac": ("read-mac", "read_mac"),
    "flash-id": ("flash-id", "flash_id"),
}
ALLOWED_ESPTOOL_COMMANDS = CURRENT_ESPTOOL_COMMANDS
FORBIDDEN_ESPTOOL_TERMS = (
    "write_flash",
    "write-flash",
    "erase_flash",
    "erase-flash",
    "erase_region",
    "erase-region",
    "write_mem",
    "write-mem",
    "load_ram",
    "load-ram",
    "monitor",
)

STALE_PROCESS_PATTERN = (
    r"[e]sp32_gateway_sim|[e]spnow_bbs_bridge|[d]osbox-x|"
    r"[d]osbox|[z]enity|[y]ad"
)

TOOL_COMMANDS = {
    "eim": [["eim", "--version"], ["eim", "version"]],
    "idf.py": [["idf.py", "--version"]],
    "esptool.py": [["esptool.py", "version"]],
    "esptool": [["esptool", "version"]],
    "cmake": [["cmake", "--version"]],
    "ninja": [["ninja", "--version"]],
    "python3": [["python3", "--version"]],
    "python": [["python", "--version"]],
    "git": [["git", "--version"]],
    "cc": [["cc", "--version"]],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def repository_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def wsl_port_for_windows(windows_port: str) -> str:
    match = re.fullmatch(r"COM([0-9]+)", windows_port.strip().upper())
    if not match:
        raise ValueError(f"unsupported Windows serial port name: {windows_port}")
    return f"/dev/ttyS{int(match.group(1))}"


def normalize_windows_port(value: str) -> str:
    return value.strip().upper()


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_flash_size(value: str | None) -> str | None:
    if value is None:
        return None
    compact = re.sub(r"\s+", "", value.upper())
    compact = compact.replace("MIB", "MB").replace("KIB", "KB")
    return compact


def current_peer_role_ports(ports: list[str]) -> dict[str, str] | None:
    normalized = [normalize_windows_port(port) for port in ports]
    if normalized != CURRENT_ACCEPTED_WINDOWS_PORTS:
        return None
    return {
        f"peer{index:02d}": port
        for index, port in enumerate(CURRENT_ACCEPTED_WINDOWS_PORTS, start=1)
    }


def uses_expected_pi_profile(host: str) -> bool:
    return host in ACCEPTED_PI_ACCESS_HOSTS


def run_command(
    argv: list[str],
    *,
    timeout: float = 10.0,
    stdin: str | None = None,
) -> dict[str, Any]:
    try:
        result = subprocess.run(
            argv,
            input=stdin,
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


def first_successful(commands: list[list[str]], timeout: float = 5.0) -> dict[str, Any]:
    attempts = [run_command(command, timeout=timeout) for command in commands]
    selected = next(
        (
            attempt
            for attempt in attempts
            if attempt.get("available") and attempt.get("returncode") == 0
        ),
        attempts[0] if attempts else {"available": False},
    )
    return {"selected": selected, "attempts": attempts}


def read_json_from_lines(lines: list[str]) -> Any:
    text = "\n".join(lines).strip()
    if not text:
        return None
    return json.loads(text)


def collect_windows_peer_inventory(ports: list[str]) -> dict[str, Any]:
    expected_ports = [normalize_windows_port(port) for port in ports]
    powershell = shutil.which("powershell.exe")
    cmd = shutil.which("cmd.exe")
    ps_ports = "@(" + ",".join(f"'{port}'" for port in expected_ports) + ")"
    script = f"""
$expected = {ps_ports}
$serial = @(Get-CimInstance Win32_SerialPort |
    Select-Object Caption,Description,DeviceID,PNPDeviceID,Status,ConfigManagerErrorCode,Name,MaxBaudRate)
$pnp = @(Get-CimInstance Win32_PnPEntity |
    Where-Object {{ $_.Name -match '\\(COM[0-9]+\\)' -or $_.DeviceID -like '*VID_10C4*PID_EA60*' }} |
    Select-Object Name,DeviceID,Status,ConfigManagerErrorCode)
[pscustomobject]@{{
    expectedPorts = $expected
    serialPorts = $serial
    pnp = $pnp
}} | ConvertTo-Json -Depth 6
"""
    inventory: dict[str, Any] = {
        "expectedPorts": expected_ports,
        "expectedUsb": EXPECTED_USB,
        "powershellPath": powershell,
        "cmdPath": cmd,
    }
    if powershell:
        ps_result = run_command(
            [powershell, "-NoProfile", "-Command", script],
            timeout=15.0,
        )
        inventory["win32SerialPorts"] = ps_result
        try:
            parsed = read_json_from_lines(ps_result.get("stdout", []))
        except json.JSONDecodeError as exc:
            parsed = None
            inventory["parseError"] = str(exc)
        inventory["parsed"] = parsed
        inventory["expectedChecks"] = check_windows_peers(parsed, expected_ports)
    else:
        inventory["win32SerialPorts"] = {
            "available": False,
            "error": "powershell.exe not found",
        }
        inventory["expectedChecks"] = {
            "ok": False,
            "items": [
                {
                    "name": "powershellAvailable",
                    "ok": False,
                    "code": "powershellMissing",
                }
            ],
        }

    inventory["mode"] = {}
    if cmd:
        for port in expected_ports:
            inventory["mode"][port] = run_command([cmd, "/c", "mode", port], timeout=5.0)
    else:
        inventory["mode"]["error"] = "cmd.exe not found"
    return inventory


def serial_port_entries(parsed: Any) -> list[dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    entries = parsed.get("serialPorts", parsed.get("serialPort"))
    return [entry for entry in ensure_list(entries) if isinstance(entry, dict)]


def check_windows_peers(parsed: Any, expected_ports: list[str]) -> dict[str, Any]:
    expected = [normalize_windows_port(port) for port in expected_ports]
    entries = serial_port_entries(parsed)
    by_port = {
        normalize_windows_port(str(entry.get("DeviceID", ""))): entry
        for entry in entries
        if entry.get("DeviceID")
    }
    cp210x_ports = sorted(
        port
        for port, entry in by_port.items()
        if EXPECTED_USB["pnpDeviceIdContains"] in str(entry.get("PNPDeviceID", ""))
        or EXPECTED_USB["descriptionContains"].lower()
        in str(entry.get("Description", "")).lower()
    )

    items: list[dict[str, Any]] = [
        {
            "name": "exactCp210xPortSet",
            "ok": cp210x_ports == sorted(expected),
            "code": (
                "unexpectedWindowsPeerSet"
                if cp210x_ports != sorted(expected)
                else None
            ),
            "expected": sorted(expected),
            "value": cp210x_ports,
        }
    ]
    for port in expected:
        entry = by_port.get(port)
        if entry is None:
            items.append(
                {
                    "name": f"{port}.present",
                    "ok": False,
                    "code": "missingWindowsPeer",
                    "value": None,
                }
            )
            continue
        description = str(entry.get("Description", ""))
        pnp_device = str(entry.get("PNPDeviceID", ""))
        status_text = str(entry.get("Status", ""))
        items.extend(
            [
                {
                    "name": f"{port}.description",
                    "ok": EXPECTED_USB["descriptionContains"].lower()
                    in description.lower(),
                    "code": "unexpectedUsbDescription",
                    "value": description,
                },
                {
                    "name": f"{port}.pnpDeviceId",
                    "ok": EXPECTED_USB["pnpDeviceIdContains"] in pnp_device,
                    "code": "unexpectedVidPid",
                    "value": pnp_device,
                },
                {
                    "name": f"{port}.status",
                    "ok": status_text == EXPECTED_USB["status"],
                    "code": "unexpectedWindowsStatus",
                    "value": status_text,
                },
            ]
        )
    for item in items:
        if item.get("ok"):
            item.pop("code", None)
    return {"ok": all(item["ok"] for item in items), "items": items}


def collect_wsl_serial_permissions(ports: list[str]) -> dict[str, Any]:
    records: dict[str, Any] = {}
    for windows_port in ports:
        wsl_port = wsl_port_for_windows(windows_port)
        path = Path(wsl_port)
        record: dict[str, Any] = {
            "path": wsl_port,
            "windowsPort": normalize_windows_port(windows_port),
            "exists": path.exists(),
            "currentUser": getpass.getuser(),
            "currentGroups": sorted(
                grp.getgrgid(gid).gr_name for gid in os.getgroups()
            ),
        }
        if path.exists():
            st = path.stat()
            record.update(
                {
                    "mode": stat.filemode(st.st_mode),
                    "octalMode": oct(stat.S_IMODE(st.st_mode)),
                    "owner": pwd.getpwuid(st.st_uid).pw_name,
                    "group": grp.getgrgid(st.st_gid).gr_name,
                    "rdevMajor": os.major(st.st_rdev),
                    "rdevMinor": os.minor(st.st_rdev),
                    "userInDeviceGroup": st.st_gid in os.getgroups(),
                }
            )
        records[normalize_windows_port(windows_port)] = record
    return {"ports": records}


def collect_toolchain_status() -> dict[str, Any]:
    record: dict[str, Any] = {
        "platform": platform.platform(),
        "pythonExecutable": sys.executable,
        "commands": {},
        "localEim": {},
        "activationScripts": {},
        "windowsEsptool": {},
        "sudoNonInteractive": run_command(["sudo", "-n", "true"], timeout=3.0),
        "espIdfCandidates": find_esp_idf_candidates(),
    }

    for name, commands in TOOL_COMMANDS.items():
        record["commands"][name] = first_successful(commands, timeout=6.0)

    for candidate in sorted((Path.home() / ".local" / "opt").glob("eim-*/eim")):
        record["localEim"][str(candidate)] = run_command(
            [str(candidate), "--version"],
            timeout=6.0,
        )

    for activation_script in sorted(
        (Path.home() / ".espressif" / "tools").glob("activate_idf_v*.sh")
    ):
        script = shlex.quote(str(activation_script))
        record["activationScripts"][str(activation_script)] = run_command(
            [
                "bash",
                "-lc",
                "source "
                + script
                + " >/dev/null && "
                + "printf 'IDF_PATH=%s\\n' \"$IDF_PATH\" && "
                + "printf 'IDF_TOOLS_PATH=%s\\n' \"$IDF_TOOLS_PATH\" && "
                + "idf.py --version && "
                + "git -C \"$IDF_PATH\" describe --tags --always && "
                + "python --version && "
                + "cmake --version && "
                + "ninja --version && "
                + "xtensa-esp32-elf-gcc --version",
            ],
            timeout=20.0,
        )

    windows_candidates = [
        Path("/mnt/c/Python314/Scripts/esptool.exe"),
        Path("/mnt/c/Python313/Scripts/esptool.exe"),
        Path("/mnt/c/Python312/Scripts/esptool.exe"),
    ]
    for candidate in windows_candidates:
        if candidate.exists():
            record["windowsEsptool"][str(candidate)] = run_command(
                [str(candidate), "version"],
                timeout=6.0,
            )
    py_exe = shutil.which("py.exe")
    if py_exe:
        record["windowsEsptool"]["py.exe -m esptool"] = run_command(
            [py_exe, "-m", "esptool", "version"],
            timeout=6.0,
        )
    return record


def find_esp_idf_candidates() -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    env_idf = os.environ.get("IDF_PATH")
    if env_idf:
        add_idf_candidate(candidates, Path(env_idf), "IDF_PATH")

    home = Path.home()
    for candidate in [
        home / "esp-idf",
        home / "esp" / "esp-idf",
        home / "Espressif" / "frameworks" / "esp-idf",
        home / ".espressif" / "esp-idf",
    ]:
        add_idf_candidate(candidates, candidate, "common-path")

    for base in [home / "esp", home / "Espressif", home / ".espressif"]:
        if base.exists():
            for idf_py in find_named_file(base, "idf.py", max_depth=5):
                if idf_py.parent.name == "tools":
                    add_idf_candidate(candidates, idf_py.parents[1], "search")

    return sorted(candidates.values(), key=lambda item: item["path"])


def find_named_file(base: Path, filename: str, *, max_depth: int) -> list[Path]:
    found: list[Path] = []
    base_depth = len(base.resolve().parts)
    for root, dirs, files in os.walk(base):
        root_path = Path(root)
        depth = len(root_path.resolve().parts) - base_depth
        if depth >= max_depth:
            dirs[:] = []
        if filename in files:
            found.append(root_path / filename)
    return found


def add_idf_candidate(
    candidates: dict[str, dict[str, Any]],
    path: Path,
    source: str,
) -> None:
    if not path.exists():
        return
    resolved = path.resolve()
    idf_py = resolved / "tools" / "idf.py"
    export_sh = resolved / "export.sh"
    record = {
        "path": str(resolved),
        "source": source,
        "hasToolsIdfPy": idf_py.exists(),
        "hasExportSh": export_sh.exists(),
    }
    if (resolved / ".git").exists():
        record["gitDescribe"] = run_command(
            ["git", "-C", str(resolved), "describe", "--tags", "--always"],
            timeout=6.0,
        )
        record["gitStatus"] = run_command(
            ["git", "-C", str(resolved), "status", "--short"],
            timeout=6.0,
        )
    candidates[str(resolved)] = record


def esptool_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for name in ("esptool.py", "esptool"):
        path = shutil.which(name)
        if path:
            candidates.append({"argv": [path], "portKind": "wsl"})
    for path in [
        Path("/mnt/c/Python314/Scripts/esptool.exe"),
        Path("/mnt/c/Python313/Scripts/esptool.exe"),
        Path("/mnt/c/Python312/Scripts/esptool.exe"),
    ]:
        if path.exists():
            candidates.append({"argv": [str(path)], "portKind": "windows"})
    py_exe = shutil.which("py.exe")
    if py_exe:
        candidates.append({"argv": [py_exe, "-m", "esptool"], "portKind": "windows"})
    return candidates


def select_esptool() -> dict[str, Any]:
    attempts = []
    for candidate in esptool_candidates():
        version = run_command(candidate["argv"] + ["version"], timeout=6.0)
        attempts.append({**candidate, "version": version})
        if version.get("available") and version.get("returncode") == 0:
            return {"selected": candidate, "attempts": attempts}
    return {"selected": None, "attempts": attempts}


def collect_peer_esp32_identities(ports: list[str]) -> dict[str, Any]:
    selected = select_esptool()
    identities: dict[str, Any] = {
        "expectedProfile": EXPECTED_ESP32,
        "allowedCommands": list(ALLOWED_ESPTOOL_COMMANDS),
        "legacyParsedCommandNames": list(LEGACY_ESPTOOL_COMMANDS),
        "forbiddenTerms": list(FORBIDDEN_ESPTOOL_TERMS),
        "toolSelection": selected,
        "ports": {},
    }
    for windows_port in ports:
        port_name = normalize_windows_port(windows_port)
        identities["ports"][port_name] = collect_esp32_identity_for_port(
            selected,
            port_name,
            wsl_port_for_windows(port_name),
        )
    identities["ok"] = all(
        identity.get("ok") for identity in identities["ports"].values()
    )
    return identities


def collect_esp32_identity_for_port(
    selected: dict[str, Any],
    windows_port: str,
    wsl_port: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "windowsPort": normalize_windows_port(windows_port),
        "wslPort": wsl_port,
        "commands": {},
    }
    tool = selected.get("selected")
    if not tool:
        record["ok"] = False
        record["error"] = "no esptool command available"
        finalize_esp32_identity(record)
        return record

    port = windows_port if tool["portKind"] == "windows" else wsl_port
    record["port"] = port
    record["portKind"] = tool["portKind"]
    record["tool"] = tool
    for command in ALLOWED_ESPTOOL_COMMANDS:
        argv = tool["argv"] + ["--port", port, command]
        if any(term in " ".join(argv) for term in FORBIDDEN_ESPTOOL_TERMS):
            record["commands"][command] = {
                "available": False,
                "blocked": True,
                "error": "forbidden esptool term would be used",
                "argv": argv,
            }
            continue
        record["commands"][command] = run_command(argv, timeout=30.0)
    finalize_esp32_identity(record)
    return record


def identity_command_result(
    commands: dict[str, Any],
    canonical_command: str,
) -> tuple[str, dict[str, Any]]:
    for command in ESPTOOL_COMMAND_ALIASES[canonical_command]:
        if command in commands:
            return command, commands[command]
    return canonical_command, {}


def collect_esptool_warnings(commands: dict[str, Any]) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    for command, result in sorted(commands.items()):
        if not isinstance(result, dict):
            continue
        for stream_name in ("stdout", "stderr"):
            for line in result.get(stream_name, []):
                text = str(line)
                lowered = text.lower()
                if "warning" in lowered or "deprecated" in lowered:
                    warnings.append(
                        {
                            "command": command,
                            "stream": stream_name,
                            "text": text,
                        }
                    )
    return warnings


def parse_esptool_identity(commands: dict[str, Any]) -> dict[str, Any]:
    lines: list[str] = []
    command_results: dict[str, bool] = {}
    command_sources: dict[str, str | None] = {}
    for command in CURRENT_ESPTOOL_COMMANDS:
        source_command, result = identity_command_result(commands, command)
        command_sources[command] = source_command if result else None
        command_results[command] = result.get("returncode") == 0
        lines.extend(str(line) for line in result.get("stdout", []))
        lines.extend(str(line) for line in result.get("stderr", []))
    text = "\n".join(lines)
    chip_match = re.search(r"Chip is\s+([A-Za-z0-9_ -]+)(?:\s+\(|$)", text)
    if chip_match:
        chip = chip_match.group(1).strip()
    else:
        chip_match = re.search(r"Detecting chip type\.\.\.\s*([A-Za-z0-9_-]+)", text)
        chip = chip_match.group(1).strip() if chip_match else None

    mac_match = re.search(r"\bMAC:\s*([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})", text)
    flash_match = re.search(
        r"Detected flash size:\s*([0-9]+)\s*([KMGT]?B?)",
        text,
        re.IGNORECASE,
    )
    manufacturer_match = re.search(r"Manufacturer:\s*([0-9a-fA-Fx]+)", text)
    device_match = re.search(r"Device:\s*([0-9a-fA-Fx]+)", text)
    parsed = {
        "chip": chip,
        "chipTextContainsExpected": EXPECTED_ESP32["chipContains"] in text,
        "mac": mac_match.group(1).lower() if mac_match else None,
        "flashSize": normalize_flash_size(
            "".join(flash_match.groups()) if flash_match else None
        ),
        "manufacturer": manufacturer_match.group(1) if manufacturer_match else None,
        "device": device_match.group(1) if device_match else None,
        "commandResults": command_results,
        "commandSources": command_sources,
        "usesLegacyCommandNames": any(
            source in LEGACY_ESPTOOL_COMMANDS
            for source in command_sources.values()
            if source
        ),
        "esptoolWarnings": collect_esptool_warnings(commands),
    }
    parsed["profileChecks"] = validate_esp32_profile(parsed)
    parsed["ok"] = (
        all(command_results.values())
        and parsed["mac"] is not None
        and parsed["profileChecks"]["ok"]
    )
    return parsed


def validate_esp32_profile(parsed: dict[str, Any]) -> dict[str, Any]:
    items = [
        {
            "name": "chip",
            "ok": bool(parsed.get("chipTextContainsExpected"))
            or EXPECTED_ESP32["chipContains"] in str(parsed.get("chip", "")),
            "code": "unexpectedChipProfile",
            "expected": EXPECTED_ESP32["chipContains"],
            "value": parsed.get("chip"),
        },
        {
            "name": "mac",
            "ok": bool(parsed.get("mac")),
            "code": "missingMac",
            "value": parsed.get("mac"),
        },
        {
            "name": "flashSize",
            "ok": parsed.get("flashSize") == EXPECTED_ESP32["flashSize"],
            "code": "unexpectedFlashProfile",
            "expected": EXPECTED_ESP32["flashSize"],
            "value": parsed.get("flashSize"),
        },
    ]
    for item in items:
        if item["ok"]:
            item.pop("code", None)
    return {"ok": all(item["ok"] for item in items), "items": items}


def finalize_esp32_identity(record: dict[str, Any]) -> dict[str, Any]:
    parsed = parse_esptool_identity(record.get("commands", {}))
    record["parsedIdentity"] = parsed
    command_ok = all(
        result.get("returncode") == 0
        for result in record.get("commands", {}).values()
    )
    record["ok"] = command_ok and parsed.get("ok", False)
    if not record["ok"] and not record.get("error"):
        record["error"] = "esptool identity output did not match expected ESP32 profile"
    return record


def remote_coordinator_tool_missing(record: dict[str, Any]) -> bool:
    commands = record.get("commands", {})
    if not commands:
        return False
    for result in commands.values():
        text = "\n".join(result.get("stdout", []) + result.get("stderr", []))
        if result.get("returncode") != 127 or "esptool not found" not in text:
            return False
    return True


def parse_fingerprint_lines(lines: list[str]) -> dict[str, str]:
    fingerprints: dict[str, str] = {}
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        key_type = parts[-1].strip("()").upper()
        fingerprints[key_type] = parts[1]
    return fingerprints


def collect_pi_identity(
    user: str,
    host: str,
    output_dir: Path | None,
    stamp: str,
    coordinator_port: str,
    skip_coordinator: bool,
    allow_discovered_host: bool,
) -> dict[str, Any]:
    use_expected_profile = uses_expected_pi_profile(host) or allow_discovered_host
    record: dict[str, Any] = {
        "target": f"{user}@{host}",
        "expected": EXPECTED_PI if use_expected_profile else None,
        "coordinatorPort": coordinator_port,
        "hostPolicy": (
            "accepted_known_host"
            if uses_expected_pi_profile(host)
            else "discovered_host_expected_identity"
            if allow_discovered_host
            else "unaccepted_host"
        ),
    }
    keyscan = run_command(["ssh-keyscan", "-T", "5", host], timeout=8.0)
    record["sshKeyscan"] = keyscan
    key_lines = [line for line in keyscan.get("stdout", []) if line.strip()]
    keygen = run_command(["ssh-keygen", "-lf", "-"], stdin="\n".join(key_lines), timeout=5.0)
    record["sshFingerprints"] = keygen
    observed = parse_fingerprint_lines(keygen.get("stdout", []))
    record["observedFingerprints"] = observed
    expected = EXPECTED_PI["sshFingerprints"] if use_expected_profile else {}
    record["fingerprintCheck"] = {
        "ok": bool(expected) and observed == expected,
        "expected": expected,
        "observed": observed,
    }
    if not key_lines:
        record["ok"] = False
        record["error"] = "ssh-keyscan returned no host keys"
        return record
    if expected and observed != expected:
        record["ok"] = False
        record["error"] = "ssh host fingerprints do not match expected gate"
        return record

    known_hosts_path: Path
    temp_file: tempfile.NamedTemporaryFile[str] | None = None
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        known_hosts_path = output_dir / f"local-known-hosts-{host}-{stamp}"
        known_hosts_path.write_text("\n".join(key_lines) + "\n", encoding="utf-8")
        record["knownHostsPath"] = repository_relative(known_hosts_path)
    else:
        temp_file = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
        temp_file.write("\n".join(key_lines) + "\n")
        temp_file.close()
        known_hosts_path = Path(temp_file.name)
        record["knownHostsPath"] = str(known_hosts_path)

    try:
        remote_script = build_pi_remote_script(coordinator_port, skip_coordinator)
        ssh = run_command(
            [
                "ssh",
                "-o",
                f"UserKnownHostsFile={known_hosts_path}",
                "-o",
                "StrictHostKeyChecking=yes",
                "-o",
                "BatchMode=yes",
                "-o",
                "ConnectTimeout=8",
                f"{user}@{host}",
                remote_script,
            ],
            timeout=90.0,
        )
    finally:
        if temp_file is not None:
            try:
                Path(temp_file.name).unlink()
            except FileNotFoundError:
                pass

    record["sshIdentity"] = ssh
    record["identityChecks"] = check_pi_identity(
        ssh.get("stdout", []),
        host,
        coordinator_port,
        allow_discovered_host=allow_discovered_host,
    )
    record["coordinatorEsp32Identity"] = parse_remote_coordinator_identity(
        ssh.get("stdout", []),
        coordinator_port,
        skipped=skip_coordinator,
    )
    record["ok"] = (
        record["fingerprintCheck"]["ok"]
        and ssh.get("returncode") == 0
        and record["identityChecks"]["ok"]
        and (skip_coordinator or record["coordinatorEsp32Identity"].get("ok"))
    )
    return record


def build_pi_remote_script(coordinator_port: str, skip_coordinator: bool) -> str:
    skip_value = "1" if skip_coordinator else "0"
    return f"""
set -u
COORDINATOR_PORT={shlex.quote(coordinator_port)}
SKIP_COORDINATOR={skip_value}
echo "__hostnamectl__"
hostnamectl
echo "__model__"
tr -d '\\000' </proc/device-tree/model || true
echo
echo "__serial__"
awk '/^Serial/ {{print $3}}' /proc/cpuinfo
echo "__root_source__"
findmnt -no SOURCE /
echo "__os_release__"
if [ -r /etc/os-release ]; then . /etc/os-release; printf '%s\\n' "${{PRETTY_NAME:-unknown}}"; fi
echo "__kernel__"
uname -a
echo "__ip_addr__"
ip -brief address
echo "__eth0_addr__"
ip -brief address show eth0 || true
echo "__listeners__"
if command -v ss >/dev/null 2>&1; then ss -ltnH; else netstat -ltn; fi | awk '$0 ~ /:(31331|31332|8080)([[:space:]]|$)/ {{print}}'
echo "__processes__"
pgrep -af '{STALE_PROCESS_PATTERN}' || true
echo "__usb_inventory__"
if command -v lsusb >/dev/null 2>&1; then lsusb; else echo "lsusb missing"; fi
ls -l /dev/ttyUSB* 2>/dev/null || true
if [ "$SKIP_COORDINATOR" = "0" ]; then
  if [ -e "$COORDINATOR_PORT" ]; then
    REMOTE_ESPNOW_ESPTOOL={shlex.quote(REMOTE_ESPNOW_ESPTOOL)}
    ESPTOOL_STUB_ARGS=""
    if [ -x "$REMOTE_ESPNOW_ESPTOOL" ]; then ESPTOOL="$REMOTE_ESPNOW_ESPTOOL";
    elif command -v esptool >/dev/null 2>&1; then ESPTOOL="esptool"; ESPTOOL_STUB_ARGS="--no-stub";
    elif command -v esptool.py >/dev/null 2>&1; then ESPTOOL="esptool.py"; ESPTOOL_STUB_ARGS="--no-stub";
    elif python3 -c 'import esptool' >/dev/null 2>&1; then ESPTOOL="python3 -m esptool"; ESPTOOL_STUB_ARGS="--no-stub";
    else ESPTOOL=""; fi
    echo "__coordinator_esptool__"
    printf '%s stub_args=%s\\n' "${{ESPTOOL:-missing}}" "${{ESPTOOL_STUB_ARGS:-none}}"
    for CMD in chip-id read-mac flash-id; do
      echo "__coordinator_${{CMD}}__"
      if [ -n "$ESPTOOL" ]; then
        $ESPTOOL $ESPTOOL_STUB_ARGS --port "$COORDINATOR_PORT" "$CMD" 2>&1
        RC=$?
      else
        echo "esptool not found"
        RC=127
      fi
      echo "__coordinator_${{CMD}}_returncode__"
      printf '%s\\n' "$RC"
    done
  else
    echo "__coordinator_missing__"
    printf '%s\\n' "$COORDINATOR_PORT"
  fi
fi
"""


def section_value(lines: list[str], section: str) -> list[str]:
    marker = f"__{section}__"
    start = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index + 1
            break
    if start is None:
        return []
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("__") and lines[index].endswith("__"):
            end = index
            break
    return lines[start:end]


def check_pi_identity(
    lines: list[str],
    host: str,
    coordinator_port: str,
    *,
    allow_discovered_host: bool = False,
) -> dict[str, Any]:
    expected = (
        EXPECTED_PI if uses_expected_pi_profile(host) or allow_discovered_host else {}
    )
    hostnamectl = "\n".join(section_value(lines, "hostnamectl"))
    model = " ".join(section_value(lines, "model")).strip()
    serial = " ".join(section_value(lines, "serial")).strip()
    root_source = " ".join(section_value(lines, "root_source")).strip()
    eth0_address = "\n".join(section_value(lines, "eth0_addr"))
    listeners = [line for line in section_value(lines, "listeners") if line.strip()]
    processes = [line for line in section_value(lines, "processes") if line.strip()]
    usb_inventory = "\n".join(section_value(lines, "usb_inventory"))
    coordinator_missing = section_value(lines, "coordinator_missing")
    items = [
        {
            "name": "hostname",
            "ok": expected.get("hostname", "") in hostnamectl,
            "code": "piHostnameMismatch",
            "value": hostnamectl,
        },
        {
            "name": "model",
            "ok": model == expected.get("model", model),
            "code": "piModelMismatch",
            "value": model,
        },
        {
            "name": "serial",
            "ok": serial == expected.get("serial", serial),
            "code": "piSerialMismatch",
            "value": serial,
        },
        {
            "name": "rootSource",
            "ok": root_source == expected.get("rootSource", root_source),
            "code": "piRootMismatch",
            "value": root_source,
        },
        {
            "name": "eth0Address",
            "ok": expected.get("eth0Address", "") in eth0_address,
            "code": "piEth0AddressMismatch",
            "value": eth0_address,
        },
        {
            "name": "closedTcpPorts",
            "ok": not listeners,
            "code": "stalePiListener",
            "value": listeners,
        },
        {
            "name": "noBridgeDosboxOrModalProcesses",
            "ok": not processes,
            "code": "stalePiProcess",
            "value": processes,
        },
        {
            "name": "coordinatorUsbPresent",
            "ok": not coordinator_missing and coordinator_port in usb_inventory,
            "code": "coordinatorUsbMissing",
            "value": usb_inventory if usb_inventory else coordinator_missing,
        },
    ]
    for item in items:
        if item["ok"]:
            item.pop("code", None)
    return {"ok": all(item["ok"] for item in items), "items": items}


def parse_remote_coordinator_identity(
    lines: list[str],
    coordinator_port: str,
    *,
    skipped: bool,
) -> dict[str, Any]:
    if skipped:
        return {"skipped": True, "ok": False}
    if section_value(lines, "coordinator_missing"):
        return {
            "ok": False,
            "port": coordinator_port,
            "error": "coordinator USB serial device missing",
            "commands": {},
            "parsedIdentity": parse_esptool_identity({}),
        }
    commands: dict[str, Any] = {}
    for command in ALLOWED_ESPTOOL_COMMANDS:
        rc_lines = section_value(lines, f"coordinator_{command}_returncode")
        try:
            returncode = int(" ".join(rc_lines).strip())
        except ValueError:
            returncode = None
        commands[command] = {
            "available": True,
            "argv": ["ssh", "remote", "esptool", "--port", coordinator_port, command],
            "returncode": returncode,
            "stdout": section_value(lines, f"coordinator_{command}"),
            "stderr": [],
        }
    record: dict[str, Any] = {
        "port": coordinator_port,
        "portKind": "pi-ssh",
        "commands": commands,
    }
    if remote_coordinator_tool_missing(record):
        record["toolMissing"] = True
        record["error"] = "Pi esptool command is not available"
    finalize_esp32_identity(record)
    return record


def collect_failures_from_items(
    section: str,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for item in items:
        if item.get("ok"):
            continue
        failures.append(
            {
                "section": section,
                "name": item.get("name"),
                "code": item.get("code", "gateFailed"),
                "expected": item.get("expected"),
                "value": item.get("value"),
            }
        )
    return failures


def validate_preflight_record(record: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    verified_facts: list[str] = []
    expected_ports = [
        normalize_windows_port(port)
        for port in record.get("expectedPeerPorts", DEFAULT_WINDOWS_PORTS)
    ]
    peer_port_policy = record.get("peerPortPolicy", {})
    peer_port_policy_mode = peer_port_policy.get("mode", "default_com_order")

    windows_checks = record.get("windowsPeerInventory", {}).get("expectedChecks")
    if not windows_checks or not windows_checks.get("ok"):
        failures.extend(
            collect_failures_from_items(
                "windowsPeerInventory",
                (windows_checks or {}).get("items", []),
            )
        )
    else:
        verified_facts.append(
            "Windows inventory contains exactly "
            + ", ".join(expected_ports)
            + " CP210x VID:PID 10C4:EA60 peers."
        )

    peer_identities = record.get("peerEsp32Identities", {}).get("ports", {})
    peer_macs: dict[str, str] = {}
    malformed_peer = False
    for port in expected_ports:
        identity = peer_identities.get(port)
        if not identity:
            malformed_peer = True
            failures.append(
                {
                    "section": "peerEsp32Identities",
                    "name": port,
                    "code": "missingPeerIdentity",
                    "value": None,
                }
            )
            continue
        parsed = identity.get("parsedIdentity", {})
        profile_checks = parsed.get("profileChecks", {})
        if not identity.get("ok"):
            malformed_peer = True
            failures.append(
                {
                    "section": "peerEsp32Identities",
                    "name": port,
                    "code": "malformedPeerIdentity",
                    "value": identity.get("error"),
                }
            )
            failures.extend(
                collect_failures_from_items(
                    f"peerEsp32Identities.{port}",
                    profile_checks.get("items", []),
                )
            )
        mac = parsed.get("mac")
        if mac:
            peer_macs[port] = mac

    mac_to_ports: dict[str, list[str]] = {}
    for port, mac in peer_macs.items():
        mac_to_ports.setdefault(mac, []).append(port)
    duplicate_macs = {
        mac: ports for mac, ports in mac_to_ports.items() if len(ports) > 1
    }
    if duplicate_macs:
        failures.append(
            {
                "section": "peerEsp32Identities",
                "name": "macUniqueness",
                "code": "duplicatePeerMac",
                "value": duplicate_macs,
            }
        )
    elif (
        peer_port_policy_mode == "accepted_mac_remap"
        and len(peer_macs) == len(expected_ports)
        and not malformed_peer
    ):
        expected_role_macs = {
            str(role): str(mac).lower()
            for role, mac in peer_port_policy.get(
                "acceptedPeerRoleMacs", ACCEPTED_PEER_ROLE_MACS
            ).items()
        }
        observed_macs = set(peer_macs.values())
        expected_macs = set(expected_role_macs.values())
        if observed_macs != expected_macs:
            failures.append(
                {
                    "section": "peerEsp32Identities",
                    "name": "acceptedPeerRoleMacs",
                    "code": "unexpectedPeerMacSet",
                    "expected": expected_role_macs,
                    "value": peer_macs,
                }
            )
        else:
            verified_facts.append(
                "Read-only esptool identity matched the accepted peer role MACs on current Windows COM ports."
            )
            current_role_ports = peer_port_policy.get("currentAcceptedRolePorts", {})
            if current_role_ports:
                verified_facts.append(
                    "Current accepted peer role port map is "
                    + ", ".join(
                        f"{role}={port}"
                        for role, port in sorted(current_role_ports.items())
                    )
                    + "."
                )
    elif len(peer_macs) == len(expected_ports) and not malformed_peer:
        verified_facts.append(
            "Read-only esptool identity passed for "
            + ", ".join(expected_ports)
            + " with distinct ESP32 MACs."
        )

    pi_identity = record.get("piIdentity", {})
    if pi_identity.get("skipped"):
        failures.append(
            {
                "section": "piIdentity",
                "name": "requiredPiGate",
                "code": "skippedRequiredGate",
                "value": "Pi identity was skipped",
            }
        )
    elif not pi_identity.get("fingerprintCheck", {}).get("ok"):
        failures.append(
            {
                "section": "piIdentity",
                "name": "sshFingerprints",
                "code": "piFingerprintMismatch",
                "expected": pi_identity.get("fingerprintCheck", {}).get("expected"),
                "value": pi_identity.get("fingerprintCheck", {}).get("observed"),
            }
        )
    else:
        verified_facts.append("Pi SSH host fingerprints match the expected gate.")

    pi_checks = pi_identity.get("identityChecks")
    if not pi_identity.get("skipped") and (not pi_checks or not pi_checks.get("ok")):
        failures.extend(
            collect_failures_from_items("piIdentity", (pi_checks or {}).get("items", []))
        )
    elif not pi_identity.get("skipped"):
        verified_facts.append(
            "Pi hostname, model, serial, root filesystem, eth0 address, stale listeners, and stale processes match the gate."
        )

    coordinator = pi_identity.get("coordinatorEsp32Identity", {})
    coordinator_mac = coordinator.get("parsedIdentity", {}).get("mac")
    if coordinator.get("skipped"):
        failures.append(
            {
                "section": "piIdentity.coordinatorEsp32Identity",
                "name": "requiredCoordinatorGate",
                "code": "skippedRequiredGate",
                "value": "Coordinator identity was skipped",
            }
        )
    elif remote_coordinator_tool_missing(coordinator) or coordinator.get("toolMissing"):
        failures.append(
            {
                "section": "piIdentity.coordinatorEsp32Identity",
                "name": "coordinatorTool",
                "code": "piCoordinatorToolMissing",
                "value": "Pi esptool command is not available",
            }
        )
    elif not coordinator.get("ok"):
        failures.append(
            {
                "section": "piIdentity.coordinatorEsp32Identity",
                "name": "coordinatorProfile",
                "code": "malformedCoordinatorIdentity",
                "value": coordinator.get("error"),
            }
        )
        failures.extend(
            collect_failures_from_items(
                "piIdentity.coordinatorEsp32Identity",
                coordinator.get("parsedIdentity", {})
                .get("profileChecks", {})
                .get("items", []),
            )
        )
    elif coordinator_mac in set(peer_macs.values()):
        failures.append(
            {
                "section": "piIdentity.coordinatorEsp32Identity",
                "name": "coordinatorMacUniqueness",
                "code": "coordinatorMacMatchesPeer",
                "value": coordinator_mac,
            }
        )
    else:
        verified_facts.append(
            "Pi /dev/ttyUSB0 coordinator read-only esptool identity passed and is distinct from the peer MACs."
        )

    peer_map: dict[str, Any] = {}
    if not failures and len(peer_macs) == len(expected_ports) and coordinator_mac:
        if peer_port_policy_mode == "accepted_mac_remap":
            role_for_mac = {
                str(mac).lower(): str(role)
                for role, mac in peer_port_policy.get(
                    "acceptedPeerRoleMacs", ACCEPTED_PEER_ROLE_MACS
                ).items()
            }
            peer_ports = [
                (role_for_mac[peer_macs[port]], port) for port in expected_ports
            ]
        else:
            peer_ports = [
                (f"peer{index:02d}", port)
                for index, port in enumerate(expected_ports, start=1)
            ]
        for peer_id, port in sorted(peer_ports):
            identity = peer_identities[port]
            peer_map[peer_id] = {
                "windowsPort": port,
                "wslPort": wsl_port_for_windows(port),
                "mac": identity["parsedIdentity"]["mac"],
                "chip": identity["parsedIdentity"]["chip"],
                "flashSize": identity["parsedIdentity"]["flashSize"],
            }
        record["coordinatorMap"] = {
            "id": "coord01",
            "piPort": record.get("coordinatorPort", DEFAULT_COORDINATOR_PORT),
            "mac": coordinator_mac,
            "chip": coordinator["parsedIdentity"]["chip"],
            "flashSize": coordinator["parsedIdentity"]["flashSize"],
        }
    record["peerMap"] = peer_map
    record["verifiedFacts"] = verified_facts
    record["failures"] = failures
    record["ok"] = not failures
    return record


def summarize_preflight_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a compact, non-secret gate summary for operator review."""

    peer_summary = {}
    peer_warnings: dict[str, list[dict[str, str]]] = {}
    for port, identity in sorted(
        record.get("peerEsp32Identities", {}).get("ports", {}).items()
    ):
        parsed = identity.get("parsedIdentity", {})
        warnings = parsed.get("esptoolWarnings", [])
        if warnings:
            peer_warnings[port] = warnings
        peer_summary[port] = {
            "ok": bool(identity.get("ok")),
            "mac": parsed.get("mac"),
            "chip": parsed.get("chip"),
            "flashSize": parsed.get("flashSize"),
            "wslPort": identity.get("wslPort"),
            "tool": " ".join(identity.get("tool", {}).get("argv", [])) or None,
            "esptoolWarnings": warnings,
        }

    coordinator_identity = (
        record.get("piIdentity", {})
        .get("coordinatorEsp32Identity", {})
    )
    coordinator_parsed = coordinator_identity.get("parsedIdentity", {})
    coordinator_warnings = coordinator_parsed.get("esptoolWarnings", [])
    coordinator_error = coordinator_identity.get("error")
    if remote_coordinator_tool_missing(coordinator_identity):
        coordinator_error = "Pi esptool command is not available"
    failure_codes = [
        failure.get("code", "gateFailed")
        for failure in record.get("failures", [])
        if isinstance(failure, dict)
    ]

    if record.get("ok"):
        next_action = (
            "Confirm physical USB-only/no-load state, then run "
            "scripts/espnow_bbs_live_gate.py prepare with "
            "--confirm-read-flash-backups."
        )
        readiness = "ready_for_prepare"
    elif "piFingerprintMismatch" in failure_codes:
        next_action = (
            "Restore or verify Pi SSH reachability at 172.16.0.2, then rerun "
            "the read-only preflight before any backup or flash step."
        )
        readiness = "blocked_pi_identity"
    elif "piCoordinatorToolMissing" in failure_codes:
        next_action = (
            "Install or activate esptool on the verified Pi, then rerun the "
            "read-only preflight before any backup or flash step."
        )
        readiness = "blocked_pi_esptool"
    elif "coordinatorUsbMissing" in failure_codes or "malformedCoordinatorIdentity" in failure_codes:
        next_action = (
            "Restore or verify the Pi /dev/ttyUSB0 coordinator identity, then "
            "rerun the read-only preflight."
        )
        readiness = "blocked_coordinator_identity"
    else:
        next_action = "Resolve listed failures and rerun the read-only preflight."
        readiness = "blocked"

    return {
        "ok": bool(record.get("ok")),
        "readiness": readiness,
        "generatedAt": record.get("generatedAt"),
        "outputPath": record.get("outputPath"),
        "expectedPeerPorts": record.get("expectedPeerPorts", DEFAULT_WINDOWS_PORTS),
        "peers": peer_summary,
        "peerMap": record.get("peerMap", {}),
        "piTarget": record.get("piIdentity", {}).get("target"),
        "coordinator": {
            "ok": bool(coordinator_identity.get("ok")),
            "port": record.get("coordinatorPort", DEFAULT_COORDINATOR_PORT),
            "mac": coordinator_parsed.get("mac"),
            "chip": coordinator_parsed.get("chip"),
            "flashSize": coordinator_parsed.get("flashSize"),
            "error": coordinator_error,
            "esptoolWarnings": coordinator_warnings,
        },
        "esptoolWarnings": {
            "peers": peer_warnings,
            "coordinator": coordinator_warnings,
        },
        "verifiedFacts": record.get("verifiedFacts", []),
        "failures": record.get("failures", []),
        "unknowns": record.get("unknowns", []),
        "readOnlyBoundary": record.get("readOnlyBoundary", {}),
        "nextAction": next_action,
    }


def validate_output_path(out_path: Path | None) -> Path | None:
    if out_path is None:
        return None
    resolved = out_path.resolve()
    out_root = OUT_ROOT.resolve()
    if resolved == out_root or out_root not in resolved.parents:
        raise SystemExit(
            f"--out must write under {repository_relative(OUT_ROOT)}"
        )
    if resolved.exists():
        raise SystemExit(f"refusing to overwrite existing output: {resolved}")
    return resolved


def write_output(record: dict[str, Any], out_path: Path | None) -> None:
    if out_path is None:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    record["outputPath"] = repository_relative(out_path)
    out_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    stamp = utc_stamp()
    out_path = validate_output_path(args.out)
    output_dir = out_path.parent if out_path else None
    ports = [normalize_windows_port(port) for port in args.windows_ports]
    current_role_ports = current_peer_role_ports(ports)
    record: dict[str, Any] = {
        "ok": False,
        "generatedAt": utc_now(),
        "tool": "scripts/live_bench_preflight.py",
        "workspace": str(ROOT),
        "expectedPeerPorts": ports,
        "peerPortPolicy": {
            "mode": (
                "accepted_mac_remap"
                if args.allow_peer_port_remap
                else "default_com_order"
            ),
            "acceptedPeerRoleMacs": (
                ACCEPTED_PEER_ROLE_MACS if args.allow_peer_port_remap else {}
            ),
            "currentAcceptedRolePorts": current_role_ports or {},
        },
        "coordinatorPort": args.coordinator_port,
        "readOnlyBoundary": {
            "noFlash": True,
            "noErase": True,
            "noMonitorAutomation": True,
            "noRelayCommands": True,
            "noXbeeWrites": True,
            "noEspNowTraffic": True,
            "noPiCapabilityChanges": True,
            "noPiPersistentBridge": True,
        },
        "assumptions": [
            "Default peer IDs are assigned by Windows port order only after the full gate passes: COM4=peer01, COM5=peer02, COM6=peer03.",
            "When --allow-peer-port-remap is used, peer IDs are assigned only by the accepted role MAC set after fresh read-only identity passes.",
            "The Pi target is accepted only when fresh host-key and identity checks match.",
            "When --allow-discovered-pi-host is used, the IP address is not trusted by itself; host-key fingerprints and Pi identity must still match.",
        ],
        "unknowns": [
            "Physical USB-only/no-load/no-relay/TFT/MicroSD/XBee wiring state is not proven by this script.",
            "ESP-IDF install state outside common paths is not exhaustively proven.",
            "No live ESP-NOW radio traffic is generated by this preflight.",
        ],
        "verifiedFacts": [],
        "failures": [],
    }

    record["windowsPeerInventory"] = (
        {"skipped": True}
        if args.skip_peers
        else collect_windows_peer_inventory(ports)
    )
    record["wslSerial"] = collect_wsl_serial_permissions(ports)
    record["toolchain"] = collect_toolchain_status()
    record["peerEsp32Identities"] = (
        {"skipped": True, "ports": {}}
        if args.skip_peers
        else collect_peer_esp32_identities(ports)
    )
    record["piIdentity"] = (
        {"skipped": True}
        if args.skip_pi
        else collect_pi_identity(
            args.pi_user,
            args.pi_host,
            output_dir,
            stamp,
            args.coordinator_port,
            args.skip_coordinator,
            args.allow_discovered_pi_host,
        )
    )
    if args.skip_peers:
        record["failures"].append(
            {
                "section": "peerEsp32Identities",
                "name": "requiredPeerGate",
                "code": "skippedRequiredGate",
                "value": "Peer identity was skipped",
            }
        )
    validate_preflight_record(record)
    write_output(record, out_path)
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture read-only ESP-NOW BBS multi-peer bench preflight evidence."
    )
    parser.add_argument(
        "--windows-ports",
        nargs="+",
        default=DEFAULT_WINDOWS_PORTS,
        help="Expected Windows CP210x peer ports in peer order.",
    )
    parser.add_argument(
        "--allow-peer-port-remap",
        action="store_true",
        help=(
            "Allow a non-default Windows COM map only when read-only identity "
            "matches the accepted peer role MACs."
        ),
    )
    parser.add_argument(
        "--current-peer-remap",
        action="store_true",
        help=(
            "Use the current accepted peer remap COM6 COM10 COM12 and require "
            "accepted peer role MAC matching."
        ),
    )
    parser.add_argument("--pi-user", default=DEFAULT_PI_USER)
    parser.add_argument(
        "--pi-host",
        default=DEFAULT_PI_HOST,
        help=(
            "Pi SSH access host. Accepted live-gate hosts are direct "
            "172.16.0.2 plus forwarded 192.168.137.93/192.168.137.105; "
            "use --allow-discovered-pi-host for a fresh LAN DHCP address."
        ),
    )
    parser.add_argument("--coordinator-port", default=DEFAULT_COORDINATOR_PORT)
    parser.add_argument(
        "--skip-peers",
        action="store_true",
        help="Diagnostic only: skip Windows and peer esptool identity checks.",
    )
    parser.add_argument(
        "--skip-pi",
        action="store_true",
        help="Diagnostic only: skip Pi host-key, identity, and coordinator checks.",
    )
    parser.add_argument(
        "--skip-coordinator",
        action="store_true",
        help="Diagnostic only: skip Pi /dev/ttyUSB0 esptool identity checks.",
    )
    parser.add_argument(
        "--allow-discovered-pi-host",
        action="store_true",
        help=(
            "Allow --pi-host to be a freshly discovered LAN address only if "
            "SSH fingerprints and Pi identity match the expected gate."
        ),
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional JSON output path under research/bench-records/live-bench/.",
    )
    parser.add_argument(
        "--from-record",
        type=Path,
        help="Summarize and revalidate an existing preflight JSON without probing hardware.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a concise gate summary instead of the full evidence JSON.",
    )
    args = parser.parse_args()
    if args.current_peer_remap:
        args.windows_ports = CURRENT_ACCEPTED_WINDOWS_PORTS
        args.allow_peer_port_remap = True
    args.windows_ports = [normalize_windows_port(port) for port in args.windows_ports]
    if args.windows_ports != DEFAULT_WINDOWS_PORTS and not args.allow_peer_port_remap:
        raise SystemExit(
            "this gate currently requires exactly COM4 COM5 COM6 unless "
            "--allow-peer-port-remap or --current-peer-remap is set"
        )
    if args.allow_peer_port_remap and len(args.windows_ports) != len(
        ACCEPTED_PEER_ROLE_MACS
    ):
        raise SystemExit(
            "--allow-peer-port-remap requires exactly three Windows peer ports"
        )
    return args


def main() -> int:
    args = parse_args()
    if args.from_record:
        record = json.loads(args.from_record.read_text(encoding="utf-8"))
        validate_preflight_record(record)
        output = summarize_preflight_record(record)
    else:
        record = build_record(args)
        output = summarize_preflight_record(record) if args.summary else record
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if record.get("ok") else 2


if __name__ == "__main__":
    sys.exit(main())
