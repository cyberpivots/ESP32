# Multi-Agentic Default Process Source Ledger - 2026-05-27

## Purpose

Record the source basis for making tiered coordinator triage and role-lens
review the default ESP32 workspace process, with project-local Codex hooks and
custom agent profiles as advisory aids.

## Verified Facts

- `SRC-CODEX-HOOKS-2026-05-27` documents project-local hooks, hook discovery,
  hook trust review, `UserPromptSubmit`, `SubagentStart`, and `PreToolUse`.
- `SRC-CODEX-HOOKS-2026-05-27` also documents that `PreToolUse` is a guardrail
  rather than a complete enforcement boundary.
- `SRC-CODEX-SUBAGENTS-2026-05-27` documents built-in `default`, `worker`, and
  `explorer` agents, project-scoped custom agents, explicit subagent spawning,
  sandbox inheritance, and global `agents.max_threads` / `agents.max_depth`.
- `SRC-CODEX-CONFIG-REFERENCE-2026-05-27` documents project-scoped
  `.codex/config.toml`, agent profile config files, `skills.config`, hook
  configuration, and project-local config limitations.
- `SRC-OPENAI-AGENTS-SDK-2026-05-27` and
  `SRC-OPENAI-AGENTS-ORCHESTRATION-2026-05-27` document agent orchestration,
  specialist collaboration, handoffs, and manager-controlled agents-as-tools.
- `SRC-ANTHROPIC-MULTI-AGENT-RESEARCH-2026-05-27` supports using multi-agent
  systems for valuable, parallel, high-context work and warns about increased
  coordination complexity and token cost.
- `SRC-LANGCHAIN-HANDOFFS-2026-05-27` and
  `SRC-LANGCHAIN-CONTEXT-ENGINEERING-2026-05-27` support state-aware handoffs,
  explicit context engineering, incremental testing, monitoring, and documented
  context strategy.
- `SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27` records the local files
  changed for the ESP32 default multi-agent process.

## Assumptions

- The project wants tiered triage for every prompt while avoiding automatic
  fan-out for trivial work.
- Runtime subagent spawning is optional and depends on explicit authority,
  safety, and available tools.

## Unknowns

- Whether future Codex releases change hook schemas, trust UX, subagent profile
  fields, or interception coverage.
- Whether future project work needs stricter managed hooks outside this repo;
  this task intentionally avoids global machine config.

## Local Record

- Task log: `.agents/TASK_LOG/0074-multi-agentic-default-process.md`
- QA handoff: `.agents/handoffs/0063-multi-agentic-default-process-to-qa.md`
- Hook config: `.codex/hooks.json`
- Static verifier: `scripts/scaffold_audit_agent_process.py`

## Closed Gates

This source ledger does not authorize firmware framework selection, firmware
runtime migration, live hardware, flashing, wiring, radio changes, serial-write
expansion, relay/load/mains work, BLE, mesh, PCAP, TFT, MicroSD, or commit/push.
