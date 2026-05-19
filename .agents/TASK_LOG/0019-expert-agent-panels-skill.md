# Task Log 0019 - Expert Agent Panels Skill

## Task

- ID: 0019-expert-agent-panels-skill
- Owner role: Agent operations
- Status: complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Create a global Codex skill named `expert-agent-panels` and record the
ESP32-specific prompt-routing, source, and skill-inventory evidence needed to
use it safely in this workspace.

## Scope

Included:

- Global skill package under `/home/cyber/.codex/skills/expert-agent-panels/`.
- Official OpenAI and Codex source references for latest model, reasoning,
  subagents, and config behavior.
- Updated ESP32 skill inventory, prompt registry, prompt doc, source index, and
  source ledger.
- Forward-test review of the skill documentation with a read-only explorer
  subagent.

Excluded:

- Firmware, framework, hardware, relay, radio, MicroSD, TFT, or live-device
  changes.
- Project-scoped `.codex/agents/*.toml`.
- Commit, push, deployment, or public Pages artifact publishing.

## Sources

- `SRC-OPENAI-LATEST-MODEL`
- `SRC-OPENAI-REASONING`
- `SRC-CODEX-SUBAGENTS`
- `SRC-CODEX-CONFIG-REFERENCE`
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-19`

## Decisions

- Keep v1 panel specialization prompt-based instead of adding project-local
  custom-agent TOML files.
- Spawn subagents only when the current user request explicitly authorizes
  subagents, delegation, parallel agents, or an agent panel.
- Re-inventory skills in future sessions because plugin cache hashes and
  installed skills can change.

## Validation

- `python3 /home/cyber/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/cyber/.codex/skills/expert-agent-panels` - pass.
- `python3 scripts/verify_scaffold.py` - pass.
- `git diff --check` - pass.
- Read-only explorer forward-test of `$expert-agent-panels` against
  `docs/prompt/` - complete; findings about read-only record updates,
  worker-agent boundaries, date-qualified model claims, and local-state
  evidence priority were addressed in the skill and workspace docs.

## Handoff

No handoff required unless a later task asks to wire this skill into a specific
repo automation or CI gate.
