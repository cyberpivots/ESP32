#!/usr/bin/env python3
"""Remind the parent to clean up completed reviewer agents."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_process_contracts import HOOK_INPUT_UNKNOWN_TRIAGE, SUBAGENT_STOP_ADVISORY  # noqa: E402


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
    message = SUBAGENT_STOP_ADVISORY
    if shape_unknown:
        message += f" {HOOK_INPUT_UNKNOWN_TRIAGE}"

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SubagentStop",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
