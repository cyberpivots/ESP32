#!/usr/bin/env python3
"""Add ESP32 workspace boundaries to newly spawned subagents."""

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    agent_type = payload.get("agent_type", "unknown")
    permission_mode = payload.get("permission_mode", "unknown")
    message = f"""ESP32 subagent boundary for {agent_type}:
- Re-read AGENTS.md and the required governance files before making claims.
- Keep verified facts, assumptions, and unknowns separate.
- Stay read-only unless the parent gave an explicit disjoint write scope.
- Preserve dirty work and never revert user or other-agent changes.
- Do not select a firmware framework unless an accepted ADR authorizes it.
- Do not run live hardware, flash, erase, monitor, serial-write, BLE, mesh, PCAP, relay, XBee write, TFT, MicroSD, load, wiring, or mains actions.
- List changed paths and validation performed if mutation is authorized.
- Do not commit or push unless the user explicitly requested it.
Current permission mode reported to the hook: {permission_mode}."""

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": message,
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
