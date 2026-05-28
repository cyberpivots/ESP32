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
BLOCKED_PREFIXES = (
    "research/bench-records/",
    "research/hardware-rapid-prototyping/",
    "cad/hardware-rapid-prototyping/",
)
BLOCKED_SUFFIXES = {
    ".3mf",
    ".gcode",
    ".gco",
    ".nc",
    ".obj",
    ".pdf",
    ".ply",
    ".scad",
    ".step",
    ".stl",
    ".stp",
}
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
URL_PATTERN = re.compile(r"url\((?:'|\")?([^'\"\)]+)(?:'|\")?\)")
SOURCE_ID_PATTERN = re.compile(r"\bSRC-[A-Z0-9-]+\b")

ALLOWED_IMAGE_SOURCES = {
    "site/github-pages/assets/blueprints/system-overview.webp",
    "site/github-pages/assets/blueprints/safety-proof-ladder.webp",
    "site/github-pages/assets/blueprints/prototype-evidence-map.webp",
    "site/github-pages/assets/blueprints/low-voltage-review-sequence.webp",
    "site/github-pages/assets/blueprints/pin-pressure-map.webp",
    "site/github-pages/assets/workbench/hero-workbench.webp",
    "site/github-pages/assets/workbench/rd-loop-backplate.webp",
    "site/github-pages/assets/workbench/admin-hmi-backplate.webp",
}

EXPECTED_IMAGE_DIMENSIONS = {
    "site/github-pages/assets/workbench/hero-workbench.webp": (1800, 1080),
    **{source: (1600, 1000) for source in ALLOWED_IMAGE_SOURCES if "hero-workbench" not in source},
}

PUBLIC_TEXT_PATTERNS = [
    (re.compile(r"/mnt/"), "local mount path"),
    (re.compile(r"/home/"), "local home path"),
    (re.compile(r"/dev/tty"), "serial device path"),
    (re.compile(r"(?<!-)\bCOM\d+\b", re.IGNORECASE), "COM port"),
    (re.compile(r"`?[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}`?"), "local device identifier"),
    (re.compile(r"user_uploads"), "private upload path"),
    (re.compile(r"research/hardware-rapid-prototyping/"), "internal workbook path"),
    (re.compile(r"cad/hardware-rapid-prototyping/"), "internal CAD path"),
    (re.compile(r"four-relay-low-voltage-fixture-kit-workbook"), "internal workbook name"),
    (re.compile(r"low_voltage_fixture_plate_v0"), "internal CAD source name"),
    (re.compile(r"IMG_\d+\.(?:jpe?g|png|webp)", re.IGNORECASE), "raw photo filename"),
    (re.compile(r"private bench notes", re.IGNORECASE), "private bench-note language"),
    (re.compile(r"\b[A-Fa-f0-9]{32,}\b"), "possible key or raw identifier"),
]


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


def collect_json_references(value: object) -> list[str]:
    references: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"href", "src", "poster"} and isinstance(child, str):
                references.append(child)
            references.extend(collect_json_references(child))
    elif isinstance(value, list):
        for child in value:
            references.extend(collect_json_references(child))
    return references


def webp_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    offset = 12
    while offset + 8 <= len(data):
        chunk_type = data[offset : offset + 4]
        chunk_size = int.from_bytes(data[offset + 4 : offset + 8], "little")
        payload = data[offset + 8 : offset + 8 + chunk_size]
        if chunk_type == b"VP8X" and len(payload) >= 10:
            width = int.from_bytes(payload[4:7], "little") + 1
            height = int.from_bytes(payload[7:10], "little") + 1
            return width, height
        if chunk_type == b"VP8 " and len(payload) >= 10 and payload[3:6] == b"\x9d\x01\x2a":
            width = int.from_bytes(payload[6:8], "little") & 0x3FFF
            height = int.from_bytes(payload[8:10], "little") & 0x3FFF
            return width, height
        if chunk_type == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2F:
            b0, b1, b2, b3 = payload[1:5]
            width = 1 + (((b1 & 0x3F) << 8) | b0)
            height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
            return width, height
        offset += 8 + chunk_size + (chunk_size % 2)
    return None


def audit_public_text(root: Path) -> list[str]:
    failures: list[str] = []
    for text_path in sorted(root.rglob("*.md")):
        text = text_path.read_text(encoding="utf-8")
        rel = text_path.relative_to(root).as_posix()
        for pattern, label in PUBLIC_TEXT_PATTERNS:
            if pattern.search(text):
                failures.append(f"public Markdown contains {label}: {rel}")
    return failures


def audit_public_source_ids(root: Path) -> list[str]:
    failures: list[str] = []
    source_index = root / "bundle" / "knowledge-base" / "source-index.md"
    if not source_index.exists():
        return ["public source index missing from generated bundle"]

    known_sources = set(SOURCE_ID_PATTERN.findall(source_index.read_text(encoding="utf-8")))
    if not known_sources:
        return ["public source index contains no SRC-* identifiers"]

    for text_path in sorted(root.rglob("*.md")):
        rel = text_path.relative_to(root).as_posix()
        if rel == "bundle/knowledge-base/source-index.md":
            continue
        text = text_path.read_text(encoding="utf-8")
        missing_sources = sorted(set(SOURCE_ID_PATTERN.findall(text)) - known_sources)
        for source_id in missing_sources:
            failures.append(f"public Markdown references missing source ID {source_id}: {rel}")
    return failures


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

    for json_path in sorted(root.rglob("*.json")):
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(f"invalid public JSON {json_path.relative_to(root).as_posix()}: {error}")
            continue
        for ref in collect_json_references(payload):
            if not local_reference(ref):
                continue
            target = resolve_local_reference(root, json_path, ref)
            if not target.exists():
                failures.append(
                    f"broken public JSON reference from {json_path.relative_to(root).as_posix()}: {ref}"
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
            elif Path(source).suffix.lower() == ".webp":
                expected_dimensions = EXPECTED_IMAGE_DIMENSIONS.get(source)
                actual_dimensions = webp_dimensions(artifact_file)
                if actual_dimensions is None:
                    failures.append(f"WebP image could not be decoded: {artifact_path}")
                elif expected_dimensions and actual_dimensions != expected_dimensions:
                    failures.append(
                        f"WebP dimensions mismatch for {artifact_path}: "
                        f"{actual_dimensions[0]}x{actual_dimensions[1]}"
                    )
        if Path(artifact_path).suffix.lower() in IMAGE_SUFFIXES and source not in ALLOWED_IMAGE_SOURCES:
            failures.append(f"image artifact is not backed by an allowed source: {artifact_path}")

    missing_images = sorted(ALLOWED_IMAGE_SOURCES - seen_image_sources)
    for source in missing_images:
        failures.append(f"allowed image missing from manifest: {source}")

    failures.extend(audit_links_and_assets(artifact_root))
    failures.extend(audit_public_text(artifact_root))
    failures.extend(audit_public_source_ids(artifact_root))
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
