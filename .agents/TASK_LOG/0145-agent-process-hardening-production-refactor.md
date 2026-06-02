# Task 0145 - Agent-Process Hardening Production Refactor

Status: implemented; QA hardening validation complete

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing Packet

- Verified facts: Task 0144 left a repo-local Tier 2 hardening pass with
  passing audits, but reviewer inspection confirmed the managed admin hook was
  not portable when copied without its support modules. Current-session user
  direction explicitly records persistent standing authorization for
  project-local read-only subagent use in this workspace.
- Assumptions: productionizing the hardening pass means repo-local tooling,
  tests, audits, docs, and records only; temp `--target-dir` installs are
  allowed for proof, while system `/etc/codex` mutation is not.
- Unknowns: active runtime managed-hook trust, installed system Codex state, and
  future subagent availability remain outside this repo-local proof.
- Selected tier: Tier 2 governance, managed-hook tooling, audit, test, docs,
  and durable-record work.
- Owner role: Agent Operations with Tooling and QA.
- Evidence need: required governance-file reread, read-only reviewer quorum,
  source inspection, temp-target install smoke, focused unit tests, scaffold
  audits, durable-record audit, publication hygiene report, scheduler self-test,
  scaffold verification, `git diff --check`, and final git status.
- Mutation boundary: repo-local `.codex`, `.agents`, `scripts`, `tests`,
  `.github/workflows`, `docs`, and `knowledge-base` only. No firmware behavior,
  live hardware, serial/COM, RF/XBee, relay/load/mains, `/etc/codex`, destructive
  git, external publication, commit, push, PR, release, or deploy mutation.
- Validation plan: close reviewer P1s with support-module installation,
  `--target-dir`, installed-hook smoke without repo `PYTHONPATH`, structured
  classifier tests, admin installer tests, scaffold audits, and final status.
- Trust boundary: hooks remain advisory under `permission_mode=bypassPermissions`;
  source records and explicit gate authority remain authoritative.

## Reviewer Quorum

- Development panel coordinator, weight 5: conditional approve for repo-local
  mutation; no P1/P2 blockers.
- Tooling reviewer, weight 3: conditional approve for mutation; P1 blockers for
  installed-hook portability, missing `--target-dir`, and missing temp install
  audit coverage.
- QA reviewer, weight 3: blocked production acceptance until installed-runtime
  portability is fixed and covered by sanitized temp-installed-hook tests.
- Evidence-record auditor, weight 3: conditional approve for Task 0145,
  Handoff 0106, source ledger, docs index, source index, and scaffold data.

Disposition: bounded mutation proceeded only to close the named P1 blockers and
record conditions. Lifecycle state listing was unavailable before spawning;
four read-only reviewers were spawned, all outputs were captured, and all
reviewers were closed before mutation.

## QA Review Addendum

- Tooling reviewer, weight 3: rejected the portability gate for a P2 import
  precedence issue where an ambient fallback `scripts/` directory could outrank
  installed sibling support modules.
- QA reviewer, weight 3: rejected the validation gate for a P2 boundary issue
  where scaffold audit dry-runs used the installer default `/etc/codex` target
  instead of a temp `--target-dir`.
- Evidence-record auditor, weight 3: no P1/P2 findings; P3 status/removal
  wording cleanup recommended.
- Security/safety reviewer, weight 3: no P1/P2 findings; P3 notes about
  advisory-only non-Tier3 risky command handling and no-space `/etc/codex`
  redirection classification.
- Development panel coordinator, weight 5: no P1/P2 findings; P3 alignment
  requested so every-prompt hook text includes safe non-trivial Tier 1 subagent
  attempts.

Disposition: current-session mutation closed the two P2 blockers and the named
P3 process/record hygiene items. Five read-only reviewers reported, outputs were
captured, and `close_agent` was called for all five reviewers before final
decision.

## Implementation Summary

- Added `scripts/agent_process_contracts.py` for shared contract IDs, compact
  routing/subagent/bypass/lifecycle text, and shared marker lists.
- Updated project-local hooks and the admin managed hook to import shared
  contract text.
