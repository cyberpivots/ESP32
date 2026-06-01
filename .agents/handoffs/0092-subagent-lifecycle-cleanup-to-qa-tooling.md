# Handoff 0092 - Subagent Lifecycle Cleanup To QA/Tooling

## Current State

The workspace now treats subagent lifecycle cleanup as part of every Tier 2 and
Tier 3 reviewer quorum. Parent agents must collect reviewer output, close
completed/stale agents, close agents before fallback/final, and record local
role-lens fallback only after cleanup attempt or unavailable/unsafe lifecycle
state.

## Files To Review

- `AGENTS.md`
- `.agents/GOVERNANCE.md`
- `.agents/ROLES.md`
- `.codex/hooks.json`
- `.codex/hooks/user_prompt_submit_agent_process.py`
- `.codex/hooks/subagent_start_agent_process.py`
- `.codex/hooks/subagent_stop_agent_process.py`
- `.codex/admin/hooks/esp32_admin_policy.py`
- `docs/agent-coordination.md`
- `docs/prompt/prompt-triage.md`
- `docs/prompt/preengineered-prompts.md`
- `docs/prompt/expert-agent-panels.md`
- `knowledge-base/prompt-registry.md`
- `scripts/scaffold_audit_agent_process.py`
- `tests/scaffold_audits/test_agent_process_hooks.py`
- `tests/scaffold_audits/test_admin_policy_hooks.py`

## QA Focus

- Confirm the lifecycle rule names the actual parent-agent actions:
  `wait_agent`, `close_agent`, close before fallback/final, and fallback only
  after cleanup attempt.
- Confirm wording does not claim repo-local hooks can guarantee Codex runtime
  slot release.
- Confirm `bypassPermissions` remains advisory only and no hook blocks yolo
  intent.
- Confirm no live hardware or system-wide `/etc/codex` authority was opened.

## Still Open

Runtime close-agent observability remains a platform/runtime unknown. Future
sessions must still actually call `close_agent`; repo-local text and tests are
guardrails, not proof that a future parent cleaned up slots.

## Validation

- Focused hook/admin/decision tests: PASS, 31 tests.
- Full scaffold audit discovery: PASS, 67 tests.
- Agent-process scaffold audit, scaffold verification, source/docs/data audits,
  and `git diff --check`: PASS.
