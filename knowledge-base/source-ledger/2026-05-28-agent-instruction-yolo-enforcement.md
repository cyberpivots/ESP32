# Agent Instruction Yolo Enforcement Source Ledger

## Routing

| Field | Value |
| --- | --- |
| Selected tier | Tier 2 governance and agent-instruction update. |
| Owner role | Agent Operations with QA and Tooling review. |
| Evidence need | Local instruction files, scaffold audit, docs audit, hook/profile tests, and system requirements absence check. |
| Mutation boundary | `AGENTS.md`, `.agents/`, `.codex/agents/*.toml`, governance/prompt docs, source records, task log, handoff, and `scripts/scaffold_audit_agent_process.py`. |
| Closed surfaces | Firmware/runtime/API/ABI/framework changes, flashing, erase, monitor, serial-write expansion, BLE/live mesh, PCAP, router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, wiring, release gates, and live bench work. |

## Sources

- `SRC-CODEX-CONFIG-REFERENCE-2026-05-27`
- `SRC-CODEX-SUBAGENTS-2026-05-27`
- `SRC-CODEX-ADMIN-REQUIREMENTS-2026-05-28`
- `SRC-CODEX-HOOKS-MANAGED-2026-05-28`
- `SRC-LOCAL-AGENT-INSTRUCTION-YOLO-ENFORCEMENT-2026-05-28`

## Verified Facts

- `AGENTS.md` now names agent instruction files as the default enforcement
  surface.
- Every `.codex/agents/*.toml` profile now includes the operator-sovereignty
  instruction.
- `scripts/scaffold_audit_agent_process.py` audits those instruction markers
  in every required project-local agent profile.
- `/etc/codex/requirements.toml` remains absent during this task.

## Assumptions

- Repo-local instructions are the correct default mechanism for governance
  enforcement when the user intends `codex --yolo` full access.

## Unknowns

- Future Codex releases may change project-local custom-agent instruction file
  loading behavior.

## Authority Limits

This ledger does not authorize firmware/runtime/API/ABI/framework changes,
flashing, erase, monitor, serial-write expansion, BLE/live mesh, PCAP,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, wiring, release
gates, or live bench work.
