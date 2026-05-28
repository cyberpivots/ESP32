# Four-Relay Low-Voltage Fixture Kit

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

Status: Tier 2 public-safe build-document package and provisional CAD source
record only.

## Purpose

This kit describes a first low-voltage fixture plate for the four-relay
XBee Wi-Fi project. The plate is a non-final printed aid for labels, cable-tie
strain relief, measurement marks, and review layout. It is not a final mount,
enclosure, electrical design, or hardware acceptance record.

The package keeps public instructions safe by stopping before relay inputs,
relay contacts, XBee settings, ESP32 carrier connections, battery or solar
work, load work, mains work, firmware changes, live printing, or live bench
actions.

## Verified Facts

- The four-relay lane remains hardware-facing blocked until exact board, relay
  module, power, XBee, TFT, MicroSD, expander, instrument, load, and safety
  evidence exists. Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`.
- Official source records cover 3D-printer, scanner, material, safety, and
  OpenSCAD planning context, but they do not verify local equipment condition,
  local ventilation, filament state, or fixture fit. Source IDs:
  `SRC-CREALITY-K1-SUPPORT-2026-05-28`,
  `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`,
  `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`,
  `SRC-OPENSCAD-DOCS-2026-05-28`,
  `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`.
- This package adds one provisional OpenSCAD source model for a blank
  low-voltage fixture plate. It intentionally avoids board-specific mounting
  holes until measured dimensions exist. Source ID:
  `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`.

## Assumptions

- The first fixture family is the four-relay low-voltage fixture kit.
- The initial public audience needs a readable safety-forward guide, while
  internal reviewers need a separate evidence workbook.
- PLA or PETG are the only initial material families discussed for future
  low-risk fixture trials; ABS, ASA, PA, and filled materials remain blocked
  until their extra evidence gates are complete.
- The CAD source is provisional and must be parameter-checked against measured
  hardware before any repeatable build procedure exists.

## Unknowns

- Exact board outline, relay-module outline, XBee adapter or carrier outline,
  MicroSD reader outline, TFT outline, expander outline, connector height,
  cable bend radius, and clearance envelopes.
- Local printer identity, firmware, nozzle condition, build plate condition,
  material profile, filament SDS, dry state, humidity, and calibration coupon.
- Local ventilation or exposure controls for the selected material and room.
- Whether the printed plate avoids all boot buttons, reset buttons, antenna
  keep-outs, heat zones, exposed conductors, and serviceable connectors.

## Parts

| Item | Public-safe role | Evidence needed before use |
| --- | --- | --- |
| Provisional fixture plate | Nonconductive layout plate with cable-tie slots, blank label zones, and a measurement grid. | CAD parameter review, exported mesh hash in an internal packet, printer/material record, and measurement check. |
| Cable ties | Temporary cable retention for low-voltage review leads only. | Tie width, tie tension, bend radius, and no-contact check near buttons, connectors, and exposed conductors. |
| Paper or adhesive labels | Human-readable channel, connector, and review labels. | Label map tied to measured fixture zones; no electrical rating claim. |
| Calipers or ruler | Measurement capture before fit claims. | Recorded dimensions in the internal workbook. |
| Printer/material coupon | Small material and dimensional proof before any project part. | Coupon dimensions, photo/check record, and reviewer signoff. |

Do not add metal fasteners, heat-set inserts, adhesive mounts, enclosure
hardware, or board-specific holes until the measurement workbook proves the
locations and clearances.

## Safety Stop Gates

- Power and voltage: keep all fixture planning unpowered unless a later bench
  gate opens a specific low-voltage measurement action.
- Boot pins and buttons: do not clamp, press, cover, or route cable ties across
  boot, reset, UART, antenna, or service areas until physical inspection proves
  the clearance.
- Isolation: do not use this plate as electrical isolation, contact guarding,
  strain-relief certification, or enclosure qualification.
- Relay/load/mains: do not connect relay contacts, loads, mains conductors, or
  mains-rated devices to this kit.
- XBee/radio/serial: do not send XBee setting writes, ESP32 serial writes, or
  firmware commands from this kit.
- Material safety: do not print ABS, ASA, PA, carbon-fiber-filled, or other
  engineering materials until SDS, ventilation, drying, nozzle, calibration,
  and review records exist.
- Public artifact: do not publish internal measurement workbooks, raw scans,
  slicer projects, machine files, local evidence paths, or private bench
  records.

## Print And Material Rationale

PLA is acceptable only for visual mockups, label placement, and short
low-stress review. PETG is the first candidate for a future functional
low-voltage plate because it is commonly used for tougher brackets and cable
guides, but this guide does not select a filament brand, profile, printer, or
temperature.

ABS, ASA, PA/nylon, carbon-fiber-filled, and other specialist materials remain
blocked because the current package has no same-session SDS, ventilation,
drying, nozzle, calibration, or coupon evidence. Source IDs:
`SRC-NIOSH-SAFE-3D-PRINTING-2024-103`,
`SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`,
`SRC-BAMBULAB-PA6-CF-2026-05-28`.

## Assembly Overview

This is an overview, not a repeatable build procedure:

1. Complete the internal evidence workbook sections for printer identity,
   material state, ventilation, and calibration coupon.
2. Measure every board, module, connector, cable, label zone, and clearance
   that the fixture could touch or obscure.
3. Review the provisional CAD parameters against those measurements.
4. Produce a small coupon before any fixture plate.
5. Place the unpowered hardware near the printed plate and confirm that the
   cable-tie slots and label zones do not force contact with buttons,
   connectors, antenna areas, exposed conductors, or heat-sensitive parts.
6. Add temporary labels only after the label map matches the measured layout.
7. Stop and revise the CAD source if any slot, edge, or label zone interferes
   with inspection or service access.

## Verification Checklist

- Source ledger and source-index IDs are present.
- Internal workbook has printer identity, material, ventilation, coupon,
  measurement, and reviewer sections completed.
- CAD source remains a single provisional OpenSCAD source with no imported
  geometry and no board-specific holes.
- Plate dimensions, thickness, corner radius, slot dimensions, label zones,
  and measurement-grid spacing are recorded.
- Printed coupon dimensions are recorded before any fixture plate is treated
  as usable.
- Hardware stays unpowered during layout review unless a later gate opens a
  named measurement action.
- Cable ties are loose enough to avoid connector strain, button pressure,
  insulation damage, or blocked service access.
- No relay input, relay contact, load, mains, XBee setting, firmware, battery,
  or solar action is performed.
- Reviewer signs off that this is still a provisional low-voltage fixture aid,
  not hardware acceptance.

## Troubleshooting

| Symptom | Stop and check |
| --- | --- |
| Plate edge blocks a connector or button | Record the interference, revise CAD parameters, and re-review before any repeat. |
| Cable tie pulls a cable sharply | Increase slot offset or remove the tie; do not force the cable. |
| Label zone hides markings or LEDs | Move the label zone and record the new placement. |
| Coupon dimensions are out of tolerance | Stop; update printer/material calibration before project parts. |
| Plate warps or corners lift | Stop; review material, bed adhesion, part orientation, and environment. |
| Odor, haze, heat, or unexpected noise appears | Stop the print plan and record the safety issue before continuing. |
| Hardware identity or dimensions are unclear | Treat the item as an unresolved gap; do not infer fit from photos. |

## Do Not Proceed If

- Any measurement, printer identity, material, ventilation, or reviewer section
  in the internal workbook is blank.
- The K1 hardened-nozzle upgrade is needed but not physically proven.
- Filament SDS, dry state, or humidity evidence is missing for the selected
  material.
- The guide would require powered hardware, relay inputs, relay contacts, load
  equipment, mains equipment, firmware commands, XBee writes, battery charging,
  or solar connections.
- A printed part contacts boot/reset buttons, antennas, exposed conductors,
  hot parts, terminal blocks, or service connectors.
- The part is being treated as a final enclosure, electrical isolation barrier,
  load guard, or qualified safety device.

## Closed Gates

This guide does not close hardware identity, power, voltage, boot-pin,
isolation, print-readiness, fit, live bench, wiring, relay, load, mains,
battery, solar, XBee, firmware, framework, public API, firmware ABI, bridge
ABI, `mesh_discovery.v1`, Gate F service-code, Win31 transport, live printing,
live scanning, or release gates.
