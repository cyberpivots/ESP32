#!/usr/bin/env python3
"""Offline-first XBee radio programming study CLI.

The v1 boundary is intentionally narrow. Inventory does not open serial ports,
profile diffing is file-only, and write-plan emits a blocked review packet
instead of applying settings. The readonly command delegates to the existing
fixed AT read-query probe and keeps that probe's explicit confirmation gate.
"""

from __future__ import annotations

import argparse
import glob
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
OUT_ROOT = probe.OUT_ROOT
ADDRESS_COMMANDS = {"SH", "SL"}
SECRET_COMMANDS = {"KY"}
SENSITIVE_COMMANDS = ADDRESS_COMMANDS | SECRET_COMMANDS
PORT_RE = re.compile(r"^COM[1-9][0-9]*$", flags=re.IGNORECASE)
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
XCTU_BLOCKED_OPERATIONS = BLOCKED_OPERATIONS + [
    "all-port discovery",
    "broad port-parameter scans",
    "network discovery",
    "remote device discovery",
    "AT or API console transmit actions",
    "write, apply, restore, or reset controls",
    "firmware library update, firmware update, or recovery tools",
    "throughput tests",
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


def repository_relative(path: Path) -> str:
    return probe.repository_relative(path)


def write_optional_output(record: dict[str, Any], out_path: Path | None) -> None:
    if out_path is None:
        return

    resolved = out_path.resolve()
    out_root = OUT_ROOT.resolve()
    if resolved == out_root or out_root not in resolved.parents:
        raise StudyError(
            "invalid_output_path",
            "--out must write under research/bench-records/xbee-readonly/",
            {"requested": str(out_path), "allowedRoot": repository_relative(OUT_ROOT)},
        )
    if resolved.exists():
        raise StudyError(
            "output_exists",
            "refusing to overwrite an existing bench record",
            {"requested": repository_relative(resolved)},
        )

    record["outputPath"] = repository_relative(resolved)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def emit(record: dict[str, Any], args: argparse.Namespace | None = None) -> int:
    write_optional_output(record, getattr(args, "out", None) if args is not None else None)
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
        if any(marker in candidate for marker in "*?[]"):
            found_paths.extend(match for match in sorted(glob.glob(candidate)) if Path(match).exists())
        elif Path(candidate).exists():
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
        "/mnt/c/Program Files (x86)/Digi/XCTU-NG/XCTU.exe",
        "/mnt/c/Program Files/Digi/XCTU-NG/XCTU.exe",
        "/mnt/c/Users/*/AppData/Local/Digi/XCTU-NG/XCTU.exe",
        "/mnt/c/Users/*/AppData/Local/Digi/XCTU/XCTU.exe",
        "C:/Program Files (x86)/Digi/XCTU/XCTU.exe",
        "C:/Program Files/Digi/XCTU/XCTU.exe",
        "C:/Program Files (x86)/Digi/XCTU-NG/XCTU.exe",
        "C:/Program Files/Digi/XCTU-NG/XCTU.exe",
        "C:/Users/*/AppData/Local/Digi/XCTU-NG/XCTU.exe",
        "C:/Users/*/AppData/Local/Digi/XCTU/XCTU.exe",
    ]
    xbee_studio_paths = [
        "/mnt/c/Program Files/Digi/XBee Studio/XBee Studio.exe",
        "/mnt/c/Program Files (x86)/Digi/XBee Studio/XBee Studio.exe",
        "C:/Program Files/Digi/XBee Studio/XBee Studio.exe",
        "C:/Program Files (x86)/Digi/XBee Studio/XBee Studio.exe",
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
            "serialOpenAttempted": False,
            "serialWritesAttempted": False,
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


def extract_com_label(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.search(r"\bCOM[1-9][0-9]*\b", value, flags=re.IGNORECASE)
    return match.group(0).upper() if match else None


def stable_candidate_key(source: str, item: dict[str, Any]) -> str:
    for field in ("deviceIdSha256", "hwidSha256", "fingerprint"):
        value = item.get(field)
        if isinstance(value, str) and value:
            return f"{source}:{field}:{value}"
    if source == "windowsComHint" and item.get("windowsPort"):
        return f"{source}:port:{item['windowsPort']}"
    if source == "wslCandidate" and item.get("path"):
        return f"{source}:path:{item['path']}"
    return f"{source}:hash:{sha256_text(json.dumps(item, sort_keys=True))}"


def sanitize_windows_pnp(item: dict[str, Any]) -> dict[str, Any]:
    raw_device_id = item.get("deviceId") or item.get("DeviceID")
    device_id_hash = item.get("deviceIdSha256")
    if not device_id_hash and raw_device_id:
        device_id_hash = sha256_text(raw_device_id)
    sanitized: dict[str, Any] = {
        "source": "windowsPnp",
        "name": item.get("name") or item.get("Name"),
        "port": extract_com_label(item.get("name") or item.get("Name")),
        "manufacturer": item.get("manufacturer") or item.get("Manufacturer"),
        "pnpClass": item.get("pnpClass") or item.get("PNPClass"),
        "status": item.get("status") or item.get("Status"),
        "deviceIdRedacted": bool(device_id_hash or raw_device_id or item.get("deviceIdRedacted")),
    }
    if device_id_hash:
        sanitized["deviceIdSha256"] = device_id_hash
    return {key: value for key, value in sanitized.items() if value not in (None, "")}


def sanitize_windows_com_hint(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "windowsComHint",
        "windowsPort": str(item.get("windowsPort", "")).upper(),
        "wslLegacyHint": item.get("wslLegacyHint"),
    }


def sanitize_wsl_candidate(item: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {
        "source": "wslCandidate",
        "path": item.get("path"),
        "candidateSource": item.get("source"),
        "description": item.get("description"),
    }
    hwid = item.get("hwid")
    if hwid:
        sanitized["hwidSha256"] = sha256_text(hwid)
        sanitized["hwidRedacted"] = True
    return {key: value for key, value in sanitized.items() if value not in (None, "")}


def inventory_candidates(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    serial = data.get("serial") if isinstance(data.get("serial"), dict) else {}
    candidates: dict[str, dict[str, Any]] = {}

    for item in serial.get("wslCandidates", []) if isinstance(serial.get("wslCandidates"), list) else []:
        if not isinstance(item, dict):
            continue
        sanitized = sanitize_wsl_candidate(item)
        candidates[stable_candidate_key("wslCandidate", sanitized)] = sanitized

    windows_hints = serial.get("windowsComHints") if isinstance(serial.get("windowsComHints"), dict) else {}
    for item in windows_hints.get("ports", []) if isinstance(windows_hints.get("ports"), list) else []:
        if not isinstance(item, dict):
            continue
        sanitized = sanitize_windows_com_hint(item)
        candidates[stable_candidate_key("windowsComHint", sanitized)] = sanitized

    windows_pnp = serial.get("windowsPnp") if isinstance(serial.get("windowsPnp"), dict) else {}
    for item in windows_pnp.get("devices", []) if isinstance(windows_pnp.get("devices"), list) else []:
        if not isinstance(item, dict):
            continue
        sanitized = sanitize_windows_pnp(item)
        candidates[stable_candidate_key("windowsPnp", sanitized)] = sanitized

    return candidates


def command_identity_delta(args: argparse.Namespace) -> dict[str, Any]:
    before = inventory_candidates(load_json_file(args.before))
    after = inventory_candidates(load_json_file(args.after))
    before_keys = set(before)
    after_keys = set(after)
    changed = []
    for key in sorted(before_keys & after_keys):
        if before[key] != after[key]:
            changed.append({"key": key, "before": before[key], "after": after[key]})

    record = base_record("identity-delta")
    record.update(
        {
            "beforeFile": str(args.before),
            "afterFile": str(args.after),
            "serialOpenAttempted": False,
            "serialWritesAttempted": False,
            "xctuLaunchAttempted": False,
            "rawIdentifiersRedacted": True,
            "candidateCounts": {"before": len(before), "after": len(after)},
            "added": [after[key] | {"key": key} for key in sorted(after_keys - before_keys)],
            "removed": [before[key] | {"key": key} for key in sorted(before_keys - after_keys)],
            "changed": changed,
            "summary": {
                "added": len(after_keys - before_keys),
                "removed": len(before_keys - after_keys),
                "changed": len(changed),
                "unchanged": len((before_keys & after_keys) - {item["key"] for item in changed}),
            },
            "notes": [
                "identity-delta compares inventory JSON files only and does not open serial ports.",
                "Deltas are host evidence; physical one-at-a-time disconnect/reconnect notes are still required before a radio identity claim.",
                "Raw PnP IDs and hardware IDs are hashed or omitted in this output.",
            ],
        }
    )
    return record


def normalize_com_ports(ports: list[str]) -> list[str]:
    normalized: list[str] = []
    for port in ports:
        value = port.strip().upper()
        if not PORT_RE.fullmatch(value):
            raise StudyError("invalid_port", "ports must use Windows COMx names", {"port": port})
        if value not in normalized:
            normalized.append(value)
    if not normalized:
        raise StudyError("no_ports", "at least one confirmed port is required")
    return normalized


def command_xctu_discovery_plan(args: argparse.Namespace) -> dict[str, Any]:
    ports = normalize_com_ports(args.ports)
    record = base_record("xctu-discovery-plan")
    record.update(
        {
            "requestedPorts": ports,
            "serialOpenAttempted": False,
            "serialWritesAttempted": False,
            "xctuLaunchAttempted": False,
            "xctuDiscoveryAttempted": False,
            "gateStatus": "locked_pending_prerequisites",
            "preconditions": [
                "Two local ports are confirmed by one-at-a-time physical disconnect/reconnect identity-delta evidence.",
                "Local-only physical evidence records adapter markings, antenna state, no ESP32 DIN/DOUT wiring, no relay/load/mains connection, and no battery/solar wiring.",
                "Voltage/carrier review records adapter power path, UART level, DIN/DOUT direction, reset/sleep/flow-control exposure, and recovery stop rules.",
                "All raw COM/PnP identifiers, SH/SL values, passive bytes, AES keys, and full setting snapshots remain local-only.",
            ],
            "manualChecklist": [
                {"order": 1, "step": "Close other serial clients and leave XCTU closed until prerequisites are present.", "status": "locked"},
                {"order": 2, "step": "Open XCTU manually only after the gate packet names these exact ports.", "status": "locked"},
                {"order": 3, "step": "Use Discover radio modules and select only the confirmed ports.", "status": "locked"},
                {"order": 4, "step": "Use default port parameters only; do not broaden baud/parameter scans.", "status": "locked"},
                {"order": 5, "step": "Add selected local devices only if found; capture redacted read-only evidence.", "status": "locked"},
                {"order": 6, "step": "Stop immediately on update, firmware, recovery, write/apply, remote/network discovery, or unexpected identity prompts.", "status": "locked"},
            ],
            "blockedOperations": XCTU_BLOCKED_OPERATIONS,
            "sourceIds": [
                "SRC-DIGI-XCTU-FEATURES-2026-05-29",
                "SRC-DIGI-XCTU-LOCAL-DISCOVERY-2026-05-29",
                "SRC-DIGI-XBEE-900HP-AP",
                "SRC-DIGI-XBEE-900HP-AO",
                "SRC-DIGI-XBEE-900HP-BD-2026-05-29",
                "SRC-DIGI-XBEE-900HP-NP",
            ],
            "notes": [
                "This command emits a planning checklist only. It does not launch XCTU or touch serial ports.",
                "XCTU all-port discovery, broad parameter scans, network discovery, remote devices, writes, firmware tools, range tests, and throughput tests remain blocked.",
            ],
        }
    )
    return record


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

    inventory = subparsers.add_parser("inventory", help="Collect host/tool inventory without opening serial ports.")
    inventory.add_argument(
        "--local-show-identifiers",
        action="store_true",
        help="Show local-only PnP identifiers. Default output hashes them.",
    )
    add_json_output_args(inventory)
    inventory.set_defaults(func=command_inventory)

    identity_delta = subparsers.add_parser(
        "identity-delta",
        help="Compare two inventory snapshots without opening serial ports.",
    )
    identity_delta.add_argument("--before", required=True, type=Path)
    identity_delta.add_argument("--after", required=True, type=Path)
    add_json_output_args(identity_delta)
    identity_delta.set_defaults(func=command_identity_delta)

    readonly = subparsers.add_parser("readonly", help="Delegate to the fixed AT read-query probe.")
    readonly.add_argument("--port", required=True)
    readonly.add_argument("--baud", required=True, type=int)
    readonly.add_argument("--confirm-sends-read-commands", action="store_true")
    readonly.add_argument(
        "--show-addresses",
        action="store_true",
        help="Show SH/SL address values for local-only evidence; default output redacts them.",
    )
    add_json_output_args(readonly)
    readonly.set_defaults(func=command_readonly)

    profile_diff = subparsers.add_parser("profile-diff", help="Compare readback JSON to target JSON without writing.")
    profile_diff.add_argument("--readback", required=True, type=Path)
    profile_diff.add_argument("--target", required=True, type=Path)
    profile_diff.add_argument(
        "--local-show-identifiers",
        action="store_true",
        help="Show local-only sensitive values. Default output redacts SH/SL/KY values.",
    )
    add_json_output_args(profile_diff)
    profile_diff.set_defaults(func=command_profile_diff)

    write_plan = subparsers.add_parser("write-plan", help="Emit a blocked review packet from a diff JSON file.")
    write_plan.add_argument("--diff", required=True, type=Path)
    add_json_output_args(write_plan)
    write_plan.set_defaults(func=command_write_plan)

    xctu_plan = subparsers.add_parser(
        "xctu-discovery-plan",
        help="Emit a locked XCTU local-discovery checklist without launching XCTU.",
    )
    xctu_plan.add_argument("--ports", nargs="+", required=True, help="Confirmed Windows COMx ports only.")
    add_json_output_args(xctu_plan)
    xctu_plan.set_defaults(func=command_xctu_discovery_plan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return emit(args.func(args), args)
    except StudyError as exc:
        return emit(error_record(args.command, exc.code, exc.message, exc.details))
    except probe.ProbeError as exc:
        return emit(error_record(args.command, exc.code, exc.message, exc.details))


if __name__ == "__main__":
    raise SystemExit(main())
