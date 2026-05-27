# Workspace Governance

## Decision policy

- User intent is authoritative.
- Technical decisions are recorded as ADRs in `.agents/DECISIONS/`.
- A decision is not accepted until the ADR status is `Accepted`.
- Framework, protocol, board, pinout, and safety decisions require source-backed
  evidence or an explicit unresolved-gap note.

## Branch and review policy

- Default branch: `main`.
- Feature branches should use `codex/<short-purpose>` or a human-selected name.
- Changes that touch hardware profiles, firmware interfaces, CI, or governance
  require review by the relevant owner in `.agents/OWNERSHIP.md`.

## Multi-agent operating policy

- Every prompt starts with coordinator triage against the four-tier process in
  `AGENTS.md`.
- Tier 0 prompts may remain read-only and single-agent after classification.
- Tier 1 prompts require the relevant owner lens and QA lens before mutation.
- Tier 2 prompts require a read-only reviewer quorum before mutation for
  governance, protocol, firmware, evidence, hook/config, or broad code work.
- Tier 3 prompts require explicit gate authority and same-session live evidence
  before any live bench, flashing, wiring, radio, serial-write, relay/load/mains,
  release-gate, or equivalent risky mutation.
- Project-local Codex hooks and custom agents are advisory enforcement aids
  unless reviewed and trusted by the active Codex runtime.
- If subagents are unavailable, unsafe, or not explicitly authorized, run the
  same role perspectives locally and record that no subagents were spawned.

## Validation gates

- Documentation links: every required document must be reachable from
  `docs/index.md`.
- Source gate: hardware claims must have source coverage in
  `knowledge-base/source-index.md`.
- Framework gate: no framework files may appear until ADR-0001 is accepted,
  except project-local framework files explicitly authorized by an accepted
  project ADR.
- Handoff gate: non-trivial work must leave a task record.
- Agent-process gate: project-local `.codex` hooks, agent profiles, and prompt
  process records must pass `scripts/scaffold_audit_agent_process.py` before
  the scaffold is considered valid.

## Current status

- Repository status: scaffold initialized, no firmware implementation.
- Framework status: workspace-neutral; `four-relay-xbee-wifi` has an accepted
  ESP-IDF v6.0.1 target in ADR-0002.
- Hardware status: photographed `four-relay-xbee-wifi` target profiles added;
  physical bench verification pending.
- Agent-process status: tiered multi-agent triage is the default workspace
  process; project-local Codex hooks remain trust-gated runtime aids.
