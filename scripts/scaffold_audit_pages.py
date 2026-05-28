#!/usr/bin/env python3
"""Public Pages and admin-HMI scaffold audits."""

from __future__ import annotations

from pathlib import Path

from scaffold_audit_data import ROOT
from scaffold_audit_docs import require_markers


def audit_admin_hmi(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    ui_index = (root / "docs/projects/four-relay-xbee-wifi/ui/index.html").read_text(
        encoding="utf-8"
    )
    ui_script = (root / "docs/projects/four-relay-xbee-wifi/ui/app.js").read_text(
        encoding="utf-8"
    )
    failures.extend(require_markers(ui_index, [
        "styles.css",
        "app.js",
        "relayGrid",
        "allOffButton",
        "lockButton",
        "lock-banner",
        "Static artifact",
        "Static non-operational demo",
    ], "UI index"))
    for endpoint in [
        "/api/state",
        "/api/relay/",
        "/api/all-off",
        "/api/safety-lock",
        "/api/storage/status",
        "/api/assets/manifest",
        "/api/logs/recent",
    ]:
        if endpoint not in ui_script:
            failures.append(f"UI script missing endpoint: {endpoint}")
    failures.extend(require_markers(ui_script, [
        "Static demo mode",
        "Relay commands available only for a validated live session",
    ], "UI script"))
    return failures


def audit_pages_build(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    pages_workflow = (root / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    failures.extend(require_markers(pages_workflow, [
        "actions/checkout@v6",
        "actions/configure-pages@v5",
        "actions/upload-pages-artifact@v4",
        "actions/deploy-pages@v4",
        "Check JSON and JavaScript syntax",
        "build/github-pages",
        "Audit public artifact",
        "Run host-side contract tests",
    ], "Pages workflow"))

    pages_build = (root / "scripts/build_github_pages.py").read_text(encoding="utf-8")
    manifest_audit = (root / "scripts/audit_public_manifest.py").read_text(
        encoding="utf-8"
    )
    smoke_script = (root / "scripts/smoke_github_pages.py").read_text(
        encoding="utf-8"
    )
    for blocked_marker in [
        ".agents/",
        "user_uploads/",
        "vendor PDFs",
        "bulky binaries",
        "internal evidence workbooks",
        "CAD source and generated CAD/print artifacts",
        "PRIVATE_BENCH_RECORDS",
    ]:
        if blocked_marker == "PRIVATE_BENCH_RECORDS":
            if "private bench records" not in pages_build:
                failures.append("Pages build script missing private bench records exclusion")
            continue
        if blocked_marker not in pages_build:
            failures.append(f"Pages build script missing exclusion marker: {blocked_marker}")
    for public_marker in [
        "blueprints.html",
        "prototype.html",
        "quality.html",
        "assets/blueprints/system-overview.webp",
        "assets/blueprints/safety-proof-ladder.webp",
        "assets/blueprints/prototype-evidence-map.webp",
        "assets/blueprints/low-voltage-review-sequence.webp",
        "assets/blueprints/pin-pressure-map.webp",
        "assets/workbench/hero-workbench.webp",
        "assets/workbench/rd-loop-backplate.webp",
        "assets/workbench/admin-hmi-backplate.webp",
        "docs/projects/four-relay-xbee-wifi/build-guide.md",
        "docs/projects/four-relay-xbee-wifi/README.md",
        "docs/projects/four-relay-xbee-wifi/prototype-build-packet.md",
        "docs/projects/four-relay-xbee-wifi/xbee-public-boundary.md",
        "docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md",
        "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md",
        "docs/projects/four-relay-xbee-wifi/rd-loop.md",
        "docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md",
        "hardware-profiles/relays/four-channel/README.md",
        "hardware-profiles/xbee/xbp9b-dput-001/README.md",
        "hardware-profiles/storage/spi-microsd-reader/README.md",
        "knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md",
        "knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md",
        "knowledge-base/source-ledger/2026-05-21-blueprint-schematic-improvement.md",
    ]:
        if public_marker not in pages_build:
            failures.append(f"Pages build script missing public allowlist marker: {public_marker}")
        if public_marker.endswith(".webp") and public_marker not in manifest_audit:
            failures.append(f"manifest audit missing image allowlist marker: {public_marker}")
    for marker in [
        "public-file-manifest.json",
        "research/bench-records/",
        "research/hardware-rapid-prototyping/",
        "cad/hardware-rapid-prototyping/",
        "user_uploads",
        ".agents",
        "ALLOWED_IMAGE_SOURCES",
        "audit_links_and_assets",
        "audit_public_text",
        "audit_public_source_ids",
        "SOURCE_ID_PATTERN",
        "webp_dimensions",
        "sha256 mismatch",
    ]:
        if marker not in manifest_audit:
            failures.append(f"manifest audit helper missing marker: {marker}")
    for marker in [
        "index.html",
        "prototype.html",
        "blueprints.html",
        "quality.html",
        "demos/admin-hmi/index.html",
        "smoke_page",
        "resolve_local_reference",
    ]:
        if marker not in smoke_script:
            failures.append(f"Pages smoke script missing marker: {marker}")
    return failures


def audit_site_pages(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    pages_index = (root / "site/github-pages/index.html").read_text(encoding="utf-8")
    failures.extend(require_markers(pages_index, [
        "ESP32 four-relay workbench",
        "Open Prototype Build Packet",
        "Open visual blueprint",
        "prototype.html",
        "blueprints.html",
        "quality.html",
        "Open quality evidence",
        "Expert review panels",
        "Page changes move through evidence lanes",
        "Open R&amp;D loop",
        "Launch admin HMI demo",
        "Relay Labels",
        "Current status",
        "Quality gates",
        "What the public artifact checks",
        "Candidate GPIO25",
        "Hardware and circuit research",
        "Qualified review gate stays closed",
    ], "Pages index"))

    pages_prototype = (root / "site/github-pages/prototype.html").read_text(
        encoding="utf-8"
    )
    failures.extend(require_markers(pages_prototype, [
        "Prototype Build Packet",
        "No blockers means findability",
        "prototype-evidence-map.webp",
        "low-voltage-review-sequence.webp",
        "pin-pressure-map.webp",
        "bundle/docs/projects/four-relay-xbee-wifi/prototype-build-packet.md",
        "bundle/docs/projects/four-relay-xbee-wifi/xbee-public-boundary.md",
        "Generated label-free backplate",
        "It is not a wiring",
        "qualified review only",
        "does not approve final wiring",
        "Public Markdown content",
    ], "Pages prototype"))

    pages_blueprints = (root / "site/github-pages/blueprints.html").read_text(
        encoding="utf-8"
    )
    failures.extend(require_markers(pages_blueprints, [
        "Conceptual system map, not wiring instructions",
        "system-overview.webp",
        "safety-proof-ladder.webp",
        "Safety evidence ladder",
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
    ], "Pages blueprints"))

    pages_quality = (root / "site/github-pages/quality.html").read_text(
        encoding="utf-8"
    )
    failures.extend(require_markers(pages_quality, [
        "What this public artifact checks",
        "Generated artifact policy",
        "Manifest, link, content, and hash audit",
        "Page smoke checks",
        "Host software contract tests",
        "not electrical safety testing",
        "Expert panel method",
        "How public-page changes are improved",
        "XBee read-only boundary",
        "Explicit non-coverage",
        "public-file-manifest.json",
        "scripts/audit_public_manifest.py",
        "public Markdown",
        "WebP decode",
        "scripts/smoke_github_pages.py",
        "does not validate live ESP32 wiring",
        "Private evidence stays private",
    ], "Pages quality"))
    return failures


def audit_pages(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(audit_admin_hmi(root))
    failures.extend(audit_pages_build(root))
    failures.extend(audit_site_pages(root))
    return failures
