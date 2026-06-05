#!/usr/bin/env python3
"""Tests for the host-only XBee hub-spoke simulator."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.simulators.xbee_hub_spoke.xbee_hub_spoke import (  # noqa: E402
    MIN_SPOKES,
    build_hub_spoke_plan,
    find_public_redaction_issues,
    parse_np_hex,
)


class XBeeHubSpokeSimulatorTests(unittest.TestCase):
    def test_builds_minimum_ten_spoke_plan_with_twelve_use_cases(self) -> None:
        plan = build_hub_spoke_plan()

        self.assertEqual("xbee_hub_spoke_plan.v1", plan["schema"])
        self.assertEqual(MIN_SPOKES, len(plan["spokes"]))
        self.assertGreaterEqual(len(plan["useCases"]), 12)
        self.assertEqual(len(plan["useCases"]), len(plan["scenarios"]))
        self.assertEqual("0x8B", plan["topology"]["transmitStatusFrame"])
        self.assertEqual("0x90", plan["topology"]["receiveFrame"])
        self.assertEqual("blocked_without_variant_proof", plan["topology"]["digiMeshForCurrentPart"])

    def test_plan_is_host_only_and_contains_no_public_identifiers(self) -> None:
        plan = build_hub_spoke_plan()
        boundary = plan["hostOnlyBoundary"]

        for key, value in boundary.items():
            self.assertFalse(value, key)
        for spoke in plan["spokes"]:
            self.assertTrue(spoke["addressRedacted"])
            self.assertFalse(spoke["rawIdentifierStored"])
            self.assertNotIn("address", {key for key in spoke if key != "addressRedacted"})
        self.assertEqual([], find_public_redaction_issues(plan))
        self.assertEqual([], plan["redaction"]["publicRedactionIssues"])

    def test_every_scenario_uses_extended_transmit_status_0x8b(self) -> None:
        plan = build_hub_spoke_plan()

        for scenario in plan["scenarios"]:
            self.assertEqual("0x8B", scenario["transmitStatusFrame"]["frameType"])
            self.assertEqual("0x90", scenario["receiveFrame"]["frameType"])
            self.assertFalse(scenario["transmitStatusFrame"]["liveDeliveryClaim"])
        self.assertNotIn("0x89", json.dumps(plan))

    def test_payload_budget_uses_np_minus_encryption_overhead(self) -> None:
        plan = build_hub_spoke_plan(np_hex="0x54")

        self.assertEqual(84, plan["payloadBudget"]["npBytes"])
        self.assertEqual(75, plan["payloadBudget"]["apsEncryptedBytes"])
        self.assertTrue(all(scenario["fitsEncryptedNpBudget"] for scenario in plan["scenarios"]))

    def test_rejects_too_few_spokes_and_invalid_np(self) -> None:
        with self.assertRaises(ValueError):
            build_hub_spoke_plan(spoke_count=9)
        with self.assertRaises(ValueError):
            parse_np_hex("not-hex")


if __name__ == "__main__":
    unittest.main()
