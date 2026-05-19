#!/usr/bin/env python3
"""Source-index and hardware-claim evidence audits."""

from __future__ import annotations

from pathlib import Path

from scaffold_audit_data import (
    PHOTO_FILENAMES,
    PHOTO_LEDGER_PATH,
    PROJECT_FACT_PATHS,
    REQUIRED_SOURCE_IDS,
    ROOT,
    SOURCE_ID_PATTERN,
)


def source_ids(root: Path = ROOT) -> set[str]:
    source_index = (root / "knowledge-base/source-index.md").read_text(
        encoding="utf-8"
    )
    return set(SOURCE_ID_PATTERN.findall(source_index))


def audit_source_index(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    source_index = (root / "knowledge-base/source-index.md").read_text(
        encoding="utf-8"
    )
    for source_id in REQUIRED_SOURCE_IDS:
        if source_id not in source_index:
            failures.append(f"source index missing {source_id}")
    return failures


def audit_project_fact_sources(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    known_source_ids = source_ids(root)
    for rel in PROJECT_FACT_PATHS:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        if "SRC-" not in text:
            failures.append(f"project fact file missing source IDs: {rel}")
        missing_ids = sorted(set(SOURCE_ID_PATTERN.findall(text)) - known_source_ids)
        for missing_id in missing_ids:
            failures.append(f"{rel} references missing source ID: {missing_id}")
        if not any(marker in text.lower() for marker in ["unknown", "unresolved", "blocked"]):
            failures.append(f"project fact file missing unknowns/gaps section: {rel}")
    return failures


def audit_photo_ledger(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    photo_ledger = (root / PHOTO_LEDGER_PATH).read_text(encoding="utf-8")
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
    return failures


def audit_sources(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(audit_source_index(root))
    failures.extend(audit_project_fact_sources(root))
    failures.extend(audit_photo_ledger(root))
    return failures
