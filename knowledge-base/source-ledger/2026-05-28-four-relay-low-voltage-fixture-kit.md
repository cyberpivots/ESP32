# Four-Relay Low-Voltage Fixture Kit Source Ledger - 2026-05-28

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`
- `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-CREALITY-K1-SUPPORT-2026-05-28`
- `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`
- `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`
- `SRC-OPENSCAD-DOCS-2026-05-28`
- `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`
- `SRC-BAMBULAB-PA6-CF-2026-05-28`

## Purpose

Record the source basis and mutation boundary for the first public-safe
DIY fixture kit in the hardware rapid-prototyping lane: a four-relay
low-voltage fixture kit with a public guide, an internal evidence workbook,
and exactly one provisional OpenSCAD source file.

## Coordinator Triage

| Field | Decision |
| --- | --- |
| Selected tier | Tier 2 documentation, public-bundle, source-record, and single CAD-source boundary. |
| Owner roles | Hardware, Fabrication/CAD, Safety/Power, Release/Tooling, and QA. |
| Evidence need | Source-index-backed public facts, unresolved-gap labels for unmeasured hardware, workbook placeholders for future proof, public-bundle redaction, and static CAD safety checks. |
| Mutation boundary | Public guide, internal workbook, one OpenSCAD source, Pages allowlist/audit safeguards, source index, source ledger, docs index, development plan/status/gaps, task log, and handoff. |
| Closed surfaces | Live printing, live scanning, wiring, flashing, serial/radio writes, relay inputs, relay contacts, load, mains, XBee writes, ESP32 carrier connections, battery/solar work, firmware/runtime/API/ABI/framework changes, hardware acceptance, generated CAD/print artifacts, slicer projects, G-code, raw scans, and hardware gate closure. |
| Validation plan | Scaffold/process checks, Pages build/audit/smoke, changed-file source-ID scan, Markdown link check, public bundle leak check, static OpenSCAD source check, optional OpenSCAD syntax check if installed, and `git diff --check`. |

## Reviewer Quorum

Read-only reviewer quorum was run before mutation with
`governance-cartographer`, `evidence-record-auditor`, and
`qa-validation-reviewer`.

- Governance reviewer: no P1; existing broad hardware rapid-prototyping
  records did not cover the specific fixture kit, workbook, or OpenSCAD source;
  Pages allowlist needed exactly the public guide.
- Evidence reviewer: no P1; print-fit and build-guide claims must stay blocked
  unless supported by workbook evidence or marked unresolved; workbook/CAD must
  not leak through the public source-index copy.
- QA reviewer: identified a P1 public-leak risk through the public source-index
  copy and P2 static-CAD/source-coverage gaps. The mutation closes these by
  adding public-source redactions, blocked public prefixes/suffixes, required
  scaffold paths, public guide source-coverage checks, and explicit static
  OpenSCAD validation.

## Verified Facts

- The existing hardware rapid-prototyping program is planning/status only and
  does not prove local printer condition, local ventilation, material state,
  fixture fit, live printing, live scanning, or hardware acceptance. Source ID:
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`.
- Existing four-relay evidence does not close exact board dimensions, relay
  module behavior, relay input behavior, relay contact safety, XBee carrier
  routing, TFT/MicroSD/expander dimensions, load, mains, or hardware fit.
  Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`.
- NIOSH 2024-103 covers 3D-printing exposure concerns and controls, but it
  does not replace local ventilation measurement, material SDS, or site safety
  review. Source ID: `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`.
- OpenSCAD official documentation supports a source-first parametric CAD
  workflow. Source ID: `SRC-OPENSCAD-DOCS-2026-05-28`.
- This package adds exactly one provisional OpenSCAD source file. It has
  parameterized plate dimensions, cable-tie slots, label zones, a measurement
  grid, and no board-specific mounting holes.

## Assumptions

- The first fixture family is the four-relay low-voltage fixture kit.
- PLA/PETG are the only initial material families discussed for future
  low-risk planning; specialist materials remain blocked until SDS,
  ventilation, drying, nozzle, and calibration evidence exists.
- The internal workbook is the evidence surface for measurements and
  same-session proof; it is not part of the public artifact.
- The public guide may mention the existence of an internal evidence process
  but must not publish internal workbook paths, CAD paths, local evidence
  paths, raw scans, or machine artifacts.

## Unknowns

- Local printer/scanner identity, firmware, nozzle condition, build plate,
  calibration, safe operating location, ventilation, filament SDS, dry state,
  and humidity.
- Exact board, relay, XBee, MicroSD, TFT, expander, connector, cable, label,
  and clearance dimensions.
- Whether any future print coupon or fixture plate meets dimensional
  tolerances, material constraints, or reviewer acceptance.

## Local Records

- Public guide:
  `docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md`
- Internal workbook:
  `research/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit-workbook.md`
- CAD source:
  `cad/hardware-rapid-prototyping/low_voltage_fixture_plate_v0.scad`
- Task log:
  `.agents/TASK_LOG/0082-four-relay-low-voltage-fixture-kit.md`
- QA handoff:
  `.agents/handoffs/0071-four-relay-low-voltage-fixture-kit-to-hardware-qa.md`

## Public Artifact Boundary

The generated Pages allowlist includes only the public guide from this package.
The internal workbook and CAD source are not copied into the public artifact.
Public source-index generation redacts the internal workbook and CAD source
paths, and the public manifest audit blocks the internal workbook/CAD prefixes
and generated CAD/print suffixes.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Public bundle leak check for workbook/CAD source names and internal paths.
- Static OpenSCAD source check: exactly one `.scad` file in this package, no
  external geometry dependency, required parameters present, no board-specific
  mounting holes, no generated-artifact instructions, and no live-action
  instructions.
- Optional OpenSCAD syntax check if `openscad` is installed.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
  built 64 public files.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- PASS: changed-file source-ID scan over 20 Markdown files.
- PASS: changed-file Markdown link check over 20 Markdown files.
- PASS: generated public fixture guide Markdown links resolve inside the Pages
  artifact.
- PASS: public bundle leak check found no workbook/CAD source names or internal
  workbook/CAD paths.
- PASS: static OpenSCAD source check.
- SKIP: optional OpenSCAD syntax/export check; `openscad` was not installed.
- PASS: `git diff --check`

## Stop Gates

This source ledger does not authorize live printing, live scanning, wiring,
flashing, monitor/serial write, radio write, relay input work, relay contact
work, XBee writes, ESP32 carrier connections, battery or solar charging,
firmware runtime changes, framework changes, public runtime API changes,
firmware ABI changes, bridge ABI changes, `mesh_discovery.v1` changes, Gate F
service map changes, Win31 transport changes, load work, mains work, release
gating, generated CAD/print artifacts, slicer projects, G-code, raw scans, or
hardware gate closure.
