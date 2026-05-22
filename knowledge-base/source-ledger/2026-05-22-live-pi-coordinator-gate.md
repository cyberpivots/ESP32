# Live Pi Coordinator Gate - 2026-05-22

## Sources

- `SRC-ESP-IDF-UART`
- `SRC-ESP-IDF-START-PROJECT`
- `SRC-ESPTOOL-BASIC`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-22`
- `SRC-LOCAL-LIVE-PI-COORDINATOR-GATE-2026-05-22`

## Verified Facts

- The current GitHub and Canva plugin cache hash is `004da724`.
- Read-only preflight on 2026-05-22 again identified Windows COM6 as a
  Silicon Labs CP210x USB-to-UART bridge to an ESP32-D0WDQ6 with MAC
  `78:e3:6d:10:4d:6c` and 4 MB flash.
- Fresh Pi SSH fingerprints matched the expected RSA, ECDSA, and ED25519
  fingerprints. SSH identity matched hostname `dos-pi4-poe`, Raspberry Pi 4
  Model B Rev 1.2, serial `10000000aaaa5b24`, root `/dev/mmcblk0p2`, and
  address `192.168.200.104`.
- The Pi had no listener on `31331`, `31332`, or `8080` before the gate check.
- The Pi USB serial inventory found no `/dev/ttyUSB*` or `/dev/ttyACM*`
  devices and pySerial reported no ports.
- After the ESP32 was moved to the Pi, the verified Pi reported `/dev/ttyUSB0`
  and `/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0`
  for a CP2102 USB-to-UART bridge with VID:PID `10C4:EA60`.
- A bounded UART probe on `/dev/ttyUSB0` sent only a coordinator `hello`
  request. The device did not return the coordinator JSON `hello` response; it
  returned `[DEVICE] ack status=ignored ...`.
- The Pi runtime now has the fixed DOS-C bridge files, a staged coordinator
  flash packet, and an isolated esptool venv reporting `esptool v5.2.0`.
- No esptool chip query, read-flash backup, erase, write-flash, DOSBox-X
  launch, bridge listener, or live dashboard proof was run.
- After user confirmation of USB-only/no relay/no XBee/no TFT/no MicroSD/no
  load/no mains state, Pi-side esptool identity matched ESP32-D0WDQ6 revision
  v1.0, MAC `78:e3:6d:10:4d:6c`, 4 MB flash, and 3.3 V flash.
- A private 4 MB read-flash backup completed before flashing. Backup SHA-256:
  `00456c2e331c9dd6a48af73b3e59e848b930e3c673e36b8041eda97712079ce4`.
- Esptool wrote and verified the staged coordinator bootloader, partition
  table, and app.
- Post-flash UART proof on `/dev/ttyUSB0` returned `status:"ok"` for
  coordinator `hello`, `state`, and `diag`.
- Live DOSBox-X/Windows 3.1 OPCON proof used the accepted path:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge 127.0.0.1:31332 ->
  serial-readonly /dev/ttyUSB0 -> ESP32 coordinator`.
- OPCON screenshot showed `backend serial-readonly`, `serial
  physical-readonly`, coordinator MAC `78:e3:6d:10:4d:6c`, `status ok`, and
  disabled Relay/Flash/Serial/PCAP controls.
- Cleanup proof showed no DOSBox-X, modal, bridge process, or
  `31331`/`31332`/`8080` listener.

## Assumptions

- The intended live architecture remains Pi USB serial to the ESP32
  coordinator, not Windows COM6 proxying.
- Future live checks will re-verify the Pi serial path before use instead of
  assuming `/dev/ttyUSB0` remains stable.

## Unknowns

- ESP-NOW peer/channel/key/radio proof remains separate and unproven.
- Relay, XBee, TFT, MicroSD, load wiring, and mains wiring remain out of scope
  and untested by this coordinator proof.
- The private backup is recorded by hash and retained in ignored Pi runtime
  storage, not in Git.

## Gate Result

The live Pi-to-ESP32 coordinator dashboard proof is accepted for the bounded
read-only coordinator scope. It proves the physical Pi USB serial coordinator
path and Windows 3.1 dashboard telemetry path.

This proof did not run ESP-NOW peer traffic, relay action, XBee write, TFT or
MicroSD mount, load wiring, mains work, Windows COM6 proxy, PCAP, or any
state-changing dashboard command.

## Validation

- `python3 scripts/live_bench_preflight.py --out research/bench-records/live-bench/live-pi-coordinator-preflight-20260522T031545Z.json`:
  PASS.
- Pi USB serial inventory over run-local SSH trust:
  BLOCKED, no `/dev/ttyUSB*`, no `/dev/ttyACM*`, no pySerial ports.
- Follow-up Pi USB serial inventory:
  PASS, `/dev/ttyUSB0` and CP2102 VID:PID `10C4:EA60` visible on the Pi.
- Follow-up coordinator UART probe:
  BLOCKED, current firmware returned `[DEVICE] ack status=ignored ...` instead
  of a coordinator `hello` JSON frame.
- Follow-up cleanup:
  PASS, no `31331`, `31332`, or `8080` listener and no bridge, DOSBox-X, or
  modal process remained.
- Private flash backup:
  PASS, full 4 MB backup read before write.
- Coordinator flash:
  PASS, esptool verified written data.
- Post-flash UART:
  PASS, `hello`/`state`/`diag` returned coordinator JSON.
- Live Win31 proof:
  PASS, bridge log recorded `hello`, `state_get`, `peer_list`, `diag_get`,
  `fw_inventory`, `coordinator_state`, and `msg_pull` over
  `serial-nullmodem`; screenshot hash
  `37b686dfcda0965272918995551f55908fc849fcbad6fefe91492b8c8bd7c745`.
