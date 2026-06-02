# Agent Instruction, Skill, Hook, CI Hardening Ledger

Source ID:
`SRC-LOCAL-AGENT-INSTRUCTION-SKILL-HOOK-CI-HARDENING-2026-06-02`

Date: 2026-06-02

## Scope

This ledger records the Tier 2 repo-local hardening pass for Codex instruction
surfaces, hook classifiers, skills, scaffold audits, CI validation, publication
hygiene, durable records, and source-backed documentation.

## Verified Facts

- Read-only reviewer quorum was attempted with project-local subagents before
  mutation; six reviewers were spawned, results were captured, and reviewers
  were closed before mutation proceeded.
- No P1 blockers were found for the repo-local hardening boundary.
- P2 implementation items were treated as mandatory: hook classifier parity,
  direct classifier tests, skill inventory drift, `xbee-radio-integration`
  config, CI scaffold-audit coverage, durable-record auditing, and publication
  hygiene.
- Official Codex docs were refreshed in-session for skills, `AGENTS.md`, hooks,
  managed configuration, and subagents using `SRC-CODEX-SKILLS-2026-06-02`,
  `SRC-CODEX-AGENTS-MD-2026-06-02`, `SRC-CODEX-HOOKS-2026-06-02`,
  `SRC-CODEX-MANAGED-CONFIG-2026-06-02`, and
  `SRC-CODEX-SUBAGENTS-2026-06-02`.
- Same-session local skill inventory recorded system skills, user skills,
  ESP32-local skills, and plugin cache hash `90718987` in
  `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-02`.

## Files

- `scripts/agent_process_classifiers.py`
- `.codex/hooks/pre_tool_use_agent_process.py`
- `.codex/hooks/user_prompt_submit_agent_process.py`
- `.codex/hooks/subagent_start_agent_process.py`
- `.codex/hooks/subagent_stop_agent_process.py`
- `.codex/admin/hooks/esp32_admin_policy.py`
- `.codex/agents/*.toml`
- `.codex/config.toml`
- `scripts/scaffold_audit_agent_process.py`
- `scripts/scaffold_audit_skills.py`
- `scripts/scaffold_audit_records.py`
- `scripts/git_publication_hygiene.py`
- `scripts/verify_scaffold.py`
- `tests/scaffold_audits/test_agent_process_classifiers.py`
- `tests/scaffold_audits/test_agent_process_hooks.py`
- `tests/scaffold_audits/test_admin_policy_hooks.py`
- `.github/workflows/scaffold-ci.yml`
- `.github/workflows/pages.yml`
- `.github/workflows/README.md`
- `docs/instruction-surface-map.md`
- `docs/agent-coordination.md`
- `docs/github-pages-public-site.md`
- `.agents/GOVERNANCE.md`
- `research/skills/available-skills.md`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0144-agent-instruction-skill-hook-ci-hardening.md`
- `.agents/handoffs/0105-agent-instruction-skill-hook-ci-hardening-to-qa-tooling.md`

## Validation

Validation is recorded in Task 0144. Required checks include focused
hook/admin/classifier tests, full scaffold-audit unittest discovery,
agent-process audit, skill audit, durable-record audit, publication hygiene
JSON report, scheduler self-test, scaffold verification, `git diff --check`,
and final git status.

## Closed Surfaces

This record does not authorize `/etc/codex` mutation, admin-strict
installation, live hardware, COM/serial access, flashing, monitor, serial
writes, RF/XBee writes, relay/load/mains work, wiring mutation, firmware
behavior changes, destructive git, GitHub publication, release, commit, push,
or PR creation.
