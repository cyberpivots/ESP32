# Task 0084: Codex Managed-Hook Profiles And Yolo Compatibility

## Routing Packet

## Verified Facts

- The repo correction keeps the work inside Tier 2 governance, hook/config,
  source-record, and machine-local requirements boundaries.
- `/etc/codex/requirements.toml` is absent during this correction pass.
- Official Codex docs support admin-enforced `requirements.toml`, managed
  hooks, `allow_managed_hooks_only`, allowed approval policies, allowed sandbox
  modes, allowed web search modes, and restrictive command prefix rules.
- Requirements can constrain `codex --yolo` when they omit
  `danger-full-access`, omit `approval_policy=never`, or enforce restrictive
  prefix rules.
- The default repo requirements and yolo-compatible profile now omit
  `allowed_sandbox_modes`, `allowed_approval_policies`, and
  `rules.prefix_rules`.
- The optional admin-strict profile is documented as explicit opt-in only and
  blocks `codex --yolo` by design.

## Assumptions

- User-intended `codex --yolo` full access is authoritative unless the user
  explicitly asks to install the admin-strict profile.
- Repo governance may advise, document, and test, but it must not silently
  override launch-time permission intent.

## Unknowns

- Future Codex releases may change hook schema, permission-mode fields, or
  supported interception paths.

## Selected Tier

Tier 2 governance, hook/config, source-record, and machine-local requirements
recovery boundary.

## Owner Role

Agent Operations with Tooling and QA.

## Evidence Need

Official OpenAI Codex docs, local repo tests, yolo-compatible TOML audits,
installer dry-run/removal validation, and direct hook fixtures.

## Mutation Boundary

- Repo: `.codex/admin/`, governance/prompt docs, scaffold audit, hook tests,
  source index, source ledger, prompt registry, task log, and handoff.
- Machine-local: `/etc/codex/requirements.toml` removal only when present.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --dry-run --profile yolo-compatible`
- `PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --remove-system-requirements`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_admin_policy_hooks.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

## Reviewer Quorum

| Role | Weight | Vote | P1/P2 blockers | Conditions |
| --- | ---: | --- | --- | --- |
| Governance cartographer | 5 | Approve correction | None | Replace strict-default wording with yolo-compatible default and explicit opt-in strict profile. |
| Evidence/QA reviewer | 3 | Approve correction | None | Add bypassPermissions regression tests and TOML audits. |
| Prompt-token triage | 2 | Approve correction | None | Preserve routing packet and weighted veto without blocking yolo mode. |
| QA/tooling reviewer | 3 | Approve correction | None | Add recovery command and validate `/etc/codex/requirements.toml` removal. |

Disposition: proceed with bounded correction. Weighted approval is 100 percent
with no P1/P2 blockers.

## Implementation Summary

- Converted `.codex/admin/requirements.toml` to a yolo-compatible default.
- Added `.codex/admin/profiles/yolo-compatible/requirements.toml`.
- Moved strict constraints into
  `.codex/admin/profiles/admin-strict/requirements.toml` as explicit opt-in.
- Updated managed hooks so `permission_mode = "bypassPermissions"` never
  denies or blocks in PreToolUse, PermissionRequest, SubagentStop, or Stop.
- Added installer `--remove-system-requirements` recovery behavior.
- Added bypassPermissions and TOML regression coverage.
- Updated governance, prompt docs, source index, source ledger, task log,
  handoff, docs index, and scaffold audit coverage.

## Validation Results

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_admin_policy_hooks.py`
  (`Ran 11 tests`).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --dry-run --profile yolo-compatible`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --remove-system-requirements`.
- PASS: `/etc/codex/requirements.toml` absence check.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (`Ran 20 tests`).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `git diff --check`.
- PASS: strict-default wording scan found no remaining default/admin-strict
  launch-override wording.
- PASS: forbidden-marker scan found no `allowed_sandbox_modes`,
  `allowed_approval_policies`, or `rules.prefix_rules` text in
  `.codex/admin/requirements.toml` or
  `.codex/admin/profiles/yolo-compatible/requirements.toml`.

## System Requirements Status

- `/etc/codex/requirements.toml`: absent after recovery validation.
- `/etc/codex/hooks/esp32_admin_policy.py`: not required for yolo recovery.
- Backups: none created during correction because the system requirements file
  was already absent.
- Yolo-compatible dry-run source hash:
  `.codex/admin/profiles/yolo-compatible/requirements.toml`
  `63e6c0dcc119263ea85f313ec6b40f307a5fa30507dcd87432c38ea61d0f8950`.
- Managed hook dry-run source hash:
  `.codex/admin/hooks/esp32_admin_policy.py`
  `f889f6580c00efd162201448decb856b79c490122f70c2e61b9db791f0873417`.

## Backup And Rollback

- Existing target files are backed up under `/etc/codex/backups/` before
  overwrite or removal.
- To remove system requirements and keep yolo unconstrained:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --remove-system-requirements
```

## Authority Limits

No firmware/runtime/API/ABI/framework changes, flashing, erase, monitor,
serial-write expansion, BLE/live mesh, PCAP, router/admin mutation, relay,
XBee, TFT, MicroSD, load, mains, wiring, release gates, or live bench work is
authorized by this task.
