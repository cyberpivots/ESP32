# Hardware Rapid Prototyping And 3D-Printed Prototype Development

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

Source ledger:
[../../../knowledge-base/source-ledger/2026-05-28-hardware-rapid-prototyping.md](../../../knowledge-base/source-ledger/2026-05-28-hardware-rapid-prototyping.md)

Status: Tier 2 documentation, research, and status planning only.

## Scope

This program adds a cross-project hardware design documentation lane for
3D-printed prototype parts, scanner-assisted fit checks, parametric CAD source
workflows, and nontechnical build guides.

It does not authorize live bench actions, wiring, flashing, serial writes,
radio writes, BLE or live mesh work, relay/load/mains work, battery/solar
charging, firmware runtime changes, framework selection, public runtime API
changes, firmware ABI changes, bridge ABI changes, `mesh_discovery.v1` schema
changes, Gate F service map changes, or Win31 transport changes.

## First Fixture Kit Package

The first concrete package in this lane is the
[four-relay low-voltage fixture kit](four-relay-low-voltage-fixture-kit.md).
It adds one public-safe guide, one internal evidence workbook, and one
provisional OpenSCAD source model for a blank low-voltage fixture plate.

That package opens only this named CAD-source boundary. It does not add
generated CAD/print artifacts, slicer projects, machine files, raw scans, live
prints, live scans, relay input work, relay contact work, XBee writes, ESP32
carrier connections, battery/solar work, load work, mains work, firmware work,
or hardware acceptance.

## Verified Facts

- The accepted ESP-NOW BBS operator path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
  Source IDs: `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`,
  `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27`.
