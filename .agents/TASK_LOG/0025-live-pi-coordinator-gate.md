# Task 0025 - Live Pi Coordinator Gate

## Task

- ID: 0025-live-pi-coordinator-gate
- Owner role: Firmware, Hardware, Communications, QA
- Status: complete for live Pi-to-ESP32 coordinator dashboard proof
- Created: 2026-05-22
- Updated: 2026-05-22

## Goal

Prepare and run the live Pi dashboard to ESP32 coordinator proof without
bypassing the accepted architecture or opening unsafe hardware gates.

## Scope

Included:

- Current skill-path refresh for plugin cache hash `004da724`.
- Read-only Windows COM6 ESP32 identity refresh.
- Fresh Pi SSH identity and listener check.
- Pi USB serial inventory for `/dev/ttyUSB*`, `/dev/ttyACM*`, and pySerial
  ports.
- Follow-up Pi USB serial inventory after the ESP32 was moved to the Pi.
- Bounded UART probe for coordinator `hello`/`state`/`diag` response shape.
- Pi-side runtime staging of the fixed DOS-C bridge files, coordinator flash
  packet, and isolated esptool venv without running any flash operation.
- Physical USB-only/no-load user confirmation before any flash command.
- Pi-side esptool identity, private read-flash backup, coordinator flash, and
  post-flash UART `hello`/`state`/`diag` proof.
- Live Windows 3.1 OPCON proof over DOSBox-X serial-nullmodem to the Pi bridge
  and physical ESP32 coordinator.
- Final cleanup proof for DOSBox-X, modal, bridge, and listener processes.
- Durable source-ledger and handoff updates.

Excluded:

- Windows-to-Pi serial proxying.
- ESP-NOW radio traffic, relay action, XBee writes, TFT or MicroSD wiring or
  mounts, load wiring, and mains work.
- ESP32 erase, monitor, relay/XBee/TFT/MicroSD firmware lanes, PCAP, and any
  dashboard state-changing command.

## Sources

- `SRC-ESP-IDF-UART`
- `SRC-ESP-IDF-START-PROJECT`
- `SRC-ESPTOOL-BASIC`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-22`
- `SRC-LOCAL-LIVE-PI-COORDINATOR-GATE-2026-05-22`

## Decisions

- Keep the accepted live path as Pi bridge to physical USB serial ESP32
  coordinator.
- Do not build a Windows COM6 proxy because it would bypass the accepted
  architecture.
- Initial stop: ESP32 was not visible to the Pi as `/dev/ttyUSB*` or
  `/dev/ttyACM*`.
- Follow-up stop: ESP32 became visible to the Pi as `/dev/ttyUSB0`, but the
  current firmware did not return coordinator `hello`/`state`/`diag` JSON
  frames. It responded to `hello` with `[DEVICE] ack status=ignored ...`.
- Opened the flash gate only after the user confirmed USB-only/no relay/no
  XBee/no TFT/no MicroSD/no load/no mains state, Pi-side esptool identity
  matched the known ESP32, and a private full-flash backup completed.
- Keep ESP-NOW, relay, XBee, TFT, MicroSD, load wiring, mains, PCAP, and
  state-changing dashboard commands closed outside this completed proof.

## Validation

- `python3 scripts/live_bench_preflight.py --out research/bench-records/live-bench/live-pi-coordinator-preflight-20260522T031545Z.json`:
  PASS.
- Pi USB serial inventory:
  BLOCKED, no `/dev/ttyUSB*`, no `/dev/ttyACM*`, and no pySerial ports.
- Follow-up Pi USB serial inventory:
  PASS, `/dev/ttyUSB0` and `/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0`.
- Follow-up UART coordinator probe:
  BLOCKED, no matching `hello` response; current firmware returned
  `[DEVICE] ack status=ignored ...`.
- Pi-side esptool preparation:
  PASS, isolated runtime venv reports `esptool v5.2.0`; no esptool chip,
  read-flash, erase, or write-flash command was run.
- Fresh physical gate after user confirmation:
  PASS, user confirmed USB-only with no relay, XBee, TFT, MicroSD, load wiring,
  or mains wiring.
- Pi-side esptool identity:
  PASS, ESP32-D0WDQ6 rev v1.0, MAC `78:e3:6d:10:4d:6c`, detected 4 MB flash,
  3.3 V flash.
- Private flash backup:
  PASS, 4 MB read-flash backup SHA-256
  `00456c2e331c9dd6a48af73b3e59e848b930e3c673e36b8041eda97712079ce4`.
- Coordinator flash:
  PASS, staged bootloader, partition table, and coordinator app were written
  and verified by esptool.
- Coordinator UART proof:
  PASS, `hello`, `state`, and `diag` returned `status:"ok"` on `/dev/ttyUSB0`.
- Live Windows 3.1 dashboard proof:
  PASS, OPCON displayed `backend serial-readonly`, `serial physical-readonly`,
  coordinator MAC `78:e3:6d:10:4d:6c`, `status ok`, and disabled safety
  controls. Cleanup showed no bridge, DOSBox-X, modal, or `31331`/`31332`/`8080`
  listener.

## Handoff

Continue through
`.agents/handoffs/0015-live-pi-coordinator-gate-to-firmware-hardware-qa.md`.
The live Pi-to-ESP32 coordinator dashboard proof is complete for the bounded
read-only coordinator scope. ESP-NOW peer/channel/key proof, relay/XBee/TFT/
MicroSD/load/mains work, and broader hardware bring-up remain out of scope.
