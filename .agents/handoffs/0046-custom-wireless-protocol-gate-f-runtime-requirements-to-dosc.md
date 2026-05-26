# Handoff 0046: Custom Wireless Protocol Gate F Runtime Requirements To DOS-C

## Status

ESP32 accepts `ADR-0007` as a requirements-only Gate F runtime owner gate. It
does not add firmware runtime code or change the DOS-C bridge/operator runtime.

## Verified Facts

- `ADR-0006` remains the accepted packet ABI design contract.
- `ADR-0007` accepts runtime requirements for bounded queues, custody lifecycle,
  retry/expiry behavior, scheduler/backpressure, volatile-only recovery, and
  live-proof prerequisites.
- Firmware flash persistence remains blocked behind a later persistence and
  wear-policy ADR.
- `control_intent` remains non-executing.
- The Pi bridge remains the durable BBS custody/export boundary.

## Assumptions

- DOS-C companion assurance should remain source/host-only.
- DOS-C source guards should verify ESP32 `ADR-0007` is accepted and indexed
  when `ESP32_REPO=/mnt/h/ESP32` is available.

## Unknowns

- No Gate F runtime implementation or live runtime proof exists.
- Exact queue depths, memory budgets, retry counts, timeout values, scheduler
  priorities, and persistence/wear policy are not finalized.

## DOS-C Next Steps

1. Add a companion source guard for ESP32 `ADR-0007` accepted/source-indexed
   status.
2. Preserve the existing source guard that `bbs_packet_job_t` is absent from
   coordinator and peer runtime code.
3. Add a DOS-C task, handoff, and source-index entry for companion assurance.
4. Do not change bridge/operator runtime behavior.

## Stop Gates

Do not open DOS-C bridge/operator runtime mutation, Win31 export controls,
ESP32 flashing, physical serial writes, PCAP, BLE, mesh, router-admin,
relay/XBee, SD-card, load, mains, erase, monitor, runtime packet queues,
persistence, scheduler, migration, or live proof from this handoff.
