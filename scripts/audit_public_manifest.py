#!/usr/bin/env python3
"""Audit the generated GitHub Pages public-file manifest."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "build" / "github-pages" / "public-file-manifest.json"

BLOCKED_PATH_PARTS = {".agents", ".git", "user_uploads"}
BLOCKED_PREFIXES = ("research/bench-records/",)
BLOCKED_SUFFIXES = {".pdf"}
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
URL_PATTERN = re.compile(r"url\((?:'|\")?([^'\"\)]+)(?:'|\")?\)")

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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            if name in {"href", "src", "poster"}:
                self.references.append(value)


def local_reference(ref: str) -> bool:
    parsed = urlsplit(ref)
    if parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
        return False
    return bool(parsed.path)


def resolve_local_reference(root: Path, base: Path, ref: str) -> Path:
    parsed = urlsplit(ref)
    if parsed.path.startswith("/"):
        target = root / parsed.path.lstrip("/")
    else:
        target = (base.parent / parsed.path).resolve()
    if target.is_dir() or parsed.path.endswith("/"):
        target = target / "index.html"
    return target


def audit_links_and_assets(root: Path) -> list[str]:
    failures: list[str] = []
    for html_path in sorted(root.rglob("*.html")):
        parser = ReferenceParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for ref in parser.references:
            if not local_reference(ref):
                continue
            target = resolve_local_reference(root, html_path, ref)
            if not target.exists():
                failures.append(
                    f"broken public reference from {html_path.relative_to(root).as_posix()}: {ref}"
                )

    for css_path in sorted(root.rglob("*.css")):
        css = css_path.read_text(encoding="utf-8")
        for ref in URL_PATTERN.findall(css):
            if not local_reference(ref):
                continue
            target = resolve_local_reference(root, css_path, ref)
            if not target.exists():
                failures.append(
                    f"broken public asset from {css_path.relative_to(root).as_posix()}: {ref}"
                )
    return failures


def audit_manifest(manifest_path: Path) -> list[str]:
    failures: list[str] = []
    if not manifest_path.exists():
        return [f"missing manifest: {manifest_path}"]

    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    files = manifest.get("files")
    if not isinstance(files, list):
        return ["manifest missing files list"]

    artifact_root = manifest_path.parent
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

        artifact_file = artifact_root / artifact_path
        if not artifact_file.exists():
            failures.append(f"manifest artifact missing on disk: {artifact_path}")
            continue
        expected_bytes = item.get("bytes")
        if isinstance(expected_bytes, int) and artifact_file.stat().st_size != expected_bytes:
            failures.append(f"byte count mismatch for public artifact: {artifact_path}")
        expected_hash = item.get("sha256")
        if isinstance(expected_hash, str) and sha256(artifact_file) != expected_hash:
            failures.append(f"sha256 mismatch for public artifact: {artifact_path}")

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

    failures.extend(audit_links_and_assets(artifact_root))
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
