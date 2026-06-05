#!/usr/bin/env python3
"""Audit durable records for new non-trivial ESP32 work."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from scaffold_audit_data import ROOT, SOURCE_ID_PATTERN


TASK_RE = re.compile(r"^(?P<id>\d{4})-(?P<slug>.+)\.md$")
DEFAULT_MIN_TASK_ID = 144


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _source_ids(root: Path) -> set[str]:
    return set(SOURCE_ID_PATTERN.findall(_read(root / "knowledge-base" / "source-index.md")))


def _task_records(root: Path, min_task_id: int) -> list[Path]:
    records: list[Path] = []
    for path in sorted((root / ".agents" / "TASK_LOG").glob("*.md")):
        match = TASK_RE.match(path.name)
        if not match:
            continue
        if int(match.group("id")) >= min_task_id:
            records.append(path)
    return records


def _task_id_collisions(root: Path) -> list[str]:
    by_id: dict[str, list[Path]] = {}
    for path in sorted((root / ".agents" / "TASK_LOG").glob("*.md")):
        match = TASK_RE.match(path.name)
        if not match:
            continue
        by_id.setdefault(match.group("id"), []).append(path)
    failures: list[str] = []
    for task_id, paths in sorted(by_id.items()):
        if len(paths) <= 1:
            continue
        rels = ", ".join(path.relative_to(root).as_posix() for path in paths)
        failures.append(f"duplicate task ID {task_id}: {rels}")
    return failures


def _audit_report_only_record(root: Path, path: Path, text: str) -> list[str]:
    header = text.split("## Routing", 1)[0].lower()
    is_report_only = "report-only" in header or ("research loop" in header and "backlog" in header)
    if not is_report_only:
        return []
    failures: list[str] = []
    rel = path.relative_to(root).as_posix()
    if "Handoff: none" not in text and "No handoff" not in text:
        failures.append(f"{rel} report-only record must explicitly use no handoff")
    if not re.search(r"\bmutation boundary\b[^.\n]*(task[- ]log )?record only", text, re.IGNORECASE):
        failures.append(f"{rel} report-only record must limit mutation boundary to the record only")
    if not re.search(r"\bdoes not (accept|authorize|claim)\b|\bnot claimed\b", text, re.IGNORECASE):
        failures.append(f"{rel} report-only record must explicitly avoid implementation or scaffold-clean claims")
    return failures


def _handoff_references(root: Path, task_id: str, slug: str) -> bool:
    needle_id = task_id.lstrip("0") or task_id
    for path in sorted((root / ".agents" / "handoffs").glob("*.md")):
        text = _read(path)
        if task_id in text or f"Task {needle_id}" in text or slug in text:
            return True
    return False


def audit_task_record(root: Path, path: Path, known_source_ids: set[str]) -> list[str]:
    failures: list[str] = []
    rel = path.relative_to(root).as_posix()
    match = TASK_RE.match(path.name)
    if not match:
        return [f"invalid task record name: {rel}"]
    task_id = match.group("id")
    slug = match.group("slug")
    text = _read(path)
    required_markers = {
        "selected tier": r"\bSelected tier\b|\bTier\s*[0-3]\b",
        "owner role": r"\bOwner role\b",
        "evidence need": r"\bEvidence need\b",
        "mutation boundary": r"\bMutation boundary\b",
        "unknowns": r"\bUnknowns?\b|\bOpen Evidence\b|\bunresolved gaps?\b",
        "validation": r"\bValidation\b",
        "authority limits": r"\bAuthority Limits\b|\bClosed Surfaces\b|\bauthority limits\b",
        "decision": r"\bDecision\b",
    }
    for label, pattern in required_markers.items():
        if not re.search(pattern, text, re.IGNORECASE):
            failures.append(f"{rel} missing durable-record marker: {label}")

    referenced_ids = set(SOURCE_ID_PATTERN.findall(text))
    if not referenced_ids and not re.search(r"\bunresolved gap\b|\bsource-ledger\b|\bsource ledger\b", text, re.IGNORECASE):
        failures.append(f"{rel} missing source ID, source ledger, or unresolved-gap note")
    for source_id in sorted(referenced_ids - known_source_ids):
        failures.append(f"{rel} references missing source ID: {source_id}")

    failures.extend(_audit_report_only_record(root, path, text))

    if "Handoff: none" not in text and "No handoff" not in text:
        if not _handoff_references(root, task_id, slug):
            failures.append(f"{rel} has no matching handoff record or explicit no-handoff note")
    return failures


def audit_records(root: Path = ROOT, min_task_id: int = DEFAULT_MIN_TASK_ID) -> list[str]:
    failures: list[str] = []
    known_source_ids = _source_ids(root)
    failures.extend(_task_id_collisions(root))
    for path in _task_records(root, min_task_id):
        failures.extend(audit_task_record(root, path, known_source_ids))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-task-id", type=int, default=DEFAULT_MIN_TASK_ID)
    args = parser.parse_args()
    failures = audit_records(min_task_id=args.min_task_id)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: ESP32 durable-record audit succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
