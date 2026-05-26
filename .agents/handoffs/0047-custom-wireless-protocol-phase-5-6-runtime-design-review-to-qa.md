# Handoff 0047: Custom Wireless Protocol Phase 5/6 Runtime Design Review To QA

## Status

ESP32 accepts `ADR-0008` as a host-only runtime design-review and simulator
prototype gate. It does not add firmware runtime code or change the DOS-C
bridge/operator runtime.

## Verified Facts

- `ADR-0006` remains the accepted packet ABI design contract.
- `ADR-0007` remains the accepted runtime requirements-only gate.
- `ADR-0008` chooses host runtime defaults for queue bounds, retry/expiry,
  scheduler order, backpressure, duplicate handling, and visible counters.
- `control_intent` remains non-executing.
- The Pi bridge remains the durable BBS custody/export boundary.

## Assumptions

- DOS-C companion assurance remains source/host-only.
- Future firmware runtime implementation requires a separate owner gate and
  must not infer flash or live proof authority from the host prototype.

## Unknowns

- No Gate F firmware runtime implementation or live runtime proof exists.
- Firmware memory budget, task ownership, persistence, migration, recovery, and
  wear policy are not accepted.

## QA Next Steps

1. Run the ESP32 custom wireless protocol host tests.
2. Run scaffold and docs build/audit/smoke checks if documentation/public
   artifacts changed.
3. Run the DOS-C companion source guard with `ESP32_REPO=/mnt/h/ESP32`.
4. Keep firmware runtime, bridge/operator runtime, and live proof closed unless
   a later owner gate explicitly opens them.

## Stop Gates

Do not open ESP32 flashing, physical serial writes, PCAP, BLE, mesh,
router-admin, relay/XBee, SD-card, TFT, MicroSD, load, mains, erase, monitor,
bridge/operator runtime mutation, firmware runtime packet queues, persistence,
scheduler migration, or live proof from this handoff.
