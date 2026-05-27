# Multi-Agentic Continuation Decision Source Ledger - 2026-05-27

## Purpose

Record the source basis and local validation for extending the ESP32 default
multi-agent process with default read-only reviewer subagents, continuation
decisions, stronger advisory hooks, and committed hook behavior tests.

## Verified Facts

- `SRC-CODEX-HOOKS-2026-05-27` documents project-local hooks, hook discovery,
  trust review, `UserPromptSubmit`, `SubagentStart`, and `PreToolUse`; it also
  records that `PreToolUse` is not a complete enforcement boundary.
- `SRC-CODEX-SUBAGENTS-2026-05-27` documents built-in subagents, custom agent
  profiles, sandbox inheritance, and project-scoped agent configuration.
- `SRC-OPENAI-AGENTS-SDK-2026-05-27`,
  `SRC-OPENAI-AGENTS-ORCHESTRATION-2026-05-27`,
  `SRC-ANTHROPIC-MULTI-AGENT-RESEARCH-2026-05-27`,
  `SRC-LANGCHAIN-HANDOFFS-2026-05-27`, and
  `SRC-LANGCHAIN-CONTEXT-ENGINEERING-2026-05-27` support bounded specialist
  orchestration, context strategy, handoffs, validation, and cost/risk
  awareness.
- Local hook tests prove the repo hook scripts handle malformed and non-object
  stdin, emit valid `hookSpecificOutput` context, and warn on mutating tool
  calls when required Tier 1+ triage fields are missing.
- Local scaffold audit now executes representative hook payloads instead of
  relying only on marker checks.

## Assumptions

- Project-local read-only subagents are safe to default-authorize for Tier 2 and
  Tier 3 reviewer quorum when available, because they do not mutate files and
  closed surfaces remain closed.
- Mutating worker agents remain separate from read-only reviewer quorum and
  require explicit disjoint write scopes.

## Unknowns

- Active Codex runtime hook trust is not proven by this local repository pass.
- Future Codex hook schemas, trust UX, subagent profiles, or interception
  coverage may change.

## Local Record

- Task log: `.agents/TASK_LOG/0077-multi-agentic-continuation-decision.md`
- QA handoff:
  `.agents/handoffs/0066-multi-agentic-continuation-decision-to-qa.md`
- Hook tests: `tests/scaffold_audits/test_agent_process_hooks.py`
- Static verifier: `scripts/scaffold_audit_agent_process.py`
- Hook scripts: `.codex/hooks/*.py`

## Closed Gates

This source ledger does not authorize firmware framework selection, firmware
runtime migration, live hardware, flashing, wiring, radio changes,
serial-write expansion, relay/load/mains work, BLE, mesh, PCAP, TFT, MicroSD,
active runtime hook trust claims, hard `PreToolUse` enforcement claims, or
commit/push.
