# Task Log 0041 - Custom Wireless Protocol Gate D DOS-C Pairing

## Task

- ID: 0041-custom-wireless-protocol-gate-d-dosc-pairing
- Owner role: Communications, QA
- Status: implemented as simulator-only Gate D
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Pair DOS-C simulator fixtures with the ESP32 Gate C custom wireless protocol
bridge adapter while preserving the accepted serial-nullmodem live path and
avoiding any live runtime or hardware claim.

## Scope

Included:

- DOS-C test-only fixture frames for simulated `msg_post`, `download_queue`,
  `telemetry_report`, `node_status`, `protocol_report`, `state_get`, and
  `control_intent`.
- Cross-repo replay of those DOS-C fixtures through ESP32 Gate C
  `process_bridge_request`.
- Regression coverage that request and response frames stay ASCII and within
  the 512-byte bridge line budget.
- A Win31 operator host-test assertion that live `download_queue` requests do
  not carry simulator payload fields.
- Source ledger, source-index entry, docs-index source-ledger link, known-gap
  update, and QA handoff.

Excluded:

- Bridge ABI freeze, firmware ABI draft, analytics/reporting retention policy,
  live DOSBox-X/Win31 proof, flashing, serial writes, monitor/erase, radio
  setting changes, PCAP, router/admin work, relay, XBee, TFT, MicroSD, load,
  mains, BLE pairing, ESP-WIFI-MESH live action, or framework migration.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-ESP-IDF-ESPNOW`

## Validation

- `/mnt/h/dos-c`: `python3 tests/espnow_bbs_bridge/test_bridge_protocol.py`
- `/mnt/h/dos-c`: `python3 tests/espnow_bbs_bridge/test_coordinator_protocol.py`
- `/mnt/h/dos-c`: `bash tests/espnow_bbs_bridge/run_tests.sh`
- `/mnt/h/dos-c`: `python3 -m unittest tests.espnow_bbs_bridge.test_gate_d_bridge_pairing`
- `/mnt/h/dos-c`: `bash tests/win31_operator/run_host_tests.sh`
- `/mnt/h/dos-c`: `bash tests/win31_netstack/run_host_tests.sh`
- `/mnt/h/dos-c`: `bash scripts/verify_scaffold.sh`
- `/mnt/h/ESP32`: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `/mnt/h/ESP32`: `python3 tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py --demo`
- `/mnt/h/ESP32`: `python3 scripts/verify_scaffold.py`
- `/mnt/h/ESP32`: `git diff --check`
- `/mnt/h/dos-c`: `git diff --check`
- Commit hashes are recorded in the execution response.

## Handoff

Continue through
[../handoffs/0030-custom-wireless-protocol-gate-d-dosc-pairing-to-qa.md](../handoffs/0030-custom-wireless-protocol-gate-d-dosc-pairing-to-qa.md)
for QA review and Gate E bridge ABI owner review.
