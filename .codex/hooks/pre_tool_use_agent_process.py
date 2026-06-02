#!/usr/bin/env python3
"""Warn on mutating tool calls when the triage packet is not visible."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_process_classifiers import (  # noqa: E402
    ROUTING_PATTERNS,
    is_mutating_tool,
    latest_text_from_transcript,
    missing,
)
from agent_process_contracts import pretool_missing_triage_message  # noqa: E402


SCHEDULER = ROOT / "scripts" / "agent_scheduler.py"
SCHEDULER_TIMEOUT_SECONDS = float(os.environ.get("ESP32_SCHEDULER_HOOK_TIMEOUT", "0.75"))


def _load_payload() -> tuple[dict[str, Any], bool]:
    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}, True
    if not isinstance(raw, dict):
        return {}, True
    return raw, False


def _scheduler_context(payload: dict[str, Any]) -> str:
    if not SCHEDULER.exists():
        return "ESP32 scheduler advisory: scheduler-unavailable; no deny/block."
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(SCHEDULER),
                "pretool-check",
                "--repo",
                str(ROOT),
                "--hook-json",
                json.dumps(payload),
                "--timeout",
                str(SCHEDULER_TIMEOUT_SECONDS),
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=SCHEDULER_TIMEOUT_SECONDS + 0.5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"ESP32 scheduler advisory: scheduler-unavailable ({exc}); no deny/block."
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
        return f"ESP32 scheduler advisory: scheduler-unavailable ({detail}); no deny/block."
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return f"ESP32 scheduler advisory: scheduler-unavailable (invalid output: {exc}); no deny/block."
    hook_output = output.get("hookSpecificOutput")
    if not isinstance(hook_output, dict):
        return ""
    context = hook_output.get("additionalContext")
    return context if isinstance(context, str) else ""


def _emit_warning(missing_fields: list[str], scheduler_context: str = "") -> None:
    message = pretool_missing_triage_message(missing_fields, scheduler_context)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": message,
        }
    }))


def main() -> int:
    payload, shape_unknown = _load_payload()
    if shape_unknown:
        _emit_warning(["valid hook input shape"])
        return 0

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    if not is_mutating_tool(tool_name, tool_input):
        return 0
    scheduler_context = _scheduler_context(payload)

    prompt = str(payload.get("prompt") or "") or latest_text_from_transcript(
        payload.get("transcript_path")
    )
    missing_fields = missing(ROUTING_PATTERNS, prompt)
    if not missing_fields:
        if scheduler_context:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": scheduler_context,
                }
            }))
        return 0

    _emit_warning(missing_fields, scheduler_context)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
