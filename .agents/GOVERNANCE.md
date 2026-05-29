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
  Project-local read-only subagents are default-authorized when available and
  safe.
- Tier 3 prompts require explicit gate authority and same-session live evidence
  before any live bench, flashing, wiring, radio, serial-write, relay/load/mains,
  release-gate, or equivalent risky mutation.
- For Tier 2 and Tier 3 gates, a no-P1/P2 reviewer quorum may approve only the
  named gate and mutation boundary. Gate acceptance does not imply firmware
  runtime, live bench, flash, serial-write, radio, relay/load/mains, release, or
  other closed-surface authority unless that authority is named in the routing
  packet.
- Project-local Codex hooks and custom agents are advisory enforcement aids
  unless reviewed and trusted by the active Codex runtime.
- Agent instruction files are the default enforcement surface:
  `AGENTS.md` is canonical, `.codex/agents/*.toml` must inherit it, and audits
  must fail if agent profiles omit the operator-sovereignty rule. Do not use
  `/etc/codex/requirements.toml` as the default enforcement path for this repo.
- Codex managed-hook profiles for this machine are sourced from
  `.codex/admin/`. The default yolo-compatible profile must not set
  `allowed_sandbox_modes`, `allowed_approval_policies`, or restrictive prefix
  rules, so a user-launched `codex --yolo` session keeps
  `danger-full-access`, `approval_policy=never`, and the intended permission
  mode. The optional `admin-strict` profile may constrain those launch choices;
  it is explicit opt-in only.
- Weighted veto is the default gate model. Coordinator or architecture-risk
  roles have weight 5, high-reasoning specialists weight 3, medium specialists
  weight 2, and low-risk helpers weight 1. A gate passes only when required
  roles are present, weighted approval is at least 70 percent, and no P1/P2
  blockers remain. Tier 3 still requires explicit live-gate authority,
  same-session evidence, recovery path, reviewer quorum, and closed-surface
  review.
- If read-only subagents are unavailable or unsafe, run the same role
  perspectives locally and record that no subagents were spawned.

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
- Codex profile gate: `.codex/admin/requirements.toml`,
  `.codex/admin/profiles/`, managed hook scripts, installer/validator, source
  records, and hook tests must pass before any managed profile is considered
  installable. The default and yolo-compatible profiles must pass the
  operator-sovereignty audit.

## Current status

- Repository status: scaffold initialized, no firmware implementation.
- Framework status: workspace-neutral; `four-relay-xbee-wifi` has an accepted
  ESP-IDF v6.0.1 target in ADR-0002.
- Hardware status: photographed `four-relay-xbee-wifi` target profiles added;
  physical bench verification pending.
- Agent-process status: tiered multi-agent triage is the default workspace
  process; project-local Codex hooks remain trust-gated runtime aids, while
  optional managed-hook profiles are available for supported Codex hook events.
  The default profile is yolo-compatible; admin-strict is not the default.
