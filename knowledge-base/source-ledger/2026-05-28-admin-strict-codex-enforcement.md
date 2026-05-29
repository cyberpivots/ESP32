# Codex Managed-Hook Profiles Source Ledger

## Routing

| Field | Value |
| --- | --- |
| Selected tier | Tier 2 governance, hook/config, source-record, and machine-local requirements recovery boundary. |
| Owner role | Agent Operations with Tooling and QA. |
| Evidence need | Official OpenAI Codex docs, local repo tests, yolo-compatible TOML audits, installer dry-run/removal validation, and direct hook fixtures. |
| Mutation boundary | `.codex/admin/`, governance/prompt docs, `scripts/scaffold_audit_agent_process.py`, hook tests, source records, task log, handoff, and `/etc/codex/requirements.toml` removal only when present. |
| Closed surfaces | Firmware/runtime/API/ABI/framework changes, flashing, erase, monitor, serial-write expansion, BLE/live mesh, PCAP, router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, wiring, release gates, and live bench work. |

## Sources

- `SRC-CODEX-ADMIN-REQUIREMENTS-2026-05-28`
- `SRC-CODEX-HOOKS-MANAGED-2026-05-28`
- `SRC-CODEX-SUBAGENTS-2026-05-27`
- `SRC-OPENAI-LLM-ACCURACY-2026-05-28`
- `SRC-LOCAL-ADMIN-STRICT-CODEX-ENFORCEMENT-2026-05-28`

## Verified Facts

- Official Codex docs identify `requirements.toml` as an admin-enforced
  configuration file and list `/etc/codex/requirements.toml` as the Unix system
  requirements path.
- Official Codex docs support `allow_managed_hooks_only`, `[features].hooks`,
  managed hook `managed_dir`, allowed approval policies, allowed sandbox modes,
  allowed web search modes, and restrictive command prefix rules.
- Official Codex hook docs support `UserPromptSubmit`, `PreToolUse`,
  `PermissionRequest`, `SubagentStart`, `SubagentStop`, and `Stop` command hook
  output shapes used by `.codex/admin/hooks/esp32_admin_policy.py`.
- A requirements file that restricts allowed sandbox or approval policies can
  block user-intended `codex --yolo` semantics.
- The local default and yolo-compatible requirements omit
  `allowed_sandbox_modes`, `allowed_approval_policies`, and
  `rules.prefix_rules`.
- The managed hook returns success with no deny/block decision for
  `permission_mode = "bypassPermissions"` in PreToolUse, PermissionRequest,
  SubagentStop, and Stop.
- The optional admin-strict profile is documented as explicit opt-in only and
  blocks `codex --yolo` by design.

## Assumptions

- User-intended `codex --yolo` full access is authoritative unless the user
  explicitly asks to install admin-strict.
- Repo governance may advise, document, and test, but it must not silently
  override launch-time permission intent.

## Unknowns

- Hook schemas, permission-mode fields, or interception coverage may change in
  future Codex releases; rerun hook tests and installer validation after Codex
  upgrades.

## Reviewer Quorum

| Role | Weight | Evidence reviewed | Vote | Blockers | Conditions | Confidence |
| --- | ---: | --- | --- | --- | --- | --- |
| Governance cartographer | 5 | Governance docs, profile TOML, operator-sovereignty requirement | Approve correction | None | Make yolo-compatible the default and strict explicit opt-in only. | High |
| Evidence/QA reviewer | 3 | Tests, source records, installer recovery command | Approve correction | None | Add bypassPermissions tests and TOML audits. | High |
| Prompt-token triage | 2 | Prompt docs and hook behavior | Approve correction | None | Keep routing packet and weighted veto advisory under yolo mode. | High |
| QA/tooling reviewer | 3 | Installer, hooks, `/etc/codex` recovery state | Approve correction | None | Verify `/etc/codex/requirements.toml` is absent after recovery. | High |

Weighted disposition: correction passes with required roles present, 100
percent weighted approval, and no P1/P2 blockers.

## Validation Evidence

- Repo and admin validation were rerun after correction; see
  `.agents/TASK_LOG/0084-admin-strict-codex-enforcement.md` for command
  results.
- `/etc/codex/requirements.toml` is absent after recovery validation.
- Yolo-compatible requirements dry-run source hash:
  `63e6c0dcc119263ea85f313ec6b40f307a5fa30507dcd87432c38ea61d0f8950`.
- Managed hook dry-run source hash:
  `f889f6580c00efd162201448decb856b79c490122f70c2e61b9db791f0873417`.

## Authority Limits

This ledger does not authorize firmware/runtime/API/ABI/framework changes,
flashing, erase, monitor, serial-write expansion, BLE/live mesh, PCAP,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, wiring, release
gates, or live bench work.
