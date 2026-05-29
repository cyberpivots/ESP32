#!/usr/bin/env python3
"""Add ESP32 workspace boundaries to newly spawned subagents."""

from __future__ import annotations

import json
import sys


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
    message = f"""ESP32 subagent boundary for {agent_type}:
- Re-read AGENTS.md and the required governance files before making claims.
- Keep verified facts, assumptions, and unknowns separate.
- Project-local read-only subagents are default-authorized for safe Tier 2 and Tier 3 reviewer quorum.
- Stay read-only unless the parent gave an explicit disjoint write scope.
- Reviewer outputs must include role, weight, evidence reviewed, P1/P2 findings, vote, conditions, and confidence.
- Missing evidence should become a next safe evidence action when automatable, not a premature stop.
- Preserve dirty work and never revert user or other-agent changes.
- Do not select a firmware framework unless an accepted ADR authorizes it.
- Do not run live hardware, flash, erase, monitor, serial-write, BLE, mesh, PCAP, relay, XBee write, TFT, MicroSD, load, wiring, or mains actions.
- List changed paths and validation performed if mutation is authorized.
- Do not commit or push unless the user explicitly requested it.
Current permission mode reported to the hook: {permission_mode}.
Project-local hooks and prompt packets are advisory aids; source-backed records and explicit gate authority remain authoritative."""
    if shape_unknown:
        message += "\nHook input shape was unknown; require explicit coordinator triage before mutation."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
