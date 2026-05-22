#!/usr/bin/env python3
"""Read-only live-bench preflight for the ESP32/Pi bench lane."""

from __future__ import annotations

import argparse
import getpass
import grp
import json
import os
import platform
import pwd
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

DEFAULT_WINDOWS_PORT = "COM6"
DEFAULT_WSL_PORT = "/dev/ttyS6"
DEFAULT_PI_USER = "dospi"
DEFAULT_PI_HOST = "192.168.200.104"

EXPECTED_COM6 = {
    "deviceId": "COM6",
    "description": "Silicon Labs CP210x USB to UART Bridge",
    "pnpDeviceIdContains": "VID_10C4&PID_EA60",
    "status": "OK",
}

EXPECTED_PI = {
    "hostname": "dos-pi4-poe",
    "model": "Raspberry Pi 4 Model B Rev 1.2",
    "serial": "10000000aaaa5b24",
    "rootSource": "/dev/mmcblk0p2",
    "networkAddress": "192.168.200.104",
    "closedTcpPorts": ["31331", "31332", "8080"],
    "sshFingerprints": {
        "RSA": "SHA256:ZA1lH2codkJpMkj3FpSIoHoqFmUbRUIHO6QpUDcBT50",
        "ECDSA": "SHA256:IaFCqHEYIHPW4vMmzYgpATf3PdDwZS25Qm62Ct6U5ek",
        "ED25519": "SHA256:3VldDFyssS+mO+xRhsc2SljowM0ijPXiYSBv/vwPubA",
    },
}

