# Handoff 0043: Gate F Firmware ABI Owner Review

Date: 2026-05-26

From: Codex planning pass

To: Architecture, Firmware, Communications, QA

## Summary

Gate F now has a proposed ESP32 owner-review package in
`.agents/DECISIONS/ADR-0006-espnow-bbs-firmware-abi.md` and source ledger
`knowledge-base/source-ledger/2026-05-26-custom-wireless-protocol-gate-f-firmware-abi.md`.

The package is docs-only. It does not accept runtime firmware behavior.

## Verified Facts

- `ADR-0006` status is `Proposed`.
- The candidate preserves existing simulator `v:1`, 512-byte bridge frame
  boundary, 250-byte ESP-NOW v1-compatible packet budget, 32-byte header,
  190-byte body, and 16-fragment maximum.
- The candidate mirrors current simulator service and custody code meanings.
- `control_intent` remains non-executing.
- Gate G export remains local-admin only under accepted `ADR-0005`.
- Gate H structured live acceptance remains the current live BBS proof packet.

## Assumptions

- Owner review should accept, revise, or replace `ADR-0006` before firmware
  runtime migration.
- Firmware persistence should stay unresolved until a separate queue/custody
  persistence and flash-wear policy is accepted.

## Unknowns

- Accepted firmware packet ABI.
- Firmware queue depth, scheduler priority, timeout, retry, backpressure,
  persistence, migration, recovery, and runtime proof policy.
- Live Gate F runtime evidence.

## Requested Next Actions

- Architecture/Communications: review whether `bbs-fw-abi.v1` should preserve
  the simulator packet fields and code meanings as written.
- Firmware: identify queue, memory, scheduler, persistence, and migration
  constraints required before implementation.
- QA: define host-test and live-gate proof requirements before any firmware
  runtime work is authorized.

## Stop Gates

Do not implement coordinator or peer runtime ABI code from this handoff until
the ADR is accepted or replaced. Do not add serial writes, bridge export
requests, Win31 export controls, flash, erase, monitor, BLE, ESP-WIFI-MESH,
PCAP, router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, or live
proof work from this handoff.
