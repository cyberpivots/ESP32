# Source Ledger - 2026-05-19 Expert Agent Panels

## Scope

Source-backed record for creating the global `expert-agent-panels` Codex skill
and adding ESP32 workspace prompt-routing records. This does not change
firmware, hardware profiles, relay behavior, radio behavior, framework status,
public Pages deployment, or live device operation.

## Verified facts

- `SRC-OPENAI-LATEST-MODEL`: As of the 2026-05-19 source access date, official
  OpenAI docs identify `gpt-5.5` as the current latest model and describe
  GPT-5.5 reasoning defaults and coding-agent orchestration guidance.
- `SRC-OPENAI-REASONING`: Official reasoning docs describe effort levels
  including `low`, `medium`, `high`, and `xhigh`; the panel skill maps these to
  task risk and complexity rather than treating higher effort as universally
  better.
- `SRC-CODEX-SUBAGENTS`: Official Codex subagent docs list built-in `default`,
  `worker`, and `explorer` agents and state that Codex only spawns subagents
  when explicitly asked.
- `SRC-CODEX-CONFIG-REFERENCE`: Official Codex config docs cover `skills.config`
  and agent settings; v1 of this skill stays prompt-based and does not add
  project-scoped `.codex/agents/*.toml`.
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-19`: Local inventory found system
  skills, the new global `expert-agent-panels` skill path, GitHub and Canva
  plugin skills under plugin cache hash `eed16198`, and all eight local
  DaVinci Resolve skills.

## Assumptions

- Installing the skill under `/home/cyber/.codex/skills/` is the right scope
  for future auto-discovery.
- ESP32 workspace records should point to the global skill, but the global
  skill itself remains outside the repository.
- The current task does not require a handoff because the implementation is
  self-contained.

## Unresolved gaps

- Future sessions may expose different plugin cache hashes, installed skills,
  or subagent types. Re-run the inventory before using old paths as current
  facts.
- Actual auto-discovery in a future Codex session cannot be proven from the
  current running session; the package validation only checks file structure.

## Source-index additions

- Added `SRC-OPENAI-REASONING`.
- Added `SRC-CODEX-SUBAGENTS`.
- Added `SRC-CODEX-CONFIG-REFERENCE`.
- Added `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-19`.
- Refreshed `SRC-OPENAI-LATEST-MODEL` access date to 2026-05-19.

## Workspace updates

- Added `/home/cyber/.codex/skills/expert-agent-panels/`.
- Added `docs/prompt/expert-agent-panels.md`.
- Linked the prompt doc and this ledger from `docs/index.md`.
- Updated `research/skills/available-skills.md`.
- Added `expert-agent-panel-loop` to `knowledge-base/prompt-registry.md`.
- Added `.agents/TASK_LOG/0019-expert-agent-panels-skill.md`.
