# ESP-NOW BBS Source Ledger

Accessed: 2026-05-20

## Verified Facts

- `SRC-ESP-IDF-ESPNOW` documents ESP-NOW as the Espressif protocol for this
  coordinator/client lane, including payload, peer, encryption, send-status,
  and application-acknowledgement considerations.
- `SRC-ESP-IDF-STABLE-ESP32` and `SRC-ESP-IDF-GET-STARTED` support choosing
  ESP-IDF stable v6.0.1 for the project-local firmware framework target.
- `SRC-ESPTOOL-BASIC` supports keeping read-only identity commands separate
  from explicitly gated flash/erase commands and supports full-flash backup
  capture with `read-flash 0 ALL`.
- `SRC-ESPTOOL-ADVANCED-VERIFY` supports optional post-write `verify-flash`
  only when matching flash mode, size, and frequency arguments are available.
- `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS` supports capturing
  `flasher_args.json` and `flash_project_args` from ESP-IDF build outputs.
- `SRC-DOSBOX-SERIAL-CONFIG` supports the serial/nullmodem configuration
  category used by the accepted DOSBox-X path; local DOSBox-X runtime behavior
  remains bench evidence, not an upstream-doc claim.
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20` records that the DOS-C side now
  has a simulator-first Pi bridge, SQLite spool, BBS message queue, and
  maintenance-intent gate.
- `SRC-LOCAL-LIVE-PI-COORDINATOR-GATE-2026-05-22` records the accepted
  Pi-visible coordinator USB serial proof for `hello`, `state`, and `diag`.
- `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22` records the first encrypted
  peer slice: firmware/bridge/OPCON implementation, ignored live PMK/LMK
  config generation, peer identity, peer backup, peer flash, and peer UART
  send-loop proof.

## Decisions Supported

- Use ESP-IDF v6.0.1 for future `espnow-bbs` coordinator/client firmware after
  toolchain and flash/recovery gates are recorded.
- Keep Windows 3.1 and the Pi bridge on newline JSON, but use compact binary
  ESP-NOW frames between ESP32 peers.
- Require application-level sequence numbers, ACKs, retries, duplicate
  suppression, and TTL/hop limits.
- Keep flashing, relay, XBee, mains/load, and SD imaging gates closed.
- Keep tracked defaults build-safe with encryption disabled and generated
  PMK/LMK values only under ignored `secrets/espnow-bbs/`.
- Require the three-peer live gate to pass fresh identity, backup, build-hash,
  recovery, and explicit write confirmation before any COM4/COM5/COM6 or Pi
  coordinator flash.

## Open Gaps

- Closed for first one-coordinator/one-peer encrypted proof by the 2026-05-22
  follow-up ledger: fresh coordinator gate, coordinator backup/flash, encrypted
  receive, application ACK, bridge log, and Win3.1 OPCON screenshot proof all
  passed. Future work remains for multi-peer behavior, chunked messages,
  provisioning, and firmware inventory.
- Relay, XBee, TFT, MicroSD, load wiring, mains wiring, PCAP, Windows COM
  proxy, erase, and dashboard state-changing commands remain closed.
- The Windows COM6 peer is identity-verified and privately backed up for this
  proof, but its carrier board remains physically unverified beyond USB serial
  identity and flash evidence.
- Three-peer live acceptance remains open until the new live gate records
  passing COM4/COM5/COM6 identity, distinct coordinator identity, private
  backups, generated ignored config, build hashes, flashes, Win3.1/Pi evidence,
  and cleanup proof.
