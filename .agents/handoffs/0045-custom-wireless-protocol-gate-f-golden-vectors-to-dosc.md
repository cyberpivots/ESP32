# Handoff 0045: Gate F Golden Vectors to DOS-C Companion Assurance

Date: 2026-05-26

From: Codex host-only assurance pass

To: DOS-C bridge QA, Communications

## Summary

Gate F now has host-only full packet golden vectors for each accepted
simulator-derived service in `ADR-0006`. The vectors are assurance fixtures
only; they do not authorize firmware runtime implementation or bridge/operator
behavior changes.

## Verified Facts

- The ESP32 host test suite covers golden hex round trips for
  `direct_message`, `file_chunk`, `telemetry_report`, `node_status`,
  `custody_ack`, and `control_intent`.
- Each vector asserts both `encode_packet(packet).hex()` and
  `decode_packet(bytes.fromhex(hex))`.
- The source-index ID for this pass is
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`.
- `ADR-0006` remains a design contract only.

## Assumptions

- DOS-C companion work should use these vectors for source/ABI assurance only.
- DOS-C runtime bridge, Win31 operator, serial, PCAP, export, and live proof
  behavior should remain unchanged unless a separate owner gate opens that
  surface.

## Unknowns

- Firmware runtime queue, scheduler, persistence, migration, recovery, and live
  proof requirements remain unresolved.
- No live Gate F runtime packet job proof exists.

## Requested Next Actions

- Add DOS-C host/source guards that verify ESP32 `ADR-0006` acceptance, source
  IDs, radio/bridge budget constants, service/custody enum parity, and absence
  of runtime coordinator/peer job structs.
- Keep the DOS-C companion record explicit that it is assurance-only and does
  not accept runtime queues, persistence, scheduler, migration, or live proof.

## Stop Gates

Do not implement DOS-C runtime bridge changes from this handoff. Do not add
serial writes, bridge export requests, Win31 export controls, flash, erase,
monitor, BLE, ESP-WIFI-MESH, PCAP, router/admin mutation, relay, XBee, TFT,
MicroSD, load, mains, or live proof work from this handoff.
