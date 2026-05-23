# Task 0026 - ESP-NOW Encrypted Peer Proof

## Task

- ID: 0026-espnow-encrypted-peer-proof
- Owner role: Firmware, Hardware, Communications, QA
- Status: accepted live encrypted one-peer proof
- Created: 2026-05-22
- Updated: 2026-05-22

## Goal

Track the first encrypted one-coordinator/one-peer ESP-NOW proof for
RETRO-CBBS-NOW while preserving the accepted Pi bridge and hardware safety
gates.

## Scope

Included:

- Current DOS-C encrypted ESP-NOW coordinator/peer implementation evidence.
- Windows COM6 peer read-only identity refresh.
- Private peer read-flash backup.
- Ignored live config generation without printing or committing PMK/LMK values.
- Clean live coordinator and peer builds with encryption enabled.
- Peer flash and read-only UART send-loop proof.
- Fresh Pi/coordinator gate, private coordinator backup, encrypted coordinator
  flash, UART proof, Win3.1 OPCON bridge proof, and cleanup.
- Durable source ledger and handoff updates.

Excluded:

- Relay, XBee, TFT, MicroSD, load, mains, PCAP, Windows COM proxy, erase, and
  dashboard state-changing commands.

## Sources

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESP-IDF-START-PROJECT`
- `SRC-ESP-IDF-UART`
- `SRC-ESPTOOL-BASIC`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-LOCAL-LIVE-PI-COORDINATOR-GATE-2026-05-22`
- `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22`

## Decisions

- Keep the first encrypted proof on the accepted path:
  Win3.1 OPCON to DOSBox-X COM1/nullmodem to Pi bridge to USB serial
  coordinator to ESP-NOW encrypted unicast peer.
- Keep tracked firmware defaults build-safe with encryption disabled.
- Keep generated PMK/LMK material only under ignored `secrets/espnow-bbs/`.
- Flash the Windows COM6 peer after identity and private backup passed.
- Flash the coordinator only after fresh Pi identity, coordinator identity,
  user-confirmed USB-only/no-load/no external wiring state, stale-listener
  absence, and private coordinator backup passed.

## Validation

- Windows COM6 serial inventory: PASS, single CP210x candidate.
- Peer `read_mac`: PASS, MAC `78:e3:6d:0a:90:14`.
- Peer `flash_id`: PASS, 4 MB flash and 3.3 V flash voltage.
- Peer private `read_flash`: PASS, 4 MB backup SHA-256
  `5b612d6070117c179e0e526228222bf0781d74a9eca1e387e1cbeea18f9151c4`.
- DOS-C clean live coordinator build: PASS.
- DOS-C clean live peer build: PASS.
- Peer flash: PASS, esptool verified written data.
- Peer UART sample: PASS for send-loop proof, `tx` increased from `6` to `9`.
- Fresh Pi/coordinator gate: PASS for Pi `dos-pi4-poe`, Raspberry Pi 4 Model B
  Rev 1.2, serial `10000000aaaa5b24`, coordinator `/dev/ttyUSB0`, ESP32-D0WDQ6
  MAC `78:e3:6d:10:4d:6c`, 4 MB flash, 3.3 V flash, and no stale proof
  listeners.
- Coordinator physical state: PASS by user confirmation; USB-only with no
  relay, XBee, TFT, MicroSD, load wiring, mains wiring, or other external
  wiring attached.
- Coordinator private `read_flash`: PASS, 4 MB backup SHA-256
  `4b8fe3d68b053dd67825576b555db18701a9371388e6079549e746d2ce63a32e`.
- Coordinator flash: PASS, esptool verified written bootloader, partition
  table, and app regions.
- Coordinator UART proof: PASS for `hello`, `state`, and `diag`; `diag` showed
  peer `peer01`, MAC `78:e3:6d:0a:90:14`, `link=espnow-enc`, RX/TX/ACK `8/8/8`,
  duplicates `0`, and TTL drops `0`.
- Win3.1 OPCON proof: PASS in run `encrypted-peer-20260522T070112Z`; screenshots
  showed status `ok`, `serial-readonly`, `physical-readonly`, peer count `1`,
  peer `peer01`, link `espnow-enc`, disabled unsafe controls, zero serial
  errors, and RX/TX/ACK counters moving from `148/148/147` to `158/158/158`.
- Cleanup: PASS, no DOSBox-X, zenity/modal, bridge process, or
  `31331`/`31332`/`8080` listener.
- ESP32 scaffold verifier: PASS, `python3 scripts/verify_scaffold.py`.
- ESP32 `git diff --check`: PASS.
- Ignored backup check: PASS, the private peer backup `.bin` is ignored.

## Handoff

No continuation handoff is required for the first encrypted one-coordinator /
one-peer proof. Future work should start from a new scoped task for chunked
message delivery, custody telemetry, provisioning, firmware inventory, or
multi-peer behavior.
