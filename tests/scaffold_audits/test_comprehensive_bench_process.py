#!/usr/bin/env python3
"""Regression tests for the comprehensive ESP32 bench process packet."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ComprehensiveBenchProcessTests(unittest.TestCase):
    def test_process_doc_defines_packet_and_closed_surfaces(self) -> None:
        text = (ROOT / "docs/prompt/comprehensive-bench-development-process.md").read_text(
            encoding="utf-8"
        )
        for marker in [
            "bench_state_packet.v1",
            "PF0530L",
            "PF0530O",
            "COM6",
            "serial/menu physical interaction accepted on retry",
            "`ENC_RAW`",
            "`ENC_EV`",
            "`BBS_MENU_STEP`",
            "`BBS_MENU_SELECT`",
            "LCD visual/glyph readability",
            "hardware/electrical acceptance",
            "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31",
            "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-LIVE-2026-06-01",
            "XBee",
            "relay",
            "ESP-NOW/BBS/CBBS",
            "SoftAP/browser",
            "DevEx",
            "does not authorize live hardware access",
            "flashing",
            "serial monitor",
            "RF transmit",
            "relay control",
            "GitHub publication",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)
        self.assertNotIn("PF0530N has not been flashed", text)
        self.assertNotIn("PF0530N is current source/test-only", text)

    def test_registry_index_and_source_records_are_linked(self) -> None:
        registry = (ROOT / "knowledge-base/prompt-registry.md").read_text(
            encoding="utf-8"
        )
        docs_index = (ROOT / "docs/index.md").read_text(encoding="utf-8")
        source_index = (ROOT / "knowledge-base/source-index.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("comprehensive-bench-development-process", registry)
        self.assertIn("bench_state_packet.v1", registry)
        self.assertIn("prompt/comprehensive-bench-development-process.md", docs_index)
        self.assertIn(
            "2026-05-31-comprehensive-bench-development-process.md",
            docs_index,
        )
        self.assertIn(
            "SRC-LOCAL-COMPREHENSIVE-BENCH-DEVELOPMENT-PROCESS-2026-05-31",
            source_index,
        )
        self.assertIn("research/known-gaps.md", source_index)

    def test_current_research_routing_uses_pf0530l_gap_state(self) -> None:
        triage = (ROOT / "research/triage-status.md").read_text(encoding="utf-8")
        ledger = (ROOT / "research/development-status-ledger.md").read_text(
            encoding="utf-8"
        )
        gaps = (ROOT / "research/known-gaps.md").read_text(encoding="utf-8")
        for text in [triage, ledger, gaps]:
            self.assertIn("PF0530L", text)
            self.assertIn("SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31", text)
            self.assertIn("SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31", text)
            self.assertIn("accepted", text)
            self.assertIn("BBS_MENU_STEP", text)
            self.assertIn("BBS_MENU_SELECT", text)
        self.assertNotIn("PF0530H-live-ready-for-user-testing", triage)
        self.assertNotIn("PF0530H-live-ready-for-user-testing", ledger)
        self.assertNotIn("PF0530L-alive-attended-input-proof-failed", triage)
        self.assertNotIn("PF0530L-alive-attended-input-proof-failed", ledger)


if __name__ == "__main__":
    unittest.main()
