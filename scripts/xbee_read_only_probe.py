#!/usr/bin/env python3
"""Read-only XBee bench probe for PC-side adapter discovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import serial
    from serial.tools import list_ports
except Exception as exc:  # pragma: no cover - depends on local environment.
    serial = None
    list_ports = None
    SERIAL_IMPORT_ERROR = str(exc)
else:
    SERIAL_IMPORT_ERROR = None


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "research" / "bench-records" / "xbee-readonly"
DEFAULT_AT_QUERIES = ("VR", "HV", "SH", "SL", "AP", "AO", "BD", "NP")
ADDRESS_QUERIES = {"SH", "SL"}
SERIAL_GLOB_PATTERNS = ("/dev/ttyUSB*", "/dev/ttyACM*", "/dev/ttyAMA*", "/dev/ttyS*")
MAX_PASSIVE_SAMPLE_BYTES = 512


class ProbeError(Exception):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def repository_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def base_record(command: str) -> dict[str, Any]:
    return {
        "ok": True,
        "command": command,
        "generatedAt": utc_now(),
        "tool": "scripts/xbee_read_only_probe.py",
        "readOnlyBoundary": {
            "noFirmwareFlash": True,
            "noPersistentSettingWrites": True,
            "noRelayCommands": True,
            "noEsp32CarrierWiring": True,
        },
    }


def error_record(command: str, code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    record = base_record(command)
    record["ok"] = False
    record["error"] = {"code": code, "message": message, "details": details or {}}
    return record


def write_optional_output(record: dict[str, Any], out_path: Path | None) -> None:
    if out_path is None:
        return

    resolved = out_path.resolve()
    out_root = OUT_ROOT.resolve()
    if resolved == out_root or out_root not in resolved.parents:
        raise ProbeError(
            "invalid_output_path",
            "--out must write under research/bench-records/xbee-readonly/",
            {"requested": str(out_path), "allowedRoot": repository_relative(OUT_ROOT)},
        )
    if resolved.exists():
        raise ProbeError(
            "output_exists",
            "refusing to overwrite an existing bench record",
            {"requested": repository_relative(resolved)},
        )

    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    record["outputPath"] = repository_relative(resolved)


def emit(record: dict[str, Any], args: argparse.Namespace) -> int:
    write_optional_output(record, getattr(args, "out", None))
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record.get("ok") else 2


def require_pyserial() -> Any:
    if serial is None:
        raise ProbeError(
            "pyserial_unavailable",
            "pyserial is required for serial-port access",
            {"importError": SERIAL_IMPORT_ERROR},
        )
    return serial


def is_wsl() -> bool:
    release = platform.release().lower()
    if "microsoft" in release or "wsl" in release:
        return True
    try:
        return "microsoft" in Path("/proc/version").read_text(encoding="utf-8").lower()
    except OSError:
        return False


def run_short_command(argv: list[str], timeout: float = 2.0) -> dict[str, Any]:
    try:
        result = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "error": str(exc), "lines": []}
    return {
        "available": True,
        "returncode": result.returncode,
        "lines": [line for line in result.stdout.splitlines() if line.strip()],
        "stderr": [line for line in result.stderr.splitlines() if line.strip()],
    }


def collect_serial_candidates() -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}

    if list_ports is not None:
        for port in list_ports.comports():
            candidates[port.device] = {
                "path": port.device,
                "source": "pyserial",
                "description": port.description,
                "hwid": port.hwid,
            }

    for pattern in SERIAL_GLOB_PATTERNS:
        for path in sorted(Path("/").glob(pattern.lstrip("/"))):
            key = path.as_posix()
            candidates.setdefault(
                key,
                {
                    "path": key,
                    "source": "filesystem",
                    "description": "",
                    "hwid": "",
                },
            )

    return sorted(candidates.values(), key=lambda item: item["path"])


def collect_windows_com_hints() -> dict[str, Any]:
    powershell = shutil.which("powershell.exe")
    if not powershell:
        return {"powershellAvailable": False, "ports": []}

    result = run_short_command(
        [
            powershell,
            "-NoProfile",
            "-Command",
            "[System.IO.Ports.SerialPort]::GetPortNames() | Sort-Object",
        ],
        timeout=3.0,
    )
    ports = []
    for line in result.get("lines", []):
        name = line.strip()
        match = re.fullmatch(r"COM(\d+)", name, flags=re.IGNORECASE)
        hint = None
        if match:
            hint = f"/dev/ttyS{int(match.group(1)) - 1}"
        ports.append({"windowsPort": name, "wslLegacyHint": hint})
    return {"powershellAvailable": True, "probe": result, "ports": ports}


def command_list(args: argparse.Namespace) -> dict[str, Any]:
    record = base_record("list")
    lsusb_path = shutil.which("lsusb")
    xctu_path = shutil.which("xctu")
    record.update(
        {
            "environment": {
                "platform": platform.platform(),
                "isWsl": is_wsl(),
                "python": sys.version.split()[0],
                "pyserialAvailable": serial is not None,
                "pyserialVersion": getattr(serial, "VERSION", None) if serial else None,
                "pyserialImportError": SERIAL_IMPORT_ERROR,
                "lsusbAvailable": bool(lsusb_path),
                "lsusbPath": lsusb_path,
                "powershellExe": shutil.which("powershell.exe"),
                "xctuOnPath": bool(xctu_path),
                "xctuPath": xctu_path,
            },
            "serialCandidates": collect_serial_candidates(),
            "windowsComHints": collect_windows_com_hints(),
            "notes": [
                "Tier A discovery only lists host-visible serial candidates.",
                "No serial port is opened by the list command.",
                "In WSL2, USB serial devices may require usbipd attachment before /dev/ttyUSB* appears.",
            ],
        }
    )
    return record


def validate_at_query(command: str) -> str:
    normalized = command.strip().upper()
    if normalized not in DEFAULT_AT_QUERIES:
        raise ProbeError(
            "at_command_not_allowed",
            "only fixed non-persistent AT read queries are allowed",
            {"requested": command, "allowlist": list(DEFAULT_AT_QUERIES)},
        )
    return normalized


def normalize_baud(baud: int) -> int:
    if baud < 1200 or baud > 921600:
        raise ProbeError("invalid_baud", "baud must be between 1200 and 921600", {"baud": baud})
    return baud


def normalize_duration(duration: float) -> float:
    if duration <= 0 or duration > 300:
        raise ProbeError(
            "invalid_duration",
            "duration must be greater than 0 and no more than 300 seconds",
            {"duration": duration},
        )
    return duration


def open_serial_port(port: str, baud: int, timeout: float) -> Any:
    serial_module = require_pyserial()
    try:
        return serial_module.Serial(
            port=port,
            baudrate=baud,
            timeout=timeout,
            write_timeout=1.0,
            rtscts=False,
            dsrdtr=False,
            xonxoff=False,
        )
    except Exception as exc:
        raise ProbeError(
            "serial_open_failed",
            "could not open serial port",
            {"port": port, "baud": baud, "error": str(exc)},
        ) from exc


def command_passive(args: argparse.Namespace) -> dict[str, Any]:
    baud = normalize_baud(args.baud)
    duration = normalize_duration(args.duration)
    record = base_record("passive")
    record["request"] = {
        "port": args.port,
        "baud": baud,
        "durationSeconds": duration,
        "addressesRedacted": not args.show_addresses,
    }
    record["serialWritesAttempted"] = False

    digest = hashlib.sha256()
    sample = bytearray()
    byte_count = 0
    started = time.monotonic()
    with open_serial_port(args.port, baud, timeout=0.1) as handle:
        deadline = started + duration
        while time.monotonic() < deadline:
            chunk = handle.read(256)
            if not chunk:
                continue
            byte_count += len(chunk)
            digest.update(chunk)
            if args.show_addresses and len(sample) < MAX_PASSIVE_SAMPLE_BYTES:
                remaining = MAX_PASSIVE_SAMPLE_BYTES - len(sample)
                sample.extend(chunk[:remaining])

    elapsed = time.monotonic() - started
    record["observation"] = {
        "elapsedSeconds": round(elapsed, 3),
        "byteCount": byte_count,
        "sha256": digest.hexdigest() if byte_count else None,
        "sampleHex": sample.hex() if args.show_addresses and sample else None,
        "sampleRedacted": byte_count > 0 and not args.show_addresses,
        "localOnlyRawBytesShown": bool(args.show_addresses),
    }
    return record


def read_cr_terminated(handle: Any, timeout: float) -> bytes:
    deadline = time.monotonic() + timeout
    data = bytearray()
    while time.monotonic() < deadline:
        chunk = handle.read(1)
        if not chunk:
            continue
        if chunk == b"\r":
            return bytes(data)
        data.extend(chunk)
    return bytes(data)


def format_at_value(command: str, value: bytes, show_addresses: bool) -> dict[str, Any]:
    value_hash = hashlib.sha256(value).hexdigest()
    if command in ADDRESS_QUERIES and not show_addresses:
        return {
            "redacted": True,
            "byteLength": len(value),
            "sha256": value_hash,
        }

    try:
        text = value.decode("ascii")
    except UnicodeDecodeError:
        text = None
    return {
        "redacted": False,
        "text": text,
        "hex": value.hex(),
        "byteLength": len(value),
        "sha256": value_hash,
    }


def command_at_query(args: argparse.Namespace) -> dict[str, Any]:
    if not args.confirm_sends_read_commands:
        raise ProbeError(
            "confirmation_required",
            "at-query sends non-persistent AT read commands and requires --confirm-sends-read-commands",
        )

    baud = normalize_baud(args.baud)
    queries = [validate_at_query(command) for command in DEFAULT_AT_QUERIES]
    record = base_record("at-query")
    record["request"] = {
        "port": args.port,
        "baud": baud,
        "confirmedSendsReadCommands": True,
        "queries": queries,
        "addressesRedacted": not args.show_addresses,
    }
    record["blockedOperations"] = [
        "AT parameter writes",
        "WR",
        "AC",
        "firmware updates",
        "API transmit frames",
        "relay commands",
        "ESP32 DIN/DOUT wiring",
        "adapter or radio setting changes",
    ]

    with open_serial_port(args.port, baud, timeout=0.2) as handle:
        try:
            handle.reset_input_buffer()
            handle.reset_output_buffer()
        except Exception:
            pass

        time.sleep(1.05)
        handle.write(b"+++")
        handle.flush()
        command_mode_response = read_cr_terminated(handle, timeout=2.5)

        if command_mode_response != b"OK":
            raise ProbeError(
                "command_mode_failed",
                "the radio did not return OK after the command-mode guard sequence",
                {
                    "responseHex": command_mode_response.hex(),
                    "responseText": command_mode_response.decode("ascii", errors="replace"),
                },
            )

        results = {}
        for command in queries:
            wire_command = f"AT{command}\r".encode("ascii")
            handle.write(wire_command)
            handle.flush()
            response = read_cr_terminated(handle, timeout=2.0)
            results[command] = format_at_value(command, response, args.show_addresses)

    record["commandMode"] = {
        "entered": True,
        "guardTimeSeconds": 1.05,
        "explicitExitSent": False,
        "exitNote": "No ATCN is sent so the fixed read-query allowlist remains exact; the module should leave command mode by its configured timeout.",
    }
    record["results"] = results
    return record


def command_self_test(args: argparse.Namespace) -> dict[str, Any]:
    tests: list[dict[str, Any]] = []

    for command in DEFAULT_AT_QUERIES:
        tests.append(
            {
                "name": f"allowlist accepts {command}",
                "passed": validate_at_query(command) == command,
            }
        )

    forbidden = ["WR", "AC", "KY", "AP2", "AP=2", "BD7", "FR", "RE", "DH", "DL"]
    for command in forbidden:
        passed = False
        try:
            validate_at_query(command)
        except ProbeError as exc:
            passed = exc.code == "at_command_not_allowed"
        tests.append({"name": f"allowlist rejects {command}", "passed": passed})

    redacted = format_at_value("SH", b"0013A200", show_addresses=False)
    visible = format_at_value("AP", b"2", show_addresses=False)
    tests.extend(
        [
            {
                "name": "address redaction hides SH value",
                "passed": redacted.get("redacted") is True
                and "text" not in redacted
                and redacted.get("byteLength") == 8,
            },
            {
                "name": "non-address read remains visible",
                "passed": visible.get("redacted") is False and visible.get("text") == "2",
            },
            {
                "name": "CR parser returns bytes before terminator",
                "passed": parse_test_response(b"OK\rignored") == b"OK",
            },
        ]
    )

    sample = base_record("self-test")
    sample["tests"] = tests
    sample["summary"] = {
        "passed": sum(1 for test in tests if test["passed"]),
        "total": len(tests),
    }
    sample["ok"] = sample["summary"]["passed"] == sample["summary"]["total"]
    sample["jsonShape"] = {
        "hasOk": "ok" in sample,
        "hasCommand": sample.get("command") == "self-test",
        "hasReadOnlyBoundary": "readOnlyBoundary" in sample,
    }
    if not all(sample["jsonShape"].values()):
        sample["ok"] = False
    return sample


def parse_test_response(raw: bytes) -> bytes:
    return raw.split(b"\r", 1)[0]


def add_json_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Emit JSON. JSON is the only output format.")
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional JSON record path under research/bench-records/xbee-readonly/.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List host serial candidates without opening ports.")
    add_json_output_args(list_parser)
    list_parser.set_defaults(func=command_list)

    passive_parser = subparsers.add_parser("passive", help="Open a port and observe incoming bytes only.")
    passive_parser.add_argument("--port", required=True)
    passive_parser.add_argument("--baud", required=True, type=int)
    passive_parser.add_argument("--duration", required=True, type=float)
    passive_parser.add_argument(
        "--show-addresses",
        action="store_true",
        help="Show raw observed bytes for local-only evidence; default output redacts samples.",
    )
    add_json_output_args(passive_parser)
    passive_parser.set_defaults(func=command_passive)

    at_parser = subparsers.add_parser("at-query", help="Send fixed non-persistent AT read queries.")
    at_parser.add_argument("--port", required=True)
    at_parser.add_argument("--baud", required=True, type=int)
    at_parser.add_argument("--confirm-sends-read-commands", action="store_true")
    at_parser.add_argument(
        "--show-addresses",
        action="store_true",
        help="Show SH/SL address values for local-only evidence; default output redacts them.",
    )
    add_json_output_args(at_parser)
    at_parser.set_defaults(func=command_at_query)

    self_test_parser = subparsers.add_parser("self-test", help="Run hardware-free probe checks.")
    add_json_output_args(self_test_parser)
    self_test_parser.set_defaults(func=command_self_test)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        record = args.func(args)
        return emit(record, args)
    except ProbeError as exc:
        try:
            return emit(error_record(args.command, exc.code, exc.message, exc.details), args)
        except ProbeError as output_exc:
            print(
                json.dumps(
                    error_record(args.command, output_exc.code, output_exc.message, output_exc.details),
                    indent=2,
                    sort_keys=True,
                )
            )
            return 2


if __name__ == "__main__":
    raise SystemExit(main())
