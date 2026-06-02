#!/usr/bin/env python3
"""Inject the ESP32 default multi-agent checklist for every prompt."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from agent_process_contracts import HOOK_INPUT_UNKNOWN_TRIAGE, PROCESS_CHECKLIST  # noqa: E402


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

    if payload.get("hook_event_name") not in (None, "UserPromptSubmit"):
        return 0
    context = PROCESS_CHECKLIST
    if shape_unknown:
        context += f" {HOOK_INPUT_UNKNOWN_TRIAGE}"

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
