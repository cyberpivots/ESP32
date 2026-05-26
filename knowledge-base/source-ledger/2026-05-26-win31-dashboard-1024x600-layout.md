# Win31 Dashboard 1024x600 Layout Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-LOCAL-WIN31-DASHBOARD-VISUAL-DESIGN-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-2026-05-26`

## Scope

Local-only Win31 OPCON layout source change for the actual 1024x600 proof
screen. The task improves sizing and layout only.

## Evidence

- DOS-C source:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- DOS-C README:
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- DOS-C task record:
  `/mnt/h/dos-c/.agents/tasks/0032-win31-dashboard-1024x600-layout.md`.
- Copied structured Gate H packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`.
- Temporary validation outputs:
  `/tmp/win31-gate-h-structured-vision-after-1024-layout.json`,
  `/tmp/win31-gate-h-structured-legibility-after-1024-layout.json`, and
  `/tmp/win31-gate-h-structured-legibility-after-1024-layout.md`.
- ESP32 task record:
  `.agents/TASK_LOG/0063-win31-dashboard-1024x600-layout.md`.
- Handoff:
  `.agents/handoffs/0052-win31-dashboard-1024x600-layout-to-qa.md`.

## Verified Facts

- The proof screen being targeted is 1024x600.
- `OPCON_CLIENT_WIDTH` is now `1000`.
- `OPCON_CLIENT_HEIGHT` is now `500`.
- The client is smaller than 1024x600 to account for Win3.1 frame and menu
  chrome added around the client by `AdjustWindowRect`.
- The Win31 operator navigation strip still uses two rows of plain labels:
  `HOME`, `BBS BOARD`, `DOWNLOADS`, `NETWORK`, `PEERS`, `DEVICES`, `OTAP`,
  `SETTINGS`, `WIZARD`, `DIAGNOSTICS`, and `SAFETY`.
- Action button captions remain `PULL MSG`, `POST`, `SEARCH`, `ACK`, `CATALOG`,
  `QUEUE`, and `OTAP INTENT`.
- Relay, Flash, Serial, and PCAP controls remain disabled; Safety and
  Diagnostics identify the external gate owners.
- The source change does not alter bridge request types, JSON request/response
  shape, ESP32 firmware ABI, serial-nullmodem transport, PCAP transport, or
  live-gate contract.
- DOS-C host tests and Open Watcom Win16 build passed after the source change.
- DOS-C vision gate on the latest copied structured Gate H packet returned
  `pass` with no failures.
- ESP32 advisory analyzer on that copied packet reported no
  `console_fit_risk` or `log_region_overflow`, but retained weak OCR and
  navigation-label-gap findings because the packet predates the 1000x500 source
  change.

## Assumptions

- A 1000x500 client is the safer 1024x600 proof-screen target for a normal
  top-left Win3.1 window.
- Copied screenshot analysis is advisory evidence and must not replace the
  transcript-first Gate H proof contract.

## Unknowns

- No copied screenshot packet has been captured from the 1000x500 layout yet.
- The revised UI has not yet produced measured OCR confidence, target-view
  mapping, bottom-margin, or navigation-label-gap improvements.

## Stop Gate

This ledger does not authorize firmware changes, bridge wire-protocol changes,
live hardware mutation, live mesh file delivery, live flashing, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, serial writes, PCAP, packet-driver,
BLE, router-admin, or ESP-WIFI-MESH live actions.
