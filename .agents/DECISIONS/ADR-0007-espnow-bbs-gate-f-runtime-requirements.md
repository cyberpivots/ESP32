# ADR-0007: ESP-NOW BBS Gate F Runtime Requirements

Status: Accepted

Date: 2026-05-26

## Context

`ADR-0006` accepts the ESP-NOW BBS custom wireless protocol firmware ABI as a
design contract only. It preserves packet layout, service codes, custody codes,
golden vectors, non-executing `control_intent`, and the Pi bridge custody/export
boundary, but it deliberately leaves runtime queues, scheduler behavior,
persistence, recovery, and live proof unresolved.

This ADR accepts host-only requirements for a later runtime implementation. It
does not add coordinator or peer runtime code.

## Verified Facts

- The accepted live BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- `ADR-0006` is accepted as a firmware ABI design contract only.
- The accepted packet contract uses protocol version `1`, service codes
  `direct_message=1`, `file_chunk=2`, `telemetry_report=3`, `node_status=4`,
  `custody_ack=5`, and `control_intent=6`.
- The accepted custody code set is `none`, `queued`, `sent`, `delivered`,
  `acked`, `failed`, and `expired`.
- Host tests pin the packet header byte layout and full encoded bytes for all
  accepted Gate F services.
- Simulator custody behavior already models retry eligibility for `queued` and
  `sent`, terminal behavior for `delivered`, `acked`, and `expired`, retry-limit
  behavior for `failed`, missing-fragment failure, and non-executing
  `control_intent`.
- ESP-NOW send callback success is MAC-layer status, not application delivery
  proof; application-level ACK, retry, timeout, sequence, and duplicate handling
  remain required for reliable application delivery.
- The Pi bridge remains the durable BBS custody and export boundary.

## Accepted Decision

Accept `gate-f-runtime-reqs.v1` as a requirements-only owner gate for a future
firmware runtime implementation.

### Packet-Job Queues

- Runtime packet jobs must remain bounded. Queue depth, memory budget, and
  overflow behavior must be explicit before implementation.
- Each queued job must preserve the `ADR-0006` packet contract: service,
  custody, flags, TTL, sequence number, message ID, fragment index/count,
  source node, destination node, body length, and bounded body bytes.
- Outbound direct-message, file-chunk, telemetry, node-status, custody-ACK, and
  non-executing control-intent records must not exceed the accepted packet and
  fragment limits.
- Queue-full or backpressure events must be bridge-visible as compact status or
  failure reasons; silent loss is not acceptable.

### Custody Lifecycle

- A bridge-accepted direct-message or file-chunk job begins as `queued`.
- A radio-send attempt moves custody to `sent` and increments the attempt count.
- `queued` and `sent` jobs are retry-eligible while attempts remain below the
  accepted retry limit and the job has not expired.
- `delivered`, `acked`, and `expired` are terminal runtime custody states.
- `failed` is retry-eligible only while attempts remain below the accepted retry
  limit; after the retry limit is reached it is terminal until a later bridge
  action creates new work.
- Missing fragments must not produce partial delivery. They must remain pending
  until recovery succeeds or fail/expire with a bridge-visible reason.

### Scheduler And Backpressure

- Runtime scheduling must be deterministic enough for host tests to assert job
  ordering, retry eligibility, expiry, and backpressure outcomes.
- Custody ACK work must not be starved by bulk file chunks.
- Bridge/UI responsiveness must not depend on unbounded radio retry loops.
- Scheduler counters for queued, sent, delivered, acked, failed, expired,
  dropped, and backpressure outcomes must be visible to the Pi bridge before
  live proof is requested.

### Recovery And Persistence

- The default for this gate is volatile firmware state only.
- Firmware must not persist packet queues, custody state, retry state, or
  scheduler state to flash under this ADR.
- Reboot or power loss may clear firmware queues; the Pi bridge spool remains
  the durable BBS custody boundary.
- Any firmware flash persistence, migration format, retention window, or wear
  policy remains blocked behind a later accepted persistence/wear-policy ADR.

### Live-Proof Prerequisites

Before a future runtime implementation can claim live acceptance, the project
must have:

- Host tests for queue bounds, retry/expiry behavior, terminal custody states,
  fragment failure, duplicate handling, and non-executing `control_intent`.
- DOS-C companion source guards confirming the accepted ESP32 ADR/source-index
  records and continued absence of packet-job runtime wiring where not
  authorized.
- Fresh same-session read-only identity/preflight, backup and manifest evidence
  if flashing is requested, exact firmware hashes, and a recovery path.
- `bridge-transcript.jsonl` plus pre-action and post-action telemetry refreshes
  for BBS/download/OTAP actions.
- Cleanup proof showing no stale DOSBox-X, modal, bridge, listener, or proof
  process state after the run.

## Assumptions

- Simulator custody semantics are the safest host-only seed for runtime
  requirements because they already have local ESP32 test coverage.
- Bounded volatile firmware state is enough for the first runtime slice because
  the Pi bridge owns durable BBS custody.
- Exact numeric queue depths, retry counts, and timeout values should be chosen
  in implementation review after memory and scheduler constraints are measured.

## Unknowns

- Exact queue depths, memory budgets, timeout values, retry counts, scheduler
  priorities, and backpressure thresholds are not finalized.
- Firmware persistence format, migration/versioning policy, flash wear impact,
  and recovery behavior are not accepted.
- No coordinator or peer firmware runtime has implemented these requirements.
- No live proof packet has exercised Gate F firmware packet queues, scheduler,
  expiry, retry-limit, recovery, or failure handling.

## Consequences

- Gate F now has accepted runtime requirements, but not runtime implementation
  authority.
- Future runtime code must remain compatible with `ADR-0006` and this ADR.
- Any implementation must preserve `control_intent` as non-executing unless a
  later accepted ADR explicitly changes that boundary.
- The Pi bridge remains the only accepted durable BBS custody/export boundary.

## Sources

- `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-ESP-IDF-ESPNOW`

## Stop Gates

This ADR does not authorize coordinator runtime migration, peer runtime
migration, serial writes, bridge export requests, Win31 export controls, flash,
erase, monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin mutation, relay, XBee,
TFT, MicroSD, load, mains, or live proof work.
