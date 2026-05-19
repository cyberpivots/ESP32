#!/usr/bin/env python3
"""Smoke-check the generated GitHub Pages artifact."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "build" / "github-pages"


class SmokeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.ids: set[str] = set()
        self.classes: set[str] = set()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True
        for name, value in attrs:
            if value is None:
                continue
            if name == "id":
                self.ids.add(value)
            if name == "class":
                self.classes.update(value.split())
            if name in {"href", "src", "poster"}:
                self.references.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "artifact",
        nargs="?",
        type=Path,
        default=DEFAULT_ARTIFACT,
        help="Generated Pages artifact root.",
    )
    return parser.parse_args()


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
        target = base.parent / parsed.path
    if target.is_dir() or parsed.path.endswith("/"):
        target = target / "index.html"
    return target


def smoke_page(
    root: Path,
    rel: str,
    required_title: str,
    required_tokens: set[str],
) -> list[str]:
    failures: list[str] = []
    path = root / rel
    if not path.exists():
        return [f"missing smoke page: {rel}"]

    parser = SmokeParser()
    text = path.read_text(encoding="utf-8")
    parser.feed(text)
    if required_title not in parser.title:
        failures.append(f"{rel} title missing {required_title!r}")

    haystack = text + "\n" + "\n".join(parser.ids | parser.classes)
    for token in sorted(required_tokens):
        if token not in haystack:
            failures.append(f"{rel} missing smoke token: {token}")

    for ref in parser.references:
        if not local_reference(ref):
            continue
        target = resolve_local_reference(root, path, ref)
        if not target.exists():
            failures.append(f"{rel} broken local reference: {ref}")
    return failures


def smoke_artifact(root: Path) -> list[str]:
    failures: list[str] = []
    for rel, title, tokens in [
        (
            "index.html",
            "ESP32 Four-Relay Premium Workbench",
            {"blueprints.html", "demos/admin-hmi/", "public-file-manifest.json"},
        ),
        (
            "blueprints.html",
            "ESP32 Four-Relay Visual Blueprints",
            {"system-overview.webp", "safety-proof-ladder.webp"},
        ),
        (
            "demos/admin-hmi/index.html",
            "Four Relay Admin HMI",
            {"relayGrid", "allOffButton", "lockButton"},
        ),
    ]:
        failures.extend(smoke_page(root, rel, title, tokens))
    return failures


def main() -> int:
    args = parse_args()
    root = args.artifact.resolve()
    failures = smoke_artifact(root)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(f"PASS: GitHub Pages smoke succeeded for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
