# Hardware Rapid Prototyping Source Ledger - 2026-05-28

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-CREALITY-K1-SUPPORT-2026-05-28`
- `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`
- `SRC-CREALITY-CR30-2026-05-28`
- `SRC-CREALITY-CR-SCAN-LIZARD-2026-05-28`
- `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`
- `SRC-OPENSCAD-DOCS-2026-05-28`
- `SRC-CADQUERY-DOCS-2026-05-28`
- `SRC-FREECAD-FEATURES-2026-05-28`
- `SRC-KICAD9-PCBNEW-3D-EXPORT-2026-05-28`
- `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`
- `SRC-BAMBULAB-PA6-CF-2026-05-28`
- `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`

## Purpose

Record the source basis for adding a hardware design documentation and
3D-printed rapid-prototype planning lane across the ESP-NOW BBS,
four-relay-XBee-WiFi, remote LCD/XBee/solar client, TFT/MicroSD/expander, and
future browser/client-node interface streams.

## Verified Facts

- [repo-verified] `research/development-plan.md` is the singular current-action
  plan and `research/development-status-ledger.md` is the detailed status
  ledger.
- [repo-verified] The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- [repo-verified] `remote-lcd-xbee-solar-client` remains a separate
  hardware-device stream and is not merged into BBS/network runtime work.
- [external] Creality K1 support specifications cover FFF/CoreXY,
  direct-drive extrusion, 0.4 mm nozzle, nozzle temperature below 300 C,
  heatbed below 100 C, and listed filament families including PETG, TPU, PA,
  ASA, PC, and carbon-fiber-filled PLA/PA/PET variants.
- [external] Anycubic official Kobra 2 Max records verify the 420 x 420 x
  500 mm large-format print volume and PLA/ABS/PETG/TPU filament support.
- [external] Creality CR-30 official store material identifies the CR-30 as a
  batch-printing, infinite-Z printer for long-model production.
- [external] Creality CR-Scan Lizard official material claims 0.05 mm
  precision and STL/OBJ/PLY output.
- [external] NIOSH Publication 2024-103 covers 3D-printer exposure concerns and
  controls including ventilation, local exhaust ventilation, ventilated
  enclosures, administrative controls, and PPE.
- [external] OpenSCAD, CadQuery, FreeCAD, and KiCad 9 official documentation
  support parametric CAD/source workflows and CAD/mesh export paths for future
  hardware documentation.
- [external] Prusa and Bambu material guidance supports the planning
  distinction between PETG, ABS/ASA, PA/nylon, composites, and PA6-CF drying or
  hardened-nozzle requirements.

## Assumptions

- The fabrication equipment list is user-stated local equipment; this source
  ledger verifies official capability claims, not current local condition.
- The K1 hardened-nozzle upgrade is user-stated and remains unverified until a
  physical inspection record is captured.
- The first implementation deliverable should be documentation and guide
  structure, not CAD files, G-code, slicer projects, firmware, or live print
  execution.

## Unknowns

- Local printer/scanner identity, serial numbers, firmware versions, nozzle
  installation, drive-path wear, calibration, bed state, belt state, and scanner
  calibration.
- Current ventilation, local exhaust, PPE, filament SDS, drying equipment,
  humidity control, and storage state.
- Exact hardware dimensions and clearances for boards, displays, encoders,
  radios, batteries, BMS boards, solar parts, relays, TFTs, MicroSD readers,
  expanders, connectors, cables, and enclosures.

## Reviewer Lenses

No subagents were spawned. Local read-only role lenses were run before
mutation:

- Hardware owner: approved a docs/status/source-record lane only, with printer
  and scanner capabilities separated from local condition.
- Safety/power reviewer: approved only if ABS/ASA/PA/CF materials require SDS,
  ventilation, drying, nozzle, and thermal controls before build instructions.
- Source/evidence auditor: approved source-index-backed facts plus unresolved
  gaps for local equipment claims.
- Fabrication/CAD reviewer: approved a source-first parametric CAD workflow
  and scanner-as-reference-only language.
- QA validation reviewer: approved scaffold checks, source-ID scan, Markdown
  link check, and `git diff --check`.
- Communications/firmware boundary reviewer: approved with no API, ABI,
  bridge, mesh, Win31 transport, framework, firmware, serial, radio, or live
  hardware changes.

## Local Records

- Program doc:
  `docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md`
- Plan: `research/development-plan.md`
- Status ledger: `research/development-status-ledger.md`
- Triage status: `research/triage-status.md`
- Device matrix: `hardware-profiles/device-matrix.md`
- Known gaps: `research/known-gaps.md`
- Task log: `.agents/TASK_LOG/0081-hardware-rapid-prototyping.md`
- QA handoff:
  `.agents/handoffs/0070-hardware-rapid-prototyping-to-hardware-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: changed-file source-ID scan over 14 Markdown files.
- PASS: changed-file Markdown link check over 14 Markdown files.
- PASS: `git diff --check`

## Stop Gates

No live bench action, wiring, flashing, monitor/serial write, radio write,
BLE/live mesh, relay/load/mains work, battery or solar charging, firmware
runtime change, framework selection, public runtime API change, firmware ABI
change, bridge ABI change, `mesh_discovery.v1` schema change, Gate F service
map change, Win31 transport change, CAD source implementation, bulky vendor
artifact, slicer project, G-code, or raw scanner capture is authorized by this
source ledger.
