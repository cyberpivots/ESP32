# Always-On Subagent Process Enforcement Source Ledger

Source ID:
`SRC-LOCAL-ALWAYS-ON-SUBAGENT-PROCESS-ENFORCEMENT-2026-06-02`

Date: 2026-06-02

## Scope

This ledger records the Tier 2 source-only process update that strengthens the
ESP32 workspace multi-agent policy from default-authorized subagents to a
mandatory subagent-attempt rule for safe non-trivial Tier 1 mutation and Tier 2/
Tier 3 reviewer quorum.

## Verified Facts

- `AGENTS.md` remains the canonical workspace operating contract.
- Project-local `.codex/agents/*.toml` profiles remain the default subagent
  instruction surface.
- The update requires a mandatory attempt to use project-local read-only
  subagents when available and safe.
- Local role-lens fallback remains valid only when subagents are unavailable,
  unsafe, or blocked by higher-priority tool policy, and the reason must be
  recorded.
- Agent lifecycle cleanup remains required: inspect completed agents, use
  `wait_agent`, close completed/stale agents with `close_agent`, and close
  agents before fallback/final.
- `bypassPermissions` remains advisory only; no machine-wide
  `/etc/codex/requirements.toml` policy was added.

## Files

- `AGENTS.md`
- `.agents/GOVERNANCE.md`
- `.agents/ROLES.md`
- `.codex/hooks/user_prompt_submit_agent_process.py`
- `.codex/hooks/subagent_start_agent_process.py`
- `docs/agent-coordination.md`
- `docs/prompt/prompt-triage.md`
- `docs/prompt/preengineered-prompts.md`
- `docs/prompt/expert-agent-panels.md`
- `knowledge-base/prompt-registry.md`
- `research/triage-status.md`
- `research/development-status-ledger.md`
- `research/known-gaps.md`
- `scripts/scaffold_audit_agent_process.py`
- `tests/scaffold_audits/test_agent_process_hooks.py`
- `.agents/TASK_LOG/0137-always-on-subagent-process-enforcement.md`
- `.agents/handoffs/0101-always-on-subagent-process-enforcement-to-qa-tooling.md`

## Validation

- PASS: focused hook/admin/process tests were included in the 60-test bundle.
- PASS: agent-process scaffold audit.
- PASS: source, docs, and data scaffold audits.
- PASS: scaffold verification.
- PASS: final `git diff --check`.

## Closed Surfaces

This process record does not prove or authorize firmware runtime changes, live
hardware, COM/serial access, flash, verify-flash, monitor, serial writes,
RF/XBee work, relay/load/mains work, wiring mutation, system-wide Codex policy,
admin-strict installation, destructive git, GitHub publication, release,
commit, or push.
