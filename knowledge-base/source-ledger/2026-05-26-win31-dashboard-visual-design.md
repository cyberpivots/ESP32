# Win31 Dashboard Visual Design Continuation Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-LOCAL-WIN31-DASHBOARD-VISUAL-DESIGN-2026-05-26`

## Scope

Local-only Win31 OPCON visual-design source change and copied-evidence
analysis. The task improves labels, layout, and disabled-control wording only.

## Evidence

- DOS-C source:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- DOS-C README:
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- Copied structured Gate H packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`.
- Temporary validation outputs:
  `/tmp/win31-gate-h-structured-vision-after-ui-source.json`,
  `/tmp/win31-gate-h-structured-legibility-after-ui-source.json`, and
  `/tmp/win31-gate-h-structured-legibility-after-ui-source.md`.
- Task record:
  `.agents/TASK_LOG/0062-win31-dashboard-visual-design-continuation.md`.
- Handoff:
  `.agents/handoffs/0051-win31-dashboard-visual-design-continuation-to-qa.md`.

## Verified Facts

- `OPCON_CLIENT_HEIGHT` is now `360`; width remains `640`.
- The Win31 operator navigation strip uses two rows of plain labels:
  `HOME`, `BBS BOARD`, `DOWNLOADS`, `NETWORK`, `PEERS`, `DEVICES`, `OTAP`,
  `SETTINGS`, `WIZARD`, `DIAGNOSTICS`, and `SAFETY`.
- Action button captions are now `PULL MSG`, `POST`, `SEARCH`, `ACK`,
  `CATALOG`, `QUEUE`, and `OTAP INTENT`.
- Relay, Flash, Serial, and PCAP controls remain disabled; Safety and
  Diagnostics identify the external gate owners.
- The source change does not alter bridge request types, JSON request/response
  shape, ESP32 firmware ABI, serial-nullmodem transport, PCAP transport, or
  live-gate contract.
- DOS-C vision gate on the latest copied structured Gate H packet returned
  `pass` with no failures.
- ESP32 advisory analyzer on that copied packet reported no
  `console_fit_risk` or `log_region_overflow`, but retained weak OCR and
  navigation-label-gap findings because the packet predates the source change.

## Assumptions

- The fixed Win3.1 viewfinder remains the accepted local operator surface until
  a later accepted design gate changes the client direction.
- Copied screenshot analysis is advisory evidence and must not replace the
  transcript-first Gate H proof contract.

## Unknowns

- No copied screenshot packet has been captured from the revised UI yet.
- The revised UI has not yet produced measured OCR confidence, target-view
  mapping, or navigation-label-gap improvements.

## Stop Gate

This ledger does not authorize firmware changes, bridge wire-protocol changes,
live hardware mutation, live mesh file delivery, live flashing, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, serial writes, PCAP, packet-driver,
BLE, router-admin, or ESP-WIFI-MESH live actions.
