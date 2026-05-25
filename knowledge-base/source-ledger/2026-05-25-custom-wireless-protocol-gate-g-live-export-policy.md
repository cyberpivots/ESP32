# Custom Wireless Protocol Gate G Live Export Policy Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`

## Scope

Policy-gate acceptance for the Gate G live analytics export surface. This
extends the simulator-only Gate G records with an accepted local-only ADR
boundary.

## Verified Facts

- `ADR-0005` is accepted.
- Gate G v1 accepts local-admin redacted JSON export using
  `gate-g.analytics.v1` and policy selector
  `adr-0005-redacted-local-operator-v1`.
- Accepted retention is a 7-day stale-export cleanup expectation for derived
  `analytics-report*.json` files in approved ignored export roots.
- Accepted privacy rules omit message bodies, file names, event details, and
  raw operator, client, message, file, telemetry, node, and device identifiers.
- No Win31/OPCON export control, firmware ABI, bridge export request, live
  hardware action, prepare, flash, erase, monitor, PCAP, router/admin mutation,
  BLE, mesh, relay, XBee, TFT, MicroSD, load, mains, or serial-write expansion
  is authorized by this policy.

## Assumptions

- The DOS-C/Pi bridge spool remains the Gate G v1 durability boundary unless a
  later accepted ADR changes it.

## Unknowns

- Firmware export ABI remains unresolved.
- Win31/OPCON export UI remains unresolved.
- A live bridge request type for analytics export remains unresolved.

## Validation

- `python3 scripts/verify_scaffold.py`
- `git diff --check`

## Result

Gate G now has an accepted local-only export policy. Implementation remains
limited to local-admin redacted JSON export from the DOS-C/Pi bridge spool.
