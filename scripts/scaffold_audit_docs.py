#!/usr/bin/env python3
"""Documentation marker audits for the ESP32 scaffold."""

from __future__ import annotations

from pathlib import Path

from scaffold_audit_data import ROOT


def require_markers(text: str, markers: list[str], label: str) -> list[str]:
    return [f"{label} missing marker: {marker}" for marker in markers if marker not in text]


def audit_docs_index(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    docs_index = (root / "docs/index.md").read_text(encoding="utf-8")
    for docs_file in sorted((root / "docs").rglob("*.md")):
        if docs_file.name == "index.md":
            continue
        required_link = docs_file.relative_to(root / "docs").as_posix()
        if required_link not in docs_index:
            failures.append(f"docs index missing link: {required_link}")

    for required_link in [
        "../knowledge-base/source-index.md",
        "../knowledge-base/model-profiles.md",
        "../knowledge-base/prompt-registry.md",
        "../knowledge-base/source-ledger/2026-05-18-esp32project-photo-analysis.md",
        "../knowledge-base/source-ledger/2026-05-18-diy-bench-hardware-blockers.md",
        "../knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md",
        "../knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md",
        "../knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md",
        "../research/known-gaps.md",
        "../research/triage-status.md",
        "../research/bench-records/TEMPLATE.md",
        "../research/skills/available-skills.md",
    ]:
        if required_link not in docs_index:
            failures.append(f"docs index missing cross-area link: {required_link}")
    return failures


def audit_bench_runbook(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    bench_runbook = (
        root / "docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md"
    ).read_text(encoding="utf-8")
    for stage in [
        "## Stage 1 - ESP32 board and expansion shield",
        "## Stage 2 - Four-channel relay module, contacts disconnected",
        "## Stage 3 - Waveshare XBee USB Adapter read-only discovery",
        "## Stage 4 - Mains-readiness review only",
    ]:
        if stage not in bench_runbook:
            failures.append(f"bench runbook missing stage: {stage}")
    for marker in [
        "Tools needed:",
        "Power-off checks:",
        "Expected measurement:",
        "Pass result:",
        "Fail result:",
        "Stop condition:",
    ]:
        if bench_runbook.count(marker) < 4:
            failures.append(f"bench runbook missing repeated QA marker: {marker}")
    return failures


def audit_project_docs(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    xbee_read_only = (
        root / "docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(xbee_read_only, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "Tier A passive discovery",
        "Tier B read-query discovery",
        "--confirm-sends-read-commands",
        "Allowed AT read queries:",
        "| `VR` |",
        "| `NP` |",
        "WR",
        "AC",
        "ESP32 DIN/DOUT wiring",
        "SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18",
    ], "XBee read-only proof"))

    xbee_probe = (root / "scripts/xbee_read_only_probe.py").read_text(encoding="utf-8")
    failures.extend(require_markers(xbee_probe, [
        "DEFAULT_AT_QUERIES",
        '"VR", "HV", "SH", "SL", "AP", "AO", "BD", "NP"',
        "confirm_sends_read_commands",
        "at_command_not_allowed",
        "serialWritesAttempted",
        "sampleRedacted",
        "research/bench-records/xbee-readonly",
    ], "XBee probe script"))

    hardware_research = (
        root
        / "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(hardware_research, [
        "## Verified facts",
        "## Current blockers",
        "## Recommended research lanes",
        "## Additional components and instruments needed",
        "## Circuit design improvement candidates",
        "## Bench validation sequence",
        "## Required documentation updates",
        "## Open questions for the user",
        "### Assumptions",
        "### Unknowns",
        "### Risks",
        "### Required next evidence",
        "### must buy",
        "### must identify",
        "### must measure",
        "### candidate only",
        "### blocked",
        "No mains wiring procedure",
        "SRC-TI-LM66100",
        "SRC-LITTELFUSE-16R-PPTC",
        "SRC-SD-ASSOCIATION-FORMATTER",
        "SRC-SALEAE-LOGIC-8",
    ], "hardware research doc"))

    rd_loop = (
        root / "docs/projects/four-relay-xbee-wifi/rd-loop.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(rd_loop, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Non-negotiable gates",
        "## Milestones",
        "## Role lanes",
        "## Cycle review rule",
        "## M2 prototype boundaries",
        "## Acceptance checks",
        "M0 intake",
        "M5 release/public package",
        "Architect",
        "Hardware",
        "Communications",
        "Firmware",
        "QA",
        "Release",
        "approved_with_gaps",
        "hardware_gate_open",
        "No XBee setting writes",
        "No relay GPIO writes",
        "SRC-ESP-IDF-STABLE-ESP32",
        "SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18",
    ], "R&D loop doc"))

    prototype_blueprint = (
        root / "docs/projects/four-relay-xbee-wifi/prototype-blueprint.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(prototype_blueprint, [
        "GPIO25/GPIO26/GPIO27/GPIO33",
        "relay input header only after 3.3 V/current gate",
        "Mains wiring: hard blocked",
        "future driver-stage",
    ], "prototype blueprint"))

    prototype_packet = (
        root / "docs/projects/four-relay-xbee-wifi/prototype-build-packet.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(prototype_packet, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Public packet map",
        "## Provisional signal map",
        "## Bench review sequence",
        "## Bench evidence checklist",
        "## Stop conditions",
        "SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21",
        "SRC-ESP-IDF-GPIO",
        "SRC-DIGI-XBP9B-DPUT-001",
        "xbee-public-boundary.md",
        "not a final wiring diagram",
    ], "prototype build packet"))

    xbee_public_boundary = (
        root / "docs/projects/four-relay-xbee-wifi/xbee-public-boundary.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(xbee_public_boundary, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Public rules",
        "## Next evidence",
        "SRC-DIGI-XBP9B-DPUT-001",
        "SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18",
        "XBee setting writes",
        "private bench records",
    ], "XBee public boundary"))

    build_guide = (
        root / "docs/projects/four-relay-xbee-wifi/build-guide.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(build_guide, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "Output A",
        "GPIO25",
        "Low-voltage construction order",
        "Qualified load review",
        "Stop if any step requires mains wiring",
    ], "build guide"))

    mains_gate = (
        root / "docs/projects/four-relay-xbee-wifi/mains-readiness-gate.md"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(mains_gate, [
        "No step-by-step mains wiring instructions.",
        "Qualified review",
        "Overcurrent protection",
        "Grounding/bonding",
        "GFCI/de-energization",
        "Strain relief",
    ], "mains readiness gate"))

    known_gaps = (root / "research/known-gaps.md").read_text(encoding="utf-8")
    failures.extend(require_markers(known_gaps, [
        "## Next evidence record required",
        "Exact ESP32 board and expansion shield",
        "Four-channel relay module",
        "Open-Smart R61509V TFT",
        "MicroSD reader and card policy",
        "XBee read-only bench proof",
        "Qualified mains package",
    ], "known gaps"))

    bench_template = (root / "research/bench-records/TEMPLATE.md").read_text(
        encoding="utf-8"
    )
    failures.extend(require_markers(bench_template, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Board and shield power",
        "## Relay module",
        "## MicroSD reader",
        "## XBee adapter or carrier",
        "## TFT module",
        "## Mux",
        "## Expander",
        "## Instruments and fixtures",
        "## Qualified review gate",
    ], "bench record template"))

    return failures


def audit_docs(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(audit_docs_index(root))
    failures.extend(audit_bench_runbook(root))
    failures.extend(audit_project_docs(root))
    return failures
