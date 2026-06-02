# Handoff 0101 - Always-On Subagent Process Enforcement To QA/Tooling

## Current State

The workspace now requires a mandatory attempt to use project-local read-only
subagents for safe non-trivial Tier 1 mutation and Tier 2/Tier 3 reviewer
quorum when the tools are available and safe. Fallback to local role lenses must
name why the mandatory attempt could not be completed and must preserve agent
lifecycle cleanup.

## Files To Review

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
- `scripts/scaffold_audit_agent_process.py`
- `tests/scaffold_audits/test_agent_process_hooks.py`

## QA Focus

- Confirm the wording says mandatory attempt, not guaranteed runtime spawn.
- Confirm fallback remains allowed for unavailable, unsafe, or higher-priority
  tool-policy conflicts and records the reason.
- Confirm `bypassPermissions` remains advisory only.
- Confirm no `/etc/codex/requirements.toml` or admin-strict install path was
  opened by this change.

## Still Open

Static repo hooks and tests cannot prove future runtime subagent availability or
slot cleanup. Parent agents must still actually call, wait on, and close agents
in each Tier 2/Tier 3 quorum.

## Validation

- Focused hook/admin/process tests were included in the 60-test bundle: PASS.
- Agent-process scaffold audit: PASS.
- Source/docs/data audits: PASS.
- Scaffold verification: PASS.
- `git diff --check`: PASS after final validation-record edits.
