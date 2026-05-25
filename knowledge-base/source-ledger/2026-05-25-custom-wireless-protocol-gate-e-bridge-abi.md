# Custom Wireless Protocol Gate E Bridge ABI Source Ledger

Date: 2026-05-25

## Verified Facts

- [repo-verified] Gate E adds a draft bridge ABI document at
  `docs/projects/espnow-bbs/bridge-abi-draft.md`.
- [repo-verified] The ESP32 Gate C simulator now requires `v:1` by default on
  bridge requests processed through `process_bridge_request`.
- [repo-verified] The simulator keeps a named legacy compatibility path for
  older unversioned Gate B/C request tests through
  `allow_legacy_unversioned=True`.
- [repo-verified] The draft request set is `msg_post`, `download_queue`,
  `telemetry_report`, `node_status`, `protocol_report`, `state_get`, and
  `control_intent`.
- [repo-verified] The draft stable bridge error reasons are
  `version_required`, `version_invalid`, `line_too_long`, `non_ascii`,
  `json_invalid`, `payload_invalid`, `field_type_invalid`, `hex_invalid`,
  `message_type_unknown`, and `state_changing_command_blocked`.
- [repo-verified] DOS-C Gate D simulator fixtures now include `v:1`, while the
  live Win31 `download_queue` request remains payload-free.

## Assumptions

- [assumption] Gate E is an owner-review ABI freeze candidate, not final
  firmware ABI.
- [assumption] The accepted serial-nullmodem path remains the live acceptance
  baseline:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Unknowns

- [unknown] No live bridge transcript, Win31/OPCON visual proof, physical
  serial proof, flashing, radio transfer, or file-transfer acceptance evidence
  was produced by Gate E.
- [unknown] Firmware ABI, analytics retention/export, and privacy policy remain
  unresolved after Gate E.

## Validation

- `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `/mnt/h/dos-c`: `python3 -m unittest tests.espnow_bbs_bridge.test_gate_d_bridge_pairing`

## Stop Gates

Gate E does not authorize flashing, erase, monitor, serial writes, live bridge
mutation, radio setting changes, PCAP, router/admin work, BLE, ESP-WIFI-MESH
live action, relay, XBee, TFT, MicroSD, load, or mains work.
