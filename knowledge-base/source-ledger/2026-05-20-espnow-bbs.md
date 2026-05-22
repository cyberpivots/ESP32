# ESP-NOW BBS Source Ledger

Accessed: 2026-05-20

## Verified Facts

- `SRC-ESP-IDF-ESPNOW` documents ESP-NOW as the Espressif protocol for this
  coordinator/client lane, including payload, peer, encryption, send-status,
  and application-acknowledgement considerations.
- `SRC-ESP-IDF-STABLE-ESP32` and `SRC-ESP-IDF-GET-STARTED` support choosing
  ESP-IDF stable v6.0.1 for the project-local firmware framework target.
- `SRC-ESPTOOL-BASIC` supports keeping read-only identity commands separate
  from explicitly gated flash/erase commands.
- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20` records that the DOS-C side now
  has a simulator-first Pi bridge, SQLite spool, BBS message queue, and
  maintenance-intent gate.

## Decisions Supported

- Use ESP-IDF v6.0.1 for future `espnow-bbs` coordinator/client firmware after
  toolchain and flash/recovery gates are recorded.
- Keep Windows 3.1 and the Pi bridge on newline JSON, but use compact binary
  ESP-NOW frames between ESP32 peers.
- Require application-level sequence numbers, ACKs, retries, duplicate
  suppression, and TTL/hop limits.
- Keep flashing, relay, XBee, mains/load, and SD imaging gates closed.

## Open Gaps

- No coordinator/client firmware source exists yet.
- No serial coordinator protocol proof exists yet.
- No first flash target and recovery method are recorded yet.
- The COM6 board remains physically unverified beyond read-only identity
  evidence from the DOS-C workspace.
