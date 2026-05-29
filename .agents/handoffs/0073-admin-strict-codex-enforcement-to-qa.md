# Handoff 0073: Codex Managed-Hook Profiles To QA

## Summary

The ESP32 Codex admin package was corrected to make yolo-compatible behavior
the default. User-intended `codex --yolo` full access must not be
silently overridden by `/etc/codex/requirements.toml`, sandbox restrictions,
approval-policy restrictions, or prefix rules.

## QA Focus

1. Verify `/etc/codex/requirements.toml` is absent unless the user explicitly
   requested a managed profile install.
2. Verify `.codex/admin/requirements.toml` and
   `.codex/admin/profiles/yolo-compatible/requirements.toml` do not contain
   `allowed_sandbox_modes`, `allowed_approval_policies`, or
   `rules.prefix_rules`.
3. Re-run bypassPermissions fixtures for PreToolUse, PermissionRequest,
   SubagentStop, and Stop; these must not deny or block under yolo mode.
4. Re-run installer `--dry-run --profile yolo-compatible` and
   `--remove-system-requirements` after Codex upgrades.
5. Confirm `.codex/admin/profiles/admin-strict/requirements.toml` remains
   explicit opt-in only and is documented as blocking `codex --yolo`.

## Closed Surfaces

This handoff does not authorize firmware/runtime/API/ABI/framework changes,
flashing, erase, monitor, serial-write expansion, BLE/live mesh, PCAP,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, wiring, release
gates, or live bench work.

## Current Status

Corrected and ready for QA validation. Same-session command results are
recorded in `.agents/TASK_LOG/0084-admin-strict-codex-enforcement.md` and the
final task response.
