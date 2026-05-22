# ESP-NOW BBS Protocol Plan

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Pi to Coordinator Serial

The Pi bridge owns durable storage and sends compact coordinator commands over
USB serial. The first serial protocol should stay newline-delimited ASCII JSON
for diagnosability and continuity with the DOS-C simulator.

Initial command families:

- `hello`
- `diag_get`
- `peer_list`
- `peer_add`
- `peer_remove`
- `msg_send`
- `msg_ack`
- `fw_inventory`

Serial writes remain blocked until the flash/recovery and coordinator-firmware
gates are recorded.

## ESP-NOW Envelope

Future ESP-NOW frames should use a compact binary envelope:

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
