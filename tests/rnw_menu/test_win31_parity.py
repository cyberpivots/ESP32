#!/usr/bin/env python3
"""Tests for the CBBS RNW Win31 parity generator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "tools" / "react-native"
DOSC_ROOT = Path("/mnt/h/dos-c")
sys.path.insert(0, str(TOOL_DIR))

from generate_win31_parity import (  # noqa: E402
    MENU_ORDER,
    PAGE_ORDER,
    PARITY_SCHEMA,
    REQUEST_NAMES,
    Win31ParityGenerationError,
    XML_PATH,
    load_contract,
)


def _load_modified_xml(modified: str, dosc_root: Path = DOSC_ROOT) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as handle:
        handle.write(modified)
        path = Path(handle.name)
    try:
        load_contract(path, dosc_root)
    finally:
        path.unlink(missing_ok=True)


class Win31ParityGeneratorTests(unittest.TestCase):
    def test_xml_source_generates_win31_parity_contract(self) -> None:
        contract = load_contract()
        self.assertEqual(contract["schema"], PARITY_SCHEMA)
        self.assertEqual(contract["visiblePlatform"], "OG Communication Retro3.1")
        self.assertEqual(contract["moduleName"], "CBBS")
        self.assertEqual([page["label"] for page in contract["pages"]], [
            "Status",
            "Messages",
            "Files",
            "Devices",
            "Help",
            "Peers",
            "Link",
            "Updates",
            "Setup",
            "Diagnostics",
            "Locks",
        ])
        self.assertEqual([menu["id"] for menu in contract["menus"]], list(MENU_ORDER))
        self.assertEqual(contract["requestNames"], list(REQUEST_NAMES))
        self.assertEqual(contract["status"], {"label": "Link wait", "counters": ["In 0", "Out 0 Err 0", "Queue 0"]})

    def test_generated_typescript_is_fresh(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL_DIR / "generate_win31_parity.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_role_coverage_is_complete(self) -> None:
        contract = load_contract()
        for role in ["client", "sysop"]:
            with self.subTest(role=role):
                rows = contract["roleCoverage"][role]  # type: ignore[index]
                self.assertEqual([row["pageId"] for row in rows], list(PAGE_ORDER))
        client_dispositions = {
            row["pageId"]: row["disposition"]
            for row in contract["roleCoverage"]["client"]  # type: ignore[index]
        }
        self.assertEqual(client_dispositions["devices"], "notRenderedRoleBoundary")
        self.assertEqual(client_dispositions["link"], "evidenceOnly")

    def test_hardware_tools_surfaces_are_mapped_to_win31_categories(self) -> None:
        contract = load_contract()
        adjacency = {
            row["pageId"]: row["adjacentTo"]
            for row in contract["hardwareAdjacency"]  # type: ignore[index]
        }
        self.assertEqual(adjacency, {
            "bench": "devices",
            "radio": "devices",
            "mesh": "link",
            "firmware": "updates",
            "fabrication": "setup",
            "safety": "locks",
            "activity": "diagnostics",
        })

    def test_source_refs_fail_closed_when_dos_c_source_is_missing(self) -> None:
        base = XML_PATH.read_text(encoding="utf-8")
        missing_source_xml = base.replace(
            'path="software/win31-operator/README.md"',
            'path="software/win31-operator/MISSING.md"',
            1,
        )
        with self.assertRaises(Win31ParityGenerationError):
            _load_modified_xml(missing_source_xml)

    def test_xml_rejections_fail_closed(self) -> None:
        base = XML_PATH.read_text(encoding="utf-8")
        cases = {
            "duplicate_page": base.replace('pageId="link"', 'pageId="peers"', 1),
            "unsafe_visible_copy": base.replace("Link wait", "Serial wait", 1),
            "unknown_request": base.replace('name="state_get"', 'name="state_missing"', 1),
            "unknown_action_request": base.replace('requestName="state_get"', 'requestName="state_missing"', 1),
            "unknown_source_ref": base.replace('sourceRef="operator-readme"', 'sourceRef="missing-source"', 1),
            "doctype": '<!DOCTYPE parity [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>' + base,
        }
        for name, xml in cases.items():
            with self.subTest(name=name), self.assertRaises(Win31ParityGenerationError):
                _load_modified_xml(xml)


if __name__ == "__main__":
    unittest.main()