ALLOWED_ESPTOOL_COMMANDS = ("chip_id", "read_mac", "flash_id")
FORBIDDEN_ESPTOOL_TERMS = (
    "write_flash",
    "erase_flash",
    "erase_region",
    "write_mem",
    "load_ram",
    "monitor",
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


def collect_windows_com_inventory(port: str) -> dict[str, Any]:
    powershell = shutil.which("powershell.exe")
    cmd = shutil.which("cmd.exe")
    script = f"""
$serial = Get-CimInstance Win32_SerialPort |
    Where-Object {{ $_.DeviceID -eq '{port}' }} |
    Select-Object Caption,Description,DeviceID,PNPDeviceID,Status,ConfigManagerErrorCode,Name,MaxBaudRate
$pnp = Get-CimInstance Win32_PnPEntity |
    Where-Object {{ $_.Name -like '*({port})*' -or $_.DeviceID -like '*VID_10C4*PID_EA60*' }} |
    Select-Object Name,DeviceID,Status,ConfigManagerErrorCode
[pscustomobject]@{{
    serialPort = $serial
    pnp = $pnp
}} | ConvertTo-Json -Depth 5
"""
    inventory = {
        "expected": EXPECTED_COM6 if port.upper() == "COM6" else None,
        "powershellPath": powershell,
        "cmdPath": cmd,
    }
    if powershell:
        ps_result = run_command(
            [powershell, "-NoProfile", "-Command", script],
            timeout=10.0,
        )
        inventory["win32SerialPort"] = ps_result
        try:
            parsed = read_json_from_lines(ps_result.get("stdout", []))
        except json.JSONDecodeError as exc:
            parsed = None
            inventory["parseError"] = str(exc)
        inventory["parsed"] = parsed
        inventory["expectedChecks"] = check_windows_com(parsed, port)
    else:
        inventory["win32SerialPort"] = {
            "available": False,
            "error": "powershell.exe not found",
        }

    if cmd:
        inventory["mode"] = run_command([cmd, "/c", "mode", port], timeout=5.0)
    else:
        inventory["mode"] = {"available": False, "error": "cmd.exe not found"}
    return inventory


def check_windows_com(parsed: Any, port: str) -> dict[str, Any]:
    checks: dict[str, Any] = {"ok": False, "items": []}
    if not isinstance(parsed, dict) or not parsed.get("serialPort"):
        checks["items"].append({"name": "serialPortPresent", "ok": False})
        return checks

    serial_port = parsed["serialPort"]
    expected = EXPECTED_COM6 if port.upper() == "COM6" else {}
    description = str(serial_port.get("Description", ""))
    pnp_device = str(serial_port.get("PNPDeviceID", ""))
    status_text = str(serial_port.get("Status", ""))
    items = [
        {
            "name": "deviceId",
            "ok": serial_port.get("DeviceID") == expected.get("deviceId", port),
            "value": serial_port.get("DeviceID"),
        },
        {
            "name": "description",
            "ok": expected.get("description", "") in description,
            "value": description,
        },
        {
            "name": "pnpDeviceId",
            "ok": expected.get("pnpDeviceIdContains", "") in pnp_device,
            "value": pnp_device,
        },
        {
            "name": "status",
            "ok": status_text == expected.get("status", status_text),
            "value": status_text,
        },
    ]
    checks["items"] = items
    checks["ok"] = all(item["ok"] for item in items)
    return checks


def collect_wsl_serial_permissions(port: str) -> dict[str, Any]:
    path = Path(port)
    record: dict[str, Any] = {
        "path": port,
        "exists": path.exists(),
        "currentUser": getpass.getuser(),
        "currentGroups": sorted(
            grp.getgrgid(gid).gr_name for gid in os.getgroups()
        ),
    }
    if not path.exists():
        return record

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
    return record


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


def collect_esp32_identity(windows_port: str, wsl_port: str) -> dict[str, Any]:
    selected = select_esptool()
    record: dict[str, Any] = {
        "allowedCommands": list(ALLOWED_ESPTOOL_COMMANDS),
        "forbiddenTerms": list(FORBIDDEN_ESPTOOL_TERMS),
        "toolSelection": selected,
        "commands": {},
    }
    tool = selected.get("selected")
    if not tool:
        record["ok"] = False
        record["error"] = "no esptool command available"
        return record

    port = windows_port if tool["portKind"] == "windows" else wsl_port
    record["port"] = port
    record["portKind"] = tool["portKind"]
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
    record["ok"] = all(
        result.get("returncode") == 0
        for result in record["commands"].values()
    )
    return record


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
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "target": f"{user}@{host}",
        "expected": EXPECTED_PI if host == DEFAULT_PI_HOST else None,
    }
    keyscan = run_command(["ssh-keyscan", "-T", "5", host], timeout=8.0)
    record["sshKeyscan"] = keyscan
    key_lines = [line for line in keyscan.get("stdout", []) if line.strip()]
    keygen = run_command(["ssh-keygen", "-lf", "-"], stdin="\n".join(key_lines), timeout=5.0)
    record["sshFingerprints"] = keygen
    observed = parse_fingerprint_lines(keygen.get("stdout", []))
    record["observedFingerprints"] = observed
    expected = EXPECTED_PI["sshFingerprints"] if host == DEFAULT_PI_HOST else {}
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
        remote_script = r"""
set -eu
echo "__hostnamectl__"
hostnamectl
echo "__model__"
tr -d '\000' </proc/device-tree/model || true
echo
echo "__serial__"
awk '/^Serial/ {print $3}' /proc/cpuinfo
echo "__root_source__"
findmnt -no SOURCE /
echo "__os_release__"
if [ -r /etc/os-release ]; then . /etc/os-release; printf '%s\n' "${PRETTY_NAME:-unknown}"; fi
echo "__kernel__"
uname -a
echo "__ip_addr__"
ip -brief address
echo "__listeners__"
if command -v ss >/dev/null 2>&1; then ss -ltnH; else netstat -ltn; fi | awk '$0 ~ /:(31331|31332|8080)([[:space:]]|$)/ {print}'
echo "__processes__"
pgrep -af '[e]sp32_gateway_sim|[d]osbox-x|[d]osbox' || true
"""
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
            timeout=20.0,
        )
    finally:
        if temp_file is not None:
            try:
                Path(temp_file.name).unlink()
            except FileNotFoundError:
                pass

    record["sshIdentity"] = ssh
    record["identityChecks"] = check_pi_identity(ssh.get("stdout", []), host)
    record["ok"] = (
        record["fingerprintCheck"]["ok"]
        and ssh.get("returncode") == 0
        and record["identityChecks"]["ok"]
    )
    return record


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


