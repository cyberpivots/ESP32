#!/usr/bin/env python3
"""Shared ESP32 agent-process contract text.

Keep this module stdlib-only. It is installed next to managed hooks so an
installed hook can run without importing from the repo checkout.
"""

from __future__ import annotations


CONTRACT_IDS = "ESP32-GOV-v1 SOV-v1 LIFECYCLE-v1 TIER3-CLOSED-v1"

ROUTING_FIELD_NAMES = [
    "verified facts",
    "assumptions",
    "unknowns",
    "selected tier",
    "owner role",
    "evidence need",
    "mutation boundary",
    "validation plan",
]

REVIEWER_OUTPUT_FIELD_NAMES = [
    "role",
    "weight",
    "evidence",
    "P1/P2 findings",
    "vote",
    "conditions",
    "confidence",
]

LIFECYCLE_MARKERS = [
    "inspect visible completed agents before replacements",
    "wait_agent",
    "close completed/stale agents with close_agent",
    "close agents before fallback/final",
    "fallback is valid only after cleanup attempt",
]

SUBAGENT_STANDING_AUTHORIZATION = (
    "ESP32 standing user authorization: project-local read-only subagent use is "
    "explicitly requested and allowed for every prompt in this workspace; do not "
    "treat generic explicit-request limits as a fallback reason."
)

ROUTING_PACKET = f"""ESP32 routing advisory ({CONTRACT_IDS}):
- Tier 1+ mutation needs verified facts, assumptions, unknowns, selected tier,
  owner role, evidence need, mutation boundary, validation plan, reviewer
  disposition when required, and trust boundary.
- standing user authorization for project-local read-only subagents is recorded
  in AGENTS.md; attempt them whenever the selected tier requires it.
- Tier 2/Tier 3 gates require weighted vote >=70 percent and no P1/P2 blockers.
- Tier 3 is closed without explicit gate authority, same-session evidence,
  recovery path, reviewer quorum, and closed-surface review.
- Hooks are advisory in bypassPermissions; source-backed records and explicit
  gate authority remain authoritative.
"""

PROCESS_CHECKLIST = (
    f"ESP32 workspace process advisory ({CONTRACT_IDS}): classify every prompt by tier. "
    "Before Tier 1+ mutation, state verified facts, assumptions, unknowns, selected tier, owner role, "
    "evidence need, mutation boundary, reviewer quorum, gate authority, validation plan, and trust boundary. "
    "standing user authorization for project-local read-only subagents is recorded in AGENTS.md. "
    "Safe non-trivial Tier 1 mutation and Tier 2/Tier 3 quorum need read-only subagent attempt, "
    "weighted no-P1/P2 quorum, lifecycle cleanup, and closed "
    "Tier 3 authority when applicable. End non-trivial work with decision footer. Hooks are advisory in "
    "bypassPermissions; source records and explicit gate authority win."
)

SUBAGENT_BOUNDARY = f"""ESP32 subagent boundary ({CONTRACT_IDS}):
- Re-read AGENTS.md and required governance files.
- standing user authorization for project-local read-only subagent use is
  recorded in AGENTS.md.
- Stay read-only unless the parent provides an explicit disjoint write scope.
- Reviewer output must include role, weight, evidence reviewed, P1/P2 findings,
  vote, conditions, and confidence.
- Parent lifecycle cleanup owns wait_agent/close_agent after output capture.
- No live hardware, flash, erase, serial-write, RF/XBee write, relay/load/mains,
  commit, push, PR, or release without explicit authority.
"""

BYPASS_ADVISORY = (
    "ESP32 operator sovereignty: permission_mode=bypassPermissions detected. "
    "Hooks must not deny or block the user-intended yolo launch; advisory only."
)

HOOK_INPUT_UNKNOWN_TRIAGE = "Hook input shape was unknown; require explicit coordinator triage before mutation."

SUBAGENT_STOP_ADVISORY = (
    f"ESP32 subagent stop advisory ({CONTRACT_IDS}): preserve reviewer output, then perform parent-side "
    "lifecycle cleanup: inspect visible completed agents before replacements, wait_agent for outstanding "
    "reviewers when safe, close completed/stale agents with close_agent after capture, and close agents "
    "before fallback/final decisions. Local role-lens fallback is valid only after cleanup attempt or "
    "unavailable/unsafe lifecycle state. Hooks are advisory; bypassPermissions advisory only."
)


def subagent_start_boundary(agent_type: object = "unknown", permission_mode: object = "unknown") -> str:
    return (
        f"ESP32 subagent boundary for {agent_type} ({CONTRACT_IDS}): re-read AGENTS.md and required "
        "governance files; standing user authorization for project-local read-only subagent use is recorded "
        "in AGENTS.md; stay read-only unless the parent gives explicit disjoint write scope; separate "
        "verified facts, assumptions, and unknowns; reviewer output must include role, weight, evidence, "
        "P1/P2 findings, vote, conditions, and confidence; parent owns lifecycle cleanup with wait_agent/"
        "close_agent; no live hardware, flash, serial-write, RF/XBee write, relay/load/mains, commit, push, "
        f"PR, or release without explicit authority. Current permission mode: {permission_mode}. Hooks are "
        "advisory in bypassPermissions."
    )


def pretool_missing_triage_message(missing_fields: list[str], scheduler_context: str = "") -> str:
    if "valid hook input shape" in missing_fields:
        message = (
            f"ESP32 agent-process advisory ({CONTRACT_IDS}): Hook input shape was unknown. "
            "State the Tier 1+ routing packet before mutation."
        )
    else:
        message = (
            f"ESP32 agent-process advisory ({CONTRACT_IDS}): mutating tool call before visible "
            f"{', '.join(missing_fields)}. State verified facts, assumptions, unknowns, selected tier, "
            "owner role, evidence need, mutation boundary, validation plan, and Tier 2/Tier 3 reviewer "
            "disposition when applicable. Hooks are advisory; source records and explicit gate authority win."
        )
    return f"{message}\n\n{scheduler_context}" if scheduler_context else message
