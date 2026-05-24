# Task Log 0034 - Win31 Viewfinder Downloads OTAP Gate Alignment

## Task

- ID: 0034-win31-viewfinder-downloads-otap-gate-alignment
- Owner role: Communications, QA
- Status: implemented pending copied live evidence
- Created: 2026-05-24
- Updated: 2026-05-24
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Align the ESP32 completion gate with the paired DOS-C Win31 dashboard update
that adds owner-drawn viewfinder UI, Downloads evidence, and gated OTAP
intent/status screens.

## Scope

Included:

- `scripts/espnow_bbs_live_gate.py complete` transcript expectations now
  include `download_list`, `download_status`, `otap_status`, and non-executing
  `otap_intent`.
- Live-bench completion fixtures include Downloads and OTAP visible states.
- ML live-gate documentation, source index, source ledger, and QA handoff
  record the updated acceptance set.

Excluded:

- Firmware changes, live mesh file delivery, live flashing, BLE,
  ESP-WIFI-MESH live action, PCAP, packet-driver, router admin, relay, XBee,
  TFT, MicroSD, load, mains, erase, monitor, or serial write expansion.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`

## Validation

- `python3 -m py_compile scripts/espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`

## Handoff

Continue through
[../handoffs/0024-win31-viewfinder-downloads-otap-gate-to-qa.md](../handoffs/0024-win31-viewfinder-downloads-otap-gate-to-qa.md)
for the next copied live evidence packet.
