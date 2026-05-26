# Handoff 0050: Remote LCD XBee Solar Client Separate Hardware Stream To Hardware QA

## Status

`remote-lcd-xbee-solar-client` is now recorded as a separate hardware-device
stream. No hardware action is authorized.

## Verified facts

- Seven private docs-only hardware submodules already exist for this lane.
- Parent documentation now records the development order and separation rules.
- This lane remains separate from ESP-NOW BBS, Win31/DOS-C, Gate F runtime,
  Gate G export, Gate H proof, mesh, BLE, network, relay, TFT, MicroSD, load,
  and mains work.
- No firmware source, framework files, submodule pointer changes, DOS-C
  changes, wiring instructions, charging instructions, radio writes, or live
  bench actions were added.

## Assumptions

- Hardware QA should begin with exact part identity and source intake inside
  each private `rlxsc-*` submodule.
- Raw photos, markings, serial identifiers, settings, and bench captures remain
  private unless a publication review approves redacted excerpts.

## Unknowns

- Exact hardware identity for every requested module remains unresolved.
- No power budget, cell condition record, charger threshold record, enclosure
  review, pin map, XBee carrier review, antenna review, read-only bench proof,
  or implementation gate exists for this lane.

## Hardware QA next steps

1. Start identity intake in each private submodule.
2. Prioritize `rlxsc-18650-cell`, `rlxsc-bms-protection`, and
   `rlxsc-solar-charger-power-path` for cell, BMS/protection, charger, panel,
   fuse/protection, enclosure, and current-limit evidence.
3. Then review `rlxsc-esp32-client-node`, `rlxsc-lcd-20x4-i2c`,
   `rlxsc-rotary-encoder`, and `rlxsc-xbee-pro-s3b` for boot/recovery,
   voltage, pullup, DIN/DOUT, antenna, and no-conflict pin-planning evidence.
4. Return to the parent repo only for coordination records, source-index
   updates, ADRs after evidence exists, and submodule pointer updates.

## Stop gates

Do not connect battery, solar, charger, BMS, LCD, encoder, XBee carrier,
antenna hardware, fuse/protection hardware, enclosure hardware, or ESP32 GPIO
from this handoff. Do not select a firmware framework, add firmware source,
open DOS-C validation, or start live bench action until a later accepted gate
authorizes the exact surface.
