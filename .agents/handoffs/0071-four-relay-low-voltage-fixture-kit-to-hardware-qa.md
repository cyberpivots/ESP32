# Handoff 0071: Four-Relay Low-Voltage Fixture Kit To Hardware QA

Date: 2026-05-28

Task:
[../TASK_LOG/0082-four-relay-low-voltage-fixture-kit.md](../TASK_LOG/0082-four-relay-low-voltage-fixture-kit.md)

## Current State

- Public guide:
  [../../docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md](../../docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md)
- Internal workbook:
  [../../research/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit-workbook.md](../../research/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit-workbook.md)
- Provisional CAD source:
  [../../cad/hardware-rapid-prototyping/low_voltage_fixture_plate_v0.scad](../../cad/hardware-rapid-prototyping/low_voltage_fixture_plate_v0.scad)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-05-28-four-relay-low-voltage-fixture-kit.md](../../knowledge-base/source-ledger/2026-05-28-four-relay-low-voltage-fixture-kit.md)

The package is Tier 2 documentation, source-record, public-bundle, and single
OpenSCAD-source work only. The public Pages bundle should include only the
public guide from this package; the workbook and CAD source remain internal.

## QA Focus

1. Confirm the public guide keeps verified facts, assumptions, unknowns, safety
   stop gates, print/material rationale, assembly overview, verification,
   troubleshooting, and do-not-proceed warnings separate.
2. Confirm the workbook has explicit slots for printer identity, K1
   hardened-nozzle proof, filament/SDS/dry state, ventilation controls,
   calibration coupon, board/relay/XBee/MicroSD/TFT/expander dimensions, and
   reviewer signoff.
3. Confirm the OpenSCAD source is provisional, parameterized, and limited to a
   blank plate with cable-tie slots, label zones, and a measurement grid.
4. Confirm no board-specific mounting holes, generated CAD/print artifacts,
   slicer projects, G-code, raw scans, live printing, live scanning, wiring,
   relay inputs, relay contacts, XBee writes, ESP32 carrier connections, load,
   mains, or hardware acceptance is implied.
5. Confirm the public source-index copy redacts workbook/CAD paths and the
   public manifest audit blocks workbook/CAD prefixes and generated
   CAD/print suffixes.

## Required Next Evidence

- Same-session printer/scanner identity and condition.
- K1 hardened-nozzle physical proof if abrasive material is proposed.
- Filament SDS, material identity, dry-state/humidity, and storage record.
- Ventilation/exposure control record aligned with NIOSH guidance.
- Calibration coupon for the selected printer/material pair.
- Board, relay, XBee, MicroSD, TFT, expander, connector, cable, label, and
  clearance measurements.
- Reviewer signoff before any live print, fit claim, or repeatable build
  procedure.

## Validation Recorded

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

Do not use this package to authorize live printing, live scanning, wiring,
flashing, monitor/serial write, radio write, relay input work, relay contact
work, XBee writes, ESP32 carrier connections, battery or solar charging,
firmware runtime changes, framework changes, public runtime API changes,
firmware ABI changes, bridge ABI changes, `mesh_discovery.v1` changes, Gate F
service map changes, Win31 transport changes, load work, mains work, release
gating, generated CAD/print artifacts, slicer projects, G-code, raw scans, or
hardware gate closure.
