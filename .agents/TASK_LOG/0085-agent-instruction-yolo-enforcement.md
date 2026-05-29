# Task 0085: Agent Instruction Yolo Enforcement

## Routing Packet

## Verified Facts

- The user requested enforcement using agent instruction files.
- `AGENTS.md` is the canonical workspace operating contract.
- `.codex/agents/*.toml` contains developer instructions for project-local
  Codex agent profiles.
- `/etc/codex/requirements.toml` remains absent during this task.

## Assumptions

- The requested enforcement means repo-local instruction-file enforcement by
  default, not machine-level requirements that override launch-time flags.
- The yolo-compatible operator-sovereignty rule should be inherited by every
  project-local agent profile.

## Unknowns

- Future Codex releases may change which project-local instruction files are
  loaded for custom agents.

## Selected Tier

Tier 2 governance and agent-instruction update.

## Owner Role

Agent Operations with QA and Tooling review.

## Evidence Need

Local instruction files, scaffold audit, docs audit, hook/profile tests, and
system requirements absence check.

## Mutation Boundary

`AGENTS.md`, `.agents/`, `.codex/agents/*.toml`, governance/prompt docs,
source records, task log, handoff, and `scripts/scaffold_audit_agent_process.py`.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_admin_policy_hooks.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `/etc/codex/requirements.toml` absence check
- `git diff --check`

## Reviewer Quorum

| Role | Weight | Vote | P1/P2 blockers | Conditions |
| --- | ---: | --- | --- | --- |
| Governance cartographer | 5 | Approve | None | Make `AGENTS.md` canonical and explicit. |
| QA/tooling reviewer | 3 | Approve | None | Add scaffold audit coverage for all agent profiles. |
| Prompt-token triage | 2 | Approve | None | Keep the instruction concise and inherited by agents. |

Disposition: proceed with bounded instruction-file enforcement.

## Implementation Summary

- Added an Agent Instruction Enforcement Boundary section to `AGENTS.md`.
- Added operator-sovereignty instructions to every `.codex/agents/*.toml`
  profile.
- Updated `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`, prompt docs, source
  records, and docs index.
- Extended `scripts/scaffold_audit_agent_process.py` so every project-local
  agent profile must include the yolo/operator-sovereignty instruction markers.

## Validation Results

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_admin_policy_hooks.py`
  (`Ran 11 tests`).
- PASS: `/etc/codex/requirements.toml` absence check.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (`Ran 20 tests`).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `git diff --check`.

## Authority Limits

No firmware/runtime/API/ABI/framework changes, flashing, erase, monitor,
serial-write expansion, BLE/live mesh, PCAP, router/admin mutation, relay,
XBee, TFT, MicroSD, load, mains, wiring, release gates, or live bench work is
authorized by this task.
