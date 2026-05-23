# Task Log 0029 - ESP-NOW BBS Live Gate Tooling

## Task

- ID: 0029-espnow-bbs-live-gate-tooling
- Owner role: Tooling, Firmware, Communications, QA
- Status: tooling implemented pending live proof
- Created: 2026-05-23
- Updated: 2026-05-23

## Goal

Implement the tooling-first live gate for the ESP-NOW BBS three-peer bench
without performing live flashing or claiming live acceptance.

## Scope

Included:

- Multi-peer read-only preflight for exactly `COM4`, `COM5`, and `COM6`
  CP210x ESP32 peer candidates.
- Pi gate for `dospi@172.16.0.2`, expected SSH fingerprints, host identity,
  `eth0=172.16.0.2/24`, stale listener/process absence, and coordinator
  `/dev/ttyUSB0` read-only identity.
- Passing-gate peer map of `COM4=peer01`, `COM5=peer02`, `COM6=peer03`.
- Prepare/flash manifest tooling with explicit backup and write confirmations,
  backup/build hashes, recovery commands, forbidden flash-argument checks, and
  coordinator-first flash order.
- Focused fixture tests for the multi-peer preflight validator.
- ESP32 documentation, source-index, source-ledger, known-gap, and handoff
  updates.

Excluded:

- Live preflight against current hardware.
- `read-flash` backups, generated live config, live ESP-IDF builds, flashing,
  monitor, relay, XBee, TFT, MicroSD, load, mains, PCAP, router admin, Windows
  COM proxy, or Win3.1/Pi live acceptance.

## Sources

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESPTOOL-BASIC`
- `SRC-ESPTOOL-ADVANCED-VERIFY`
- `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS`
- `SRC-DOSBOX-SERIAL-CONFIG`
- `SRC-LOCAL-ESPNOW-MULTIPEER-DASHBOARD-2026-05-23`
- `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23`

## Decisions

- Preserve ADR-0003 ESP-IDF v6.0.1 for the `espnow-bbs` lane.
- Keep live flashing closed unless `espnow_bbs_live_gate.py flash` is run with
  an unchanged prepare manifest and explicit `--confirm-write-flash`.
- Keep unsafe relay, XBee, TFT, MicroSD, load, mains, PCAP, router-admin, and
  packet-driver lanes closed.

## Validation

- `python3 -m py_compile scripts/live_bench_preflight.py scripts/espnow_bbs_live_gate.py tests/live_bench/test_multipeer_preflight.py`
- `python3 tests/live_bench/test_multipeer_preflight.py`

Additional scaffold and DOS-C validation results are recorded in the final
implementation report for this task.

## Handoff

Continue through
`.agents/handoffs/0019-espnow-bbs-live-gate-to-qa.md` before any live bench
action.
