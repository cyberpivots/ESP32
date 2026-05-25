# Task Log 0042 - Custom Wireless Protocol Gate E Bridge ABI

## Task

- ID: 0042-custom-wireless-protocol-gate-e-bridge-abi
- Owner role: Communications, QA
- Status: implemented as draft simulator/documentation Gate E
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Create a draft bridge ABI freeze candidate after Gate D while preserving the
accepted serial-nullmodem live path and avoiding firmware or live-runtime
mutation.

## Scope

Included:

- Draft bridge ABI document at
  [../../docs/projects/espnow-bbs/bridge-abi-draft.md](../../docs/projects/espnow-bbs/bridge-abi-draft.md).
- `v:1` required by default for new ESP32 Gate C simulator bridge requests.
- Explicit legacy unversioned compatibility path only for named Gate B/C tests.
- DOS-C Gate D simulator fixture updates to emit `v:1`.
- Stable draft bridge error reasons and source-ledger/source-index updates.

Excluded:

- Final firmware ABI, live bridge transcript, Win31/OPCON proof, serial writes,
  flashing, erase, monitor, radio setting changes, PCAP, router/admin work,
  BLE, ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load, mains,
  analytics retention/export policy, or privacy policy.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`

## Validation

- `/mnt/h/ESP32`: `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `/mnt/h/dos-c`: `python3 -m unittest tests.espnow_bbs_bridge.test_gate_d_bridge_pairing`
- Full Gate E validation is recorded in the execution response.

## Handoff

Continue with
[../handoffs/0031-custom-wireless-protocol-gate-e-bridge-abi-to-qa.md](../handoffs/0031-custom-wireless-protocol-gate-e-bridge-abi-to-qa.md).
