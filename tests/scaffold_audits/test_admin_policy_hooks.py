#!/usr/bin/env python3
"""Regression tests for ESP32 admin-managed Codex hooks."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".codex" / "admin" / "hooks" / "esp32_admin_policy.py"
DEFAULT_REQUIREMENTS = ROOT / ".codex" / "admin" / "requirements.toml"
YOLO_REQUIREMENTS = ROOT / ".codex" / "admin" / "profiles" / "yolo-compatible" / "requirements.toml"


def run_hook(payload: object | str) -> subprocess.CompletedProcess[str]:
    stdin_text = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin_text,
        text=True,
        capture_output=True,
        check=False,
    )


def output(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


class AdminPolicyHookTests(unittest.TestCase):
    def assert_clean_json(self, result: subprocess.CompletedProcess[str]) -> dict[str, object]:
        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)
        return output(result)

    def test_malformed_stdin_does_not_crash(self) -> None:
        result = run_hook("{")
        data = self.assert_clean_json(result)
        self.assertIn("hookSpecificOutput", data)

    def test_missing_triage_on_mutating_tool_denies(self) -> None:
        result = run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "touch blocked"},
            "prompt": "",
        })
        data = self.assert_clean_json(result)
        hook = data["hookSpecificOutput"]
        self.assertEqual("deny", hook["permissionDecision"])
        self.assertIn("missing routing packet fields", hook["permissionDecisionReason"])

    def test_complete_tier2_triage_allows_docs_mutation(self) -> None:
        prompt = (
            "Verified facts: docs change. Assumptions: none. Unknowns: none. "
            "Selected tier: Tier 2. Owner role: Agent Operations. Evidence need: local. "
            "Mutation boundary: docs only. Validation plan: unit tests."
        )
        result = run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "touch allowed"},
            "prompt": prompt,
        })
        self.assert_clean_json(result)
        self.assertEqual("", result.stdout)

    def test_tier3_command_denies_without_live_authority(self) -> None:
        prompt = (
            "Verified facts: local command. Assumptions: none. Unknowns: none. "
            "Selected tier: Tier 2. Owner role: QA. Evidence need: local. "
            "Mutation boundary: docs. Validation plan: unit tests."
        )
        result = run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "idf.py flash"},
            "prompt": prompt,
        })
        data = self.assert_clean_json(result)
        hook = data["hookSpecificOutput"]
        self.assertEqual("deny", hook["permissionDecision"])
        self.assertIn("Tier 3 command denied", hook["permissionDecisionReason"])

    def test_permission_request_denies_missing_authority(self) -> None:
        result = run_hook({
            "hook_event_name": "PermissionRequest",
            "tool_name": "Bash",
            "tool_input": {"command": "sudo idf.py flash"},
            "prompt": "Verified facts: none.",
        })
        data = self.assert_clean_json(result)
        decision = data["hookSpecificOutput"]["decision"]
        self.assertEqual("deny", decision["behavior"])

    def test_subagent_stop_rejects_incomplete_vote_record(self) -> None:
        result = run_hook({
            "hook_event_name": "SubagentStop",
            "last_assistant_message": "Looks fine.",
        })
        data = self.assert_clean_json(result)
        self.assertEqual("block", data["decision"])
        self.assertIn("reviewer output missing", data["reason"])

    def test_subagent_stop_rejects_open_blocker_or_reject_vote(self) -> None:
        messages = [
            (
                "Role: QA\n"
                "Evidence reviewed: tests\n"
                "P1/P2 findings: P2 missing decision helper\n"
                "Vote: approve\n"
                "Conditions: add tests\n"
                "Confidence: high\n",
                "open P1/P2",
            ),
            (
                "Role: QA\n"
                "Evidence reviewed: tests\n"
                "P1/P2 findings: none\n"
                "Vote: reject acceptance\n"
                "Conditions: add tests\n"
                "Confidence: high\n",
                "rejected",
            ),
        ]
        for message, marker in messages:
            with self.subTest(marker=marker):
                result = run_hook({"hook_event_name": "SubagentStop", "last_assistant_message": message})
                data = self.assert_clean_json(result)
                self.assertEqual("block", data["decision"])
                self.assertIn(marker, data["reason"])

    def test_stop_continues_when_footer_missing_after_mutation(self) -> None:
        result = run_hook({
            "hook_event_name": "Stop",
            "last_assistant_message": "Implemented the admin policy and ran tests.",
        })
        data = self.assert_clean_json(result)
        self.assertEqual("block", data["decision"])
        self.assertIn("decision footer", data["reason"])

    def test_stop_blocks_nonterminal_or_incomplete_footer(self) -> None:
        messages = [
            (
                "Implemented changes.\n"
                "Decision: continue\n"
                "Next gate: more tests\n"
                "Owner role: QA\n"
                "Evidence: local\n"
                "Validation: unittest\n"
                "Durable records: task log\n"
                "Authority limits: no live hardware\n",
                "not terminal",
            ),
            (
                "Implemented changes.\n"
                "Decision: ready_for_mutation\n"
                "Next gate: mutation\n"
                "Owner role: QA\n"
                "Evidence: local\n"
                "Validation: unittest\n"
                "Durable records: task log\n"
                "Authority limits: no live hardware\n",
                "not terminal",
            ),
            (
                "Implemented changes.\n"
                "Decision: handoff\n"
                "Next gate: QA\n"
                "Owner role: QA\n"
                "Evidence: local\n"
                "Validation: pending\n"
                "Durable records: task log\n"
                "Authority limits: no live hardware\n",
                "validation is pending",
            ),
            (
                "Implemented changes.\n"
                "Decision: handoff\n"
                "Next gate: QA\n"
                "Owner role: QA\n"
                "Evidence: local\n"
                "Validation: unittest\n"
                "Durable records: missing\n"
                "Authority limits: no live hardware\n",
                "durable records are pending",
            ),
        ]
        for message, marker in messages:
            with self.subTest(marker=marker):
                result = run_hook({"hook_event_name": "Stop", "last_assistant_message": message})
                data = self.assert_clean_json(result)
                self.assertEqual("block", data["decision"])
                self.assertIn(marker, data["reason"])

    def test_stop_allows_complete_footer(self) -> None:
        message = (
            "Implemented the admin policy.\n"
            "Decision: handoff\n"
            "Next gate: QA review\n"
            "Owner role: QA\n"
            "Evidence: local tests\n"
            "Validation: unittest\n"
            "Durable records: task log\n"
            "Authority limits: no live hardware\n"
        )
        result = run_hook({"hook_event_name": "Stop", "last_assistant_message": message})
        self.assert_clean_json(result)
        self.assertEqual("", result.stdout)

    def test_transcript_context_can_supply_triage(self) -> None:
        prompt = (
            "Verified facts: docs change. Assumptions: none. Unknowns: none. "
            "Selected tier: Tier 2. Owner role: QA. Evidence need: local. "
            "Mutation boundary: tests. Validation plan: unittest."
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
            handle.write(json.dumps({"role": "user", "content": prompt}) + "\n")
            path = handle.name
        try:
            result = run_hook({
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "touch allowed"},
                "transcript_path": path,
            })
            self.assert_clean_json(result)
            self.assertEqual("", result.stdout)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_bypass_permissions_never_denies_or_blocks(self) -> None:
        payloads = [
            {
                "hook_event_name": "PreToolUse",
                "permission_mode": "bypassPermissions",
                "tool_name": "Bash",
                "tool_input": {"command": "rm -rf build"},
                "prompt": "",
            },
            {
                "hook_event_name": "PreToolUse",
                "permission_mode": "bypassPermissions",
                "tool_name": "Bash",
                "tool_input": {"command": "git reset --hard HEAD"},
                "prompt": "",
            },
            {
                "hook_event_name": "PreToolUse",
                "permission_mode": "bypassPermissions",
                "tool_name": "Bash",
                "tool_input": {"command": "idf.py flash"},
                "prompt": "",
            },
            {
                "hook_event_name": "PermissionRequest",
                "permission_mode": "bypassPermissions",
                "tool_name": "Bash",
                "tool_input": {"command": "sudo idf.py flash"},
                "prompt": "",
            },
            {
                "hook_event_name": "SubagentStop",
                "permission_mode": "bypassPermissions",
                "last_assistant_message": "Looks fine.",
            },
            {
                "hook_event_name": "Stop",
                "permission_mode": "bypassPermissions",
                "last_assistant_message": "Implemented changes without a footer.",
            },
        ]
        for payload in payloads:
            with self.subTest(event=payload["hook_event_name"], command=payload.get("tool_input")):
                result = run_hook(payload)
                self.assert_clean_json(result)
                self.assertEqual("", result.stdout)

    def test_default_and_yolo_profiles_do_not_constrain_yolo(self) -> None:
        for path in [DEFAULT_REQUIREMENTS, YOLO_REQUIREMENTS]:
            with self.subTest(path=path):
                raw = path.read_text(encoding="utf-8")
                self.assertNotIn("allowed_sandbox_modes", raw)
                self.assertNotIn("allowed_approval_policies", raw)
                self.assertNotIn("rules.prefix_rules", raw)
                with path.open("rb") as handle:
                    data = tomllib.load(handle)
                self.assertNotIn("allowed_sandbox_modes", data)
                self.assertNotIn("allowed_approval_policies", data)
                rules = data.get("rules")
                if isinstance(rules, dict):
                    self.assertNotIn("prefix_rules", rules)


if __name__ == "__main__":
    unittest.main()
