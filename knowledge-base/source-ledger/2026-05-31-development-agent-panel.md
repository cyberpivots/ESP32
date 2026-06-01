# Development Agent Panel Source Ledger - 2026-05-31

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-CODEX-SUBAGENTS-2026-05-27`
- `SRC-CODEX-CONFIG-REFERENCE-2026-05-27`
- `SRC-OPENAI-AGENTS-SDK-2026-05-27`
- `SRC-OPENAI-AGENTS-ORCHESTRATION-2026-05-27`
- `SRC-ANTHROPIC-MULTI-AGENT-RESEARCH-2026-05-27`
- `SRC-LANGCHAIN-HANDOFFS-2026-05-27`
- `SRC-LANGCHAIN-CONTEXT-ENGINEERING-2026-05-27`
- `SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27`
- `SRC-LOCAL-MULTI-AGENTIC-CONTINUATION-DECISION-2026-05-27`
- `SRC-LOCAL-AGENT-INSTRUCTION-YOLO-ENFORCEMENT-2026-05-28`
- `SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`
- `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`
- `SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31`

## Purpose

Record the source basis for the Tier 2 development-agent panel implementation:
project-local read-only specialist profiles, config registration, prompt
registry row, scaffold audit coverage, and durable task record.

This ledger first reused existing source IDs. A follow-on records-only gate now
adds docs-index and source-index linkage for
`SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31`.

## Verified Facts

- [repo-verified] `AGENTS.md` remains the canonical contract for tier
  selection, reviewer quorum, operator sovereignty, and Tier 3 prerequisites.
- [repo-verified] `.codex/config.toml` now registers read-only panel profiles
  for coordinator, firmware/device, XBee/radio, UI/UX, source research,
  data/KB, tooling, off-grid communications, security/safety, DevEx/release,
  KB/prompt curation, protocol/bridge ABI, and power/wiring/isolation review.
- [repo-verified] Existing roles continue to cover workspace cartography,
  LCD/menu review, bounded implementation, QA, and live-bench gate review.
- [repo-verified] Each new profile is read-only and defines purpose, inputs,
  outputs, read scope, later mutation scope, stop conditions, escalation
  conditions, required evidence, validation method, and tier boundaries.
- [repo-verified] The panel keeps LCD/UI intents separate from RF, relay,
  flash, serial-write, persistent-config, credential, external-service, and
  GitHub-publication actions.
- [repo-verified] Scaffold audit coverage now requires the new profile files,
  config registrations, structured boundary markers, prompt-registry marker,
  this source ledger, and the task record.
- [repo-verified] A follow-on records-only gate links the task record and this
  source ledger from `docs/index.md` and adds
  `SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31` to
  `knowledge-base/source-index.md`.

## Assumptions

- The panel is a governance and routing surface; it does not itself implement
  firmware runtime behavior, live hardware access, RF behavior, relay control,
  persistent writes, or external service changes.
- Future mutations may use the panel profiles as read-only reviewers, but
  write work still requires explicit disjoint worker scopes.
- Future source-index or docs-index edits remain separate records-only gates
  unless included in an approved mutation boundary.

## Unknowns

- Whether future Codex runtimes will expose all project-local agents without a
  fresh config reload.
- Whether future tasks will need additional specialist profiles for a narrower
  hardware family or external integration.
- Whether additional future panel records should get separate source IDs.

## Reviewer Quorum

Read-only reviewer quorum and local role lenses approved the named Tier 2
boundary before mutation.

- Coordinator/Architecture-risk local lens, weight 5: approved.
- Governance cartographer subagent, weight 2: conditional approve.
- QA validation reviewer subagent, weight 3: conditional approve.
- Tooling/Evidence local lens, weight 3: approved.

Weighted approval: 13/13. No P1/P2 blockers remained after constraining the
work to the allowed mutation scope and reusing existing source IDs.

Follow-on records-linkage quorum:

- Coordinator/Architecture-risk local lens, weight 5: approved.
- Evidence Records subagent, weight 2: conditional approve.
- QA validation subagent, weight 3: conditional approve.

Weighted approval: 10/10. No P1/P2 blockers remained for adding docs-index and
source-index linkage inside the four-file records-only boundary.

## Mutation Boundary

- `.codex/agents/`
- `.codex/config.toml`
- `docs/prompt/expert-agent-panels.md`
- `knowledge-base/prompt-registry.md`
- this source ledger
- `.agents/TASK_LOG/0119-development-agent-panel.md`
- `scripts/scaffold_audit_agent_process.py`
- `tests/scaffold_audits/test_development_agent_panel.py`
- follow-on: `docs/index.md`
- follow-on: `knowledge-base/source-index.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `.codex/config.toml` and `.codex/agents/*.toml` parse check.
- Closed-surface scan for live hardware, flash, serial-write, RF, relay,
  persistent-config, credential, destructive-operation, external-service, and
  GitHub-publication authority.
- `rg -n "0119-development-agent-panel|2026-05-31-development-agent-panel" docs/index.md`
- `rg -n "SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31|2026-05-31-development-agent-panel" knowledge-base/source-index.md`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `git diff --check`

## Validation

- PASS: `.codex/config.toml` and `.codex/agents/*.toml` parse check.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_development_agent_panel` (3 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (52 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: closed-surface scan confirmed the changed files preserve live hardware,
  flash, serial-write, RF, relay, persistent-config, credential, destructive,
  external-service, GitHub-publication, and Tier 3 stop-gate language.
- PASS: `rg -n "0119-development-agent-panel|2026-05-31-development-agent-panel" docs/index.md`
- PASS: `rg -n "SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31|2026-05-31-development-agent-panel" knowledge-base/source-index.md`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `git diff --check`

## Stop Gates

This record does not authorize live hardware access, flashing, serial writes,
RF transmit, XBee profile writes, relay control, persistent settings writes,
credential access, destructive filesystem/device operations, external service
changes, GitHub publication, release gates, framework selection beyond
accepted ADRs, or any action where device identity or recovery path is not
freshly proven.
