#!/usr/bin/env python3
"""Audit the generated GitHub Pages public-file manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "build" / "github-pages" / "public-file-manifest.json"

BLOCKED_PATH_PARTS = {".agents", ".git", "user_uploads"}
BLOCKED_PREFIXES = ("research/bench-records/",)
BLOCKED_SUFFIXES = {".pdf"}
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}

ALLOWED_IMAGE_SOURCES = {
    "site/github-pages/assets/blueprints/system-overview.webp",
    "site/github-pages/assets/blueprints/safety-proof-ladder.webp",
    "site/github-pages/assets/workbench/hero-workbench.webp",
    "site/github-pages/assets/workbench/rd-loop-backplate.webp",
    "site/github-pages/assets/workbench/admin-hmi-backplate.webp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to build/github-pages/public-file-manifest.json.",
    )
    return parser.parse_args()


def has_blocked_path(path_text: str) -> bool:
    parts = set(path_text.split("/"))
    if parts & BLOCKED_PATH_PARTS:
        return True
    if any(path_text.startswith(prefix) for prefix in BLOCKED_PREFIXES):
        return True
    return Path(path_text).suffix.lower() in BLOCKED_SUFFIXES


def audit_manifest(manifest_path: Path) -> list[str]:
    failures: list[str] = []
    if not manifest_path.exists():
        return [f"missing manifest: {manifest_path}"]

    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    files = manifest.get("files")
    if not isinstance(files, list):
        return ["manifest missing files list"]

    seen_image_sources: set[str] = set()
    for item in files:
        if not isinstance(item, dict):
            failures.append("manifest contains non-object file entry")
            continue
        source = str(item.get("source", ""))
        artifact_path = str(item.get("path", ""))
        if not source or not artifact_path:
            failures.append(f"manifest entry missing source or path: {item!r}")
            continue

        for value, label in ((source, "source"), (artifact_path, "artifact path")):
            if has_blocked_path(value):
                failures.append(f"blocked public {label}: {value}")

        if Path(source).suffix.lower() in IMAGE_SUFFIXES:
            seen_image_sources.add(source)
            if source not in ALLOWED_IMAGE_SOURCES:
                failures.append(f"image source is not allowlisted: {source}")
        if Path(artifact_path).suffix.lower() in IMAGE_SUFFIXES and source not in ALLOWED_IMAGE_SOURCES:
            failures.append(f"image artifact is not backed by an allowed source: {artifact_path}")

    missing_images = sorted(ALLOWED_IMAGE_SOURCES - seen_image_sources)
    for source in missing_images:
        failures.append(f"allowed image missing from manifest: {source}")

    return failures


def main() -> int:
    args = parse_args()
    failures = audit_manifest(args.manifest)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(f"PASS: public manifest audit succeeded for {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
