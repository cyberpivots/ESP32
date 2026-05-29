# Consolidated Development Plan

Source index: [../knowledge-base/source-index.md](../knowledge-base/source-index.md)
Detailed status ledger:
[development-status-ledger.md](development-status-ledger.md)

Date: 2026-05-28

This is the singular tracked development plan for the ESP32 workspace. It is a
thin action layer over the canonical status ledger. Historical task logs,
handoffs, ADRs, source ledgers, and bench records remain evidence records and
are not rewritten as current truth.

## Verified Facts

- Current status truth is recorded in
  [development-status-ledger.md](development-status-ledger.md).
- Blockers and evidence requirements are recorded in
  [known-gaps.md](known-gaps.md).
- Accepted decisions are recorded as ADRs under `.agents/DECISIONS/`.
- Non-trivial work must leave a task record and, when continuation is needed, a
  handoff.
- Companion SoftAP Gate 1 has tooling-only validation records, but no live
  SoftAP, Windows Wi-Fi, physical output, bridge, vision, completion, or cleanup
  proof.
- Full-service mesh discovery Gate M2-A has paired DOS-C host-only
  bridge/operator support recorded in
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`.
- The BBS UI System Operation Improvement Program is recorded as a
  documentation/status/source-record program under
  `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`; it does not change
  runtime public APIs, firmware ABI, bridge ABI, serial ABI, Gate F service
  codes, `mesh_discovery.v1`, or Win31 transport.
- The Hardware Rapid Prototyping Program is recorded under
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28` as a Tier 2
  documentation/status/source-record lane for printer/scanner planning,
  parametric CAD workflows, build-guide templates, and hardware-lane prototype
  needs.
- The first package in that lane is recorded under
  `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28` with one
  public-safe fixture guide, one internal evidence workbook, and one
  provisional OpenSCAD source model. It does not close print, scan, fit,
  relay/load/mains, or hardware acceptance gates.
- The XBee continuation is recorded under
  `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29` as host-only inventory,
  identity-delta, and locked XCTU checklist tooling. No serial port was opened
  because same-session physical isolation, voltage/carrier, antenna, recovery,
  and cleanup evidence were not present.

## Assumptions

- This plan is current-state routing, not a replacement for detailed evidence.
- Each lane advances only through the next named gate and source-index-backed
  record.
- Historical records may contain stale blocker text; the current classification
  in this plan and the status ledger is authoritative for new work.

## Unknowns

- No current same-session live bench identity, no-load state, Windows Wi-Fi
  state, or process cleanup proof was captured by this consolidation pass.
- No current live proof opens firmware runtime migration, BLE, live mesh, PCAP,
  relay, XBee, TFT, MicroSD, load, mains, erase, monitor, router/admin
  mutation, or serial-write expansion.
- No current same-session printer/scanner identity, material, ventilation,
  calibration, measurement, live print, live scan, or fixture-fit proof is
  accepted.

## Agent-Optimized Plan

