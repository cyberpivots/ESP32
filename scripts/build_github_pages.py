#!/usr/bin/env python3
"""Build the curated static GitHub Pages artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_SOURCE = ROOT / "site" / "github-pages"
DEFAULT_OUTPUT = ROOT / "build" / "github-pages"

SITE_FILES = [
    "index.html",
    "blueprints.html",
    "quality.html",
    "styles.css",
    "app.js",
    "site-data.json",
    "404.html",
    ".nojekyll",
]

SITE_ASSET_FILES = [
    "assets/blueprints/system-overview.webp",
    "assets/blueprints/safety-proof-ladder.webp",
    "assets/workbench/hero-workbench.webp",
    "assets/workbench/rd-loop-backplate.webp",
    "assets/workbench/admin-hmi-backplate.webp",
]

PUBLIC_BUNDLE_FILES = [
    ("README.md", "workspace"),
    ("docs/github-pages-public-site.md", "site-policy"),
    ("docs/architecture/system-overview.md", "architecture"),
    ("docs/architecture/modular-boundaries.md", "architecture"),
    ("docs/architecture/communication-interfaces.md", "architecture"),
    ("docs/architecture/board-contract.md", "architecture"),
    ("docs/architecture/protocol-contract.md", "architecture"),
    ("docs/projects/four-relay-xbee-wifi/README.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/build-guide.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/architecture.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/prototype-blueprint.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md", "four-relay"),
    (
        "docs/projects/four-relay-xbee-wifi/hardware-circuit-improvement-research.md",
        "four-relay",
    ),
    ("docs/projects/four-relay-xbee-wifi/rd-loop.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/power-and-safety.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/mains-readiness-gate.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/pin-plan.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/tft-relay-expansion.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/web-interface.md", "four-relay"),
    ("docs/projects/four-relay-xbee-wifi/firmware-task-model.md", "four-relay"),
    ("hardware-profiles/device-matrix.md", "hardware-profile"),
    (
        "hardware-profiles/esp32/esp-wroom-32-dev-board/README.md",
        "hardware-profile",
    ),
    ("hardware-profiles/esp32/devkitc/README.md", "hardware-profile"),
    ("hardware-profiles/displays/open-smart-r61509v/README.md", "hardware-profile"),
    (
        "hardware-profiles/interface-expansion/cd74hc4067/README.md",
        "hardware-profile",
    ),
    (
        "hardware-profiles/interface-expansion/tca9555-mcp23017/README.md",
        "hardware-profile",
    ),
    (
        "hardware-profiles/interface-expansion/tpic6b595/README.md",
        "hardware-profile",
    ),
    ("hardware-profiles/relays/four-channel/README.md", "hardware-profile"),
    ("hardware-profiles/xbee/xbp9b-dput-001/README.md", "hardware-profile"),
    (
        "hardware-profiles/xbee/waveshare-xbee-usb-adapter/README.md",
        "hardware-profile",
    ),
    ("hardware-profiles/storage/spi-microsd-reader/README.md", "hardware-profile"),
    ("comm-protocols/wireless/xbee-api-four-relay.md", "protocol"),
    ("knowledge-base/source-index.md", "source-index"),
    (
        "knowledge-base/source-ledger/2026-05-18-four-relay-xbee-wifi-design.md",
        "source-ledger",
    ),
    (
        "knowledge-base/source-ledger/2026-05-18-diy-bench-hardware-blockers.md",
        "source-ledger",
    ),
    (
        "knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md",
        "source-ledger",
    ),
    (
        "knowledge-base/source-ledger/2026-05-18-tft-relay-expansion.md",
        "source-ledger",
    ),
    (
        "knowledge-base/source-ledger/2026-05-18-xbee-read-only-bench-proof.md",
        "source-ledger",
    ),
    (
        "knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md",
        "source-ledger",
    ),
]

ADMIN_HMI_FILES = [
    "index.html",
    "styles.css",
    "app.js",
    "manifest.json",
]

ALLOWED_SUFFIXES = {".css", ".html", ".js", ".json", ".md"}
ALLOWED_PUBLIC_IMAGE_ASSETS = {
    f"site/github-pages/{rel}" for rel in SITE_ASSET_FILES
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output directory for the generated Pages artifact.",
    )
    return parser.parse_args()


def relative_to_root(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_safe_source(path: Path) -> None:
    resolved = path.resolve()
    if ROOT not in resolved.parents and resolved != ROOT:
        raise ValueError(f"source escapes repository root: {path}")
    rel = relative_to_root(path)
    if any(part in {".git", "user_uploads", ".agents"} for part in path.parts):
        raise ValueError(f"blocked private or bulky source path: {rel}")
    if path.name != ".nojekyll" and path.suffix.lower() not in ALLOWED_SUFFIXES:
        if rel in ALLOWED_PUBLIC_IMAGE_ASSETS:
            return
        raise ValueError(f"blocked file type for public artifact: {rel}")


def copy_file(source: Path, destination: Path, artifact_root: Path) -> dict[str, object]:
    if not source.exists():
        raise FileNotFoundError(relative_to_root(source))
    if not source.is_file():
        raise ValueError(f"not a file: {relative_to_root(source)}")
    assert_safe_source(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return {
        "source": relative_to_root(source),
        "path": destination.relative_to(artifact_root).as_posix(),
        "bytes": destination.stat().st_size,
        "sha256": digest(destination),
    }


def clean_output(out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)


def assert_safe_output(out_dir: Path) -> None:
    build_root = (ROOT / "build").resolve()
    if out_dir != build_root and build_root not in out_dir.parents:
        raise ValueError("--out must resolve inside the repository build/ directory")


def build(out_dir: Path) -> dict[str, object]:
    out_dir = out_dir.resolve()
    assert_safe_output(out_dir)
    clean_output(out_dir)

    manifest_files: list[dict[str, object]] = []

    for rel in SITE_FILES:
        source = SITE_SOURCE / rel
        record = copy_file(source, out_dir / rel, out_dir)
        record["category"] = "site"
        manifest_files.append(record)

    for rel in SITE_ASSET_FILES:
        source = SITE_SOURCE / rel
        record = copy_file(source, out_dir / rel, out_dir)
        record["category"] = "site-blueprint-asset"
        manifest_files.append(record)

    for rel, category in PUBLIC_BUNDLE_FILES:
        source = ROOT / rel
        record = copy_file(source, out_dir / "bundle" / rel, out_dir)
        record["category"] = category
        manifest_files.append(record)

    admin_source = ROOT / "docs" / "projects" / "four-relay-xbee-wifi" / "ui"
    for rel in ADMIN_HMI_FILES:
        source = admin_source / rel
        record = copy_file(source, out_dir / "demos" / "admin-hmi" / rel, out_dir)
        record["category"] = "admin-hmi-demo"
        manifest_files.append(record)

    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generator": "scripts/build_github_pages.py",
        "policy": {
            "allowlistOnly": True,
            "excludes": [
                ".agents/",
                "user_uploads/",
                "raw photos",
                "generated screenshots except allowlisted technical backplates",
                "vendor PDFs",
                "bulky binaries",
                "private bench notes",
                "image binaries except named site/github-pages/assets/**/*.webp",
            ],
        },
        "files": sorted(manifest_files, key=lambda item: str(item["path"])),
    }

    manifest_path = out_dir / "public-file-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {out_dir} with {len(manifest_files)} public files")
    return manifest


def main() -> int:
    args = parse_args()
    build(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
