# ESP-NOW BBS Protocol Plan

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Pi to Coordinator Serial

The Pi bridge owns durable storage and sends compact coordinator commands over
USB serial. The first serial protocol should stay newline-delimited ASCII JSON
for diagnosability and continuity with the DOS-C simulator.

Current physical proof command surface:

- `hello`
- `state`
- `diag`
- `peer_list`

The bridge and Win3.1 dashboard expose higher-level simulator/database
requests such as `diag_get`, `peer_list`, `msg_send`, `msg_ack`, and
`fw_inventory`, but the physical coordinator serial request surface remains
read-only for accepted live proof.

Current compact physical response fields include:

- `peers`
- `rx`
- `tx`
- `acks`
- `dups`
- `ttl_drop`
- `id`
- `mac`
- `role`
- `fw`
- `link`
- `rssi`
- `seen_ms`

Serial writes and dashboard state-changing commands remain blocked until a
separate accepted gate opens them.

## ESP-NOW Envelope

Current ESP-NOW frames use a compact binary envelope:

- version
- frame type
- source peer ID
- destination peer ID or broadcast marker
- sequence number
- ACK target
- TTL
- chunk index and chunk count
- payload
- CRC

Use v1-compatible payload sizing by default. Do not rely on ESP-NOW v2 longer
packets until every participating device is verified to support the selected
format.

The first live implementation uses encrypted unicast with PMK/LMK material from
ignored generated config, not tracked source. Tracked defaults keep encryption
disabled so build-only validation cannot accidentally embed live keys.

The first peer payload is a bounded `PING` frame from peer `peer01` to
coordinator `coord01`. The coordinator validates the peer, destination, and
allowed MAC before counting RX and returning an application-level ACK.

The accepted 2026-05-23 proof supports exactly three encrypted peer slots for
`peer01`, `peer02`, and `peer03` through ignored per-peer LMK/MAC overrides.
That proof accepted the then-current `COM4=peer01`, `COM5=peer02`, and
`COM6=peer03` map after fresh identity, backups, manifest review, and
flash/verify evidence.

The current 2026-05-25 America/Denver LAN/current-remap preflight, with UTC
evidence filenames on 2026-05-26, validates the current read-only identity map
as `COM6=peer01`, `COM10=peer02`, and `COM12=peer03`, with the coordinator on
Pi `/dev/ttyUSB0`. This remap evidence does not prove a fresh BBS runtime or
radio run. Before any future prepare or flash, the coordinator must be freshly
identified and must differ from all peer MACs.

## Reliability

ESP-NOW send status is not enough to prove application delivery. The firmware
must implement:

- application-level ACKs
- retry limits
- sequence numbers
- duplicate suppression
- TTL/hop limits
- explicit custody status returned to the Pi bridge

## Security Boundary

Use a peer allowlist and encrypted unicast where keys are provisioned. Broadcast
or discovery frames must not contain secrets. Keys, pairing tokens, and device
secrets must not be tracked in Git.

The 2026-05-22 encrypted proof closes the first one-coordinator/one-peer path:
the peer sent bounded encrypted PING frames, the coordinator returned
application ACKs, and the accepted Pi bridge/Win3.1 OPCON path showed peer
`peer01`, link `espnow-enc`, peer count `1`, zero serial errors, and changing
RX/TX/ACK counters.

The 2026-05-23 corrected proof accepts USB-only three-peer live radio behavior
for that proof packet. Later Gate H structured live acceptance proves the
accepted serial-nullmodem path with `bridge-transcript.jsonl`, BBS
post/pull/search/ack, download queue, non-executing OTAP intent, zero serial
errors, three `espnow-enc` peers, moving counters, DOS-C vision `pass`, ESP32
completion `pass`, and cleanup proof.

Gate G is accepted only as a local-admin redacted JSON export from the DOS-C/Pi
bridge spool under `ADR-0005`. Firmware export ABI, Win31 export controls, and
live bridge export request types remain closed.
