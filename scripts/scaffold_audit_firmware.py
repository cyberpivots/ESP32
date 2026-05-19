#!/usr/bin/env python3
"""Firmware skeleton and safe-core contract audits."""

from __future__ import annotations

from pathlib import Path

from scaffold_audit_data import (
    FIRMWARE_SOURCE_SCAN_ROOT,
    FORBIDDEN_FIRMWARE_MARKERS,
    ROOT,
)
from scaffold_audit_docs import require_markers


def audit_firmware_readme(root: Path = ROOT) -> list[str]:
    firmware_readme = (
        root / "firmware/projects/four-relay-xbee-wifi/README.md"
    ).read_text(encoding="utf-8")
    return require_markers(firmware_readme, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Hard gates",
        "No GPIO writes",
        "No expander writes",
        "No XBee setting writes",
        "No flash or monitor step",
        "No live bench mutation",
        "pure-C API payload validation",
        "normalized state snapshots",
        "split host-test binaries",
        "SRC-ESP-IDF-STABLE-ESP32",
        "SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18",
        "SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19",
    ], "firmware skeleton README")


def audit_safe_core_contract(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    core_header = (
        root
        / "firmware/projects/four-relay-xbee-wifi/components/safe_core/include/four_relay_core.h"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(core_header, [
        "FR_REJECT_HARDWARE_GATE_OPEN",
        "fr_relay_request_set",
        "fr_relay_request_set_public",
        "fr_relay_public_channel_to_index",
        "fr_safety_supervisor_accepts_change",
        "fr_config_store_default",
        "fr_http_classify_route",
        "fr_api_validate_relay_payload",
        "fr_api_build_state_snapshot",
        "fr_api_assets_manifest_default",
        "fr_api_logs_recent_empty",
        "fr_storage_status_default",
        "fr_xbee_encode_api2",
        "fr_xbee_decode_api2",
        "fr_xbee_parse_at_response",
        "fr_xbee_parse_receive_packet",
    ], "safe core header"))

    host_test_runner = (
        root / "tests/four_relay_safe_core/run_host_tests.py"
    ).read_text(encoding="utf-8")
    host_test_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "tests/four_relay_safe_core").glob("test_*.c"))
    )
    failures.extend(require_markers(host_test_text, [
        "hardware_gate_open",
        "public relay channel zero route rejects",
        "public relay channel 4 maps to internal index three",
        "GET /api/state response snapshot includes storage",
        "POST /api/all-off payload contract accepts sequence",
        "GET /api/assets/manifest response exposes file list",
        "GET /api/logs/recent response defaults empty",
        "XBee API2 encode succeeds in memory",
        "bad checksum rejects",
        "XBee truncated escape rejects",
        "AT response frame parses command",
        "receive-packet payload parses",
    ], "safe core host tests"))
    for marker in ["-Werror", "test_relay_safety", "safe_core"]:
        if marker not in host_test_runner:
            failures.append(f"safe core test runner missing marker: {marker}")
    return failures


def audit_firmware_forbidden_markers(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    scan_root = root / FIRMWARE_SOURCE_SCAN_ROOT.relative_to(ROOT)
    for source_file in sorted(scan_root.rglob("*")):
        if source_file.suffix not in {".c", ".h", ".txt"} and source_file.name != "CMakeLists.txt":
            continue
        text = source_file.read_text(encoding="utf-8")
        rel = source_file.relative_to(root).as_posix()
        for forbidden in FORBIDDEN_FIRMWARE_MARKERS:
            if forbidden in text:
                failures.append(f"firmware skeleton contains forbidden marker {forbidden}: {rel}")
    return failures


def audit_firmware(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(audit_firmware_readme(root))
    failures.extend(audit_safe_core_contract(root))
    failures.extend(audit_firmware_forbidden_markers(root))
    return failures
