# ADR-0008: ESP-NOW BBS Phase 5/6 Runtime Design Review

Status: Accepted

Date: 2026-05-26

## Context

`ADR-0007` accepts Gate F runtime requirements as host-only planning for a
future firmware runtime implementation. It deliberately leaves exact queue
depths, retry values, expiry values, scheduler ordering, and backpressure
thresholds unresolved.

This ADR accepts a Phase 5 runtime design review and a Phase 6 host-only
runtime prototype. It does not add coordinator or peer firmware runtime code.

## Verified Facts

- The accepted live BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- `ADR-0006` remains the accepted packet ABI design contract.
- `ADR-0007` remains requirements-only and blocks firmware queue persistence
  behind a later persistence/wear-policy ADR.
- The existing simulator enforces 512-byte ASCII bridge lines, 250-byte radio
  payloads, 32-byte headers, 190-byte bodies, and 16-fragment packet jobs.
- DOS-C source guards already verify `ADR-0007` accepted/source-indexed status
  and preserve the absence of `bbs_packet_job_t` from coordinator and peer
  runtime source.

## Accepted Decision

Accept `gate-f-runtime-host-prototype.v1` as a host-only Phase 5/6 design and
test gate.

### Runtime Defaults

- `outbound_radio_jobs=32`
- `inbound_packets=32`
- `custody_ack_events=16`
- `telemetry_reports=8`
- `node_status_reports=8`
- `control_intent_records=8`
- `duplicate_window=64`
- `max_attempts=3`, counting the first send attempt
- `tick_ms=250` as metadata only; host tests advance integer ticks
- `retry_delay_ticks=2`
- `job_expiry_ticks=20`

### Scheduler Order

For each dispatch decision, the host runtime prototype must use this order:

1. Expire due jobs.
2. Apply inbound ACK and duplicate handling before dispatch.
3. Dispatch custody ACK work before bulk data.
4. Dispatch due retries.
5. Dispatch queued direct messages.
6. Dispatch one queued file chunk using deterministic ordering.
7. Dispatch telemetry or node-status work.
8. Preserve `control_intent` as report-only and non-executing.

Same-priority ordering uses `(created_tick, sequence, message_id,
fragment_index)`.

### Backpressure

- Packet-job admission is atomic. If a bridge request needs more packet slots
  than are available, the whole request fails with
  `reason:"backpressure_queue_full"` plus `queue`, `needed`, and `available`.
- Custody ACK work is not evicted by bulk jobs.
- Telemetry and node-status reports may coalesce the latest report per node and
  must increment bridge-visible counters when they do.
- Silent loss fails the gate.

### Runtime Interface

The host-only prototype may add simulator code for:

- `RuntimeConfig`
- `PacketJob`
- `RuntimeState`
- `RuntimeScheduler.submit_bridge_frame()`
- `RuntimeScheduler.submit_bridge_line()`
- `RuntimeScheduler.enqueue_packet_job()`
- `RuntimeScheduler.apply_inbound_packet()`
- `RuntimeScheduler.apply_custody_ack()`
- `RuntimeScheduler.tick()`
- `RuntimeScheduler.dispatch_one()`
- `RuntimeScheduler.snapshot()`
- `RuntimeScheduler.protocol_report()`

## Assumptions

- Balanced host defaults are acceptable for simulator coverage and future
  implementation review; they are not measured firmware memory budgets.
- Volatile runtime state remains the only accepted default for this gate.
- The Pi bridge remains the durable BBS custody/export boundary.

## Unknowns

- Firmware memory budget, ISR/task ownership, ESP-NOW callback integration,
  and C runtime data structures are not accepted.
- Firmware persistence format, migration/versioning policy, retention window,
  and flash wear policy are not accepted.
- No live proof has exercised this runtime prototype on ESP32 firmware.

## Consequences

- Host tests now pin exact runtime design defaults and scheduler/backpressure
  behavior before firmware implementation begins.
- Future firmware runtime work must either match this host design or update it
  through a later accepted owner gate.
- This ADR does not authorize flash, erase, monitor, serial writes, live proof,
  bridge export requests, Win31 export controls, BLE, mesh, PCAP, relay, XBee,
  TFT, MicroSD, load, mains, or router/admin mutation.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`
- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`

## Stop Gates

This ADR does not authorize coordinator runtime migration, peer runtime
migration, firmware queue persistence, serial writes, bridge export requests,
Win31 export controls, flash, erase, monitor, BLE, ESP-WIFI-MESH, PCAP,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, or live proof
work.