- `remote-lcd-xbee-solar-client` is a separate hardware-device stream and must
  not be folded into ESP-NOW BBS, Win31/DOS-C, mesh, BLE, relay, TFT, MicroSD,
  load, or mains runtime work. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26`.
- Creality K1 support specifications identify an FFF CoreXY printer with a
  direct-drive extruder, 0.4 mm nozzle, nozzle temperature below 300 C, heatbed
  below 100 C, and supported filament families including PLA, PETG, TPU, PA,
  ASA, PC, PLA-CF, PA-CF, and PET-CF. Source ID:
  `SRC-CREALITY-K1-SUPPORT-2026-05-28`.
- The K1 hardened-nozzle upgrade is user-stated local equipment context only;
  it still needs same-session physical proof before any abrasive-filament
  build instruction treats it as verified.
- Anycubic official Kobra 2 Max material records verify a 420 x 420 x 500 mm
  print volume and support for PLA, ABS, PETG, and TPU. Source ID:
  `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`.
- Creality positions CR-30 as a 3DPrintMill / infinite-Z belt printer for batch
  and long-model production. Source ID: `SRC-CREALITY-CR30-2026-05-28`.
- Creality CR-Scan Lizard materials claim up to 0.05 mm precision and STL, OBJ,
  and PLY output. Source ID: `SRC-CREALITY-CR-SCAN-LIZARD-2026-05-28`.
- NIOSH Publication 2024-103 identifies possible ultrafine particle, chemical,
  heat, and mechanical/moving-part hazards in 3D-printing settings and points
  to controls including ventilation, local exhaust ventilation, ventilated
  enclosures, administrative controls, and PPE. Source ID:
  `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`.
- OpenSCAD documentation provides script-oriented parametric modeling and
  import/export documentation links. Source ID:
  `SRC-OPENSCAD-DOCS-2026-05-28`.
- CadQuery documentation identifies a Python parametric CAD workflow with
  output formats including STEP, AMF, 3MF, and STL. Source ID:
  `SRC-CADQUERY-DOCS-2026-05-28`.
- FreeCAD official feature docs identify a parametric CAD environment with
  Python scripting and import/export support including STEP, IGES, OBJ, STL,
  VRML, and OpenSCAD CSG. Source ID:
  `SRC-FREECAD-FEATURES-2026-05-28`.
- KiCad 9 PCB editor documentation supports 3D model export formats including
  STEP, GLB, BREP, XAO, PLY, and STL, and footprint models in STEP, VRML, or
  IDF. Source ID: `SRC-KICAD9-PCBNEW-3D-EXPORT-2026-05-28`.
- Prusa's material guide marks ASA and ABS as enclosure-recommended, PETG as
  not requiring enclosure/drybox/hardened nozzle in that guide, nylon as
  enclosure-recommended and drybox-recommended, and composite materials as
  requiring a hardened nozzle. Source ID:
  `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`.
- Bambu Lab PA6-CF material guidance recommends hardened-steel hotends, drying
  before printing, low-humidity storage while printing, 260-290 C nozzle
  temperature, and 80-100 C bed temperature. Source ID:
  `SRC-BAMBULAB-PA6-CF-2026-05-28`.

## Assumptions

- The available fabrication equipment is user-stated: Creality K1 with a
  hardened nozzle upgrade, Anycubic Kobra 2 Max, Creality CR-30, and Creality
  CR-Scan Lizard.
- Printer availability, nozzle installation, filament inventory, drying
  equipment, ventilation, slicer profiles, build plates, and calibration state
  are not proven by this documentation pass.
- Parametric CAD source files should be treated as the design authority;
  slicer-ready meshes and G-code are build artifacts.
- Fit scans are useful as reference geometry, but they are not dimensional
  evidence until checked against known dimensions or caliper measurements.

## Unknowns

- Local serial numbers, firmware versions, nozzle material/condition, build
  plate condition, extrusion calibration, belt calibration, and scanner
  calibration state.
- Whether the current workspace has active ventilation, local exhaust, a
  ventilated enclosure, fire/smoke monitoring policy, PPE, filament SDS files,
  drying containers, or humidity measurement.
- Whether ABS, ASA, PETG, PA/nylon, PA-CF, PET-CF, or other engineering
  filaments are physically present, dry, compatible with the selected printer,
  and safe to run in the current room.
- Exact enclosure dimensions, connector clearances, cable bend radii, mounting
  hole patterns, board stack heights, battery/solar clearances, and load
  separation requirements for the hardware lanes.

## Risks

- Treating official printer material support as build authorization can skip
  local nozzle, SDS, ventilation, drying, bed adhesion, enclosure, and thermal
  risk checks.
- ABS/ASA and high-temperature materials can raise exposure and odor concerns;
  controls must be recorded before a nontechnical guide recommends them.
- Abrasive filaments such as carbon-fiber-filled materials can damage
  non-hardened nozzles or drive components if the upgrade is not actually
  installed and suitable.
- PA/nylon and PA-CF can produce weak, warped, or dimensionally unstable parts
  if moisture and drying are not controlled.
- Large enclosure parts can warp, split, or hide collision/clearance problems
  if the CAD model does not include measured hardware and fastener keep-outs.
- Belt-printer output on CR-30 can fail through belt adhesion, slicer-angle,
  or continuous-print calibration gaps if treated like normal bedslinger or
  CoreXY printing.
- Scanner meshes can include optical, alignment, scale, or surface-material
  error; they must not replace measured dimensions.

## Equipment Defaults

| Equipment | Default role | Required evidence before build instructions |
| --- | --- | --- |
| Creality K1 | Smaller engineering-material parts, compact brackets, fixture blocks, clips, cable anchors, and first-pass functional prototypes. | Physical proof of hardened nozzle upgrade before abrasive filament; filament SDS; drying/humidity record for PA/PA-CF; enclosure/ventilation record for ABS/ASA/PA; slicer profile and small test coupon. |
| Anycubic Kobra 2 Max | Large enclosures, flat panels, bezels, low-voltage fixture plates, nonconductive test jigs, and oversized visual mockups. | Bed calibration, adhesion test, material profile, enclosure/ventilation decision for ABS/ASA, and print-time risk review for large parts. |
| Creality CR-30 | Batch rails, long cable guides, repeated small brackets, and conveyor-belt experiments only after belt proof. | Belt adhesion/calibration proof, slicer support for belt geometry, part orientation trial, continuous-run stop rule, and first-article inspection. |
| CR-Scan Lizard | Fit/reference scans, ergonomic mockups, enclosure contour capture, and before/after fit comparison. | Calibration state, known-dimension artifact check, caliper cross-check, surface preparation note, and scale/orientation verification. |

## Deployment Lane Map

| Lane | Prototype needs | Boundary | Required next evidence |
| --- | --- | --- | --- |
| ESP-NOW BBS path | Pi/ESP32 USB strain relief, serial cable guides, nonconductive coordinator/peer tray, labels, protective covers, and operator-facing transport diagrams. | Preserve the accepted serial-nullmodem path. No COM, serial, bridge, firmware, flash, radio, or Win31 transport change. | Measured board and cable dimensions, heat/airflow clearance, connector bend radius, and proof that fixtures do not touch boot pins or buttons unintentionally. |
| Four-relay XBee Wi-Fi | Low-voltage-only fixture plate, relay-contact guard mockup, XBee dock bracket, MicroSD access mockup, TFT bezel, LED or logic-analyzer fixture mounts, cable combs, and enclosure studies. | No relay input wiring, no relay contact wiring, no load/mains procedure, no XBee writes, no DIN/DOUT carrier wiring, no final pin map. | Exact board/shield/relay/MicroSD/TFT/expander/mux dimensions, low-voltage separation plan, instrument inventory, and qualified-review path before any load enclosure. |
| Four-relay low-voltage fixture kit | Public guide, internal workbook, and provisional blank fixture plate source for labels, cable-tie slots, and measurement grid. | Source-only CAD package. No board-specific mounting holes, generated CAD/print artifacts, live prints, live scans, relay inputs, relay contacts, XBee writes, load, mains, or fit acceptance. | Complete the internal workbook: printer identity, K1 hardened-nozzle proof if needed, filament/SDS/dry state, ventilation controls, calibration coupon, dimensions, and reviewer signoff. |
| Remote LCD XBee solar client | Handheld/field enclosure concepts, 20x4 LCD bezel, encoder knob clearance, XBee antenna clearance mockup, 18650/BMS/charger bay placeholders, solar lead strain relief, and weathering study placeholders. | Keep this as a separate hardware-device stream in `rlxsc-*` submodules. No battery charging, solar wiring, radio writes, firmware, or live bench action. | Source-backed identity intake in private submodules, cell/BMS/charger/panel/fuse/enclosure evidence, current limits, thermals, and recovery/stop rules. |
| TFT, MicroSD, expander, storage | Bezel/frame tests, SD-card access doors, standoffs, connector keep-outs, I2C expander shield mockups, mux input label plates, and serviceability jigs. | No wiring, bus assignment, pullup decision, firmware dependency, or runtime storage claim. | Exact module sources, pin and connector dimensions, voltage/pullup evidence, boot-pin conflict review, and removable-media service policy. |
| Future browser/client-node interface | Phone/laptop stand, QR/label holders, client-node enclosure mockups, selected-board tray, and read-only demo fixture. | No live browser proof, Wi-Fi mutation, BLE pairing, dummy-output control, or selected-board role claim until a later gate. | Selected board identity, power/voltage/boot-pin/isolation review, recovery path, browser support matrix, and static/simulated proof first. |

## CAD Workflow

1. Use OpenSCAD for small parametric brackets, cable guides, spacer blocks, and
   template-like parts where a text-source model and simple parameter edits are
   enough.
2. Use CadQuery for Python-based assemblies, repeatable variants, and parts
   that need STEP/3MF output from scripted geometry.
3. Use FreeCAD with Python where measured hardware assemblies, sketches,
   constraints, drawings, and editable parametric history are needed.
4. Use KiCad 9 3D exports for board-fit envelopes and PCB/mechanical fit
   checks. STEP is preferred for mechanical CAD exchange; STL/PLY can support
   print/scanner workflows but remains derivative.
5. Keep CAD source files, parameter tables, and measurement ledgers separate
   from slicer outputs. Do not commit bulky vendor CAD packages, G-code,
   binary slicer projects, or raw scanner captures unless a later artifact
   policy explicitly opens that scope.
6. Each printable artifact must carry a print packet: source model path,
   exported mesh hash, printer, nozzle, material, dry state, layer height,
   perimeters, infill, supports, orientation, estimated print time, safety
   controls, acceptance dimensions, and stop rule.

## Material Policy

| Material | Default use | Gates |
| --- | --- | --- |
| PLA | Visual mockups, label plates, simple fit checks, and low-risk templates. | Heat/UV/mechanical limits must be stated; do not use for hot enclosures or stressed field hardware without review. |
| PETG | General functional prototypes, cable guides, brackets, and large Kobra 2 Max enclosure trials when heat load is modest. | Dry/adhesion profile, dimensional coupon, and edge/corner fit check before large prints. |
| ABS | Only after ventilation/enclosure/exposure controls and material SDS are recorded. | Enclosure, ventilation or local exhaust decision, odor/exposure control, warping coupon, and thermal review. |
| ASA | Outdoor/UV-oriented prototypes only after the same exposure and enclosure controls as ABS. | Enclosure, ventilation or local exhaust decision, material SDS, UV/temperature rationale, and fit coupon. |
| PA/nylon | Wear or toughness experiments after drying and dimensional-stability review. | Drying/humidity record, enclosure/bed profile, moisture warning, and measured coupon. |
| PA-CF / CF-nylon | Restricted to specialist prototype trials. | Hardened nozzle and drive-path proof, drying/humidity record, SDS, ventilation/exposure review, printer compatibility, abrasive-wear inspection, and noncritical first coupon. |

## Nontechnical Build Guide Template

Use this template for future operator-facing prototype guides. Keep every item
source-backed or marked as an unresolved gap.

1. Purpose: what the part does and which project lane it belongs to.
2. Parts list: printed parts, hardware, labels, inserts, adhesives, and
   replacement/spare items.
3. Safety stop gates: power, voltage, boot-pin, battery/solar, radio, relay,
   load/mains, heat, ventilation, and moving-part stops.
4. Tools: printer, scanner, calipers, PPE, ventilation control, hand tools, and
   inspection tools.
5. Print settings and material rationale: printer, nozzle, material, dry state,
   layer height, perimeters, infill, support, orientation, and why that material
   is acceptable for this part.
6. Assembly steps: short physical assembly actions with no firmware, wiring,
   charging, radio, relay/load, or mains instructions unless a later gate opens
   those exact actions.
7. Verification checklist: dimensions, fit, clearance, connector relief,
   fastener torque/retention if applicable, label placement, and interference
   checks.
8. Troubleshooting: print defects, fit mismatch, warping, loose fasteners,
   cable strain, and scanner/CAD mismatch.
9. Do not proceed if: unresolved source gaps, wet filament, missing ventilation,
   unverified hardened nozzle, missing caliper check, heat/odor, unexpected
   movement, battery swelling/damage, exposed conductors, relay/load/mains
   connection, or any unclear role/identity.

## Required Next Evidence

- Same-session local equipment inventory: printer/scanner model, serial or
  visible identity, firmware, nozzle, build plate, calibration state, and
  current safe operating location.
- Ventilation/exposure record aligned to NIOSH controls before ABS, ASA,
  PA/nylon, PA-CF, PET-CF, or long unattended prints.
- Filament SDS/material record, dry-state/humidity record, and storage policy.
- Calibration coupons for each printer/material pair before project parts.
- Scan-to-caliper validation record before scanner meshes drive fit decisions.
- Per-lane measurement packets for board, LCD, encoder, radio, battery, BMS,
  charger, solar, relay, TFT, MicroSD, expander, connector, cable, and
  enclosure clearances.
- A QA-reviewed nontechnical guide for the first candidate part before it is
  treated as a repeatable build procedure.

## Closed Gates

This document does not close any hardware identity, power, voltage, boot-pin,
isolation, wiring, radio, relay, load, mains, battery, solar charging, firmware,
framework, bridge, Win31, browser-client, or live-proof gate.
