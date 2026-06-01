# Task 0119: Development Agent Panel

Status: implemented; validated; indexed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Goal

Implement the approved Tier 2 development-agent panel in the ESP32 workspace:
read-only specialist agent profiles, config registration, prompt governance,
prompt-registry row, source ledger, task record, and scaffold audit coverage.

## Verified Facts

- The ESP32 workspace contract requires coordinator triage before every prompt.
- Tier 2 governance/config/scaffold work requires a read-only reviewer quorum
  before mutation.
- Tier 3 surfaces remain closed unless same-session evidence, explicit gate
  authority, recovery path, and closed-surface review exist.
- Existing project-local agents already covered workspace cartography, LCD
  menu UX, QA validation, evidence records, live-bench gates, source/skill
  curation, bounded implementation, governance docs, and KB records.
- The initial mutation boundary did not include `docs/index.md` or
  `knowledge-base/source-index.md`; a follow-on records-only gate now adds
  those links.

## Assumptions

- The development-agent panel is a governance/routing implementation, not a
  firmware, radio, live hardware, or release implementation.
- New profiles are read-only reviewers by default; mutating work remains routed
  through existing bounded workers with explicit disjoint write scopes.
- Future index or linkage updates remain records-only gates unless included in
  the approved mutation boundary.

## Unknowns

- Whether future Codex runtimes will expose all new project-local agents
  without a fresh config load.
- Whether future development phases need narrower hardware-family profiles.
- Whether additional future panel records should get separate source IDs.

## Reviewer Quorum

Read-only reviewer quorum approved the named Tier 2 boundary before mutation.

- Coordinator/Architecture-risk local lens, weight 5: approved.
- Governance cartographer subagent, weight 2: conditional approve.
- QA validation reviewer subagent, weight 3: conditional approve.
- Tooling/Evidence local lens, weight 3: approved.

Weighted approval: 13/13. No P1/P2 blockers remained after the work was
constrained to the approved mutation scope and existing source IDs.

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
- `knowledge-base/source-ledger/2026-05-31-development-agent-panel.md`
- this task record
- `scripts/scaffold_audit_agent_process.py`
- `tests/scaffold_audits/test_development_agent_panel.py`
- follow-on: `docs/index.md`
- follow-on: `knowledge-base/source-index.md`

## Implemented Panel Roles

- `development-panel-coordinator`
- `esp32-firmware-device-reviewer`
- `xbee-radio-protocol-reviewer`
- `ui-ux-interface-reviewer`
- `source-research-reviewer`
- `data-model-kb-reviewer`
- `tooling-resource-reviewer`
- `offgrid-comms-domain-reviewer`
- `security-safety-risk-reviewer`
- `devex-ci-release-reviewer`
- `kb-prompt-registry-curator`
- `protocol-bridge-abi-reviewer`
- `power-wiring-isolation-reviewer`

Existing profiles continue to cover workspace cartography, LCD/menu/display
review, source/evidence records, bounded code implementation, QA, hardware
bench gate review, and knowledge-record mutation.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `.codex/config.toml` and `.codex/agents/*.toml` parse check.
- Closed-surface scan.
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

## Handoff

No handoff is currently required if validation passes. Create a QA handoff only
if scaffold validation exposes a residual blocker or another owner must
continue the work.

## Closed Surfaces

Live hardware access, flashing, serial writes, RF transmit, XBee profile
writes, relay control, persistent settings writes, credential access,
destructive filesystem/device operations, external service changes, GitHub
publication, release gates, framework selection beyond accepted ADRs, and any
action where device identity or recovery path is not freshly proven remain
closed.
