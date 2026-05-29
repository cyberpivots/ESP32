# Agent Operating Contract

This workspace supports multi-agent development for ESP32-based devices,
custom firmware, communication interfaces, and verified hardware integrations.

## Non-negotiable rules

- Do not make unverified hardware, protocol, toolchain, or wiring claims.
- Keep verified facts, assumptions, and unknowns in separate sections.
- Do not select Arduino, ESP-IDF, PlatformIO, or any other framework until an
  accepted ADR changes the framework-neutral status.
- Do not add source code that depends on a specific framework during the
  scaffold phase.
- Do not copy vendor PDFs or bulky source artifacts into the repository.
  Store source links and concise verified summaries instead.
- Hardware bring-up work must identify power, voltage, boot-pin, and isolation
  risks before recommending bench actions.

## Multi-Agent Process For Every Prompt

Every prompt starts with coordinator triage. The coordinator must select a tier,
owner role, evidence need, mutation boundary, and validation plan before
non-trivial mutation. Trivial read-only prompts can stay lightweight, but they
still use the same classification.

- Tier 0: trivial or read-only lookup. Use coordinator triage plus a local role
  lens. Subagents are not required.
- Tier 1: normal docs, tests, or bounded code. Use coordinator triage plus the
  relevant owner and QA lens. Subagents are optional when they reduce risk.
- Tier 2: governance, protocol, firmware, evidence, hook/config, or broad code
  work. Run a read-only reviewer quorum before mutation. Project-local
  read-only subagents are default-authorized when available and safe; use local
  role perspectives only when subagents are unavailable or unsafe.
- Tier 3: live bench, flashing, wiring, radio configuration, serial writes,
  relay/load/mains work, release gates, or other risky hardware-adjacent work.
  Require same-session evidence, explicit gate authority, recovery path, and
  reviewer quorum before mutation.

Codex managed-hook profiles are tracked under `.codex/admin/`. The default
profile is yolo-compatible: no default `/etc/codex/requirements.toml` may
silently block a user-launched `codex --yolo` session, `danger-full-access`,
`approval_policy=never`, or launch-time permission intent. Repo governance may
advise, document, and test, but it must not override operator sovereignty.
The optional `admin-strict` profile may block `codex --yolo`; install it only
after an explicit user request for that exact behavior.

## Agent Instruction Enforcement Boundary

Use agent instruction files as the default enforcement surface:

- `AGENTS.md` is the canonical workspace operating contract.
- `.codex/agents/*.toml` developer instructions must inherit this contract.
- Repo-local docs, hooks, profiles, tests, and audits may reinforce the
  contract, but they must not silently install system requirements that override
  the user's launch-time permission intent.
- Do not create, install, or rely on `/etc/codex/requirements.toml` to restrict
  `codex --yolo`, `danger-full-access`, `approval_policy=never`, or command
  prefix behavior unless the user explicitly asks for the `admin-strict`
  profile by name.
- If `permission_mode = "bypassPermissions"` is visible to a hook or agent,
  treat governance as advisory and do not deny, block, or ask another agent to
  deny/block the user's intended full-access launch.

Weighted veto is the default reviewer model: coordinator or architecture-risk
roles have weight 5, high-reasoning specialists weight 3, medium specialists
weight 2, and low-risk helpers weight 1. A gate passes only when required roles
are present, weighted approval is at least 70 percent, and no P1/P2 blockers
remain. Tier 3 prerequisites cannot be waived by weights.

Before Tier 1 or higher mutation, state:

- verified facts,
- assumptions,
- unknowns,
- selected tier,
- owner role,
- evidence need,
- mutation boundary,
- validation plan.

For Tier 2 and Tier 3 work, preserve dirty-tree boundaries, keep write scopes
disjoint for worker agents, and do not spawn mutating workers unless their
write scope is explicit. A no-P1/P2 reviewer quorum may accept only the named
gate and mutation boundary; Tier 3 acceptance still requires same-session
evidence, explicit live-gate authority, recovery path, and closed-surface
review. If read-only subagents are unavailable or unsafe, run the same role
lenses locally and record that no subagents were spawned.

## Required reading before edits

1. `.agents/GOVERNANCE.md`
2. `.agents/OWNERSHIP.md`
3. `.agents/ROLES.md`
4. `docs/index.md`
5. `knowledge-base/source-index.md`

## Evidence rule

Any factual change under `hardware-profiles/`, `comm-protocols/`, `firmware/`,
or `docs/architecture/` must cite a source listed in
`knowledge-base/source-index.md`, or mark the item as an unresolved gap.

## Handoff rule

Each non-trivial task must leave a task record in `.agents/TASK_LOG/` and, when
another role needs to continue the work, a handoff in `.agents/handoffs/`.