def check_pi_identity(lines: list[str], host: str) -> dict[str, Any]:
    expected = EXPECTED_PI if host == DEFAULT_PI_HOST else {}
    hostnamectl = "\n".join(section_value(lines, "hostnamectl"))
    model = " ".join(section_value(lines, "model")).strip()
    serial = " ".join(section_value(lines, "serial")).strip()
    root_source = " ".join(section_value(lines, "root_source")).strip()
    addresses = "\n".join(section_value(lines, "ip_addr"))
    listeners = [line for line in section_value(lines, "listeners") if line.strip()]
    processes = [line for line in section_value(lines, "processes") if line.strip()]
    items = [
        {
            "name": "hostname",
            "ok": expected.get("hostname", "") in hostnamectl,
            "value": hostnamectl,
        },
        {
            "name": "model",
            "ok": model == expected.get("model", model),
            "value": model,
        },
        {
            "name": "serial",
            "ok": serial == expected.get("serial", serial),
            "value": serial,
        },
        {
            "name": "rootSource",
            "ok": root_source == expected.get("rootSource", root_source),
            "value": root_source,
        },
        {
            "name": "networkAddress",
            "ok": expected.get("networkAddress", "") in addresses,
            "value": addresses,
        },
        {
            "name": "closedTcpPorts",
            "ok": not listeners,
            "value": listeners,
        },
        {
            "name": "noBridgeOrDosboxProcesses",
            "ok": not processes,
            "value": processes,
        },
    ]
    return {"ok": all(item["ok"] for item in items), "items": items}


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
    record: dict[str, Any] = {
        "ok": True,
        "generatedAt": utc_now(),
        "tool": "scripts/live_bench_preflight.py",
        "workspace": str(ROOT),
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
            "COM6 is only a candidate ESP32 target until this read-only evidence and physical bench evidence match.",
            "The Pi target is accepted only when fresh host-key and identity checks match.",
        ],
        "unknowns": [
            "Physical USB-only/no-load/no-relay/TFT/MicroSD/XBee wiring state is not proven by this script.",
            "ESP-IDF install state outside common paths is not exhaustively proven.",
        ],
    }
    record["windowsComInventory"] = collect_windows_com_inventory(args.windows_port)
    record["wslSerial"] = collect_wsl_serial_permissions(args.wsl_port)
    record["toolchain"] = collect_toolchain_status()
    record["esp32Identity"] = (
        {"skipped": True}
        if args.skip_esp32
        else collect_esp32_identity(args.windows_port, args.wsl_port)
    )
    record["piIdentity"] = (
        {"skipped": True}
        if args.skip_pi
        else collect_pi_identity(args.pi_user, args.pi_host, output_dir, stamp)
    )
    record["ok"] = all(
        section.get("ok", True)
        for section in [
            record["windowsComInventory"].get("expectedChecks", {"ok": True}),
            record["esp32Identity"],
            record["piIdentity"],
        ]
        if not section.get("skipped")
    )
    write_output(record, out_path)
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture read-only ESP32/Pi bench preflight evidence."
    )
    parser.add_argument("--windows-port", default=DEFAULT_WINDOWS_PORT)
    parser.add_argument("--wsl-port", default=DEFAULT_WSL_PORT)
    parser.add_argument("--pi-user", default=DEFAULT_PI_USER)
    parser.add_argument("--pi-host", default=DEFAULT_PI_HOST)
    parser.add_argument(
        "--skip-esp32",
        action="store_true",
        help="Skip esptool chip_id/read_mac/flash_id identity commands.",
    )
    parser.add_argument(
        "--skip-pi",
        action="store_true",
        help="Skip Pi host-key and SSH identity checks.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional JSON output path under research/bench-records/live-bench/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    record = build_record(args)
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record.get("ok") else 2


if __name__ == "__main__":
    sys.exit(main())