- Made `.codex/admin/hooks/esp32_admin_policy.py` prefer sibling support
  modules when installed, with repo `scripts` as source-tree fallback.
- Replaced `.codex/admin/install_admin_policy.py` with a target-layout based
  installer supporting `--target-dir PATH`, defaulting to `/etc/codex`.
- Installer dry-run, install, validate, and remove reporting now includes the
  requirements file, managed hook, `agent_process_classifiers.py`, and
  `agent_process_contracts.py` with hashes, modes, owners, diffs, and backups.
- Added structured `ClassificationResult` and classifier functions while
  preserving existing boolean wrappers.
- Extended unit and scaffold audits to prove temp install, validate, removal,
  support hash/mode drift detection, and installed-hook execution without repo
  `PYTHONPATH`.
- Updated admin docs, instruction-surface map, docs index, source index,
  scaffold audit data, task log, handoff, and source ledger.
- Persisted standing user authorization for project-local read-only subagent use
  in `AGENTS.md`, governance/role docs, agent coordination docs, instruction
  surface map, admin README, shared hook contract text, and hook/audit tests.
- Forced the managed admin hook to keep its installed hook directory at the
  front of `sys.path`, even when Python preloads that directory, so sibling
  support modules outrank any ambient fallback `scripts/` directory.
- Changed scaffold audit admin dry-runs to use temp `--target-dir` paths rather
  than the installer default `/etc/codex` target.
- Strengthened copied-hook smoke coverage with stale fallback support modules,
  installed-copy `PreToolUse` denial, and installed-copy
  `bypassPermissions` no-op fixtures.
- Added no-space `/etc/codex` redirection classification coverage and made temp
  removal output say `removed target requirements`.

## Sources

- `SRC-LOCAL-AGENT-INSTRUCTION-SKILL-HOOK-CI-HARDENING-2026-06-02`
- `SRC-LOCAL-AGENT-PROCESS-HARDENING-PRODUCTION-REFACTOR-2026-06-02`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_classifiers tests.scaffold_audits.test_agent_process_hooks tests.scaffold_audits.test_admin_policy_hooks`
  (36 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_admin_policy_hooks tests.scaffold_audits.test_agent_process_classifiers`
  (27 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (97 tests).
- PASS: temp install smoke: installed yolo-compatible into a temp
  `--target-dir`, executed copied `esp32_admin_policy.py` with `PYTHONPATH`
  cleared from outside the repo, validated, removed the temp requirements file,
  confirmed `requirements.toml` was absent, and removed the temp directory.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --dry-run --profile yolo-compatible`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --dry-run --profile admin-strict`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`.
  Report showed branch `main`, upstream `origin/main`, ahead `0`, behind `0`,
  no open PRs, no local `codex/*` branches, and no remote `codex/*` branches;
  dirty entries are the expected repo-local files from Task 0144 and Task 0145.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.
- PASS: `git status --short --branch --untracked-files=all` showed
  `main...origin/main`, no ahead/behind divergence, and the expected dirty
  repo-local hardening files.

## Authority Limits

No `/etc/codex` mutation, admin-strict install, live hardware, COM/serial
access, flashing, monitor, serial writes, RF/XBee writes, relay/load/mains,
wiring mutation, firmware behavior changes, destructive git, GitHub
publication, release, commit, push, PR creation, Pages deployment, or external
service mutation is authorized by this task.

## Decision Footer

Decision: complete. Next gate: none for the named Task 0145 QA/tooling review.
Owner role: QA with Tooling and Agent Operations. Evidence: reviewer quorum with
lifecycle cleanup, repo-local implementation, temp install smoke, focused tests,
full scaffold-audit discovery, scaffold audits, durable records, publication
hygiene report, scaffold verification, `git diff --check`, and git status.
Durable records: this task log, Handoff 0106, source ledger, source-index row,
docs-index links, and scaffold audit data entries. Authority limits: no live
hardware, `/etc/codex`, admin-strict install, destructive git, commit, push, PR,
release, deploy, or publication authority.

## Handoff

Handoff: [.agents/handoffs/0106-agent-process-hardening-production-refactor-to-qa-tooling.md](../handoffs/0106-agent-process-hardening-production-refactor-to-qa-tooling.md)
