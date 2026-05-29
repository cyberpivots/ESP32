#!/usr/bin/env python3
"""Regression tests for ESP32 agent-process hooks."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK_DIR = ROOT / ".codex" / "hooks"


def run_hook(script: str, stdin_text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK_DIR / script)],
        input=stdin_text,
        text=True,
        capture_output=True,
        check=False,
    )


def hook_output(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


class AgentProcessHookTests(unittest.TestCase):
    def assert_hook_context(
        self,
        result: subprocess.CompletedProcess[str],
        event_name: str,
        *markers: str,
    ) -> str:
        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)
        output = hook_output(result)
        hook_specific = output.get("hookSpecificOutput")
        self.assertIsInstance(hook_specific, dict)
        assert isinstance(hook_specific, dict)
        self.assertEqual(event_name, hook_specific.get("hookEventName"))
        context = hook_specific.get("additionalContext")
        self.assertIsInstance(context, str)
        assert isinstance(context, str)
        self.assertTrue(context.strip())
        for marker in markers:
            self.assertIn(marker, context)
        return context

    def test_user_prompt_hook_emits_routing_and_decision_context(self) -> None:
        result = run_hook(
            "user_prompt_submit_agent_process.py",
            json.dumps({"hook_event_name": "UserPromptSubmit"}),
        )
        self.assert_hook_context(
            result,
            "UserPromptSubmit",
            "evidence need",
            "default-authorized",
            "Weighted vote",
            "Missing evidence",
            "decision footer",
            "advisory aids",
        )

    def test_subagent_hook_emits_default_read_only_boundary(self) -> None:
        result = run_hook(
            "subagent_start_agent_process.py",
            json.dumps({"agent_type": "qa-validation-reviewer", "permission_mode": "read-only"}),
        )
        self.assert_hook_context(
            result,
            "SubagentStart",
            "default-authorized",
            "explicit disjoint write scope",
            "role, weight",
            "premature stop",
            "advisory aids",
        )

    def test_hooks_do_not_crash_on_malformed_or_non_object_stdin(self) -> None:
        scripts = [
            ("user_prompt_submit_agent_process.py", "UserPromptSubmit"),
            ("subagent_start_agent_process.py", "SubagentStart"),
            ("pre_tool_use_agent_process.py", "PreToolUse"),
        ]
        for script, event_name in scripts:
            for stdin_text in ["{", "[]", "null", '"x"']:
                with self.subTest(script=script, stdin_text=stdin_text):
                    result = run_hook(script, stdin_text)
                    self.assert_hook_context(result, event_name, "Hook input shape was unknown")

    def test_pre_tool_warns_for_mutation_without_triage(self) -> None:
        result = run_hook(
            "pre_tool_use_agent_process.py",
            json.dumps({
                "tool_name": "functions.exec_command",
                "tool_input": {"cmd": "touch should-warn"},
                "prompt": "",
            }),
        )
        context = self.assert_hook_context(
            result,
            "PreToolUse",
            "verified facts",
            "assumptions",
            "unknowns",
            "selected tier",
            "owner role",
            "evidence need",
            "mutation boundary",
            "validation path",
            "weighted reviewer disposition",
            "advisory aids",
        )
        self.assertIn("explicit gate authority", context)

    def test_hooks_json_matches_current_exec_tool_name(self) -> None:
        hooks = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
        pretool = json.dumps(hooks["hooks"]["PreToolUse"])
        self.assertIn("functions\\\\.exec_command", pretool)

    def test_pre_tool_partial_triage_still_warns_for_missing_fields(self) -> None:
        result = run_hook(
            "pre_tool_use_agent_process.py",
            json.dumps({
                "tool_name": "functions.exec_command",
                "tool_input": {"cmd": "touch should-warn"},
                "prompt": "Tier 2 validation plan mutation boundary",
            }),
        )
        context = self.assert_hook_context(
            result,
            "PreToolUse",
            "verified facts",
            "assumptions",
            "unknowns",
            "owner role",
            "evidence need",
        )
        self.assertNotIn("selected tier, validation path, mutation boundary", context)

    def test_pre_tool_read_only_command_does_not_warn(self) -> None:
        result = run_hook(
            "pre_tool_use_agent_process.py",
            json.dumps({
                "tool_name": "functions.exec_command",
                "tool_input": {"cmd": "rg -n default-multi-agentic-process docs"},
                "prompt": "",
            }),
        )
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        self.assertEqual("", result.stdout)

    def test_pre_tool_complete_triage_does_not_warn(self) -> None:
        prompt = (
            "Verified facts: local hook edit. Assumptions: none. Unknowns: active "
            "runtime trust. Selected tier: Tier 2. Owner role: QA. Evidence need: "
            "local. Mutation boundary: hook tests. Validation plan: unit tests."
        )
        result = run_hook(
            "pre_tool_use_agent_process.py",
            json.dumps({
                "tool_name": "functions.exec_command",
                "tool_input": {"cmd": "touch allowed-by-visible-triage"},
                "prompt": prompt,
            }),
        )
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main()
