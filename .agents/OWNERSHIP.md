# Ownership Map

## Areas

- Architecture owner: `docs/architecture/`, `firmware/interfaces/`
- Hardware owner: `hardware-profiles/`, `knowledge-base/hardware/`
- Communications owner: `comm-protocols/`, `knowledge-base/comms/`
- Agent operations owner: `.agents/`, `.codex/`, `docs/prompt/`,
  `knowledge-base/model-profiles.md`, `knowledge-base/prompt-registry.md`
- Tooling owner: `scripts/`, `tools/`, `.github/workflows/`,
  project-local hook scripts
- QA owner: `tests/`, verification scripts, acceptance gates,
  `scripts/scaffold_audit_agent_process.py`

## Multi-agent review ownership

- Coordinator triage owner: Agent operations.
- Reviewer quorum owner: QA, with the relevant area owner for the selected tier.
- Worker-agent scope owner: the area owner whose files are in the explicit write
  boundary.
- Hook trust follow-up owner: QA and Tooling.

## Escalation

1. Record the blocker in `research/known-gaps.md`.
2. Add a task or update the active task in `.agents/TASK_LOG/`.
3. If another owner must continue, create a handoff in `.agents/handoffs/`.
4. Do not fill the gap with inference.
