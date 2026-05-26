# Handoff 0051 - Win31 Dashboard Visual Design Continuation To QA

## Context

The DOS-C Win31 operator source now has the two-row plain-label navigation
strip, 640x360 client height, expanded action labels, disabled footer labels,
and Safety/Diagnostics external-gate copy requested for the visual-design
continuation.

## Verified Facts

- Source changed only under `/mnt/h/dos-c/software/win31-operator/`.
- Existing request handlers, resource IDs, bridge request types, serial
  transport, and ESP32 firmware behavior were preserved.
- DOS-C copied-evidence vision gate on the latest structured Gate H packet
  still returns `pass`.
- ESP32 advisory analysis on that same copied packet still reports weak OCR and
  navigation-label gaps because those screenshots predate the revised UI.
- The copied packet maps `7/10` target views; Settings, Wizard, and Devices are
  absent from that packet.

## Next QA Step

Capture or copy a fresh revised UI packet without driving unsafe lanes. The
packet should include Home, BBS Board, Downloads, Network, Peers, Devices,
OTAP, Settings, Wizard, Diagnostics, and Safety views; `bridge-transcript.jsonl`;
cleanup proof; and a DOS-C `vision-gate.json`.

## Acceptance Checks

- DOS-C `scripts/win31_dashboard_vision_gate.py` reports `status: pass`.
- ESP32 advisory analyzer maps `10/10` target views.
- No `console_fit_risk` or `log_region_overflow`.
- Bottom margin stays at or above the current safe threshold.
- Navigation-label gaps disappear or are reduced with source-backed evidence.
- OCR/CV remains advisory; bridge transcript behavior remains authoritative.

## Stop Gates

Do not open PCAP, packet-driver, BLE, mesh, router-admin, relay/XBee, TFT,
MicroSD, load, mains, ESP32 flash/erase/monitor, physical serial writes, or
firmware runtime migration as part of this visual QA handoff.
