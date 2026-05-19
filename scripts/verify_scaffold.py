#!/usr/bin/env python3
"""Validate the initial ESP32 workspace scaffold."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    ".agents/GOVERNANCE.md",
    ".agents/OWNERSHIP.md",
    ".agents/ROLES.md",
    ".agents/TASK_TEMPLATE.md",
    ".agents/TASK_LOG/0001-workspace-scaffold.md",
    ".agents/TASK_LOG/0002-four-relay-xbee-wifi-design-package.md",
    ".agents/TASK_LOG/0003-esp32project-photo-analysis.md",
    ".agents/TASK_LOG/0004-diy-bench-hardware-blueprint.md",
    ".agents/TASK_LOG/0005-admin-hmi-microsd-assets-logs.md",
    ".agents/TASK_LOG/0006-github-pages-public-diy-site.md",
    ".agents/TASK_LOG/0008-github-pages-workbench-build-guide.md",
    ".agents/TASK_LOG/0011-github-pages-blueprints-schematics.md",
    ".agents/TASK_LOG/0012-xbee-read-only-bench-proof.md",
    ".agents/TASK_LOG/0013-hardware-circuit-improvement-research.md",
    ".agents/TASK_LOG/0014-rd-loop-disabled-skeleton.md",
    ".agents/TASK_LOG/0015-public-wow-factor-workbench.md",
    ".agents/TASK_LOG/0016-codebase-research-integration-review.md",
    ".agents/DECISIONS/ADR-0001-framework-choice.md",
    ".agents/DECISIONS/ADR-0002-four-relay-xbee-wifi-framework.md",
    ".agents/handoffs/0002-design-to-hardware-firmware-qa.md",
    ".agents/handoffs/0003-photo-analysis-to-hardware-qa.md",
    ".agents/handoffs/0004-blueprint-to-hardware-qa.md",
    ".agents/handoffs/0005-admin-hmi-to-firmware-hardware-qa.md",
    ".agents/handoffs/0006-github-pages-public-diy-site.md",
    ".agents/handoffs/0008-github-pages-blueprints-to-release-qa.md",
    ".agents/handoffs/0009-xbee-read-only-proof-to-hardware-comms-qa.md",
    ".agents/handoffs/0010-hardware-circuit-research-to-hardware-qa.md",
    ".agents/handoffs/0011-rd-loop-disabled-skeleton-to-role-lanes.md",
    ".agents/handoffs/0012-codebase-research-integration-to-role-lanes.md",
    "docs/index.md",
    "docs/agent-coordination.md",
    "docs/handoff-and-review.md",
    "docs/risk-and-safety.md",
    "docs/github-pages-public-site.md",
    "docs/architecture/system-overview.md",
    "docs/architecture/modular-boundaries.md",
    "docs/architecture/board-onboarding-flow.md",
    "docs/architecture/communication-interfaces.md",
    "docs/architecture/board-contract.md",
    "docs/architecture/protocol-contract.md",
    "docs/projects/four-relay-xbee-wifi/README.md",
    "docs/projects/four-relay-xbee-wifi/build-guide.md",
    "docs/projects/four-relay-xbee-wifi/architecture.md",
    "docs/projects/four-relay-xbee-wifi/prototype-blueprint.md",
    "docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md",
    "docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md",
    "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md",
    "docs/projects/four-relay-xbee-wifi/rd-loop.md",
    "docs/projects/four-relay-xbee-wifi/mains-readiness-gate.md",
    "docs/projects/four-relay-xbee-wifi/power-and-safety.md",
    "docs/projects/four-relay-xbee-wifi/pin-plan.md",
    "docs/projects/four-relay-xbee-wifi/firmware-task-model.md",
    "docs/projects/four-relay-xbee-wifi/web-interface.md",
    "docs/projects/four-relay-xbee-wifi/ui/index.html",
    "docs/projects/four-relay-xbee-wifi/ui/styles.css",
    "docs/projects/four-relay-xbee-wifi/ui/app.js",
    "docs/projects/four-relay-xbee-wifi/ui/manifest.json",
    "docs/projects/four-relay-xbee-wifi/ui/assets/.gitkeep",
    "docs/prompt/prompt-triage.md",
    "docs/prompt/preengineered-prompts.md",
    "docs/prompt/autoencoded-model-selection.md",
    "knowledge-base/source-index.md",
    "knowledge-base/model-profiles.md",
    "knowledge-base/prompt-registry.md",
    "knowledge-base/source-ledger/2026-05-18-four-relay-xbee-wifi-design.md",
    "knowledge-base/source-ledger/2026-05-18-esp32project-photo-analysis.md",
    "knowledge-base/source-ledger/2026-05-18-diy-bench-hardware-blockers.md",
    "knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md",
    "knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md",
    "knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md",
    "knowledge-base/toolchain/four-relay-xbee-wifi-toolchain.md",
    "research/known-gaps.md",
    "research/triage-status.md",
    "research/skills/available-skills.md",
    "hardware-profiles/device-matrix.md",
    "hardware-profiles/esp32/esp-wroom-32-dev-board/README.md",
    "hardware-profiles/esp32/devkitc/README.md",
    "hardware-profiles/storage/spi-microsd-reader/README.md",
    "hardware-profiles/xbee/xbp9b-dput-001/README.md",
    "hardware-profiles/xbee/waveshare-xbee-usb-adapter/README.md",
    "hardware-profiles/relays/single-channel/README.md",
    "hardware-profiles/relays/four-channel/README.md",
    "hardware-profiles/relays/eight-channel/README.md",
    "hardware-profiles/relays/sixteen-channel/README.md",
    "hardware-profiles/heltec/wifi-lora32-v2/README.md",
    "comm-protocols/wireless/xbee-api-four-relay.md",
    "firmware/interfaces/README.md",
    "firmware/boards/README.md",
    "firmware/comms/README.md",
    "firmware/projects/four-relay-xbee-wifi/README.md",
    "firmware/projects/four-relay-xbee-wifi/CMakeLists.txt",
    "firmware/projects/four-relay-xbee-wifi/main/CMakeLists.txt",
    "firmware/projects/four-relay-xbee-wifi/main/main.c",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/CMakeLists.txt",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/include/four_relay_core.h",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/src/api_contract.c",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/src/config_store.c",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/src/relay_state.c",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/src/safety_supervisor.c",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/src/storage_status.c",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/src/xbee_frame.c",
    "tests/four_relay_safe_core/run_host_tests.py",
    "tests/four_relay_safe_core/test_safe_core.c",
    "site/github-pages/index.html",
    "site/github-pages/blueprints.html",
    "site/github-pages/styles.css",
    "site/github-pages/app.js",
    "site/github-pages/site-data.json",
    "site/github-pages/404.html",
    "site/github-pages/.nojekyll",
    "site/github-pages/assets/blueprints/system-overview.webp",
    "site/github-pages/assets/blueprints/safety-proof-ladder.webp",
    "site/github-pages/assets/workbench/hero-workbench.webp",
    "site/github-pages/assets/workbench/rd-loop-backplate.webp",
    "site/github-pages/assets/workbench/admin-hmi-backplate.webp",
    "scripts/build_github_pages.py",
    "scripts/audit_public_manifest.py",
    "scripts/xbee_read_only_probe.py",
    ".github/workflows/README.md",
    ".github/workflows/pages.yml",
]

PROHIBITED_FRAMEWORK_FILES = [
    "CMakeLists.txt",
    "sdkconfig",
    "platformio.ini",
    "idf_component.yml",
    "arduino-cli.yaml",
]

ALLOWED_PROJECT_FRAMEWORK_FILES = {
    "firmware/projects/four-relay-xbee-wifi/CMakeLists.txt",
    "firmware/projects/four-relay-xbee-wifi/main/CMakeLists.txt",
    "firmware/projects/four-relay-xbee-wifi/components/safe_core/CMakeLists.txt",
}

FIRMWARE_SOURCE_SCAN_ROOT = ROOT / "firmware" / "projects" / "four-relay-xbee-wifi"
FORBIDDEN_FIRMWARE_MARKERS = [
    "gpio_set_level",
    "gpio_config",
    "uart_write_bytes",
    "i2c_master_write",
    "esp_wifi_start",
    "httpd_start",
    "esp_vfs_fat",
    "esp_partition_erase",
    "idf.py flash",
    "idf.py monitor",
]

PROJECT_FACT_PATHS = [
    "docs/projects/four-relay-xbee-wifi/README.md",
    "docs/projects/four-relay-xbee-wifi/build-guide.md",
    "docs/projects/four-relay-xbee-wifi/architecture.md",
    "docs/projects/four-relay-xbee-wifi/prototype-blueprint.md",
    "docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md",
    "docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md",
    "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md",
    "docs/projects/four-relay-xbee-wifi/rd-loop.md",
    "docs/projects/four-relay-xbee-wifi/mains-readiness-gate.md",
    "docs/projects/four-relay-xbee-wifi/power-and-safety.md",
    "docs/projects/four-relay-xbee-wifi/pin-plan.md",
    "docs/projects/four-relay-xbee-wifi/firmware-task-model.md",
    "docs/projects/four-relay-xbee-wifi/web-interface.md",
    "docs/github-pages-public-site.md",
    "knowledge-base/source-ledger/2026-05-18-four-relay-xbee-wifi-design.md",
    "knowledge-base/source-ledger/2026-05-18-esp32project-photo-analysis.md",
    "knowledge-base/source-ledger/2026-05-18-diy-bench-hardware-blockers.md",
    "knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md",
    "knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md",
    "knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md",
    "knowledge-base/toolchain/four-relay-xbee-wifi-toolchain.md",
    "firmware/projects/four-relay-xbee-wifi/README.md",
    "hardware-profiles/device-matrix.md",
    "hardware-profiles/esp32/esp-wroom-32-dev-board/README.md",
    "hardware-profiles/esp32/devkitc/README.md",
    "hardware-profiles/storage/spi-microsd-reader/README.md",
    "hardware-profiles/relays/four-channel/README.md",
    "hardware-profiles/xbee/xbp9b-dput-001/README.md",
    "hardware-profiles/xbee/waveshare-xbee-usb-adapter/README.md",
    "comm-protocols/wireless/xbee-api-four-relay.md",
]

PHOTO_LEDGER_PATH = "knowledge-base/source-ledger/2026-05-18-esp32project-photo-analysis.md"

PHOTO_FILENAMES = [
    "IMG_5678.jpeg",
    "IMG_5679.jpeg",
    "IMG_5680.jpeg",
    "IMG_5681.jpeg",
    "IMG_5682.jpeg",
    "IMG_5683.jpeg",
    "IMG_5684.jpeg",
    "IMG_5685.jpeg",
    "IMG_5686.jpeg",
    "IMG_5687.jpeg",
]

SOURCE_ID_PATTERN = re.compile(r"\bSRC-[A-Z0-9-]+\b")

ALLOWED_IMAGE_BINARY_PATHS = {
    "site/github-pages/assets/blueprints/system-overview.webp",
    "site/github-pages/assets/blueprints/safety-proof-ladder.webp",
    "site/github-pages/assets/workbench/hero-workbench.webp",
    "site/github-pages/assets/workbench/rd-loop-backplate.webp",
    "site/github-pages/assets/workbench/admin-hmi-backplate.webp",
    "build/github-pages/assets/blueprints/system-overview.webp",
    "build/github-pages/assets/blueprints/safety-proof-ladder.webp",
    "build/github-pages/assets/workbench/hero-workbench.webp",
    "build/github-pages/assets/workbench/rd-loop-backplate.webp",
    "build/github-pages/assets/workbench/admin-hmi-backplate.webp",
}

GENERATED_QA_IMAGE_PREFIXES = (
    "build/qa-screenshots/",
)


def main() -> int:
    failures = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            failures.append(f"missing required path: {rel}")

    for candidate in ROOT.rglob("*"):
        if ".git" in candidate.parts:
            continue
        if not candidate.is_file():
            continue
        rel = candidate.relative_to(ROOT).as_posix()
        if (
            candidate.name in PROHIBITED_FRAMEWORK_FILES
            or candidate.name.startswith("sdkconfig")
        ) and rel not in ALLOWED_PROJECT_FRAMEWORK_FILES:
            failures.append(
                "framework file present before implementation gate: "
                f"{rel}"
            )
        if candidate.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            if rel.startswith(GENERATED_QA_IMAGE_PREFIXES):
                continue
            if not rel.startswith("user_uploads/") and rel not in ALLOWED_IMAGE_BINARY_PATHS:
                failures.append(f"image binary present in source path: {rel}")

    source_index = (ROOT / "knowledge-base/source-index.md").read_text(encoding="utf-8")
    source_ids = set(SOURCE_ID_PATTERN.findall(source_index))
    for source_id in [
        "SRC-OPENAI-LATEST-MODEL",
        "SRC-GITHUB-PAGES-WHAT-IS",
        "SRC-GITHUB-PAGES-PUBLISHING-SOURCE",
        "SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS",
        "SRC-GITHUB-PAGES-LIMITS",
        "SRC-ESP-IDF-LATEST",
        "SRC-ESP-IDF-STABLE-ESP32",
        "SRC-ESP-IDF-GET-STARTED",
        "SRC-ESP-IDF-HTTP-SERVER",
        "SRC-ESP-IDF-WIFI",
        "SRC-ESP-IDF-GPIO",
        "SRC-ESP-IDF-UART",
        "SRC-ESP-IDF-NVS",
        "SRC-ESP-IDF-FATFS",
        "SRC-ESP-IDF-SDSPI",
        "SRC-ESP-IDF-SDMMC",
        "SRC-ESP-IDF-SD-PULLUP",
        "SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE",
        "SRC-ESP-IDF-SDSPI-EXAMPLE",
        "SRC-ESP-IDF-FATAL-BROWNOUT",
        "SRC-SD-ASSOCIATION-FORMATTER",
        "SRC-SD-ASSOCIATION-CAPACITY",
        "SRC-ESP32-WROOM-32-DATASHEET",
        "SRC-ESP32-HARDWARE-DESIGN-GUIDELINES",
        "SRC-ESP32-DEVKITC",
        "SRC-DIGI-XBP9B-DPUT-001",
        "SRC-DIGI-XBEE-PRO-900HP",
        "SRC-DIGI-XBEE-900HP-USER-GUIDE",
        "SRC-DIGI-XBEE-900HP-AP",
        "SRC-DIGI-XBEE-900HP-AO",
        "SRC-DIGI-XBEE-900HP-DELIVERY",
        "SRC-DIGI-XBEE-900HP-NP",
        "SRC-DIGI-XCTU",
        "SRC-LOCAL-TOOLCHAIN-PROBE-2026-05-18",
        "SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18",
        "SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18",
        "SRC-ESP32-IO-SHIELD-CANDIDATE",
        "SRC-TI-LM66100",
        "SRC-LITTELFUSE-16R-PPTC",
        "SRC-LITTELFUSE-SLVU2-8-TVS",
        "SRC-HELTEC-WIFI-LORA-32-V2",
        "SRC-WAVESHARE-XBEE-USB-ADAPTER",
        "SRC-SONGLE-SRD-05VDC-SL-C",
        "SRC-NIOSH-ELECTRICAL-SAFETY",
        "SRC-OSHA-DEENERGIZED-WORK",
        "SRC-OSHA-GFCI",
        "SRC-OSHA-AEGCP",
        "SRC-OSHA-GROUNDING-OVERCURRENT",
        "SRC-OSHA-1910-305",
        "SRC-NEMA-ENCLOSURES",
        "SRC-NEMA-250-ENCLOSURES",
        "SRC-TI-ULN2003A",
        "SRC-FLUKE-87V",
        "SRC-KEYSIGHT-E36200",
        "SRC-SALEAE-LOGIC-8",
    ]:
        if source_id not in source_index:
            failures.append(f"source index missing {source_id}")

    docs_index = (ROOT / "docs/index.md").read_text(encoding="utf-8")
    for docs_file in sorted((ROOT / "docs").rglob("*.md")):
        if docs_file.name == "index.md":
            continue
        required_link = docs_file.relative_to(ROOT / "docs").as_posix()
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
        "../research/skills/available-skills.md",
    ]:
        if required_link not in docs_index:
            failures.append(f"docs index missing cross-area link: {required_link}")

    for rel in PROJECT_FACT_PATHS:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if "SRC-" not in text:
            failures.append(f"project fact file missing source IDs: {rel}")
        missing_ids = sorted(set(SOURCE_ID_PATTERN.findall(text)) - source_ids)
        for missing_id in missing_ids:
            failures.append(f"{rel} references missing source ID: {missing_id}")
        if not any(marker in text.lower() for marker in ["unknown", "unresolved", "blocked"]):
            failures.append(f"project fact file missing unknowns/gaps section: {rel}")

    photo_ledger = (ROOT / PHOTO_LEDGER_PATH).read_text(encoding="utf-8")
    for filename in PHOTO_FILENAMES:
        if filename not in photo_ledger:
            failures.append(f"photo ledger missing filename: {filename}")
    for section in ["## Visible facts", "## Assumptions", "## Unresolved gaps"]:
        if section not in photo_ledger:
            failures.append(f"photo ledger missing evidence-boundary section: {section}")
    for marker in [
        "electrical",
        "trigger polarity",
        "input current",
        "isolation",
        "UART voltage",
    ]:
        if marker not in photo_ledger:
            failures.append(f"photo ledger missing unresolved electrical marker: {marker}")

    bench_runbook = (
        ROOT / "docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md"
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

    xbee_read_only = (
        ROOT / "docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md"
    ).read_text(encoding="utf-8")
    for marker in [
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
    ]:
        if marker not in xbee_read_only:
            failures.append(f"XBee read-only proof missing marker: {marker}")

    xbee_probe = (ROOT / "scripts/xbee_read_only_probe.py").read_text(encoding="utf-8")
    for marker in [
        "DEFAULT_AT_QUERIES",
        '"VR", "HV", "SH", "SL", "AP", "AO", "BD", "NP"',
        "confirm_sends_read_commands",
        "at_command_not_allowed",
        "serialWritesAttempted",
        "sampleRedacted",
        "research/bench-records/xbee-readonly",
    ]:
        if marker not in xbee_probe:
            failures.append(f"XBee probe script missing marker: {marker}")

    hardware_research = (
        ROOT
        / "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md"
    ).read_text(encoding="utf-8")
    for marker in [
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
    ]:
        if marker not in hardware_research:
            failures.append(f"hardware research doc missing marker: {marker}")

    rd_loop = (
        ROOT / "docs/projects/four-relay-xbee-wifi/rd-loop.md"
    ).read_text(encoding="utf-8")
    for marker in [
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
    ]:
        if marker not in rd_loop:
            failures.append(f"R&D loop doc missing marker: {marker}")

    firmware_readme = (
        ROOT / "firmware/projects/four-relay-xbee-wifi/README.md"
    ).read_text(encoding="utf-8")
    for marker in [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Hard gates",
        "No GPIO writes",
        "No expander writes",
        "No XBee setting writes",
        "No flash or monitor step",
        "No live bench mutation",
        "SRC-ESP-IDF-STABLE-ESP32",
        "SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18",
    ]:
        if marker not in firmware_readme:
            failures.append(f"firmware skeleton README missing marker: {marker}")

    core_header = (
        ROOT
        / "firmware/projects/four-relay-xbee-wifi/components/safe_core/include/four_relay_core.h"
    ).read_text(encoding="utf-8")
    for marker in [
        "FR_REJECT_HARDWARE_GATE_OPEN",
        "fr_relay_request_set",
        "fr_relay_request_set_public",
        "fr_relay_public_channel_to_index",
        "fr_safety_supervisor_accepts_change",
        "fr_config_store_default",
        "fr_http_classify_route",
        "fr_storage_status_default",
        "fr_xbee_encode_api2",
        "fr_xbee_decode_api2",
    ]:
        if marker not in core_header:
            failures.append(f"safe core header missing marker: {marker}")

    host_test_runner = (
        ROOT / "tests/four_relay_safe_core/run_host_tests.py"
    ).read_text(encoding="utf-8")
    host_test_source = (
        ROOT / "tests/four_relay_safe_core/test_safe_core.c"
    ).read_text(encoding="utf-8")
    for marker in [
        "hardware_gate_open",
        "XBee API2 encode succeeds in memory",
        "storage route classified",
        "bad checksum rejects",
        "public relay channel zero route rejects",
        "public relay channel 4 maps to internal index three",
        "XBee truncated escape rejects",
    ]:
        if marker not in host_test_source:
            failures.append(f"safe core host test missing marker: {marker}")
    for marker in ["-Werror", "test_safe_core", "safe_core"]:
        if marker not in host_test_runner:
            failures.append(f"safe core test runner missing marker: {marker}")

    for source_file in sorted(FIRMWARE_SOURCE_SCAN_ROOT.rglob("*")):
        if source_file.suffix not in {".c", ".h", ".txt"} and source_file.name != "CMakeLists.txt":
            continue
        text = source_file.read_text(encoding="utf-8")
        rel = source_file.relative_to(ROOT).as_posix()
        for forbidden in FORBIDDEN_FIRMWARE_MARKERS:
            if forbidden in text:
                failures.append(f"firmware skeleton contains forbidden marker {forbidden}: {rel}")

    prototype_blueprint = (
        ROOT / "docs/projects/four-relay-xbee-wifi/prototype-blueprint.md"
    ).read_text(encoding="utf-8")
    for marker in [
        "GPIO25/GPIO26/GPIO27/GPIO33",
        "relay input header only after 3.3 V/current gate",
        "Mains wiring: hard blocked",
        "future driver-stage",
    ]:
        if marker not in prototype_blueprint:
            failures.append(f"prototype blueprint missing marker: {marker}")

    build_guide = (
        ROOT / "docs/projects/four-relay-xbee-wifi/build-guide.md"
    ).read_text(encoding="utf-8")
    for marker in [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "Output A",
        "GPIO25",
        "Low-voltage construction order",
        "Qualified load review",
        "Stop if any step requires mains wiring",
    ]:
        if marker not in build_guide:
            failures.append(f"build guide missing marker: {marker}")

    mains_gate = (
        ROOT / "docs/projects/four-relay-xbee-wifi/mains-readiness-gate.md"
    ).read_text(encoding="utf-8")
    for marker in [
        "No step-by-step mains wiring instructions.",
        "Qualified review",
        "Overcurrent protection",
        "Grounding/bonding",
        "GFCI/de-energization",
        "Strain relief",
    ]:
        if marker not in mains_gate:
            failures.append(f"mains readiness gate missing marker: {marker}")

    ui_index = (ROOT / "docs/projects/four-relay-xbee-wifi/ui/index.html").read_text(
        encoding="utf-8"
    )
    ui_script = (ROOT / "docs/projects/four-relay-xbee-wifi/ui/app.js").read_text(
        encoding="utf-8"
    )
    for expected in [
        "styles.css",
        "app.js",
        "relayGrid",
        "allOffButton",
        "lockButton",
        "lock-banner",
        "Static artifact",
    ]:
        if expected not in ui_index:
            failures.append(f"UI index missing expected marker: {expected}")
    for endpoint in ["/api/state", "/api/relay/", "/api/all-off", "/api/safety-lock"]:
        if endpoint not in ui_script:
            failures.append(f"UI script missing endpoint: {endpoint}")
    for marker in [
        "Static demo mode",
        "Relay commands available only for a validated live session",
    ]:
        if marker not in ui_script:
            failures.append(f"UI script missing safety copy marker: {marker}")

    pages_workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    for marker in [
        "actions/checkout@v6",
        "actions/configure-pages@v5",
        "actions/upload-pages-artifact@v4",
        "actions/deploy-pages@v4",
        "build/github-pages",
    ]:
        if marker not in pages_workflow:
            failures.append(f"Pages workflow missing marker: {marker}")

    pages_build = (ROOT / "scripts/build_github_pages.py").read_text(encoding="utf-8")
    manifest_audit = (ROOT / "scripts/audit_public_manifest.py").read_text(
        encoding="utf-8"
    )
    for blocked_marker in [
        ".agents/",
        "user_uploads/",
        "vendor PDFs",
        "bulky binaries",
        "PRIVATE_BENCH_NOTES",
    ]:
        if blocked_marker == "PRIVATE_BENCH_NOTES":
            if "private bench notes" not in pages_build:
                failures.append("Pages build script missing private bench notes exclusion")
            continue
        if blocked_marker not in pages_build:
            failures.append(f"Pages build script missing exclusion marker: {blocked_marker}")
    for public_marker in [
        "blueprints.html",
        "assets/blueprints/system-overview.webp",
        "assets/blueprints/safety-proof-ladder.webp",
        "assets/workbench/hero-workbench.webp",
        "assets/workbench/rd-loop-backplate.webp",
        "assets/workbench/admin-hmi-backplate.webp",
        "docs/projects/four-relay-xbee-wifi/build-guide.md",
        "docs/projects/four-relay-xbee-wifi/README.md",
        "docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md",
        "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md",
        "docs/projects/four-relay-xbee-wifi/rd-loop.md",
        "hardware-profiles/relays/four-channel/README.md",
        "hardware-profiles/xbee/xbp9b-dput-001/README.md",
        "hardware-profiles/storage/spi-microsd-reader/README.md",
        "comm-protocols/wireless/xbee-api-four-relay.md",
        "knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md",
        "knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md",
    ]:
        if public_marker not in pages_build:
            failures.append(f"Pages build script missing public allowlist marker: {public_marker}")
        if public_marker.endswith(".webp") and public_marker not in manifest_audit:
            failures.append(f"manifest audit missing image allowlist marker: {public_marker}")
    for marker in [
        "public-file-manifest.json",
        "research/bench-records/",
        "user_uploads",
        ".agents",
        "ALLOWED_IMAGE_SOURCES",
    ]:
        if marker not in manifest_audit:
            failures.append(f"manifest audit helper missing marker: {marker}")

    pages_index = (ROOT / "site/github-pages/index.html").read_text(encoding="utf-8")
    for marker in [
        "ESP32 four-relay workbench",
        "Open visual blueprint",
        "blueprints.html",
        "Open R&amp;D loop",
        "Launch admin HMI demo",
        "Relay Labels",
        "Generated artifact only",
        "Hardware and circuit research",
        "Qualified review gate stays closed",
    ]:
        if marker not in pages_index:
            failures.append(f"Pages index missing marker: {marker}")

    pages_blueprints = (ROOT / "site/github-pages/blueprints.html").read_text(
        encoding="utf-8"
    )
    for marker in [
        "Conceptual system map, not wiring instructions",
        "system-overview.webp",
        "safety-proof-ladder.webp",
        "rd-loop-backplate.webp",
        "Conceptual schematic, not a wiring diagram",
        "Relay/load wiring",
        "mains wiring",
        "TFT wiring",
        "expander-to-relay wiring remain",
        "pinouts",
        "serial IDs",
        "MicroSD assets/logs",
        "GPIO",
        "Expander",
        "Hardware gate",
    ]:
        if marker not in pages_blueprints:
            failures.append(f"Pages blueprints missing marker: {marker}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: ESP32 scaffold validation succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
