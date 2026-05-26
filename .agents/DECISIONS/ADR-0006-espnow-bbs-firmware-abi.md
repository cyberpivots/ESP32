# ADR-0006: ESP-NOW BBS Gate F Firmware ABI Design Contract

Status: Accepted

Date: 2026-05-26

## Context

Gate B, Gate C, Gate D, and Gate E have simulator and draft bridge evidence for
the custom wireless protocol lane. Gate G is accepted only as a local-admin
redacted JSON export under `ADR-0005`. Gate H structured live acceptance is
accepted for the existing serial-nullmodem BBS path.

Gate F is the firmware-facing owner-reviewed design-contract step. It describes
what the coordinator/client firmware ABI must preserve from the simulator before
any packet jobs, queues, persistence, scheduler, migration, or runtime proof work
can be accepted.

## Verified Facts

- The accepted live BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Gate E bridge fixtures use `v:1`, newline-delimited ASCII JSON, and a
  512-byte pre-newline bridge-frame budget.
- The Gate E draft bridge request set is `msg_post`, `download_queue`,
  `telemetry_report`, `node_status`, `protocol_report`, `state_get`, and
  `control_intent`.
- The simulator radio packet model uses protocol version `1`, a
  v1-compatible 250-byte ESP-NOW payload budget, a 32-byte packet header, a
  190-byte body budget, and a 16-fragment maximum.
- The simulator service code meanings are:

| Service | Code |
| --- | ---: |
| `direct_message` | 1 |
| `file_chunk` | 2 |
| `telemetry_report` | 3 |
| `node_status` | 4 |
| `custody_ack` | 5 |
| `control_intent` | 6 |

- The simulator custody code meanings are:

| Custody status | Code |
| --- | ---: |
| `none` | 0 |
| `queued` | 1 |
| `sent` | 2 |
| `delivered` | 3 |
| `acked` | 4 |
| `failed` | 5 |
| `expired` | 6 |

- Simulator `control_intent` records are non-executing and report
  `executed: false` with reason `control_intent_non_executing`.
- `ADR-0003` accepts ESP-IDF v6.0.1 only for the `espnow-bbs` project lane;
  this ADR does not add firmware code.
- Same-session agent quorum owner review on 2026-05-26 found no P1/P2 blockers
  for accepting this ADR as a design contract only.

## Accepted Decision

Accept `bbs-fw-abi.v1` as a firmware ABI design contract only. This acceptance
does not authorize coordinator or peer runtime code and must not be wired into a
firmware implementation until a separate owner gate accepts queue, scheduler,
persistence, migration, runtime-proof, and recovery requirements.

The accepted design-contract firmware ABI must preserve these
simulator-derived boundaries:

- `v:1` for bridge-facing request and response compatibility.
- ESP-NOW v1-compatible radio packet budgeting unless a later accepted ADR
  expands the payload size.
- The current simulator service and custody code meanings exactly as listed in
  this ADR.
- A packet header field set matching the simulator model: version, service
  code, flags, TTL, sequence number, message ID, fragment index, fragment
  count, source node, destination node, body length, and custody status.
- Packetized service jobs for direct messages, file chunks, telemetry reports,
  node status reports, custody ACKs, and non-executing control intents.
- Application-level ACK, retry, duplicate suppression, TTL expiry, fragment
  reassembly, and custody-status reporting before any delivery claim.

The firmware review package should treat these as review labels, not accepted
runtime object names:

- `outbound_radio_jobs`: bridge-owned work split into bounded radio packets.
- `inbound_packets`: decoded packets awaiting validation, dedupe, and service
  handling.
- `custody_ack_events`: application ACK frames and custody updates visible to
  the Pi bridge.
- `telemetry_reports`: compact node/link/status reports to the bridge.
- `control_intent_records`: non-executing intent records only.

The Pi bridge remains the durable BBS custody and export boundary. No firmware
analytics export ABI, Win31 export control, live bridge export request type, or
firmware-resident report export is proposed by Gate F.

## Assumptions

- The simulator constants are the safest candidate ABI seed because they are
  already covered by ESP32 host tests and DOS-C fixture replay.
- Keeping the 250-byte ESP-NOW v1-compatible packet budget avoids accepting a
  larger format before all participating devices and fixtures are explicitly
  reviewed.
- Firmware persistence, if ever needed, requires a separate source-backed
  persistence and wear-policy review before storing queue or custody state in
  flash.
- Runtime migration should start from simulator parity and host tests before a
  live firmware build, flash, or radio run is requested.

## Unknowns

- Firmware queue depths, memory budgets, timeout values, retry counts,
  scheduler priority, backpressure policy, and failure telemetry are not
  finalized.
- Firmware persistence format, migration/versioning policy, flash wear impact,
  and recovery behavior are not accepted.
- No coordinator or peer firmware runtime has implemented this ABI.
- No live proof packet has exercised Gate F firmware packet jobs, queues,
  persistence, scheduler behavior, migration, or runtime failure handling.

## Owner Review Evidence

- Governance/docs review: PASS, no P1/P2 blockers.
- Evidence-boundary review: PASS, no P1/P2 blockers.
- Protocol/ABI review: PASS, no P1/P2 blockers.
- QA review: PASS, no P1/P2 blockers.
- P3 follow-ups were handled or recorded: host-only ABI-freeze tests now pin the
  request set, service codes, custody codes, frame budgets, and packet header
  byte layout; runtime queue, persistence, scheduler, migration, recovery, and
  live proof remain future gates.

## Consequences

- Gate F has an accepted ESP32 firmware ABI design contract only.
- Future firmware work may use this ADR for host-only ABI-freeze tests and
  planning, but runtime code still requires a separate owner gate before adding
  packet/job queues, persistence, scheduler, migration, or live proof behavior.
- Gate E bridge ABI, Gate G export policy, and Gate H live acceptance remain
  supporting evidence only; none of them accepts firmware ABI runtime behavior.
- `control_intent` stays non-executing and cannot be treated as relay, flash,
  erase, radio, router/admin, BLE, mesh, TFT, MicroSD, load, mains, or serial
  write authority.

## Sources

- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIEF-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`

## Stop Gates

This ADR does not authorize coordinator runtime migration, peer runtime
migration, serial writes, bridge export requests, Win31 export controls, flash,
erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin mutation, relay, XBee,
TFT, MicroSD, load, mains, or live proof work.
