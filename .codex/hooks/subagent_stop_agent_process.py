#!/usr/bin/env python3
"""Remind the parent to clean up completed reviewer agents."""

from __future__ import annotations

import json
import sys


MESSAGE = """ESP32 subagent stop lifecycle reminder:
- Preserve the reviewer output before using it in quorum evidence.
- agent lifecycle cleanup is required: inspect completed agents before spawning replacement reviewers, use wait_agent for outstanding reviewers when safe, and close completed/stale agents with close_agent after output is captured.
- close agents before fallback/final decisions; local role-lens fallback is valid only as fallback only after cleanup attempt, or after lifecycle state is unavailable or unsafe.
- Project-local hooks and prompt packets are advisory aids; source-backed records and explicit gate authority remain authoritative; bypassPermissions advisory only."""


def _load_payload() -> tuple[dict[str, object], bool]:
    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}, True
    if not isinstance(raw, dict):
        return {}, True
    return raw, False


def main() -> int:
    payload, shape_unknown = _load_payload()
    if payload.get("hook_event_name") not in (None, "SubagentStop"):
        return 0
    message = MESSAGE
    if shape_unknown:
        message += "\nHook input shape was unknown; require explicit coordinator triage before mutation."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SubagentStop",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
