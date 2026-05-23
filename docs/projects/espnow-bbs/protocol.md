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
- `peer_list` (source-level implementation added for the next three-peer
  proof; live acceptance still pending)

The bridge and Win3.1 dashboard may expose higher-level simulator/database
requests such as `diag_get`, `peer_list`, `msg_send`, `msg_ack`, and
`fw_inventory`, but the physical coordinator serial request surface remains
read-only for the encrypted peer proof.

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

The next source-level coordinator shape supports exactly three encrypted peer
slots for `peer01`, `peer02`, and `peer03` through ignored per-peer LMK/MAC
overrides. Live acceptance requires fresh COM4/COM5/COM6 identity and backup
evidence before any flash.

The live gate maps peers by verified Windows port order only after a passing
preflight: `COM4=peer01`, `COM5=peer02`, and `COM6=peer03`. The coordinator
must be freshly identified on Pi `/dev/ttyUSB0`, and its MAC must differ from
all peer MACs before prepare or flash work can proceed.

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

The 2026-05-23 source update extends the parser and config shape for three
peers, and the follow-up ESP32 tooling adds preflight/manifest gates, but this
does not prove live three-peer radio behavior.
