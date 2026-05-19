# Handoff 0012 - Codebase Research Integration To Role Lanes

## From

Architect, Firmware, Communications, QA, Release

## To

Architect, Hardware, Communications, Firmware, QA, Release

## Summary

The M0/M1 integration pass aligned the public relay channel contract to
`1..4`, kept internal relay state zero-based inside `safe_core`, expanded host
negative tests, and added a generated Pages manifest audit helper.

## Required next checks

- Hardware must continue source-backed or bench-backed evidence collection for
  board/shield power, relay module behavior, MicroSD, XBee carrier, TFT, mux,
  expander, bench tools, enclosure, and load gates.
- Communications should add AT response and receive-packet payload validation
  vectors while preserving the read-only Tier A/Tier B probe boundary.
- Firmware may build on the safe-core public-channel helpers, but must keep
  GPIO, expander, UART, storage mount, Wi-Fi, flash, and monitor behavior
  disabled until the matching gate closes.
- QA should keep `scripts/audit_public_manifest.py` in the Pages release gate
  and avoid expanding marker checks inside `scripts/verify_scaffold.py` until
  validation categories are refactored.
- Release must keep public artifacts allowlist-only and exclude `.agents/`,
  `user_uploads/`, raw photos, private bench records, vendor PDFs, unredacted
  radio IDs, and unsafe wiring detail.

## Blockers

- Relay/load wiring remains blocked.
- Mains/load design and public load wiring procedures remain blocked.
- XBee setting writes, API transmit frames to hardware, relay commands, and
  ESP32 DIN/DOUT carrier wiring remain blocked.
- Relay GPIO writes and relay-expander writes remain blocked.
- ESP-IDF build/flash validation remains blocked until toolchain availability
  is installed, verified, and authorized.
- Hardware gate closure remains blocked by missing physical evidence.

## Evidence

- Task record:
  `.agents/TASK_LOG/0016-codebase-research-integration-review.md`.
- Safe-core API contract:
  `firmware/projects/four-relay-xbee-wifi/components/safe_core/`.
- Host tests:
  `tests/four_relay_safe_core/test_safe_core.c`.
- Public manifest audit:
  `scripts/audit_public_manifest.py`.
