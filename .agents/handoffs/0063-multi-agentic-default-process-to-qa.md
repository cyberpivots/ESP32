# Handoff 0063 - Multi-Agentic Default Process To QA

Date: 2026-05-27

## Current State

- `AGENTS.md` now defines the four-tier default multi-agent process for every
  prompt.
- `.codex/config.toml` registers existing read-only profiles plus
  `qa-validation-reviewer`, `governance-doc-worker`, `kb-record-worker`, and
  `bounded-implementation-worker`.
- `.codex/hooks.json` adds `UserPromptSubmit`, `SubagentStart`, and
  `PreToolUse` command hooks that inject checklist or warning context.
- `scripts/scaffold_audit_agent_process.py` is wired into
  `scripts/verify_scaffold.py`.

## QA Focus

1. Review and trust project-local hooks in the active Codex runtime before
   treating them as runtime aids.
2. Confirm hook warning behavior remains advisory and does not claim a hard
   security boundary.
3. Re-run `python3 scripts/scaffold_audit_agent_process.py` and
   `python3 scripts/verify_scaffold.py` after any future profile or hook edit.
4. Check that worker agents always receive disjoint write scopes before
   mutation.

## Do Not Claim

- Do not claim hooks are active until the runtime has reviewed and trusted them.
- Do not claim `PreToolUse` fully intercepts all mutations.
- Do not claim this process authorizes live hardware, flashing, wiring, radio,
  relay/load/mains, serial writes, BLE/mesh, PCAP, TFT, MicroSD, or framework
  selection.

## Closed Surfaces

Firmware framework selection, firmware runtime implementation, live hardware,
flashing, erase, monitor, serial-write expansion, radio setting changes,
router/admin mutation, BLE, mesh, PCAP, relay/XBee writes, TFT, MicroSD, load,
mains, and commit/push remain closed.