| Lane | Status | Next action | Owner | Tier | Evidence needed | Closed surfaces | Current truth |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan governance | current | Keep this plan aligned with the status ledger, source index, task logs, and handoffs after each non-trivial lane change. | Agent Operations + QA | Tier 2 | `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27` | Live bench, firmware runtime, hardware mutation | This file and `research/development-status-ledger.md` |
| ESP-NOW BBS live baseline | accepted-live | Use structured Gate H transcript proof as the current live baseline; any rerun starts with fresh Tier 3 preflight and authority. | Communications + QA | Tier 3 for live, Tier 2 for docs | `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` | Flash/erase/monitor unless a new live gate opens them | `research/development-status-ledger.md` |
| Custom wireless Gate F | accepted-host-prototype-only | Keep runtime firmware implementation closed; continue only host or owner-review slices until a later implementation gate is accepted. | Communications + Firmware + QA | Tier 2 | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26` | Firmware runtime, persistence, live proof | ADR-0006, ADR-0007, ADR-0008 |
| Full-service mesh discovery | gate-m2a-implemented-host-only | Gate M3: firmware mapping review/design-only for `mesh_discovery.v1`; live proof remains a separate future Tier 3 gate. | Communications + Architecture + QA | Tier 2 | `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27` | Live mesh, BLE pairing, Android app, router/admin, firmware mapping | ADR-0009 plus DOS-C commit `62c4db6` |
| BBS UI system operation program | ui0-m2b-implemented-host-only | Continue with Gate M3 mapping review/design-only or Client-1 static/simulated browser proof; live proof remains a separate future Tier 3 gate. | Agent Operations + UI/Protocol + Communications + QA | Tier 2 docs/status; Tier 3 for any later live proof | `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`, `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`, `SRC-LOCAL-WIN31-DASHBOARD-INTERFACE-IMPROVEMENT-2026-05-27`, `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24` | Runtime API changes, firmware ABI, bridge ABI, serial ABI, Gate F service-code changes, live browser proof, live mesh, BLE, PCAP, router/admin, flash, serial writes, hardware | UI-0/M2-B packet, task 0083, handoff 0072, DOS-C commit `7f0b5df` |
| Companion SoftAP Gate 1 | implemented-host-tooling-only | Re-run ESP32 and paired DOS-C host tests before any continuation; live proof needs fresh Tier 3 identity, recovery, Windows Wi-Fi, companion proof, and cleanup evidence. | Communications + QA | Tier 2 tooling; Tier 3 live | `SRC-LOCAL-ESPNOW-BBS-COMPANION-SOFTAP-LIVE-GATE-TOOLING-2026-05-27` | Live SoftAP, Windows Wi-Fi mutation, dummy GPIO/output, flash, cleanup acceptance | Task 0076 and handoff 0065 |
| Win31/OPCON and DOS-C companion | mixed | Treat Gate H and serial-nullmodem path as accepted; keep fullscreen human acceptance, CBBS input proof, and launcher/live proof as separate gated work. | QA + UI/Protocol | Tier 2 or Tier 3 by action | `SRC-LOCAL-WIN31-CBBS-INPUT-RENAME-ICON-UI-2026-05-27`, `SRC-LOCAL-WIN31-DASHBOARD-FULLSCREEN-RECOVERY-2026-05-26` | PCAP, packet-driver replacement, unsafe controls | Status ledger and Win31 task/handoff records |
| Four-relay XBee Wi-Fi | continued-host-inventory-live-blocked | Complete low-voltage identity, power, relay, XBee adapter, TFT, MicroSD, expander, and instrument records before hardware-facing enablement; for XBee, continue only through physical one-at-a-time adapter mapping and read-only gates. | Hardware + Firmware + QA | Tier 2 docs/tooling; Tier 3 bench | `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`, `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29` | Relay/load/mains, XBee writes, XCTU live discovery, serial reads, flashing, live output enablement | Four-relay docs, XBee study docs, and known gaps |
| Remote LCD XBee solar client | private-submodule-scaffolded-design-only | Perform source-backed identity intake inside private `rlxsc-*` submodules, prioritizing cell, BMS, charger/power path, panel, fuse/protection, enclosure, and current limits. | Hardware + QA | Tier 2 docs | `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26` | Wiring, charging, XBee writes, firmware, live bench | `docs/projects/remote-lcd-xbee-solar-client/development-stream.md` |
| Hardware rapid prototyping and CAD | planned-doc-status-program | Use the new cross-project program for 3D-printed enclosures, brackets, fixtures, cable guides, scanner fit checks, parametric CAD source workflows, and nontechnical build-guide templates. | Hardware + Fabrication/CAD + Safety/Power + QA | Tier 2 docs/status; Tier 3 for any later live print/bench proof | `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`, `SRC-CREALITY-K1-SUPPORT-2026-05-28`, `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`, `SRC-CREALITY-CR30-2026-05-28`, `SRC-CREALITY-CR-SCAN-LIZARD-2026-05-28`, `SRC-NIOSH-SAFE-3D-PRINTING-2024-103` | Live printing treated as build action until scoped; wiring, flashing, serial/radio writes, battery/solar charging, relay/load/mains, firmware runtime, framework selection, bulky CAD/vendor artifacts, slicer projects, G-code, raw scans | `docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md` |
| Four-relay low-voltage fixture kit | provisional-doc-cad-package | Complete workbook evidence before treating the guide or plate as repeatable; keep public artifact limited to the guide. | Hardware + Fabrication/CAD + Safety/Power + Release/Tooling + QA | Tier 2 docs/CAD source; Tier 3 for any later live print or bench use | `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`, `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`, `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`, `SRC-OPENSCAD-DOCS-2026-05-28` | Live printing, live scanning, board-specific holes, generated CAD/print artifacts, slicer projects, G-code, raw scans, wiring, relay inputs, relay contacts, XBee writes, ESP32 carrier connections, load, mains, firmware/runtime/API/ABI/framework changes | Public guide, workbook, one OpenSCAD source, source ledger, task 0082, handoff 0071 |
| Public docs and GitHub Pages | implemented-validated | Run build, manifest audit, and smoke checks before public-site changes. | Release + QA | Tier 2 | `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21` | Private evidence, bulky artifacts, unsupported hardware claims | `docs/index.md` and public-site scripts |
| Blocked future gates | blocked | Reopen only by a source-backed gate naming exact authority, recovery path, validation, and cleanup/rollback. | Relevant owner + QA | Tier 3 when live | Status-ledger source IDs or unresolved gap | Firmware runtime, BLE, live mesh, PCAP, relay, XBee, TFT, MicroSD, load, mains, router/admin, serial-write expansion | `research/development-status-ledger.md` |

## BBS UI System Operation Improvement Program

### Agent Execution Packet

| Field | Routing |
| --- | --- |
| Program status | `planned-doc-status-program` |
| Selected tier | Tier 2 for planning, status, source records, host-only tests, and copied evidence review; Tier 3 for any future live bench, selected-board browser proof, flash, serial write, radio, or hardware action. |
| Owner roles | Agent Operations owns routing records; UI/Protocol owns Win31/CBBS and browser-client UI boundaries; Communications owns bridge/discovery summary boundaries; QA owns validation and gate evidence. |
| Baseline path | Preserve `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`. |
| Evidence anchors | `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27`, `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`, `SRC-LOCAL-WIN31-DASHBOARD-INTERFACE-IMPROVEMENT-2026-05-27`, `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`. |
| Mutation boundary | Documentation/status/source records and host-only tests only unless a later gate explicitly opens a narrower surface. |
| Public interface change | Documentation structure in this file only. No runtime public API, firmware ABI, bridge ABI, coordinator serial ABI, `mesh_discovery.v1` schema, Gate F service-code map, or Win31 transport change. |
| Validation | Scaffold checks, agent-process audit, scaffold audit unit tests, changed-file source-ID scan, changed-file Markdown link check, custom wireless protocol tests when discovery/bridge claims are touched, Win31 legibility analyzer tests only when analyzer-backed records change, and `git diff --check`. |
| Stop gates | Live bench, prepare/flash/complete, erase, monitor, serial-write expansion, firmware runtime migration, BLE, live ESP-WIFI-MESH, Android app behavior, browser live proof, PCAP, router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, and cleanup acceptance. |

### Reviewer Quorum And Voting

Use the existing reviewer roles before any Tier 2 or Tier 3 lane movement:
`governance-cartographer`, `evidence-record-auditor`,
`ui-code-protocol-analyst`, `source-skill-curator`,
`qa-validation-reviewer`, `win31-dashboard-vision-gate` only for copied
screenshot/OCR/CV evidence, and `live-bench-gate-reviewer` only for later
live gates.

Decision weighting:

| Criterion | Weight |
| --- | --- |
| Safety and gate correctness | 25% |
| Source and evidence quality | 20% |
| Non-technical operator usefulness | 20% |
| Implementation feasibility | 15% |
| Testability and reproducibility | 10% |
| Performance and latency impact | 10% |

A no-P1/P2 quorum may accept only the named gate and mutation boundary. A Tier
3 acceptance still requires same-session evidence, explicit live-gate
authority, recovery path, and closed-surface review.

### Continuous Update Rule

Every non-trivial lane change in this program must update the singular plan,
development status ledger, source index, source ledger, task log, handoff when
another role must continue, known gaps, validation results, and next-gate owner.
Do not create a second roadmap for this program.

### Skill Routing

- Use `expert-agent-panels` for the evidence-first panel loop.
- Use `esp32-live-gate-coordinator` for live-gate boundary checks only.
- Use `win31-dashboard-vision-gate` only for copied screenshot/OCR/CV evidence.
- Use `skill-creator` only if a later authorized edit updates skills.
- Keep `research/skills/available-skills.md` refreshed before relying on
  installed path claims.

### Phase Gates

| Phase | Scope | Output | Stop gate |
| --- | --- | --- | --- |
| UI-0 | Review current Win31/CBBS UI and existing legibility/interface backlog for non-technical operator clarity. | Ranked improvements for labels, disabled-control explanations, view hierarchy, contrast, OCR confidence, footer/log density, and transcript-first proof wording. | No runtime or live proof claim from screenshots alone. |
| M2-B | Strengthen host-only Network/Services discovery UX using current `discovery_snapshot`, `discovery_events`, `service_catalog`, and `capability_report` support. | Proof that summaries stay read-only, bounded to 512-byte bridge lines, schema-versioned where applicable, and separate from coordinator serial ABI and Gate F service codes. | No live mesh, BLE, router/admin, firmware runtime, or serial ABI expansion. |
| M3 | Review firmware mapping design for ESP-WIFI-MESH events/APIs to `mesh_discovery.v1`. | Design notes and fixtures only. | No runtime firmware, live mesh, BLE, router/admin, flash, monitor, or serial writes. |
| Client-1 | Plan browser/client-node interface testing from simulated/static or read-only browser evidence. | Screenshots, console/network logs, smoke checks, and optional CV/OCR review for generated/static UI artifacts. | Do not label connected devices as coordinator/router/end-node until same-session read-only inventory verifies identity and role. |
| Client-2 | Future selected-board read-only Wi-Fi browser proof after a separate Tier 3 gate. | Same-session board identity, power/voltage/boot-pin/isolation review, recovery path, browser proof, and cleanup evidence. | Dummy-output control remains later and requires explicit GPIO, fixture, no-load/no-relay/no-mains evidence. |

Current UI-0/M2-B result:
[../docs/projects/espnow-bbs/bbs-ui-ui0-m2b-host-slice.md](../docs/projects/espnow-bbs/bbs-ui-ui0-m2b-host-slice.md)
records the ranked UI-0 packet and M2-B host-only Network/Services proof.
DOS-C commit `7f0b5df` supplies the paired operator wording and source tests.
This result does not open M3 firmware mapping, Client-1 browser proof, Client-2
selected-board proof, dummy-output control, or any live/hardware gate.

## Hardware Design And 3D-Printed Prototype Program

Detailed plan:
[../docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md](../docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md)

| Field | Routing |
| --- | --- |
| Program status | `planned-doc-status-program` |
| Selected tier | Tier 2 for docs, source records, status ledgers, CAD workflow planning, and nontechnical guide templates. Later live printing, scanning sessions, or bench fixture use must open the exact gate needed. |
| Owner roles | Hardware owns equipment/lane needs; Safety/Power owns material, ventilation, thermal, battery/solar, and relay/load/mains stops; Fabrication/CAD owns OpenSCAD, CadQuery, FreeCAD, KiCad, scanner, and slicer boundaries; Communications/Firmware owns API/ABI/transport closure; QA owns validation and evidence records. |
| Equipment defaults | K1 for smaller engineering-material parts after nozzle/material/safety proof; Kobra 2 Max for large enclosures/panels/jigs; CR-30 for batch or long rails/cable guides after belt proof; CR-Scan Lizard for fit/reference scans only after known-dimension checks. |
| Evidence anchors | `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`, `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`, `SRC-CREALITY-K1-SUPPORT-2026-05-28`, `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`, `SRC-CREALITY-CR30-2026-05-28`, `SRC-CREALITY-CR-SCAN-LIZARD-2026-05-28`, `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`, `SRC-OPENSCAD-DOCS-2026-05-28`, `SRC-CADQUERY-DOCS-2026-05-28`, `SRC-FREECAD-FEATURES-2026-05-28`, `SRC-KICAD9-PCBNEW-3D-EXPORT-2026-05-28`, `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`, `SRC-BAMBULAB-PA6-CF-2026-05-28`. |
| Mutation boundary | Documentation/status/source records plus exactly one provisional OpenSCAD source for the four-relay low-voltage fixture kit. No additional CAD source, generated CAD/print artifact, slicer project, G-code, raw scan, firmware, framework file, or live proof artifact is added. |
| Stop gates | Live bench, wiring, flashing, monitor/serial write, radio write, BLE/live mesh, relay/load/mains, battery/solar charging, firmware runtime, framework selection, runtime API/ABI changes, bridge ABI changes, `mesh_discovery.v1`, Gate F service map, Win31 transport, bulky vendor artifacts, slicer projects, G-code, and raw scanner captures. |

| Lane | Prototype planning need | Next evidence |
| --- | --- | --- |
| ESP-NOW BBS path | Nonconductive coordinator/peer trays, serial cable strain relief, labels, cable guides, and Pi/ESP32 transport fixtures. | Measured cable/board dimensions and proof the fixture does not change the accepted serial-nullmodem path or touch boot/reset pins unintentionally. |
| Four-relay XBee Wi-Fi | Low-voltage fixture plate, relay-contact guard mockups, XBee dock bracket, MicroSD access mockup, TFT bezel, expander/mux test jigs, and cable guides. | Exact module dimensions and low-voltage-only separation before any fixture becomes a guide; relay/load/mains stays closed. |
| Four-relay low-voltage fixture kit | Public-safe guide, internal workbook, and provisional plate source with cable-tie slots, label zones, and measurement grid. | Fill the workbook with printer identity, K1 hardened-nozzle proof if needed, filament/SDS/dry state, ventilation controls, calibration coupon, dimensions, and reviewer signoff before any repeatable build claim. |
| Remote LCD XBee solar client | Separate field-device enclosure concepts, LCD/encoder fit, XBee antenna clearance, battery/BMS/charger placeholders, solar lead strain relief, and nontechnical guide templates. | Source-backed identity intake in private `rlxsc-*` submodules before parent integration claims. |
| TFT/MicroSD/expander/storage | Bezel, SD access, connector keep-out, standoff, and serviceability prototypes. | Exact module sources, dimensions, voltage/pullup evidence, and boot-pin conflict review. |
| Future browser/client-node interface | Phone/laptop stand, node enclosure mockups, QR/label holders, and selected-board tray. | Static/simulated proof first; selected-board Wi-Fi proof requires a later Tier 3 gate. |

## Human-Readable Plan

1. Keep the status system clean.
   Use this file for the next-action plan and
   [development-status-ledger.md](development-status-ledger.md) for detailed
   evidence. Update the task log, handoff, source ledger, source index, docs
   index, and known gaps whenever a lane changes state.

2. Continue ESP-NOW BBS work through host and companion gates first.
   The accepted live path remains
   `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
   Gate M2-A now provides DOS-C companion bridge/operator support and a
   read-only Win31 Network/Services summary. The next safe mesh-discovery step
   is Gate M3 firmware mapping review/design-only. Companion SoftAP remains
   tooling-only until a new Tier 3 live proof opens it.

