# Four-Relay Low-Voltage Fixture Kit Evidence Workbook

Source index: [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)

Source ledger:
[../../knowledge-base/source-ledger/2026-05-28-four-relay-low-voltage-fixture-kit.md](../../knowledge-base/source-ledger/2026-05-28-four-relay-low-voltage-fixture-kit.md)

Public guide:
[../../docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md](../../docs/projects/hardware-rapid-prototyping/four-relay-low-voltage-fixture-kit.md)

CAD source:
[../../cad/hardware-rapid-prototyping/low_voltage_fixture_plate_v0.scad](../../cad/hardware-rapid-prototyping/low_voltage_fixture_plate_v0.scad)

Status: Internal evidence workbook. Do not include this workbook in the public
Pages allowlist.

## Verified Facts

- The public guide is documentation-only and does not authorize live printing,
  live scanning, wiring, flashing, serial/radio writes, relay/load/mains work,
  battery/solar work, firmware runtime changes, or framework changes.
- The OpenSCAD source is provisional and has no board-specific mounting holes.
- Required material, printer, ventilation, and measurement evidence is not
  recorded in this workbook yet.

## Assumptions

- The first fixture family is the four-relay low-voltage fixture kit.
- Measurements will be taken from physical hardware or source-backed drawings,
  not inferred from photos alone.
- Public documentation will mention only public-safe facts and unresolved gaps.

## Unknowns

- Local printer and scanner identity, firmware, nozzle condition, build plate,
  calibration, and safe operating location.
- Filament brand, material, SDS, dry state, humidity, storage, and selected
  printer profile.
- Ventilation, local exhaust, enclosure, administrative control, PPE, and
  print-supervision plan.
- Board, relay, XBee, MicroSD, TFT, expander, cable, connector, and clearance
  dimensions.

## Evidence Packet

| Evidence item | Required record | Status | Reviewer notes |
| --- | --- | --- | --- |
| Printer identity | Model, visible identity, firmware, build plate, location, and current condition. | Not recorded |  |
| K1 hardened-nozzle proof | Physical proof of nozzle type and installation if abrasive material is proposed. | Not recorded |  |
| Filament identity | Brand, material, color, diameter, spool condition, and SDS link or file reference. | Not recorded |  |
| Filament dry state | Drying method, time, storage, humidity, and handling note. | Not recorded |  |
| Ventilation controls | Room, enclosure, local exhaust or ventilation decision, PPE, supervision, and stop rule. | Not recorded |  |
| Calibration coupon | Coupon source, dimensions, material, printer, profile, measured result, and acceptance. | Not recorded |  |
| CAD parameters | Plate length, width, thickness, corner radius, slot dimensions, label zones, and grid spacing. | Not recorded |  |
| Board dimensions | Board outline, connector protrusions, button areas, antenna keep-out, height, and heat zones. | Not recorded |  |
| Relay dimensions | Relay module outline, terminal block clearance, indicator location, and low-voltage header clearance. | Not recorded |  |
| XBee dimensions | Adapter or carrier outline, antenna area, connector clearance, and access direction. | Not recorded |  |
| MicroSD dimensions | Reader outline, card insertion direction, card overhang, and connector clearance. | Not recorded |  |
| TFT dimensions | Display outline, ribbon/header clearance, viewing area, and bezel keep-out. | Not recorded |  |
| Expander dimensions | Board outline, address jumper access, header clearance, and pullup/voltage review gap. | Not recorded |  |
| Cable-tie review | Tie width, slot fit, bend radius, strain, and no-contact observation. | Not recorded |  |
| Label review | Label zones, channel names, source of labels, and no-obstruction check. | Not recorded |  |
| Low-voltage separation | Proof that fixture use remains low-voltage-only and does not approach relay contacts, loads, or mains. | Not recorded |  |
| Public package review | Confirm guide is public-safe and workbook/CAD/generated artifacts are not in the public allowlist. | Not recorded |  |

## Measurement Table

| Item | Dimension | Value | Method | Source or record | Open gap |
| --- | --- | --- | --- | --- | --- |
| Fixture plate | Overall length |  |  |  | Yes |
| Fixture plate | Overall width |  |  |  | Yes |
| Fixture plate | Thickness |  |  |  | Yes |
| Cable-tie slot | Slot width |  |  |  | Yes |
| Cable-tie slot | Slot length |  |  |  | Yes |
| Board | Outline length |  |  |  | Yes |
| Board | Outline width |  |  |  | Yes |
| Board | Tallest part height |  |  |  | Yes |
| Relay module | Outline length |  |  |  | Yes |
| Relay module | Outline width |  |  |  | Yes |
| Relay module | Contact-side keep-out |  |  |  | Yes |
| XBee adapter/carrier | Outline and antenna keep-out |  |  |  | Yes |
| MicroSD reader | Card insertion clearance |  |  |  | Yes |
| TFT module | Viewing and connector keep-outs |  |  |  | Yes |
| Expander | Header and jumper keep-outs |  |  |  | Yes |

## Review Signoff

| Role | Required decision | Name/date | Status |
| --- | --- | --- | --- |
| Hardware | Dimensions are measured or unresolved gaps are explicit. |  | Pending |
| Safety/Power | Material, ventilation, low-voltage, relay/load/mains, and stop gates are explicit. |  | Pending |
| Fabrication/CAD | CAD parameters match measured evidence; no generated artifacts are committed. |  | Pending |
| Release/Tooling | Public Pages bundle includes only the public guide, not this workbook or CAD source. |  | Pending |
| QA | Validation commands, source-ID scan, link scan, static CAD check, and diff check pass. |  | Pending |

## Stop Gates

- Stop if a reviewer needs an unrecorded measurement to evaluate fixture fit.
- Stop if the material choice requires SDS, ventilation, drying, or nozzle
  evidence that is not recorded.
- Stop if the fixture would touch boot/reset buttons, antennas, hot parts,
  exposed conductors, terminal blocks, or service connectors.
- Stop if any step requires relay inputs, relay contacts, load equipment,
  mains equipment, firmware commands, serial/radio writes, battery charging, or
  solar connections.
- Stop if this workbook, raw evidence, generated machine files, or private
  local paths are added to the public Pages allowlist.

## Validation Notes

Record the exact command, result, and date for each validation run:

| Check | Result | Notes |
| --- | --- | --- |
| Scaffold validation | Pending |  |
| Agent-process audit | Pending |  |
| Pages build | Pending |  |
| Public manifest audit | Pending |  |
| Pages smoke | Pending |  |
| Static OpenSCAD source check | Pending |  |
| Changed-file source-ID scan | Pending |  |
| Markdown link check | Pending |  |
| `git diff --check` | Pending |  |
