#!/usr/bin/env python3
"""Deterministic host-only XBee hub-spoke planning simulator.

The simulator models payload and custody behavior only. It does not open serial
ports, build live transmit frames, launch Digi tools, or touch hardware.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from typing import Any


SCHEMA = "xbee_hub_spoke_plan.v1"
DEFAULT_NP_HEX = "0100"
MIN_SPOKES = 10
SOURCE_IDS = [
    "SRC-DIGI-XBP9B-DPUT-001",
    "SRC-DIGI-XBEE-900HP-AP",
    "SRC-DIGI-XBEE-900HP-AO",
    "SRC-DIGI-XBEE-900HP-NP",
    "SRC-DIGI-XBEE-900HP-DELIVERY",
    "SRC-DIGI-XBEE-900HP-TO-2026-06-05",
    "SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05",
    "SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05",
]

USE_CASES: list[dict[str, Any]] = [
    {
        "id": "custody_ack_backhaul",
        "rank": 1,
        "messageType": "custody_ack",
        "direction": "spoke-to-hub",
        "summary": "Custody acknowledgements for queued BBS items.",
        "payloadBytes": 48,
    },
    {
        "id": "node_status_rollup",
        "rank": 2,
        "messageType": "node_status",
        "direction": "spoke-to-hub",
        "summary": "Heartbeat, link, queue, uptime, and health summaries.",
        "payloadBytes": 64,
    },
    {
        "id": "direct_message_exchange",
        "rank": 3,
        "messageType": "direct_message",
        "direction": "bidirectional",
        "summary": "Small BBS message metadata exchange without file bodies.",
        "payloadBytes": 72,
    },
    {
        "id": "small_file_queue",
        "rank": 4,
        "messageType": "file_chunk_notice",
        "direction": "bidirectional",
        "summary": "Packetized bulletin or small-file queue metadata.",
        "payloadBytes": 72,
    },
    {
        "id": "field_console_status",
        "rank": 5,
        "messageType": "lcd_status",
        "direction": "hub-to-spoke-review",
        "summary": "Remote LCD display status feed; input stays local.",
        "payloadBytes": 56,
    },
    {
        "id": "service_catalog_sideband",
        "rank": 6,
        "messageType": "capability_report",
        "direction": "spoke-to-hub",
        "summary": "Service and capability inventory for aliases only.",
        "payloadBytes": 60,
    },
    {
        "id": "commissioning_evidence_lane",
        "rank": 7,
        "messageType": "link_probe_review",
        "direction": "bidirectional-review",
        "summary": "Synthetic link-probe/readback readiness records.",
        "payloadBytes": 40,
    },
    {
        "id": "field_telemetry_snapshot",
        "rank": 8,
        "messageType": "telemetry_report",
        "direction": "spoke-to-hub",
        "summary": "Battery, solar, and field-node telemetry slots.",
        "payloadBytes": 64,
    },
    {
        "id": "saved_evidence_analysis",
        "rank": 9,
        "messageType": "analysis_import",
        "direction": "host-only",
        "summary": "Hardware Tools import of redacted planning records.",
        "payloadBytes": 32,
    },
    {
        "id": "control_intent_audit",
        "rank": 10,
        "messageType": "control_intent_audit",
        "direction": "host-only",
        "summary": "Non-executing operator intent rehearsal records.",
        "payloadBytes": 40,
    },
    {
        "id": "lock_state_broadcast",
        "rank": 11,
        "messageType": "lock_state",
        "direction": "hub-to-spoke-review",
        "summary": "Closed-surface lock state visibility.",
        "payloadBytes": 52,
    },
    {
        "id": "solar_client_health_beacon",
        "rank": 12,
        "messageType": "solar_health",
        "direction": "spoke-to-hub",
        "summary": "Remote solar-client health beacon placeholder.",
        "payloadBytes": 56,
    },
]

PUBLIC_RED_FLAG_PATTERNS = [
    re.compile(r"\bCOM[1-9][0-9]*\b", re.IGNORECASE),
    re.compile(r"/dev/tty[A-Za-z0-9_./-]*"),
    re.compile(r"\b0013A2[0-9A-Fa-f]{10,}\b"),
    re.compile(r"\bKY\s*[:=]", re.IGNORECASE),
    re.compile(r"\b[A-Fa-f0-9]{32,}\b"),
    re.compile(r"private[-_\s]?(key|address)\s*[:=]", re.IGNORECASE),
]


def parse_np_hex(value: str | int) -> int:
    if isinstance(value, int):
        np_bytes = value
    else:
        normalized = value.strip().lower()
        if normalized.startswith("0x"):
            normalized = normalized[2:]
        if not re.fullmatch(r"[0-9a-f]+", normalized):
            raise ValueError("np value must be hexadecimal")
        np_bytes = int(normalized, 16)
    if np_bytes <= 0:
        raise ValueError("np value must be positive")
    return np_bytes


def _spoke_aliases(spoke_count: int) -> list[dict[str, Any]]:
    if spoke_count < MIN_SPOKES:
        raise ValueError(f"spoke_count must be at least {MIN_SPOKES}")
    return [
        {
            "alias": f"spoke-{index:02d}",
            "role": "spoke",
            "addressRedacted": True,
            "rawIdentifierStored": False,
        }
        for index in range(1, spoke_count + 1)
    ]


def _scenario_for(use_case: dict[str, Any], source_alias: str, budget_bytes: int) -> dict[str, Any]:
    payload_bytes = int(use_case["payloadBytes"])
    fits_budget = payload_bytes <= budget_bytes
    return {
        "id": f"scenario-{use_case['rank']:02d}-{use_case['id']}",
        "useCaseId": use_case["id"],
        "sourceAlias": source_alias,
        "sequence": use_case["rank"],
        "messageType": use_case["messageType"],
        "direction": use_case["direction"],
        "payloadBytes": payload_bytes,
        "fitsEncryptedNpBudget": fits_budget,
        "receiveFrame": {
            "frameType": "0x90",
            "sourceAlias": source_alias,
            "addressRedacted": True,
        },
        "transmitStatusFrame": {
            "frameType": "0x8B",
            "frameIdAlias": f"frame-{use_case['rank']:02d}",
            "deliveryStatus": "synthetic_success" if fits_budget else "synthetic_payload_too_large",
            "liveDeliveryClaim": False,
        },
        "outcome": "planned" if fits_budget else "payload_budget_gap",
    }


def build_hub_spoke_plan(spoke_count: int = MIN_SPOKES, np_hex: str | int = DEFAULT_NP_HEX) -> dict[str, Any]:
    np_bytes = parse_np_hex(np_hex)
    aps_encrypted_budget = max(np_bytes - 9, 0)
    secure_session_budget = max(np_bytes - 4, 0)
    spokes = _spoke_aliases(spoke_count)
    scenarios = [
        _scenario_for(use_case, spokes[(use_case["rank"] - 1) % len(spokes)]["alias"], aps_encrypted_budget)
        for use_case in USE_CASES
    ]
    plan = {
        "schema": SCHEMA,
        "topology": {
            "model": "XBP9B-DPUT-001",
            "radioFamily": "XBee-PRO 900HP S3B",
            "defaultDelivery": "point-to-multipoint",
            "tenKProduct": True,
            "digiMeshForCurrentPart": "blocked_without_variant_proof",
            "receiveFrame": "0x90",
            "transmitRequestFrame": "0x10",
            "transmitStatusFrame": "0x8B",
        },
        "hostOnlyBoundary": {
            "serialOpenAttempted": False,
            "serialWritesAttempted": False,
            "xctuLaunchAttempted": False,
            "xbeeStudioLaunchAttempted": False,
            "apiTransmitGenerated": False,
            "rfTransmitAttempted": False,
            "firmwareMutationAttempted": False,
            "relayOrLoadMutationAttempted": False,
        },
        "payloadBudget": {
            "npBytes": np_bytes,
            "apsEncryptedBytes": aps_encrypted_budget,
            "secureSessionOptionBytes": secure_session_budget,
            "sourceIds": [
                "SRC-DIGI-XBEE-900HP-NP",
                "SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05",
            ],
        },
        "hub": {"alias": "hub-operator", "role": "hub", "addressRedacted": True},
        "spokes": spokes,
        "useCases": deepcopy(USE_CASES),
        "scenarios": scenarios,
        "closedSurfaceFlags": ["serial_write", "rf_xbee_write", "relay_or_load", "firmware_abi"],
        "sourceIds": SOURCE_IDS,
        "redaction": {
            "rawAddressesIncluded": False,
            "keysIncluded": False,
            "privateComMappingsIncluded": False,
            "fullSettingSnapshotsIncluded": False,
        },
        "notes": [
            "Synthetic host-only plan; does not prove live radio delivery.",
            "Use 0x8B for 900HP transmit status associated with 0x10 requests.",
            "Current exact part stays point-to-multipoint; DigiMesh is blocked for the 10k build unless a later source and readback prove another variant.",
        ],
    }
    issues = find_public_redaction_issues(plan)
    plan["redaction"]["publicRedactionIssues"] = issues
    return plan


def find_public_redaction_issues(record: dict[str, Any]) -> list[str]:
    rendered = json.dumps(record, sort_keys=True)
    issues: list[str] = []
    for pattern in PUBLIC_RED_FLAG_PATTERNS:
        if pattern.search(rendered):
            issues.append(pattern.pattern)
    return issues
