# Expert Agent Panels

## Source basis

This guidance references `SRC-OPENAI-LATEST-MODEL`,
`SRC-OPENAI-REASONING`, `SRC-CODEX-SUBAGENTS`,
`SRC-CODEX-CONFIG-REFERENCE`, and
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-19`.

## Intent

Use the global `$expert-agent-panels` skill when a task needs a specialist
review loop that can inspect workspace truth, inventory skills, close knowledge
gaps, perform source-backed research, choose a bounded next action, validate
the result, and update durable records.

## Verified facts

- As of the source access date in `knowledge-base/source-index.md`, official
  OpenAI model guidance identifies `gpt-5.5` as the current latest model and
  describes `medium` reasoning as the balanced default for GPT-5.5.
- Official reasoning guidance lists `low`, `medium`, `high`, and `xhigh`
  reasoning effort as workload-tuning levels and reserves higher effort for
  harder, higher-value, or longer-running work.
- Official Codex subagent guidance says Codex uses built-in `default`,
  `worker`, and `explorer` agents and only spawns subagents when explicitly
  asked.
- Official Codex configuration guidance documents project/user config,
  `skills.config`, and agent settings; this workspace does not need a
  project-scoped `.codex/agents/*.toml` file for the v1 panel skill.
- The verified local skill inventory for this pass uses plugin cache hash
  `eed16198`; older plugin cache hashes are stale for this session.

## Assumptions

- The skill is installed under `/home/cyber/.codex/skills/` so future Codex
  sessions can discover it globally.
- ESP32 workspace records capture the project-specific prompt routing and
  source evidence, but no firmware, hardware, relay, radio, or framework
  behavior changes are implied by this prompt.

## Unknowns

- Future sessions may expose additional skills, plugins, MCP servers, or
  subagent types. Run a fresh inventory before relying on the list in this
  document.

## Prompt pattern

```text
Use $expert-agent-panels to run an expert panel review and improvement loop for
this task. Read the workspace contract first, inventory available skills,
separate verified facts from assumptions and unknowns, use official or primary
sources for missing facts, spawn subagents only when explicitly authorized, then
implement the best bounded action and validate it.
```

## Expected output

- Workspace map and active contract.
- Skill inventory marked relevant, conditional, or irrelevant.
- Knowledge gaps with source or probe paths.
- Source-backed findings.
- Implementation or no-mutation recommendation.
- Validation evidence.
- Source-index, source-ledger, prompt-registry, and task-log updates when the
  workspace contract requires durable records.
