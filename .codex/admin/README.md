# Codex Managed-Hook Profiles

This directory is the repo source of truth for ESP32 workspace Codex managed
hook profiles. The default policy is yolo-compatible: a user-launched
`codex --yolo` session must keep full access as intended.

## Scope

- Default profile: `.codex/admin/profiles/yolo-compatible/requirements.toml`
- Optional strict profile: `.codex/admin/profiles/admin-strict/requirements.toml`
- Compatibility template: `.codex/admin/requirements.toml`
- System target when explicitly installed: `/etc/codex/requirements.toml`
- Managed hook target: `/etc/codex/hooks/esp32_admin_policy.py`
- Installer and validator: `.codex/admin/install_admin_policy.py`

The yolo-compatible profile keeps managed hooks available without setting
`allowed_sandbox_modes`, `allowed_approval_policies`, or restrictive
`rules.prefix_rules`. When a hook input reports
`permission_mode = "bypassPermissions"`, managed hooks must not deny or block.
They may provide advisory context only.

The admin-strict profile is explicit opt-in only. It may block `codex --yolo`
by disallowing `danger-full-access`, `approval_policy=never`, and prefix-rule
free operation. Do not install it unless the user asks for that exact behavior.

These profiles support the workspace multi-agent routing packet, weighted-veto
review model, Tier 2/Tier 3 authority boundaries, and decision-footer
requirements for supported Codex hook events.

## Authority Limits

This package does not authorize firmware, flashing, serial writes, radio
configuration, live bench, BLE, ESP-WIFI-MESH, PCAP, relay/load/mains, XBee
writes, TFT, MicroSD, router/admin mutation, release gates, framework changes,
or hardware wiring. Tier 3 work still requires explicit live-gate authority,
same-session evidence, a recovery path, reviewer quorum, and closed-surface
review.

## Install

Dry-run first:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --dry-run --profile yolo-compatible
```

Install the yolo-compatible profile only when managed hooks are desired without
constraining yolo:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --install --profile yolo-compatible
```

Validate installed files:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --validate --profile yolo-compatible
```

Install admin-strict only after an explicit user request for strict behavior
that blocks yolo:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --install --profile admin-strict
```

The installer backs up existing target files before overwrite, installs stable
permissions, parses TOML with `tomllib`, and prints SHA-256 hashes for the
template and installed files.

## Rollback

Remove system requirements and restore full launch-time operator control:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .codex/admin/install_admin_policy.py --remove-system-requirements
```

The removal command backs up `/etc/codex/requirements.toml` when present,
removes it, and validates that no system requirements file remains to constrain
`codex --yolo`. If disabling this ESP32 policy entirely, also remove
`/etc/codex/hooks/esp32_admin_policy.py` after preserving hashes in the task
log. Restart Codex so the requirements layer is reloaded.
