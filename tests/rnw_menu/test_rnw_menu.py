#!/usr/bin/env python3
"""Tests for the CBBS RNW product menu generator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "tools" / "react-native"
sys.path.insert(0, str(TOOL_DIR))

from generate_rnw_menu import (  # noqa: E402
    MENU_SCHEMA,
    RnwMenuGenerationError,
    XML_PATH,
    load_menu,
)


def _load_modified_xml(modified: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as handle:
        handle.write(modified)
        path = Path(handle.name)
    try:
        load_menu(path)
    finally:
        path.unlink(missing_ok=True)


class RnwMenuGeneratorTests(unittest.TestCase):
    def test_xml_source_generates_fixed_hardware_tools_pages(self) -> None:
        menu = load_menu()
        self.assertEqual(menu.schema, MENU_SCHEMA)
        self.assertEqual(menu.app_id, "hardware-tools")
        self.assertEqual([page.label for page in menu.pages], [
            "Bench",
            "Radio",
            "Mesh",
            "Firmware",
            "Fabrication",
            "Safety",
            "Activity",
        ])
        self.assertEqual(menu.pages[1].sections[0].items[0].action_id, "hardware.radioInventory")
        self.assertEqual(menu.pages[3].sections[0].items[0].label, "Build Review")

    def test_generated_typescript_is_fresh(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL_DIR / "generate_rnw_menu.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_actions_are_page_scoped(self) -> None:
        menu = load_menu()
        for page in menu.pages:
            with self.subTest(page=page.page_id):
                for section in page.sections:
                    self.assertEqual(section.page_id, page.page_id)
                    self.assertEqual(section.target_page, page.page_id)
                    for item in section.items:
                        self.assertEqual(item.page_id, page.page_id)
                        self.assertEqual(item.target_page, page.page_id)
                        self.assertEqual(item.capability_group, page.capability_group)
        radio_actions = {item.action_id for section in menu.pages[1].sections for item in section.items}
        self.assertEqual(radio_actions, {
            "hardware.radioInventory",
            "hardware.radioReadStatusPlan",
            "hardware.radioProfileCompare",
            "hardware.radioChangePlan",
        })

    def test_xml_rejections_fail_closed(self) -> None:
        base = XML_PATH.read_text(encoding="utf-8")
        cases = {
            "duplicate_page": base.replace('pageId="mesh"', 'pageId="radio"', 1),
            "invalid_target": base.replace('targetPage="mesh"', 'targetPage="unknown"', 1),
            "unsafe_visible_label": base.replace("Radio Inventory", "XBee Inventory", 1),
            "secret_like_attribute": base.replace(
                '<item itemId="bench-target-readiness"',
                '<item token="hidden" itemId="bench-target-readiness"',
                1,
            ),
            "unknown_action": base.replace("hardware.meshSummary", "hardware.meshUnknown", 1),
            "unknown_bridge_action": base.replace("mesh.statusSnapshot", "mesh.rawSnapshot", 1),
            "doctype": '<!DOCTYPE menu [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>' + base,
        }
        for name, xml in cases.items():
            with self.subTest(name=name), self.assertRaises(RnwMenuGenerationError):
                _load_modified_xml(xml)


if __name__ == "__main__":
    unittest.main()
