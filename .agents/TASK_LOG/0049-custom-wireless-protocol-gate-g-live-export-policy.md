# Task Log 0049 - Custom Wireless Protocol Gate G Live Export Policy

## Task

- ID: 0049-custom-wireless-protocol-gate-g-live-export-policy
- Owner role: Communications, QA
- Status: proposed policy gate; live export disabled
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Prepare the policy gate for future Gate G live analytics export without adding
or enabling any live export surface.

## Verified Facts

- Gate G remains simulator-only.
- `ADR-0005` is proposed, not accepted.
- `ADR-0005` requires accepted retention period, privacy/redaction rules,
  export format, storage location, operator access, and cleanup expectations
  before live analytics export can be implemented.
- No bridge request, Win31/OPCON export control, firmware ABI, live export
  file, live hardware action, prepare, flash, erase, monitor, PCAP,
  router/admin mutation, BLE, mesh, relay, XBee, TFT, MicroSD, load, mains, or
  serial-write expansion was added by this task.

## Assumptions

- The Pi bridge remains the likely durability boundary for a later accepted
  export, but that storage location is not accepted until the ADR is accepted.

## Unknowns

- Accepted retention period.
- Accepted privacy and redaction rules.
- Accepted export format and schema version.
- Accepted storage location and permissions.
- Accepted operator access and cleanup policy.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-G-ANALYTICS-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`

## Validation

- `python3 scripts/verify_scaffold.py`
- `git diff --check`

## Handoff

Continue with
[../handoffs/0038-custom-wireless-protocol-gate-g-live-export-policy-to-qa.md](../handoffs/0038-custom-wireless-protocol-gate-g-live-export-policy-to-qa.md).
