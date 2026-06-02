#!/usr/bin/env python3
"""Table-driven tests for ESP32 agent-process classifiers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import agent_process_classifiers as classifiers  # noqa: E402


class AgentProcessClassifierTests(unittest.TestCase):
    def test_read_only_shell_chains_are_not_mutating(self) -> None:
        commands = [
            "pwd && rg --files",
            "for f in AGENTS.md docs/index.md; do sed -n '1,40p' \"$f\"; done",
            "nl -ba AGENTS.md | sed -n '1,120p'",
            "git status --short --branch --untracked-files=all",
            "PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(classifiers.is_shell_read_only_command(command))
                self.assertFalse(classifiers.is_mutating_tool("functions.exec_command", {"cmd": command}))
                self.assertFalse(classifiers.is_live_tier3_tool("functions.exec_command", {"cmd": command}))

    def test_mutating_shell_commands_are_detected(self) -> None:
        commands = [
            "touch x",
            "rg foo > out.txt",
            "rg foo | tee out.txt",
            "git add AGENTS.md",
            "git reset --hard HEAD",
            "gh pr create --title x",
            "python3 scripts/build_github_pages.py --out build/github-pages",
            "python3 tool.py write-record",
            "cp a b",
            "install -m 644 a b",
            "sed -i 's/a/b/' AGENTS.md",
            "python3 /etc/codex/hooks/esp32_admin_policy.py",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(classifiers.is_mutating_tool("Bash", {"command": command}))

    def test_live_tier3_commands_are_detected(self) -> None:
        commands = [
            "idf.py flash",
            "esptool.py --port COM6 flash_id",
            "python3 scripts/xbee_radio_study.py list",
            "screen /dev/ttyUSB0 115200",
            "tcpdump -i wlan0",
            "relay test",
            "mains bringup",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(classifiers.is_live_tier3_tool("Bash", {"command": command}))

    def test_mcp_and_apply_patch_mutation_detection(self) -> None:
        self.assertTrue(classifiers.is_mutating_tool("apply_patch", {"command": "*** Begin Patch"}))
        self.assertTrue(classifiers.is_mutating_tool("mcp__fs__write_file", {}))
        self.assertFalse(classifiers.is_mutating_tool("mcp__fs__read_file", {}))

    def test_structured_classification_flags_risk_categories(self) -> None:
        cases = [
            ("rg foo | tee out.txt", "mutation", "redirection_or_tee"),
            ("python3 /etc/codex/hooks/esp32_admin_policy.py", "system_codex", "system_codex"),
            ("echo x >/etc/codex/requirements.toml", "system_codex", "system_codex"),
            ("git reset --hard HEAD", "destructive_git", "destructive_git"),
            ("gh pr create --title x", "publication", "publication"),
            ("idf.py flash", "tier3", "tier3"),
        ]
        for command, category, flag in cases:
            with self.subTest(command=command):
                result = classifiers.classify_tool("functions.exec_command", {"cmd": command})
                self.assertEqual(category, result.category)
                self.assertTrue(getattr(result, flag))
                self.assertFalse(result.read_only)

    def test_structured_classification_preserves_wrapper_compatibility(self) -> None:
        read_only = classifiers.classify_shell_command("PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py")
        self.assertEqual("read_only", read_only.category)
        self.assertTrue(read_only.read_only)
        self.assertFalse(read_only.mutation)
        self.assertFalse(classifiers.is_mutating_tool("functions.exec_command", {"cmd": "git status --short"}))

    def test_validation_performed_is_not_a_mutation_claim(self) -> None:
        self.assertIsNone(classifiers.MUTATION_CLAIM_RE.search("Validation performed: unittest PASS."))
        self.assertIsNotNone(classifiers.MUTATION_CLAIM_RE.search("Implemented classifier changes."))

    def test_footer_semantics_reject_nonterminal_or_pending_records(self) -> None:
        self.assertIn("not terminal", classifiers.footer_semantic_failure(
            "Decision: continue\nValidation: unittest\nDurable records: task log\n"
        ) or "")
        self.assertIn("validation is pending", classifiers.footer_semantic_failure(
            "Decision: handoff\nValidation: pending\nDurable records: task log\n"
        ) or "")
        self.assertIsNone(classifiers.footer_semantic_failure(
            "Decision: handoff\nValidation: unittest\nDurable records: task log\n"
        ))


if __name__ == "__main__":
    unittest.main()