3. Keep Win31 and DOS-C status precise.
   Gate H and the serial-nullmodem path are accepted. Later Win31 items are not
   globally accepted: fullscreen physical-panel acceptance, CBBS input proof,
   and live launcher proof remain separate gates.

4. Improve BBS UI operation through gated, source-backed slices.
   UI-0 and M2-B now have a host-only source packet and paired DOS-C operator
   proof. Next choose Gate M3 firmware mapping review/design-only or Client-1
   static/simulated browser proof; transcript proof remains authoritative and
   live proof requires a separate Tier 3 gate.

5. Use rapid prototyping as evidence support, not hardware acceptance.
   3D-printed enclosures, brackets, fixtures, cable guides, scanner fit checks,
   and nontechnical guides must remain source-backed and lane-bounded. The K1,
   Kobra 2 Max, CR-30, and CR-Scan Lizard defaults are planning defaults only
   until same-session equipment, material, ventilation, calibration, and
   measurement evidence exists. The four-relay fixture kit is the first
   provisional package and adds one OpenSCAD source only; it is not a print or
   fit acceptance record.

6. Keep hardware streams separate.
   Four-relay work stays blocked for hardware-facing enablement until exact
   board, relay, power, XBee, TFT, MicroSD, expander, instrument, load, and
   safety evidence exists. Remote LCD/XBee/solar work stays in private
   docs-first submodules until identity and power/safety records exist.

7. Publish only after validation.
   Public docs changes require the generated Pages build, manifest audit, smoke
   test, source-ID scan, link check, closed-surface review, and `git diff
   --check`.

## Closed Gates

This consolidation does not authorize firmware runtime migration, firmware
persistence, live SoftAP proof, Windows Wi-Fi mutation, physical output proof,
flash, erase, monitor, physical serial writes, serial-write expansion, BLE
pairing, live ESP-WIFI-MESH, Android app behavior, PCAP, router/admin mutation,
relay, XBee writes, TFT, MicroSD, live printing, live scanning, generated
CAD/print artifacts, slicer projects, G-code, raw scans, load, mains, release
gating, or cleanup acceptance.
