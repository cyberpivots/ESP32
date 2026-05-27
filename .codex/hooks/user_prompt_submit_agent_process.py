#!/usr/bin/env python3
"""Inject the ESP32 default multi-agent checklist for every prompt."""

from __future__ import annotations

import json
import sys


CHECKLIST = """ESP32 workspace default-multi-agentic-process:
- Classify this prompt as Tier 0, Tier 1, Tier 2, or Tier 3 before non-trivial mutation.
- State verified facts, assumptions, unknowns, selected tier, owner role, mutation boundary, and validation plan before Tier 1+ mutation.
- Tier 2 work needs a read-only reviewer quorum before mutation.
- Tier 3 work needs same-session evidence and explicit gate authority before live bench, flashing, wiring, radio, serial-write, relay/load/mains, or release-gate mutation.
- Spawn project-local subagents only when explicitly authorized and safe; otherwise run the same role lenses locally and say no subagents were spawned.
- Preserve dirty work, keep worker write scopes disjoint, keep factual claims source-backed, and do not select a firmware framework unless an accepted ADR authorizes it."""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    if payload.get("hook_event_name") not in (None, "UserPromptSubmit"):
        return 0

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": CHECKLIST,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
