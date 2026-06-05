# Agent Coordination

Start future process work with
[Agentic planning guide](agentic-planning-guide.md). `AGENTS.md` remains
canonical; the guide is the route map for source precedence, lane selection,
packet shapes, subagent depth limits, and decision footers.

## Required sequence

1. Read `AGENTS.md`.
2. Identify the owner role in `.agents/OWNERSHIP.md`.
3. Select the tier from the workspace multi-agent process.
4. State verified facts, assumptions, unknowns, owner role, mutation boundary,
   evidence need, and validation plan before non-trivial mutation.
5. Open or update a task record in `.agents/TASK_LOG/`.
6. Check source coverage before editing factual docs.
7. Leave validation evidence and handoff notes.

Use the compact contract IDs in hooks and subagent prompts when the full text
would be noisy: `ESP32-GOV-v1`, `SOV-v1`, `LIFECYCLE-v1`, and
`TIER3-CLOSED-v1`. The full definitions remain in `AGENTS.md`,
`.agents/GOVERNANCE.md`, and [Instruction surface map](instruction-surface-map.md).

## Tiers

- Tier 0: trivial or read-only. Coordinator triage plus local role lens.
- Tier 1: normal docs, tests, or bounded code. Coordinator plus owner and QA
  lens; attempt project-local read-only subagents for non-trivial mutation when
  available and safe.
- Tier 2: governance, protocol, firmware, evidence, hook/config, or broad code.
  Read-only reviewer quorum before mutation with mandatory subagent attempt
  when tools are available and safe.
- Tier 3: live bench, flashing, wiring, radio, serial writes, relay/load/mains,
  or release gates. Same-session evidence and explicit gate authority required.

## Reviewer quorum

Tier 2 and Tier 3 work needs at least coordinator, relevant owner, and QA
perspectives before mutation. Project-local read-only subagents are
mandatory to attempt when available and safe. Use local role lenses only when
subagents are unavailable, unsafe, or blocked by higher-priority tool policy
after lifecycle cleanup, and record that no subagents were spawned and why the
mandatory subagent attempt could not be completed.

Standing user authorization for project-local read-only subagent use is recorded
in `AGENTS.md`; treat subagent use as requested and allowed for every prompt in
this workspace. Do not treat generic explicit-user-request limits as a fallback
reason when a selected tier requires subagent review.

A no-P1/P2 reviewer quorum may accept only the named gate and mutation
boundary. Tier 3 acceptance also requires same-session evidence, explicit
live-gate authority, recovery path, and closed-surface review.

## Agent Lifecycle Cleanup

Before spawning reviewers for Tier 2 or Tier 3 work, the coordinator checks any
visible subagent lifecycle state and inspects completed agents before spawning
new ones. The coordinator uses `wait_agent` to collect outstanding reviewer
results when safe, captures the reviewer evidence, then closes completed/stale
agents with `close_agent`.

After quorum collection, close agents before fallback/final decisions and
before spawning replacement reviewers. If the parent falls back to local role
lenses, the task record must state that fallback only after cleanup attempt was
made, or that lifecycle state was not visible or was unsafe to act on.

This protocol reduces stuck reviewer slots, but it is not a hard runtime
guarantee: project-local hooks can remind and audits can check text fixtures,
while only the parent agent's actual `close_agent` calls release visible Codex
runtime slots. In `bypassPermissions` launches, this remains advisory only.

## Weighted veto

Weighted veto is the default quorum rollup. Coordinator or architecture-risk
roles have weight 5, high-reasoning specialists weight 3, medium specialists
weight 2, and low-risk helpers weight 1. A gate passes only when required roles
are present, weighted approval reaches at least 70 percent, and no P1/P2
blockers remain. A Tier 3 gate also needs explicit live-gate authority,
same-session evidence, recovery path, and closed-surface review; weights cannot
waive those prerequisites.

## Continuation decision

End non-trivial work with a decision footer: `continue`, `ask_user`,
`blocked`, `ready_for_mutation`, or `handoff`; the next gate or slice; owner
role; evidence need; approved mutation boundary; validation command; required
durable record; and authority limits.

Missing evidence is a continuation condition when safe evidence collection
remains. Use `scripts/agent_process_decision.py` or the same packet shape to
record weighted votes and choose the next action: continue automatable work,
ask for one irreducible physical fact, or block at a hard safety or authority
boundary.

## Project-local profiles

- Read-only reviewers: `governance-cartographer`, `evidence-record-auditor`,
  `live-bench-gate-reviewer`, `win31-dashboard-vision-gate`,
  `ui-code-protocol-analyst`, `source-skill-curator`,
  `prompt-token-triage`, and `qa-validation-reviewer`.
- Workers: `governance-doc-worker`, `kb-record-worker`, and
  `bounded-implementation-worker`.
- Workers require an explicit disjoint write scope from the parent and must
  preserve dirty work, avoid framework selection, avoid live hardware actions,
  list changed paths, and skip commit/push unless explicitly requested.

## Enforcement

No feature or factual document should be considered accepted unless it has:

- a task record,
- a source-index reference where factual claims are made,
- explicit unknowns,
- validation results,
- an owner for the next action,
- selected tier and mutation boundary for non-trivial work.
- continuation decision and authority limits.
- skill/config audit coverage when Codex skills or `.codex/config.toml` skill
  routing changes.
- durable-record audit coverage for new non-trivial task records.
- publication-hygiene report before any explicit commit, push, PR, branch
  cleanup, release, or Pages publication gate.

Project-local Codex hooks under `.codex/hooks.json` add model-visible reminders
for triage, subagent boundaries, agent lifecycle cleanup, and mutating tool
calls. They remain advisory runtime aids.

Agent instruction files are the default enforcement surface. `AGENTS.md` is
canonical, and every `.codex/agents/*.toml` developer-instruction profile must
inherit the operator-sovereignty rule: do not create, install, or rely on
`/etc/codex/requirements.toml` to restrict `codex --yolo`,
`danger-full-access`, `approval_policy=never`, or command prefix behavior
unless the user explicitly asks for the `admin-strict` profile by name.

Managed-hook profiles under `.codex/admin/` are optional machine-local profiles
for supported Codex hook events. The default yolo-compatible profile must not
constrain `codex --yolo`, while the admin-strict profile is explicit opt-in
only and may block yolo semantics.
