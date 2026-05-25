# Custom Wireless Protocol Gate D DOS-C Pairing Source Ledger

Date: 2026-05-25

## Sources Used

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-ESP-IDF-ESPNOW`

## Verified Facts

- [repo-verified] Gate D adds DOS-C test-only bridge/operator simulator
  fixtures in `/mnt/h/dos-c/tests/espnow_bbs_bridge/` and replays them through
  the ESP32 Gate C `process_bridge_request` simulator adapter.
- [repo-verified] The Gate D fixture set covers simulated `msg_post`,
  `download_queue`, `telemetry_report`, `node_status`, `protocol_report`,
  `state_get`, and `control_intent` request frames.
- [repo-verified] The Gate D `download_queue` fixture includes simulator-only
  payload content so ESP32 Gate C can packetize file chunks; the Win31 operator
  host test separately asserts that the live operator `download_queue` request
  carries no `content` or `content_hex` field.
- [repo-verified] The Gate D replay test checks that emitted DOS-C request
  lines and ESP32 simulator responses remain ASCII and within the 512-byte
  newline-delimited bridge line budget.
- [repo-verified] Simulated `control_intent` remains accepted but
  non-executing, while simulated state-changing `relay_set` remains rejected by
  ESP32 Gate C.

## Assumptions

- [assumption] Gate D remains a simulator-pairing proof and does not freeze the
  bridge ABI, firmware ABI, report schema, retention policy, or live acceptance
  criteria.
- [assumption] Gate E remains the next owner-review gate for any `v:1` bridge
  ABI contract and backward-compat parser rules.

## Unknowns

- [unknown] No live DOSBox-X, Pi bridge, `/dev/ttyUSB0`, ESP32 coordinator,
  Win31, OPCON screenshot, or bridge transcript evidence was produced by Gate D.
- [unknown] No firmware-facing structure, persistent analytics schema, privacy
  policy, or live file-transfer proof was accepted by Gate D.

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

## Boundary Notes

- [non-goal] This ledger does not authorize flashing, serial writes, bridge
  runtime mutation, radio setting changes, PCAP, router/admin work, relay,
  XBee, TFT, MicroSD, load, mains, BLE pairing, ESP-WIFI-MESH live action,
  erase, monitor automation, or framework migration.
