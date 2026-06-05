from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import scaffold_audit_react_native as rn_audit  # noqa: E402
import scaffold_audit_pages as pages_audit  # noqa: E402
import verify_scaffold  # noqa: E402


class ScaffoldAuditReportingTests(unittest.TestCase):
    def test_rnw_generated_output_groups_are_summarized(self) -> None:
        groups = rn_audit.summarize_forbidden_output_groups(
            [
                Path("CbbsClientWindows/obj"),
                Path("CbbsClientWindows/obj/project.assets.json"),
                Path("CbbsClientWindows/x64/Debug"),
                Path("CbbsClientWindows/x64/Debug/app.exe"),
                Path("CbbsClientWindows.Package/bin/x64/Debug/app.exe"),
            ]
        )

        self.assertEqual(
            [
                (Path("CbbsClientWindows.Package/bin"), 1),
                (Path("CbbsClientWindows/obj"), 2),
                (Path("CbbsClientWindows/x64/Debug"), 2),
            ],
            groups,
        )

    def test_verify_scaffold_reports_groups_before_details(self) -> None:
        lines = verify_scaffold.format_audit_groups(
            [
                ("react_native", ["rnw failure"]),
                ("skills", ["skill failure"]),
            ]
        )

        self.assertEqual("FAIL: ESP32 scaffold validation failed", lines[0])
        self.assertEqual("FAIL-GROUP: react_native (1 failures)", lines[1])
        self.assertEqual("FAIL-GROUP: skills (1 failures)", lines[2])
        self.assertLess(
            lines.index("FAIL-GROUP: skills (1 failures)"),
            lines.index("FAIL-GROUP-DETAILS: react_native"),
        )
        self.assertIn("FAIL: [react_native] rnw failure", lines)
        self.assertIn("FAIL: [skills] skill failure", lines)

    def test_pages_workflow_preserves_hidden_nojekyll(self) -> None:
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("actions/upload-pages-artifact@v4", workflow)
        self.assertIn("include-hidden-files: true", workflow)
        self.assertEqual([], pages_audit.audit_pages_build(ROOT))


if __name__ == "__main__":
    unittest.main()
