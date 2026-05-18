# Ownership Map

## Areas

- Architecture owner: `docs/architecture/`, `firmware/interfaces/`
- Hardware owner: `hardware-profiles/`, `knowledge-base/hardware/`
- Communications owner: `comm-protocols/`, `knowledge-base/comms/`
- Agent operations owner: `.agents/`, `docs/prompt/`, `knowledge-base/model-profiles.md`
- Tooling owner: `scripts/`, `tools/`, `.github/workflows/`
- QA owner: `tests/`, verification scripts, acceptance gates

## Escalation

1. Record the blocker in `research/known-gaps.md`.
2. Add a task or update the active task in `.agents/TASK_LOG/`.
3. If another owner must continue, create a handoff in `.agents/handoffs/`.
4. Do not fill the gap with inference.

