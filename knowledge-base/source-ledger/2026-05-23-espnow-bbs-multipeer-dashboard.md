# ESP-NOW BBS Multi-Peer Dashboard Source Ledger

Accessed: 2026-05-23

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESPTOOL-BASIC`
- `SRC-ESPTOOL-ADVANCED-VERIFY`
- `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS`
- `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22`
- `SRC-LOCAL-ESPNOW-MULTIPEER-DASHBOARD-2026-05-23`
- `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23`

## Verified Facts

- The accepted live transport remains Win3.1 OPCON through DOSBox-X COM1
  nullmodem to the Pi bridge and Pi USB serial coordinator.
- The 2026-05-23 work is source-level only unless live evidence later proves
  fresh COM4/COM5/COM6 peer identity, backups, builds, flashes, and three-peer
  radio counters.
- DOS-C source now has a bounded `peer_list` coordinator serial response path,
  three encrypted coordinator peer slots, ignored timestamped live config
  generation, OPCON bounded peer/message row parsing, Message Board search, and
  a Program Manager DDE helper.
- ESP32 source now has a tooling-first three-peer gate that refuses live flash
  until a passing preflight, full backups, build hashes, recovery commands, and
  explicit write confirmation are present.

## Unknowns

- Current Windows peer inventory for COM4, COM5, and COM6.
- Current MAC-to-peer mapping for the three-peer bench.
- Live three-peer ESP-NOW encrypted RX/TX/ACK behavior.
- Reboot persistence of the Win3.1 Program Manager item.
- Whether the live gate prepare/flash sequence passes against the actual
  COM4/COM5/COM6 and Pi `/dev/ttyUSB0` devices in a same-session run.

## Stop Gate

Do not flash coordinator or peer firmware from this record alone. Live work
must start with fresh identity, private backups, build hashes, and recovery
path evidence.
