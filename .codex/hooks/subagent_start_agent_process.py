#!/usr/bin/env python3
"""Add ESP32 workspace boundaries to newly spawned subagents."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_process_contracts import HOOK_INPUT_UNKNOWN_TRIAGE, subagent_start_boundary  # noqa: E402


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

    agent_type = payload.get("agent_type", "unknown")
    permission_mode = payload.get("permission_mode", "unknown")
    message = subagent_start_boundary(agent_type, permission_mode)
    if shape_unknown:
        message += f" {HOOK_INPUT_UNKNOWN_TRIAGE}"

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
