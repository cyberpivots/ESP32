#!/usr/bin/env python3
"""Inject the ESP32 default multi-agent checklist for every prompt."""

from __future__ import annotations

import json
import sys


CHECKLIST = """ESP32 workspace default-multi-agentic-process:
- Classify this prompt as Tier 0, Tier 1, Tier 2, or Tier 3 before non-trivial mutation.
- Emit a routing packet with verified facts, assumptions, unknowns, selected tier, owner role, evidence need, mutation boundary, reviewer quorum, gate authority, validation plan, and trust boundary before Tier 1+ mutation.
- Tier 2 work needs a read-only reviewer quorum before mutation; project-local read-only subagents are default-authorized when available and safe.
- Tier 3 work needs same-session evidence, explicit gate authority, recovery path, and reviewer quorum before live bench, flashing, wiring, radio, serial-write, relay/load/mains, or release-gate mutation.
- Mutating workers require explicit disjoint write scopes; preserve dirty work and never revert user or other-agent changes.
- End non-trivial work with a decision footer: continue, ask_user, blocked, ready_for_mutation, or handoff; next gate; owner; evidence; approved mutation boundary; validation; durable records; and authority limits.
- Project-local hooks and prompt packets are advisory aids; source-backed records and explicit gate authority remain authoritative."""


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
    context = CHECKLIST
    if shape_unknown:
        context += "\n- Hook input shape was unknown; require explicit coordinator triage before mutation."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
