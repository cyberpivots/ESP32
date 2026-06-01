#!/usr/bin/env python3
"""Regression tests for the ESP32 development-agent panel profiles."""

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PANEL_PROFILES = [
    "development-panel-coordinator",
    "esp32-firmware-device-reviewer",
    "xbee-radio-protocol-reviewer",
    "ui-ux-interface-reviewer",
    "source-research-reviewer",
    "data-model-kb-reviewer",
    "tooling-resource-reviewer",
    "offgrid-comms-domain-reviewer",
    "security-safety-risk-reviewer",
    "devex-ci-release-reviewer",
    "kb-prompt-registry-curator",
    "protocol-bridge-abi-reviewer",
    "power-wiring-isolation-reviewer",
]
STRUCTURED_MARKERS = [
    "Purpose:",
    "Inputs:",
    "Outputs:",
    "Read scope:",
    "Later mutation scope if separately authorized:",
    "Stop conditions:",
    "Escalation conditions:",
    "Required evidence before action:",
    "Validation method:",
    "Tier boundaries:",
]
SAFETY_MARKERS = [
    "AGENTS.md as the canonical contract",
    "operator sovereignty",
    "/etc/codex/requirements.toml",
    "codex --yolo",
    "permission_mode=bypassPermissions",
    "governance is advisory",
    "admin-strict profile by name",
]


class DevelopmentAgentPanelTests(unittest.TestCase):
    def test_panel_profiles_are_registered_and_read_only(self) -> None:
        config = tomllib.loads((ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
        agents = config["agents"]
        for profile in PANEL_PROFILES:
            with self.subTest(profile=profile):
                entry = agents[profile]
                self.assertEqual(f"agents/{profile}.toml", entry["config_file"])
                data = tomllib.loads(
                    (ROOT / ".codex/agents" / f"{profile}.toml").read_text(encoding="utf-8")
                )
                self.assertEqual(profile, data["name"])
                self.assertEqual("read-only", data["sandbox_mode"])

    def test_panel_profiles_preserve_boundaries(self) -> None:
        for profile in PANEL_PROFILES:
            with self.subTest(profile=profile):
                text = (ROOT / ".codex/agents" / f"{profile}.toml").read_text(
                    encoding="utf-8"
                )
                for marker in STRUCTURED_MARKERS + SAFETY_MARKERS:
                    self.assertIn(marker, text)
                self.assertIn("Tier 3", text)

    def test_prompt_registry_has_panel_prompt(self) -> None:
        registry = (ROOT / "knowledge-base/prompt-registry.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("development-agent-panel", registry)
        self.assertIn("mandatory human gates", registry)


if __name__ == "__main__":
    unittest.main()
