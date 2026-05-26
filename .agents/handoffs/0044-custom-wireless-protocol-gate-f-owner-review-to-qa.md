# Handoff 0044: Gate F Firmware ABI Accepted Design Contract

Date: 2026-05-26

From: Codex owner-review pass

To: Firmware, Communications, QA

## Summary

`ADR-0006` is accepted as the ESP-NOW BBS Gate F firmware ABI design contract
only. The acceptance freezes simulator-derived ABI meanings for host-only review
and future planning, but it does not authorize coordinator or peer firmware
runtime implementation.

## Verified Facts

- Governance/docs, evidence-boundary, protocol/ABI, and QA reviewers returned
  PASS with no P1/P2 blockers.
- The accepted design contract preserves bridge `v:1`, the 512-byte bridge line
  budget, the ESP-NOW v1-compatible 250-byte radio packet budget, 32-byte packet
  header, 190-byte body budget, 16-fragment maximum, service code meanings,
  custody code meanings, and non-executing `control_intent`.
- Host-only ABI-freeze tests pin the bridge request set, service/custody code
  maps, frame budgets, and packet header field byte offsets.

## Assumptions

- Firmware runtime work will start with a separate owner gate for queue,
  scheduler, persistence, migration, recovery, and live-proof requirements.
- The Pi bridge remains the durable BBS custody and export boundary unless a
  later accepted ADR changes it.

## Unknowns

- Firmware queue depth, memory budget, timeout, retry, backpressure,
  persistence, migration/versioning, flash-wear, scheduler, recovery, and live
  proof policy remain unresolved.
- No coordinator or peer firmware runtime has implemented the Gate F contract.
- No live Gate F runtime evidence exists.

## Requested Next Actions

- QA: keep the ABI-freeze tests in the host-only suite and require a new owner
  gate before runtime or live proof work.
- Firmware/Communications: use `ADR-0006` as the design contract for planning
  only; do not add runtime queues, packet jobs, persistence, scheduler, migration,
  or bridge/export behavior without a separate accepted gate.

## Stop Gates

Do not implement coordinator or peer runtime ABI code from this handoff. Do not
add serial writes, bridge export requests, Win31 export controls, flash, erase,
monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin mutation, relay, XBee, TFT,
MicroSD, load, mains, or live proof work from this handoff.
