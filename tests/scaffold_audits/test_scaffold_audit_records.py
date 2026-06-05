from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import scaffold_audit_records as records_audit  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


VALID_RECORD = """# Task 0171: Valid Record

Status: complete

Source IDs:
`SRC-LOCAL-TEST-2026-06-05`

## Routing

- Selected tier: Tier 2.
- Owner role: Tooling.
- Evidence need: focused tests.
- Mutation boundary: test fixture.
- Unknowns: none.

## Validation

PASS: focused fixture.

## Authority Limits

No Tier 3.

## Handoff

No handoff is required.

## Decision

Decision: complete.
"""


class ScaffoldAuditRecordsTests(unittest.TestCase):
    def test_duplicate_numeric_task_ids_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "knowledge-base/source-index.md", "| SRC-LOCAL-TEST-2026-06-05 |\n")
            _write(root / ".agents/TASK_LOG/0171-alpha.md", VALID_RECORD)
            _write(root / ".agents/TASK_LOG/0171-beta.md", VALID_RECORD)

            failures = records_audit.audit_records(root, min_task_id=171)

        self.assertTrue(any("duplicate task ID 0171" in failure for failure in failures))

    def test_valid_report_only_record_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "knowledge-base/source-index.md", "| SRC-LOCAL-TEST-2026-06-05 |\n")
            _write(
                root / ".agents/TASK_LOG/0171-report.md",
                VALID_RECORD.replace("Status: complete", "Status: report-only complete")
                .replace("Mutation boundary: test fixture.", "Mutation boundary: this task record only.")
                .replace("Decision: complete.", "Decision: complete. This does not accept implementation."),
            )

            failures = records_audit.audit_records(root, min_task_id=171)

        self.assertEqual([], failures)

    def test_report_only_record_without_boundary_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "knowledge-base/source-index.md", "| SRC-LOCAL-TEST-2026-06-05 |\n")
            _write(
                root / ".agents/TASK_LOG/0171-report.md",
                VALID_RECORD.replace("Status: complete", "Status: report-only complete")
                .replace("Decision: complete.", "Decision: complete. This does not accept implementation."),
            )

            failures = records_audit.audit_records(root, min_task_id=171)

        self.assertTrue(any("report-only record must limit mutation boundary" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
