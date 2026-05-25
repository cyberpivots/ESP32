# Custom Wireless Protocol Gate G Live Export Implementation Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`

## Scope

Gate G local-admin redacted analytics export implementation after `ADR-0005`
acceptance.

## Verified Facts

- `ADR-0005` is accepted for policy selector
  `adr-0005-redacted-local-operator-v1`.
- DOS-C bridge implementation adds a local-admin JSON export from a file-backed
  bridge spool to `analytics-report.v1.json` under approved ignored
  runtime/proof roots.
- The export omits message bodies, file names, event details, and raw
  operator/client/message/file/node/device identifiers.
- The export uses salted SHA-256 hashes for derived identifiers and writes
  owner-only permissions where the filesystem supports them.
- The export rejects in-memory spools, missing or non-accepted policy
  selection, existing destinations, and paths outside approved ignored roots.
- Cleanup removes stale `analytics-report*.json` files from approved ignored
  export roots after the accepted 7-day retention window.
- ESP32 simulator analytics now reference the accepted policy while remaining
  simulator-only.
- Fresh read-only preflight passed for Pi `192.168.137.105`, coordinator
  `/dev/ttyUSB0`, and accepted peer remap `COM9`/`COM6`/`COM7`.
- Live export proof reused the existing structured Gate H proof spool and wrote
  ignored `analytics-report.v1.json` artifacts into the DOS-C proof packet and
  paired ESP32 live-bench copy.
- String audit did not find the known live message body, `sysop`, `client-01`,
  or default file names in the JSON report.
- Cleanup proof removed one stale `analytics-report-stale.json` file and kept
  the current `analytics-report.v1.json`.

## Assumptions

- Gate G v1 proof storage remains the DOS-C/Pi proof packet, copied into the
  ignored ESP32 live-bench record only for proof handoff.

## Unknowns

- Firmware export ABI is not defined.
- Win31/OPCON export UI is not defined.
- A live bridge request type for analytics export is not defined.

## Validation

- `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- DOS-C `python3 tests/espnow_bbs_bridge/test_bridge_protocol.py`
- Gate G read-only preflight with accepted peer remap: `ok:true`
- Gate G export command wrote `analytics-report.v1.json`
- Gate G cleanup command removed one stale export
- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 scripts/verify_scaffold.py`
- `git diff --check`
- Paired DOS-C bridge, vision, operator, netstack, scaffold, and diff checks

## Result

Gate G live export is opened only as a local-admin redacted JSON export surface.
All Win31, firmware, bridge-request, flashing, serial-write expansion, PCAP,
BLE, mesh, relay/XBee, TFT, MicroSD, load, mains, and router/admin lanes remain
closed.
