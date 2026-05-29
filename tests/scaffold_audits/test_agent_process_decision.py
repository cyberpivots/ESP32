#!/usr/bin/env python3
"""Tests for the ESP32 weighted reviewer decision helper."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import agent_process_decision as decision  # noqa: E402


def base_packet() -> dict[str, object]:
    return {
        "gate": "unit-test-gate",
        "tier": "Tier 2",
        "approvalThreshold": 0.70,
        "requiredRoles": ["coordinator", "qa"],
        "votes": [
            {
                "role": "coordinator",
                "vote": "approve",
                "p1Findings": [],
                "p2Findings": [],
                "evidenceReviewed": ["AGENTS.md"],
                "conditions": [],
                "confidence": "high",
            },
            {
                "role": "qa",
                "vote": "approve",
                "p1Findings": [],
                "p2Findings": [],
                "evidenceReviewed": ["tests"],
                "conditions": [],
                "confidence": "high",
            },
        ],
        "evidenceGaps": [],
        "workRemaining": [],
    }


class AgentProcessDecisionTests(unittest.TestCase):
    def test_gate_passes_with_required_roles_threshold_and_no_blockers(self) -> None:
        record = decision.evaluate_packet(base_packet())

        self.assertTrue(record["gatePasses"])
        self.assertEqual("ready_for_mutation", record["decision"])
        self.assertEqual(8, record["approvalWeight"])
        self.assertEqual(8, record["totalWeight"])
        self.assertEqual([], record["missingRoles"])
        self.assertEqual([], record["blockers"])

    def test_p1_or_p2_blocker_rejects_even_with_full_approval(self) -> None:
        packet = base_packet()
        votes = packet["votes"]
        assert isinstance(votes, list)
        votes[0]["p1Findings"] = ["open live-radio identity blocker"]
        votes[1]["p2Findings"] = ["missing durable record"]

        record = decision.evaluate_packet(packet)

        self.assertFalse(record["gatePasses"])
        self.assertEqual("blocked", record["decision"])
        self.assertIn("coordinator P1: open live-radio identity blocker", record["blockers"])
        self.assertIn("qa P2: missing durable record", record["blockers"])

    def test_missing_required_role_rejects_gate_but_continues_review_collection(self) -> None:
        packet = base_packet()
        packet["requiredRoles"] = ["coordinator", "qa", "hardware"]

        record = decision.evaluate_packet(packet)

        self.assertFalse(record["gatePasses"])
        self.assertEqual("continue", record["decision"])
        self.assertEqual(["hardware"], record["missingRoles"])

    def test_unknown_role_weight_and_malformed_vote_reject(self) -> None:
        packet = base_packet()
        packet["votes"] = [
            {"role": "mystery-reviewer", "vote": "approve"},
            {"role": "qa", "vote": "maybe", "weight": 3},
            "not-an-object",
        ]

        record = decision.evaluate_packet(packet)

        rendered_errors = "\n".join(record["errors"])
        self.assertFalse(record["gatePasses"])
        self.assertEqual("blocked", record["decision"])
        self.assertIn("unknown weight", rendered_errors)
        self.assertIn("invalid vote", rendered_errors)
        self.assertIn("vote 2 must be an object", rendered_errors)

    def test_below_threshold_rejects(self) -> None:
        packet = base_packet()
        votes = packet["votes"]
        assert isinstance(votes, list)
        votes.append({"role": "hardware", "vote": "abstain", "weight": 5})

        record = decision.evaluate_packet(packet)

        self.assertFalse(record["gatePasses"])
        self.assertIn("below threshold", "\n".join(record["errors"]))

    def test_tier3_requires_all_live_gate_prerequisites(self) -> None:
        packet = base_packet()
        packet["tier"] = "Tier 3"
        packet["tier3Prerequisites"] = {
            "explicitLiveGateAuthority": True,
            "sameSessionEvidence": False,
            "recoveryPath": True,
            "reviewerQuorum": True,
            "closedSurfaceReview": False,
        }
        packet["evidenceGaps"] = [
            {
                "description": "same-session physical isolation evidence",
                "automatable": False,
                "requiresHuman": True,
                "hardBlocker": False,
            }
        ]

        record = decision.evaluate_packet(packet)

        self.assertFalse(record["gatePasses"])
        self.assertEqual("ask_user", record["decision"])
        self.assertIn("same-session evidence", record["missingTier3Prerequisites"])
        self.assertIn("closed-surface review", record["missingTier3Prerequisites"])

    def test_automatable_missing_evidence_continues_instead_of_stopping(self) -> None:
        packet = base_packet()
        packet["evidenceGaps"] = [
            {
                "description": "run no-serial host inventory",
                "automatable": True,
                "requiresHuman": False,
                "hardBlocker": False,
            }
        ]

        record = decision.evaluate_packet(packet)

        self.assertTrue(record["gatePasses"])
        self.assertEqual("continue", record["decision"])
        self.assertIn("run no-serial host inventory", record["nextActions"])


if __name__ == "__main__":
    unittest.main()
