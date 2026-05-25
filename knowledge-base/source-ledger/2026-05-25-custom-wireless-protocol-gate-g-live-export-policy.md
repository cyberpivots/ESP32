# Custom Wireless Protocol Gate G Live Export Policy Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`

## Scope

Policy-gate preparation for a future live analytics export surface. This
extends the simulator-only Gate G records with a proposed ADR boundary.

## Verified Facts

- `ADR-0005` is proposed, not accepted.
- Live analytics export remains disabled until an accepted ADR records:
  retention period, privacy/redaction rules, export format, storage location,
  operator access, and cleanup expectations.
- Gate G remains a prepare-live-export planning gate only.
- No bridge request, Win31/OPCON export control, firmware ABI, live export
  artifact, live hardware action, prepare, flash, erase, monitor, PCAP,
  router/admin mutation, BLE, mesh, relay, XBee, TFT, MicroSD, load, mains, or
  serial-write expansion was added by this task.

## Assumptions

- The Pi bridge remains the likely future durability boundary unless a later
  accepted ADR changes it.

## Unknowns

- Accepted retention period.
- Accepted privacy and redaction rules.
- Accepted export format and schema version.
- Accepted storage location and permissions.
- Accepted operator access rules.
- Accepted cleanup expectations.

## Validation

- `python3 scripts/verify_scaffold.py`
- `git diff --check`

## Result

Future Gate G live export work has an ADR-shaped acceptance gate. The export
surface remains closed until the policy is accepted.
