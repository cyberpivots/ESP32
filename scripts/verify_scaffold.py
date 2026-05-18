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
    ".agents/DECISIONS/ADR-0001-framework-choice.md",
    ".agents/DECISIONS/ADR-0002-four-relay-xbee-wifi-framework.md",
    ".agents/handoffs/0002-design-to-hardware-firmware-qa.md",
    ".agents/handoffs/0003-photo-analysis-to-hardware-qa.md",
    ".agents/handoffs/0004-blueprint-to-hardware-qa.md",
    ".agents/handoffs/0005-admin-hmi-to-firmware-hardware-qa.md",
    ".agents/handoffs/0006-github-pages-public-diy-site.md",
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
    "docs/projects/four-relay-xbee-wifi/architecture.md",
    "docs/projects/four-relay-xbee-wifi/prototype-blueprint.md",
    "docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md",
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
    "site/github-pages/index.html",
    "site/github-pages/styles.css",
    "site/github-pages/app.js",
    "site/github-pages/site-data.json",
    "site/github-pages/404.html",
    "site/github-pages/.nojekyll",
    "scripts/build_github_pages.py",
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

PROJECT_FACT_PATHS = [
    "docs/projects/four-relay-xbee-wifi/README.md",
    "docs/projects/four-relay-xbee-wifi/architecture.md",
    "docs/projects/four-relay-xbee-wifi/prototype-blueprint.md",
    "docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md",
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
    "knowledge-base/toolchain/four-relay-xbee-wifi-toolchain.md",
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
        if candidate.name in PROHIBITED_FRAMEWORK_FILES or candidate.name.startswith("sdkconfig"):
            failures.append(
                "framework file present before implementation gate: "
                f"{candidate.relative_to(ROOT).as_posix()}"
            )
        if candidate.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            rel = candidate.relative_to(ROOT).as_posix()
            if not rel.startswith("user_uploads/"):
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
        "SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18",
        "SRC-ESP32-IO-SHIELD-CANDIDATE",
        "SRC-HELTEC-WIFI-LORA-32-V2",
        "SRC-WAVESHARE-XBEE-USB-ADAPTER",
        "SRC-SONGLE-SRD-05VDC-SL-C",
        "SRC-NIOSH-ELECTRICAL-SAFETY",
        "SRC-OSHA-DEENERGIZED-WORK",
        "SRC-OSHA-GFCI",
        "SRC-OSHA-AEGCP",
        "SRC-OSHA-GROUNDING-OVERCURRENT",
        "SRC-NEMA-ENCLOSURES",
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
    for expected in ["styles.css", "app.js", "relayGrid", "allOffButton", "lockButton"]:
        if expected not in ui_index:
            failures.append(f"UI index missing expected marker: {expected}")
    for endpoint in ["/api/state", "/api/relay/", "/api/all-off", "/api/safety-lock"]:
        if endpoint not in ui_script:
            failures.append(f"UI script missing endpoint: {endpoint}")

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
        "docs/projects/four-relay-xbee-wifi/README.md",
        "hardware-profiles/relays/four-channel/README.md",
        "hardware-profiles/xbee/xbp9b-dput-001/README.md",
        "hardware-profiles/storage/spi-microsd-reader/README.md",
        "comm-protocols/wireless/xbee-api-four-relay.md",
    ]:
        if public_marker not in pages_build:
            failures.append(f"Pages build script missing public allowlist marker: {public_marker}")

    pages_index = (ROOT / "site/github-pages/index.html").read_text(encoding="utf-8")
    for marker in [
        "ESP32 DIY Control Prototypes",
        "Open DIY package",
        "Launch admin HMI demo",
        "Review safety gates",
        "DIY concept/prototype documentation only",
    ]:
        if marker not in pages_index:
            failures.append(f"Pages index missing marker: {marker}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: ESP32 scaffold validation succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
