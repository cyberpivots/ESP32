# Task 0082: Four-Relay Low-Voltage Fixture Kit

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-28

## Goal

Create the first DIY hardware build-document package around a 3D-printed
four-relay low-voltage fixture kit, with a public-safe guide, an internal
evidence workbook, and one provisional OpenSCAD source model. Keep generated
CAD/print artifacts, live printing, live scanning, wiring, flashing,
serial/radio writes, relay/load/mains, firmware/runtime/API/ABI/framework
changes, and hardware gate closure out of scope.

## Verified Facts

- Required governance files, docs index, and source index were re-read before
  mutation.
- The worktree already contained broad hardware rapid-prototyping edits and
  unrelated BBS UI program edits; this task preserves those edits.
- Existing broad hardware rapid-prototyping records did not include a specific
  four-relay fixture kit guide, internal workbook, or OpenSCAD source.
- The public Pages builder previously allowed the source index into the public
  bundle, so this task adds workbook/CAD redaction and manifest audit blocks.
- No same-session printer/scanner identity, K1 hardened-nozzle proof,
  filament/SDS/dry state, ventilation, calibration coupon, dimensions, live
  print, live scan, or fixture-fit evidence was captured.

## Assumptions

- The first fixture family is the four-relay low-voltage fixture kit.
- One tracked OpenSCAD source is allowed for this package, but generated
  CAD/print artifacts and additional CAD sources are not.
- PLA/PETG language is planning-only; specialist materials remain blocked
  until their evidence gates are recorded.
- The internal workbook is the evidence surface for future measurement and
  reviewer signoff and is not public.

## Unknowns

- Local printer/scanner condition, material state, ventilation, and calibration.
- Exact board, relay, XBee, MicroSD, TFT, expander, connector, cable, label,
  and clearance dimensions.
- Whether any future printed coupon or fixture plate is dimensionally usable.

## Reviewer Quorum

Read-only reviewer quorum was run before mutation:

- `governance-cartographer`: no P1; existing broad prototyping package did not
  cover this kit and Pages needed exactly the public guide.
- `evidence-record-auditor`: no P1; unsupported print-fit and material claims
  must stay blocked; workbook/CAD details must not leak to public bundle.
- `qa-validation-reviewer`: identified a public source-index leak risk and
  static `.scad` audit gap; this task adds redaction/audit coverage and an
  explicit static CAD validation plan.

## Mutation Boundary

- `docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md`
- `research/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit-workbook.md`
- `cad/hardware-rapid-prototyping/low_voltage_fixture_plate_v0.scad`
- `scripts/build_github_pages.py`
- `scripts/audit_public_manifest.py`
- `scripts/scaffold_audit_data.py`
- `scripts/scaffold_audit_pages.py`
- `docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-28-four-relay-low-voltage-fixture-kit.md`
- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- this task record
- `.agents/handoffs/0071-four-relay-low-voltage-fixture-kit-to-hardware-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Public bundle leak check for workbook/CAD source names and internal paths.
- Static OpenSCAD source check.
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

## Handoff

Continue with
[../handoffs/0071-four-relay-low-voltage-fixture-kit-to-hardware-qa.md](../handoffs/0071-four-relay-low-voltage-fixture-kit-to-hardware-qa.md).

## Closed Surfaces

Live printing, live scanning, wiring, flashing, monitor/serial write, radio
write, relay input work, relay contact work, XBee writes, ESP32 carrier
connections, battery or solar charging, firmware runtime changes, framework
changes, public runtime API changes, firmware ABI changes, bridge ABI changes,
`mesh_discovery.v1` changes, Gate F service map changes, Win31 transport
changes, load work, mains work, release gating, generated CAD/print artifacts,
slicer projects, G-code, raw scans, and hardware gate closure remain closed.
