#!/usr/bin/env python3
"""Offline-first XBee radio programming study CLI.

The v1 boundary is intentionally narrow. Inventory does not open serial ports,
profile diffing is file-only, and write-plan emits a blocked review packet
instead of applying settings. The readonly command delegates to the existing
fixed AT read-query probe and keeps that probe's explicit confirmation gate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import xbee_read_only_probe as probe


READ_ONLY_AT_QUERIES = tuple(probe.DEFAULT_AT_QUERIES)
ADDRESS_COMMANDS = {"SH", "SL"}
SECRET_COMMANDS = {"KY"}
SENSITIVE_COMMANDS = ADDRESS_COMMANDS | SECRET_COMMANDS
FORBIDDEN_AT_COMMANDS = {
    "AC",
    "DH",
    "DL",
    "FR",
    "KY",
    "RE",
    "WR",
}
BLOCKED_OPERATIONS = [
    "AT setting-value commands",
    "WR persistent writes",
    "AC apply changes",
    "firmware recovery or update",
    "factory reset or restore",
    "API transmit frames",
    "range tests or RF transmit exercises",
    "ESP32 DIN/DOUT carrier wiring",
    "relay, load, or mains actions",
]
KNOWN_SETTING_COMMANDS = set(READ_ONLY_AT_QUERIES) | FORBIDDEN_AT_COMMANDS | {"AP", "AO", "BD", "EE", "ID", "CE", "TO", "NI"}


class StudyError(Exception):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


@dataclass(frozen=True)
class ProfileEntry:
    command: str
    value: Any
    redacted: bool = False
    unsafe_reason: str | None = None
    value_hash: str | None = None
    byte_length: int | None = None


def base_record(command: str) -> dict[str, Any]:
    return {
        "ok": True,
        "command": command,
        "generatedAt": probe.utc_now(),
        "tool": "scripts/xbee_radio_study.py",
        "v1Boundary": {
            "inventoryOpensSerialPorts": False,
            "profileDiffWritesSerialData": False,
            "writePlanApplyImplemented": False,
            "noPersistentRadioSettingWrites": True,
            "noApiTransmitFrames": True,
            "noFirmwareUpdate": True,
            "noEsp32CarrierWiring": True,
        },
    }


def error_record(command: str, code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    record = base_record(command)
    record["ok"] = False
    record["error"] = {"code": code, "message": message, "details": details or {}}
    return record


def emit(record: dict[str, Any]) -> int:
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record.get("ok") else 2


def sha256_text(value: Any) -> str:
    if isinstance(value, bytes):
        raw = value
    else:
        raw = str(value).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()


def local_tool_presence(name: str, extra_paths: list[str] | None = None) -> dict[str, Any]:
    path = shutil.which(name)
    found_paths = [path] if path else []
    for candidate in extra_paths or []:
        if Path(candidate).exists():
            found_paths.append(candidate)
    return {"name": name, "onPath": bool(path), "path": path, "knownInstallPathsFound": found_paths}


def python_package_status(distribution: str, module: str) -> dict[str, Any]:
    try:
        spec = importlib.util.find_spec(module)
    except ModuleNotFoundError:
        spec = None
    try:
        version = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        version = None
    return {
        "distribution": distribution,
        "module": module,
        "importable": spec is not None,
        "installedVersion": version,
    }


def collect_windows_pnp(local_show_identifiers: bool) -> dict[str, Any]:
    powershell = shutil.which("powershell.exe")
    if not powershell:
        return {"powershellAvailable": False, "devices": []}

    script = (
        "$items = Get-CimInstance Win32_PnPEntity | "
        "Where-Object { $_.Name -match '\\(COM[0-9]+\\)' -or $_.Name -match 'CP210|XBee|Digi International|Silicon Labs|USB Serial' } | "
        "Select-Object Name, Manufacturer, PNPClass, Status, DeviceID; "
        "$items | ConvertTo-Json -Compress"
    )
    result = probe.run_short_command([powershell, "-NoProfile", "-Command", script], timeout=5.0)
    devices: list[dict[str, Any]] = []
    if result.get("available") and result.get("returncode") == 0 and result.get("lines"):
        try:
            parsed = json.loads("\n".join(result["lines"]))
        except json.JSONDecodeError:
            parsed = []
        if isinstance(parsed, dict):
            parsed = [parsed]
        if isinstance(parsed, list):
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                raw_device_id = item.get("DeviceID")
                device: dict[str, Any] = {
                    "name": item.get("Name"),
                    "manufacturer": item.get("Manufacturer"),
                    "pnpClass": item.get("PNPClass"),
                    "status": item.get("Status"),
                }
                if local_show_identifiers:
                    device["deviceId"] = raw_device_id
                    device["localOnlyIdentifiersShown"] = True
                elif raw_device_id:
                    device["deviceIdRedacted"] = True
                    device["deviceIdSha256"] = sha256_text(raw_device_id)
                devices.append(device)

    safe_probe = dict(result)
    if not local_show_identifiers:
        safe_probe["lines"] = []
        safe_probe["rawOutputRedacted"] = True
        safe_probe["rawLineCount"] = len(result.get("lines", []))

    return {
        "powershellAvailable": True,
        "probe": safe_probe,
        "devices": devices,
        "identifiersRedacted": not local_show_identifiers,
    }


def command_inventory(args: argparse.Namespace) -> dict[str, Any]:
    record = base_record("inventory")
    xctu_paths = [
        "/mnt/c/Program Files (x86)/Digi/XCTU/XCTU.exe",
        "/mnt/c/Program Files/Digi/XCTU/XCTU.exe",
    ]
    xbee_studio_paths = [
        "/mnt/c/Program Files/Digi/XBee Studio/XBee Studio.exe",
        "/mnt/c/Program Files (x86)/Digi/XBee Studio/XBee Studio.exe",
    ]
    record.update(
        {
            "environment": {
                "platform": platform.platform(),
                "isWsl": probe.is_wsl(),
                "python": sys.version.split()[0],
                "pyserialAvailable": probe.serial is not None,
                "pyserialVersion": getattr(probe.serial, "VERSION", None) if probe.serial else None,
                "pyserialImportError": probe.SERIAL_IMPORT_ERROR,
            },
            "serial": {
                "serialOpenAttempted": False,
                "wslCandidates": probe.collect_serial_candidates(),
                "windowsComHints": probe.collect_windows_com_hints(),
                "windowsPnp": collect_windows_pnp(args.local_show_identifiers),
            },
            "tools": {
                "xctu": local_tool_presence("xctu", xctu_paths),
                "xbeeStudio": {
                    "candidates": [
                        local_tool_presence("xbee-studio", xbee_studio_paths),
                        local_tool_presence("xbee-studio-cli"),
                    ]
                },
            },
            "pythonPackages": {
                "digiXbee": python_package_status("digi-xbee", "digi.xbee"),
            },
            "notes": [
                "Inventory does not open serial ports.",
                "COM/PnP records are local evidence; do not publish private COM mappings.",
                "XCTU and XBee Studio, if present, remain reference tools only in this v1 boundary.",
            ],
        }
    )
    return record


def command_readonly(args: argparse.Namespace) -> dict[str, Any]:
    if not args.confirm_sends_read_commands:
        raise StudyError(
            "confirmation_required",
            "readonly delegates to at-query and sends non-persistent serial read commands; pass --confirm-sends-read-commands to continue",
            {"allowedQueries": list(READ_ONLY_AT_QUERIES)},
        )

    delegate_args = argparse.Namespace(
        port=args.port,
        baud=args.baud,
        confirm_sends_read_commands=True,
        show_addresses=args.show_addresses,
    )
    delegated = probe.command_at_query(delegate_args)
    record = base_record("readonly")
    record.update(
        {
            "delegatedTo": "scripts/xbee_read_only_probe.py at-query",
            "serialReadQueryTrafficSent": True,
            "persistentSettingWritesAttempted": False,
            "allowedQueries": list(READ_ONLY_AT_QUERIES),
            "blockedOperations": BLOCKED_OPERATIONS,
            "readback": delegated,
        }
    )
    return record


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise StudyError("file_read_failed", "could not read JSON file", {"path": str(path), "error": str(exc)}) from exc
    except json.JSONDecodeError as exc:
        raise StudyError("invalid_json", "could not parse JSON file", {"path": str(path), "error": str(exc)}) from exc
    if not isinstance(data, dict):
        raise StudyError("invalid_json_shape", "profile JSON must be an object", {"path": str(path)})
    return data


def looks_like_setting_value_command(command: str) -> bool:
    normalized = command.strip().upper()
    if "=" in normalized or " " in normalized:
        return True
    if len(normalized) > 2 and normalized[:2] in KNOWN_SETTING_COMMANDS:
        return True
    return False


def unsafe_command_reason(command: str) -> str | None:
    normalized = command.strip().upper()
    if looks_like_setting_value_command(normalized):
        return "setting_value_at_command"
    if normalized in FORBIDDEN_AT_COMMANDS:
        return "forbidden_at_command"
    if normalized not in KNOWN_SETTING_COMMANDS and normalized not in READ_ONLY_AT_QUERIES:
        return "unreviewed_at_command"
    return None


def unwrap_profile_map(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("results", "settings", "targets", "target", "desired"):
        value = data.get(key)
        if isinstance(value, dict):
            return value
    return data


def entry_value(command: str, raw: Any) -> ProfileEntry:
    normalized = command.strip().upper()
    reason = unsafe_command_reason(normalized)
    if isinstance(raw, dict):
        redacted = bool(raw.get("redacted"))
        value = raw.get("text")
        if value is None:
            value = raw.get("value")
        if value is None:
            value = raw.get("hex")
        value_hash = raw.get("sha256") if isinstance(raw.get("sha256"), str) else None
        byte_length = raw.get("byteLength") if isinstance(raw.get("byteLength"), int) else None
        return ProfileEntry(
            command=normalized,
            value=value,
            redacted=redacted,
            unsafe_reason=reason,
            value_hash=value_hash,
            byte_length=byte_length,
        )
    return ProfileEntry(command=normalized, value=raw, unsafe_reason=reason)


def extract_profile_entries(data: dict[str, Any]) -> dict[str, ProfileEntry]:
    profile = unwrap_profile_map(data)
    entries: dict[str, ProfileEntry] = {}
    for raw_command, raw_value in profile.items():
        command = str(raw_command).strip().upper()
        if command in {"OK", "COMMAND", "GENERATEDAT", "TOOL", "V1BOUNDARY", "READONLYBOUNDARY"}:
            continue
        entries[command] = entry_value(command, raw_value)
    return entries


def render_value(entry: ProfileEntry | None, local_show_identifiers: bool) -> dict[str, Any] | None:
    if entry is None:
        return None
    if (entry.command in SENSITIVE_COMMANDS or entry.redacted) and not local_show_identifiers:
        rendered: dict[str, Any] = {"redacted": True}
        if entry.value_hash:
            rendered["sha256"] = entry.value_hash
        elif entry.value is not None:
            rendered["sha256"] = sha256_text(entry.value)
        if entry.byte_length is not None:
            rendered["byteLength"] = entry.byte_length
        elif entry.value is not None:
            rendered["byteLength"] = len(str(entry.value))
        return rendered
    return {
        "redacted": False,
        "value": entry.value,
        "localOnlyIdentifiersShown": bool(entry.command in SENSITIVE_COMMANDS and local_show_identifiers),
    }


def same_value(left: ProfileEntry | None, right: ProfileEntry | None) -> bool:
    if left is None or right is None:
        return False
    if left.redacted or right.redacted:
        return left.value_hash is not None and left.value_hash == right.value_hash
    return str(left.value) == str(right.value)


def command_profile_diff(args: argparse.Namespace) -> dict[str, Any]:
    readback = extract_profile_entries(load_json_file(args.readback))
    target = extract_profile_entries(load_json_file(args.target))
    record = base_record("profile-diff")
    diffs: list[dict[str, Any]] = []
    safety_violations: list[dict[str, Any]] = []

    for command in sorted(set(readback) | set(target)):
        read_entry = readback.get(command)
        target_entry = target.get(command)
        reasons = sorted({reason for reason in [
            read_entry.unsafe_reason if read_entry else None,
            target_entry.unsafe_reason if target_entry else None,
        ] if reason})
        if reasons:
            for reason in reasons:
                safety_violations.append({"command": command, "reason": reason})

        if target_entry is None:
            status = "read_only_observed"
            requires_write = False
        elif read_entry is None:
            status = "blocked_write" if reasons else "target_only"
            requires_write = True
        elif reasons:
            status = "blocked_write"
            requires_write = True
        elif same_value(read_entry, target_entry):
            status = "match"
            requires_write = False
        elif read_entry.redacted or target_entry.redacted:
            status = "unresolved_gap"
            requires_write = False
        else:
            status = "diff"
            requires_write = True

        diffs.append(
            {
                "command": command,
                "status": status,
                "requiresWriteGate": requires_write,
                "readback": render_value(read_entry, args.local_show_identifiers),
                "target": render_value(target_entry, args.local_show_identifiers),
                "safetyReasons": reasons,
            }
        )

    record.update(
        {
            "readbackFile": str(args.readback),
            "targetFile": str(args.target),
            "serialOpenAttempted": False,
            "serialWritesAttempted": False,
            "applyAllowed": False,
            "diffs": diffs,
            "safetyViolations": safety_violations,
            "summary": {
                "total": len(diffs),
                "matches": sum(1 for item in diffs if item["status"] == "match"),
                "diffs": sum(1 for item in diffs if item["status"] == "diff"),
                "blockedWrites": sum(1 for item in diffs if item["status"] == "blocked_write"),
                "unresolvedGaps": sum(1 for item in diffs if item["status"] == "unresolved_gap"),
            },
            "notes": [
                "profile-diff is offline and never opens a serial port.",
                "A target-only or differing setting is evidence for review, not permission to apply.",
            ],
        }
    )
    return record


def command_write_plan(args: argparse.Namespace) -> dict[str, Any]:
    diff = load_json_file(args.diff)
    record = base_record("write-plan")
    proposed_actions = []
    for item in diff.get("diffs", []):
        if not isinstance(item, dict):
            continue
        if item.get("status") in {"diff", "target_only", "blocked_write"} or item.get("requiresWriteGate"):
            proposed_actions.append(
                {
                    "command": item.get("command"),
                    "reviewStatus": "blocked_pending_tier3",
                    "reason": "v1 has no apply command and no radio write authority",
                    "sourceStatus": item.get("status"),
                    "safetyReasons": item.get("safetyReasons", []),
                }
            )

    record.update(
        {
            "diffFile": str(args.diff),
            "applyAllowed": False,
            "applyCommandImplemented": False,
            "serialOpenAttempted": False,
            "serialWritesAttempted": False,
            "blockedOperations": BLOCKED_OPERATIONS,
            "reviewSequence": [
                {"order": 1, "gate": "same-session Tier 3 authority", "status": "blocked"},
                {"order": 2, "gate": "current settings backup/readback", "status": "blocked"},
                {"order": 3, "gate": "address, AES key, antenna, carrier, rollback review", "status": "blocked"},
                {"order": 4, "gate": "closed-surface reviewer quorum", "status": "blocked"},
                {"order": 5, "gate": "operator-approved write procedure", "status": "blocked"},
            ],
            "proposedActions": proposed_actions,
            "summary": {
                "proposedActionCount": len(proposed_actions),
                "allActionsBlocked": True,
            },
        }
    )
    return record


def add_json_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Emit JSON. JSON is the only output format.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory", help="Collect host/tool inventory without opening serial ports.")
    inventory.add_argument(
        "--local-show-identifiers",
        action="store_true",
        help="Show local-only PnP identifiers. Default output hashes them.",
    )
    add_json_arg(inventory)
    inventory.set_defaults(func=command_inventory)

    readonly = subparsers.add_parser("readonly", help="Delegate to the fixed AT read-query probe.")
    readonly.add_argument("--port", required=True)
    readonly.add_argument("--baud", required=True, type=int)
    readonly.add_argument("--confirm-sends-read-commands", action="store_true")
    readonly.add_argument(
        "--show-addresses",
        action="store_true",
        help="Show SH/SL address values for local-only evidence; default output redacts them.",
    )
    add_json_arg(readonly)
    readonly.set_defaults(func=command_readonly)

    profile_diff = subparsers.add_parser("profile-diff", help="Compare readback JSON to target JSON without writing.")
    profile_diff.add_argument("--readback", required=True, type=Path)
    profile_diff.add_argument("--target", required=True, type=Path)
    profile_diff.add_argument(
        "--local-show-identifiers",
        action="store_true",
        help="Show local-only sensitive values. Default output redacts SH/SL/KY values.",
    )
    add_json_arg(profile_diff)
    profile_diff.set_defaults(func=command_profile_diff)

    write_plan = subparsers.add_parser("write-plan", help="Emit a blocked review packet from a diff JSON file.")
    write_plan.add_argument("--diff", required=True, type=Path)
    add_json_arg(write_plan)
    write_plan.set_defaults(func=command_write_plan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return emit(args.func(args))
    except StudyError as exc:
        return emit(error_record(args.command, exc.code, exc.message, exc.details))
    except probe.ProbeError as exc:
        return emit(error_record(args.command, exc.code, exc.message, exc.details))


if __name__ == "__main__":
    raise SystemExit(main())
