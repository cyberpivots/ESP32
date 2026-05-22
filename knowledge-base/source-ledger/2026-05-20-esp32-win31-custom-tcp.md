# Source Ledger - DOS-C Windows 3.1 Custom TCP Bridge

## Verified Facts

- ESP-IDF lwIP supports common BSD socket API usage in ESP-IDF. Source ID:
  `SRC-ESP-IDF-LWIP-SOCKETS`.
- The local safe-core contract uses public relay channels `1..4`, rejects `0`
  and values above `4`, and keeps hardware gates explicit. Source ID:
  `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`.
- The checked-in bridge for this cycle is a host-side simulator and protocol
  test target only.
- The simulator `state` response is compacted for the DOS-C 512-byte
  newline-delimited JSON limit and covered by protocol tests.
- DOS-C captured read-only COM6 evidence for a DevKitC-class ESP32-D0WDQ6
  board; use source ID `SRC-LOCAL-DOSC-ESP32-COM6-2026-05-20` for board
  inventory only, not final pinout or flashing decisions.

## Assumptions

- DOS-C owns the Windows 3.1 operator console and guest TCP/IP stack.
- ESP32 owns the simulator protocol shape and future firmware socket task.
- Simulator-first proof precedes live ESP32, relay, XBee, flashing, or monitor
  actions.

## Unknowns

- Whether the DOSBox-X SLIRP proof can complete from the Win16 app without more
  packet-driver work.
- Whether the later PCAP proof on Pi `eth0` will need package, capability, or
  switch-port changes.
- Final firmware task, storage, and Wi-Fi integration remain future work.
