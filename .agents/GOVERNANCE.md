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

## Validation gates

- Documentation links: every required document must be reachable from
  `docs/index.md`.
- Source gate: hardware claims must have source coverage in
  `knowledge-base/source-index.md`.
- Framework gate: no framework files may appear until ADR-0001 is accepted.
- Handoff gate: non-trivial work must leave a task record.

## Current status

- Repository status: scaffold initialized, no firmware implementation.
- Framework status: workspace-neutral; `four-relay-xbee-wifi` has an accepted
  ESP-IDF v6.0.1 target in ADR-0002.
- Hardware status: photographed `four-relay-xbee-wifi` target profiles added;
  physical bench verification pending.
