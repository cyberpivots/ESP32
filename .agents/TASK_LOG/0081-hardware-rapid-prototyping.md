# Task 0081: Hardware Rapid Prototyping Program

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-28

## Goal

Add a source-backed Tier 2 hardware design documentation and 3D-printed rapid
prototype planning lane without authorizing live bench, wiring, flashing,
serial/radio writes, firmware runtime changes, battery/solar charging, or
relay/load/mains work.

## Verified Facts

- Required governance and planning records were re-read before mutation.
- The current worktree already contained uncommitted BBS UI program edits in
  several target files; this task preserves those edits.
- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Official/primary sources now cover the K1, Kobra 2 Max, CR-30, CR-Scan
  Lizard, NIOSH 2024-103, OpenSCAD, CadQuery, FreeCAD, KiCad 9, and material
  guidance used by this planning pass.

## Assumptions

- Repository edits are limited to documentation/status/source records.
- User-stated local equipment exists, but current identity, condition,
  calibration, ventilation, and nozzle state are not proven by this task.
- Scanner geometry is advisory until checked against known dimensions or
  caliper measurements.

## Unknowns

- No same-session printer/scanner identity, nozzle proof, material SDS,
  drying, ventilation, calibration, or local print/scan evidence was captured.
- No hardware dimensions, enclosure fit, board clearance, battery/solar
  current, radio, relay/load/mains, firmware, bridge, Win31, or browser-client
  gate was closed.

## Reviewer Quorum

No subagents were spawned. Local role lenses were run before mutation:

- Hardware owner: approved docs/status/source-record updates only.
- Safety/power reviewer: approved only with material, ventilation, drying,
  nozzle, and thermal gates left open.
- Source/evidence auditor: approved official-source citations and unresolved
  local-equipment gaps.
- Fabrication/CAD reviewer: approved parametric CAD source-first guidance and
  scanner-as-reference-only language.
- QA validation reviewer: approved scaffold, source-ID, link, and diff
  validation.
- Communications/firmware boundary reviewer: approved because no runtime API,
  ABI, bridge, mesh, Win31 transport, framework, firmware, serial, radio, or
  live hardware mutation is included.

## Mutation Boundary

- `docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md`
- `hardware-profiles/device-matrix.md`
- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-28-hardware-rapid-prototyping.md`
- this task record
- `.agents/handoffs/0070-hardware-rapid-prototyping-to-hardware-qa.md`

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

## Handoff

Continue with
[../handoffs/0070-hardware-rapid-prototyping-to-hardware-qa.md](../handoffs/0070-hardware-rapid-prototyping-to-hardware-qa.md).

## Closed Surfaces

Live bench action, wiring, flashing, monitor/serial write, radio write,
BLE/live mesh, relay/load/mains work, battery or solar charging, firmware
runtime change, framework selection, public runtime API change, firmware ABI
change, bridge ABI change, `mesh_discovery.v1` schema change, Gate F service
map change, Win31 transport change, CAD source implementation, bulky vendor
artifact, slicer project, G-code, and raw scanner capture remain closed.
