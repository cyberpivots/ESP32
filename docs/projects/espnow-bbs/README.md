# ESP-NOW BBS Coordinator and Client Firmware

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Purpose

This project lane supports the DOS-C off-grid BBS architecture:

`Windows 3.1 dashboard -> DOSBox-X/NETTSR -> Raspberry Pi bridge -> USB serial -> ESP32 coordinator -> ESP-NOW clients`

The ESP32 firmware responsibility is limited to the coordinator and client
radio/device behavior. Durable BBS storage, sysop UI, and firmware management
remain outside the ESP32 firmware image.

## Current Status

- ADR-0003 accepts ESP-IDF v6.0.1 for this `espnow-bbs` lane.
- The accepted live baseline is the Pi-visible ESP32 coordinator answering
  USB serial `hello`, `state`, and `diag` through the Win3.1 OPCON dashboard
  path.
- DOS-C now contains the first encrypted one-peer ESP-NOW PING/ACK
  implementation, with tracked defaults keeping encryption disabled and live
  PMK/LMK material generated only under ignored `secrets/espnow-bbs/`.
- The Windows COM6 peer was identified as ESP32-D0WDQ6 MAC
  `78:e3:6d:0a:90:14`, privately backed up, flashed with the live encrypted
  peer build, and observed sending bounded PING attempts.
- The first live encrypted proof is accepted: after fresh Pi/coordinator
  identity, USB-only/no-load/no external wiring confirmation, and private
  coordinator backup, the coordinator was flashed and Win3.1 OPCON showed
  peer `peer01`, link `espnow-enc`, peer count `1`, and moving RX/TX/ACK
  counters over the accepted Pi bridge path.
- DOS-C source now contains the next multi-peer dashboard slice: original
  Win31 retro splash, Message Board search/pull/post/ack controls, bounded
  peer/message row parsing, coordinator serial `peer_list`, three encrypted
  coordinator peer slots, and ignored timestamped live config generation for
  `peer01` through `peer03`. This is source-level implementation only until
  fresh COM4/COM5/COM6 identity, backups, builds, flashes, and live radio proof
  pass.
- ESP32 tooling now provides the three-peer live gate: read-only preflight for
  `COM4`, `COM5`, `COM6`, Pi `172.16.0.2`, and coordinator `/dev/ttyUSB0`,
  plus prepare/flash manifest tooling that records backups, build hashes, and
  recovery commands before any explicit write-confirmed flash.
- A fresh read-only preflight on 2026-05-23 found exactly three Windows CP210x
  ESP32 peers on `COM4`, `COM5`, and `COM6`, all ESP32-D0WDQ6 with 4 MB flash
  and distinct MACs. Direct Pi access at `172.16.0.2` failed from the current
  host route, but the accepted WAN-side SSH-forwarded address
  `192.168.137.93` reached the Pi and passed host-key, hostname, serial, root,
  `eth0=172.16.0.2/24`, stale listener, stale process, and `/dev/ttyUSB0`
  presence gates. Pi-side `esptool` was installed from Debian Trixie and the
  live gate now uses `--no-stub` for Pi coordinator operations. The latest
  forwarded read-only preflight passed with coordinator MAC
  `78:e3:6d:10:4d:6c`, distinct from the three peers. Source ID:
  `SRC-LOCAL-ESPNOW-LIVE-PREFLIGHT-2026-05-23`.
- ADR-0004 proposes ESP-WIFI-MESH as a future self-healing branch and BLE GATT
  as the Android client-node interface model, but no firmware migration is
  accepted. The paired DOS-C bridge/operator source now has simulator-only
  network metadata and a read-only Win31 Network view.

## Firmware Roles

- Coordinator: USB serial command endpoint, ESP-NOW peer table, read-only
  `hello`/`state`/`diag`/`peer_list`, channel/key
  policy, ACK/retry handling, duplicate suppression, TTL enforcement, and
  compact telemetry back to the Pi bridge.
- Client: provisioned identity, bounded receive/send queues, app-level ACKs,
  diagnostics, firmware version reporting, and store-and-forward message
  handling.

## Safety Boundaries

- This lane does not control relays, XBee modules, mains/load wiring, or SD
  imaging.
- The peer flash was limited to the Windows COM6 ESP32 after read-only identity
  and private backup evidence passed.
- The coordinator encrypted flash was limited to the accepted Pi USB serial
  device after fresh identity, USB-only/no-load/no external wiring evidence,
  stale listener absence, and private backup passed.
- Relay, XBee, TFT, MicroSD, load, mains, PCAP, Windows COM proxy, erase, and
  dashboard state-changing commands remain closed.
- Three-peer flashing remains closed until the new live gate passes in a fresh
  same-session run and `scripts/espnow_bbs_live_gate.py flash` is invoked with
  explicit write confirmation.

## Implementation Order

1. Preserve the accepted serial-nullmodem dashboard path and stop extending the
   failed SLIRP packet-driver callback lane for OPCON.
2. Keep ESP-IDF v6.0.1 toolchain evidence current.
3. Preserve the accepted coordinator USB serial `hello`/`state`/`diag` proof.
4. Add chunked message delivery and custody telemetry.
5. Add provisioning and firmware inventory flows.
6. Prove multi-peer behavior only under the new three-peer live gate.
7. Keep ESP-WIFI-MESH/BLE GATT work design-only until ADR-0004 is accepted and
   fresh mesh, BLE, coexistence, backup, recovery, and cleanup evidence exists.
8. Confirm physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state,
   then run the backup/manifest `prepare` step before any flash or Win31 live
   acceptance work.
