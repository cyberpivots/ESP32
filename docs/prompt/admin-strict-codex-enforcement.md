# Codex Managed-Hook Profiles

## Source Basis

This prompt policy references `SRC-CODEX-ADMIN-REQUIREMENTS-2026-05-28`,
`SRC-CODEX-HOOKS-MANAGED-2026-05-28`,
`SRC-CODEX-SUBAGENTS-2026-05-27`,
`SRC-CODEX-CONFIG-REFERENCE-2026-05-27`, and
`SRC-OPENAI-LLM-ACCURACY-2026-05-28`.

## Verified Facts

- Codex supports admin-enforced `requirements.toml` at `/etc/codex/` on Unix
  systems, including Linux and macOS.
- Requirements can constrain approval policy, sandbox mode, web search mode,
  feature flags, managed hooks, and restrictive command prefix rules.
- Requirements that omit `danger-full-access` from `allowed_sandbox_modes` or
  omit `never` from `allowed_approval_policies` constrain `codex --yolo`.
- Managed hooks can be configured under `[hooks]`, and `managed_dir` must point
  at an absolute directory containing the hook scripts.
- `allow_managed_hooks_only = true` skips user, project, session, and plugin
  hooks while still allowing managed hooks.
- Codex `PreToolUse` is a guardrail for supported tool paths and is not a
  complete enforcement boundary for every possible action.
- The repo default profile is yolo-compatible and must not set
  `allowed_sandbox_modes`, `allowed_approval_policies`, or restrictive
  `rules.prefix_rules`.
- The optional admin-strict profile is explicit opt-in only and may block
  `codex --yolo`.
- Agent instruction files are the default enforcement surface for workspace
  governance: `AGENTS.md` is canonical, and `.codex/agents/*.toml` profiles
  must inherit the operator-sovereignty rule.

## Assumptions

- User-intended `codex --yolo` full-access launch behavior must remain
  authoritative unless the user explicitly asks to install admin-strict.
- Repo-local instructions, docs, hooks, profiles, tests, and audits may advise
  or validate behavior, but they must not silently install system requirements
  that override launch-time permission intent.
- Managed-profile install authority is limited to
  `/etc/codex/requirements.toml` and
  `/etc/codex/hooks/esp32_admin_policy.py`.

## Unknowns

- Future Codex releases may change hook schemas or supported interception
  paths; rerun the installer validation and hook tests after Codex upgrades.

## Required Routing Packet

Before Tier 1 or higher mutation, state verified facts, assumptions, unknowns,
selected tier, owner role, evidence need, mutation boundary, and validation
plan. Tier 2 and Tier 3 require reviewer quorum before mutation. Tier 3 also
requires explicit live-gate authority, same-session evidence, recovery path,
and closed-surface review.

## Weighted Veto

Record every vote with role, weight, evidence reviewed, vote, blockers,
conditions, and final disposition.

- Coordinator or architecture-risk: weight 5.
- High-reasoning specialist: weight 3.
- Medium specialist: weight 2.
- Low-risk helper: weight 1.

A gate passes only when required roles are present, weighted approval reaches
at least 70 percent, and there are no P1/P2 blockers. P1/P2 blockers, QA veto,
safety veto, missing required roles, or missing Tier 3 prerequisites fail the
gate regardless of weighted percentage.

`scripts/agent_process_decision.py` is the repo-local packet evaluator for this
rule. Missing evidence should route to `continue` when the next evidence step is
automatable, to `ask_user` only for one irreducible physical fact, and to
`blocked` only at a hard safety or authority boundary. `ready_for_mutation` is
valid only after the named gate passes.

## Managed Hook Contract

- `UserPromptSubmit`: inject routing requirements and block obvious attempts to
  bypass workspace governance.
- `PreToolUse`: deny supported mutating tool calls when the routing packet is
  missing; deny Tier 3 command patterns without live-gate authority fields.
- `PermissionRequest`: deny approval requests that conflict with missing
  routing or Tier 3 authority.
- `SubagentStart`: inject read-only or explicit-write-scope boundaries.
- `SubagentStop`: require reviewer outputs to include role, evidence reviewed,
  P1/P2 findings, vote, conditions, and confidence; continue the reviewer when
  it reports open blockers or rejects the gate.
- `Stop`: continue non-trivial mutation turns that omit the required decision
  footer or try to end with a non-terminal `continue` or `ready_for_mutation`
  decision.
- `bypassPermissions`: when hook input reports this permission mode, PreToolUse,
  PermissionRequest, SubagentStop, and Stop must not deny or block. Advisory
  context is allowed; overriding the user's `codex --yolo` intent is not.

## Closed Surfaces

This policy does not authorize firmware, framework changes, flashing, erase,
monitor, serial-write expansion, BLE, live ESP-WIFI-MESH, PCAP, router/admin
mutation, relay, XBee writes, TFT, MicroSD, load, mains, wiring, release gates,
or live bench work.
