# ESP-NOW Encrypted Peer Proof Ledger

Accessed: 2026-05-22

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESP-IDF-START-PROJECT`
- `SRC-ESP-IDF-UART`
- `SRC-ESPTOOL-BASIC`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-LOCAL-LIVE-PI-COORDINATOR-GATE-2026-05-22`
- `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22`

## Verified Facts

- The accepted coordinator baseline remains MAC `78:e3:6d:10:4d:6c` from the
  2026-05-22 live Pi coordinator gate.
- Fresh Pi identity for the encrypted coordinator flash pass reported
  `dos-pi4-poe`, Raspberry Pi 4 Model B Rev 1.2, serial
  `10000000aaaa5b24`, root `/dev/mmcblk0p2`, and no stale
  `31331`/`31332`/`8080` listeners.
- Windows serial enumeration found exactly one serial port for this pass:
  Silicon Labs CP210x USB to UART Bridge on `COM6`, PNP ID
  `USB\VID_10C4&PID_EA60\0001`.
- Read-only peer identity on COM6 reported ESP32-D0WDQ6 revision v1.0, MAC
  `78:e3:6d:0a:90:14`, 40 MHz crystal, 4 MB flash, and 3.3 V flash.
- The peer MAC is distinct from the accepted coordinator MAC.
- The generated encrypted bench override was written to ignored
  `/mnt/h/dos-c/secrets/espnow-bbs/sdkconfig.live.defaults`. The generator
  reported that secrets were generated but not printed.
- Generated coordinator and peer `sdkconfig` files were ignored and showed
  encryption enabled, channel `1`, coordinator MAC `78:e3:6d:10:4d:6c`, and
  peer MAC `78:e3:6d:0a:90:14`. PMK and LMK values were not printed in records.
- A private peer read-flash backup completed before the peer write:
  `research/bench-records/live-bench/peer-com6-read-flash-20260522T055649Z.bin`.
- Peer backup size: `4194304` bytes.
- Peer backup SHA-256:
  `5b612d6070117c179e0e526228222bf0781d74a9eca1e387e1cbeea18f9151c4`.
- Clean live ESP-IDF builds passed for both coordinator and peer after tracked
  defaults were combined with the ignored encrypted live override.
- Peer flash on COM6 used esptool `write-flash`, auto-detected 4 MB flash, and
  verified the bootloader, partition table, and app regions.
- A 20-second read-only COM6 UART sample after peer flash showed the peer send
  loop running:
  - `tx=6`, `rx=0`, `app_acks=0`
  - `tx=7`, `rx=0`, `app_acks=0`
  - `tx=8`, `rx=0`, `app_acks=0`
  - `tx=9`, `rx=0`, `app_acks=0`
- The user confirmed the coordinator was USB-only with no relay, XBee, TFT,
  MicroSD, load wiring, mains wiring, or other external wiring attached before
  coordinator flash.
- Fresh Pi-side coordinator identity on `/dev/ttyUSB0` reported
  ESP32-D0WDQ6 revision v1.0, MAC `78:e3:6d:10:4d:6c`, 40 MHz crystal, 4 MB
  flash, and 3.3 V flash.
- A private coordinator read-flash backup completed before the coordinator
  write:
  `research/bench-records/live-bench/encrypted-coordinator-read-flash-20260522T064120Z.bin`.
- Coordinator backup size: `4194304` bytes.
- Coordinator backup SHA-256:
  `4b8fe3d68b053dd67825576b555db18701a9371388e6079549e746d2ce63a32e`.
- Coordinator encrypted flash on the Pi passed and esptool verified the
  bootloader, partition table, and app regions.
- Physical UART proof on `/dev/ttyUSB0` passed for `hello`, `state`, and
  `diag`; the `diag` response showed peer `peer01`, MAC
  `78:e3:6d:0a:90:14`, role `peer`, link `espnow-enc`, RX/TX/ACK `8/8/8`,
  duplicates `0`, TTL drops `0`, RSSI `-12`, and recent `seen_ms`.
- Final Win3.1 OPCON proof passed in
  `research/bench-records/live-bench/encrypted-peer-20260522T070112Z/`.
  Screenshots showed status `ok`, `serial-readonly`, `physical-readonly`, peer
  count `1`, peer `peer01`, MAC `78:e3:6d:0a:90:14`, link `espnow-enc`,
  disabled unsafe controls, zero serial errors, and RX/TX/ACK counters moving
  from `148/148/147` to `158/158/158`.
- Cleanup proof showed no DOSBox-X, zenity/modal, bridge process, or
  `31331`/`31332`/`8080` listener remained.

## Implementation Facts

- DOS-C firmware now has tracked build-safe defaults with ESP-NOW encryption
  disabled and no tracked PMK/LMK values.
- DOS-C firmware has an ignored live config generator for one coordinator and
  one peer, validating channel and MAC inputs and refusing zero/equal MACs.
- Coordinator firmware initializes Wi-Fi STA and ESP-NOW only when live config
  is complete, registers the encrypted peer, validates peer PING frames, counts
  RX/TX/ACK/duplicate/TTL-drop telemetry, and keeps receive callbacks short by
  queueing radio work to a task.
- Peer firmware initializes Wi-Fi STA and ESP-NOW only when live config is
  complete, registers the encrypted coordinator peer, sends bounded PING frames,
  and logs send/ACK counters.
- The Pi bridge and OPCON parser/display now propagate peer count, RX/TX, ACKs,
  duplicates, TTL drops, identity, MAC, role, firmware, link, RSSI, and seen
  age through the existing read-only dashboard path.

## Assumptions

- The first encrypted bench proof uses channel `1`, coordinator ID `coord01`,
  and peer ID `peer01`.
- The peer is USB-only on the Windows 11 host for this proof. No relay, XBee,
  TFT, MicroSD, load, or mains wiring was verified or touched.

## Unknowns

- Multi-peer behavior, chunked message delivery, custody beyond PING/ACK,
  provisioning UX, and firmware inventory flows remain future work.

## Stop Gate

The first encrypted one-coordinator/one-peer proof gate is closed. Do not infer
authorization for relay, XBee, TFT, MicroSD, load, mains, PCAP, Windows COM
proxy, erase, or dashboard state-changing controls from this result.
