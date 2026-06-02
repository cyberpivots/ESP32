# Task 0144 - Agent Instruction, Skill, Hook, CI Hardening

Status: implemented and validated; QA/Tooling handoff ready

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing Packet

- Verified facts: the user provided a ready-for-mutation Tier 2 plan for
  repo-local instruction, skill, hook, audit, CI, and record hardening; current
  governance requires reviewer quorum before Tier 2 mutation; no live hardware,
  `/etc/codex`, destructive git, commit, push, or PR authority was granted.
- Assumptions: the plan's named source basis is acceptable, but current repo
  files and official Codex docs must be re-read before edits.
- Unknowns: active runtime hook trust and future subagent availability remain
  outside static repo control; plugin cache paths are local and drift-prone.
- Selected tier: Tier 2 governance, hook/config, audit, CI, source-record, and
  broad instruction-surface work.
- Owner role: Agent Operations with Tooling, QA, Evidence Records, Source Skill
  Curation, and DevEx/Release lenses.
- Evidence need: same-session repo inspection, read-only reviewer quorum,
  official Codex docs refresh, skill inventory, focused tests, scaffold audits,
  publication hygiene report, durable records, and final git status.
- Mutation boundary: repo-local `.codex`, `.agents`, `scripts`, `tests`,
  `.github/workflows`, `docs`, `research/skills`, and `knowledge-base` records
  only. No firmware runtime behavior, live bench, serial/RF writes,
  relay/load/mains, `/etc/codex`, admin-strict install, destructive git,
  external service mutation, commit, push, PR, release, or Pages publication.
- Validation plan: focused hook/admin/classifier tests, full scaffold-audit
  unittest discovery, agent-process audit, skill audit, durable-record audit,
  publication hygiene JSON, scheduler self-test, scaffold verification,
  `git diff --check`, and final `git status`.

## Reviewer Quorum

- Coordinator/development panel, weight 5: no P1/P2 blockers for mutation
  inside the repo-local boundary; required contract IDs and disjoint write
  scopes.
- Tooling reviewer, weight 3: no P1 blockers; P2s for shared classifier parity,
  direct classifier tests, import mechanics, and publication hygiene.
- QA reviewer, weight 3: no P1 blockers; rejected acceptance until CI, direct
  classifier tests, skill audit, durable-record audit, and admin dry-run
  coverage were implemented.
- Source-skill curator, weight 3: no P1 blockers; P2s for stale plugin cache
  inventory and missing `xbee-radio-integration` config.
- DevEx/CI/release reviewer, weight 3: no P1 blockers; P2s for non-deploy PR
  CI and `git diff --check` coverage.
- Evidence-record auditor output focused on an unrelated PF0530W live lane; it
  was retained only as an authority-limit reminder for no live hardware or
  publication claims.

Weighted disposition for this mutation boundary: the relevant same-session
reviewer set identified no P1 blockers; P2 findings were accepted as mandatory
implementation items before final acceptance. Lifecycle state listing was not
available before spawning reviewers; six reviewers were spawned, outputs were
captured, and all spawned agents were closed before mutation.

## Implementation Summary

- Added shared stdlib-only hook and text classifier helpers in
  `scripts/agent_process_classifiers.py`.
- Refactored project-local and managed admin hooks to use the shared
  classifier module.
- Compacted hook and agent-profile instruction surfaces with contract IDs:
  `ESP32-GOV-v1`, `SOV-v1`, `LIFECYCLE-v1`, and `TIER3-CLOSED-v1`.
- Added direct classifier tests and updated local/admin hook parity tests.
- Refreshed skill inventory to plugin cache hash `90718987`, marked plugin
  paths drift-prone, and enabled `xbee-radio-integration` in `.codex/config.toml`.
- Added `scripts/scaffold_audit_skills.py`,
  `scripts/scaffold_audit_records.py`, and `scripts/git_publication_hygiene.py`.
- Added non-deploy `scaffold-ci.yml` and hardened Pages validation with
  `git diff --check` plus scaffold-audit unittest discovery.
- Added `docs/instruction-surface-map.md` and publication hygiene docs.
- Added source-index, source-ledger, task, and handoff records.

## Sources

- `SRC-CODEX-SKILLS-2026-06-02`
- `SRC-CODEX-AGENTS-MD-2026-06-02`
- `SRC-CODEX-HOOKS-2026-06-02`
- `SRC-CODEX-MANAGED-CONFIG-2026-06-02`
- `SRC-CODEX-SUBAGENTS-2026-06-02`
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-02`
- `SRC-LOCAL-AGENT-INSTRUCTION-SKILL-HOOK-CI-HARDENING-2026-06-02`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_classifiers tests.scaffold_audits.test_agent_process_hooks tests.scaffold_audits.test_admin_policy_hooks`
  (31 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (92 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`.
  Report showed branch `main`, upstream `origin/main`, ahead `0`, behind `0`,
  no open PRs, no local `codex/*` branches, and no remote `codex/*` branches;
  dirty entries were the expected files from this task.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.
- PASS: `git status --short --branch --untracked-files=all` showed
  `main...origin/main`, no ahead/behind divergence, and only this task's
  modified/untracked files.

## Authority Limits

No `/etc/codex` mutation, admin-strict install, live hardware, COM/serial
access, flashing, monitor, serial writes, RF/XBee writes, relay/load/mains,
wiring mutation, firmware behavior changes, destructive git, GitHub
publication, release, commit, push, PR creation, or Pages deployment is
authorized by this task.

## Decision Footer

Decision: handoff. Next gate: QA/Tooling review of the implemented Tier 2
hardening pass. Owner role: QA with Tooling and Agent Operations. Evidence:
same-session reviewer quorum, official Codex docs refresh, skill inventory,
source ledger, focused tests, scaffold-audit discovery, agent/skill/record
audits, publication hygiene report, scheduler self-test, scaffold verification,
`git diff --check`, and final git status. Approved mutation boundary:
repo-local instructions/hooks/skills/audits/CI/docs/records only. Durable
records: this task log, Handoff 0105, source ledger, source-index rows, and
docs-index links. Authority limits: no live hardware, `/etc/codex`,
admin-strict install, destructive git, commit, push, PR, release, deploy, or
publication authority.

## Handoff

Handoff: [.agents/handoffs/0105-agent-instruction-skill-hook-ci-hardening-to-qa-tooling.md](../handoffs/0105-agent-instruction-skill-hook-ci-hardening-to-qa-tooling.md)
