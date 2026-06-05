# Development Overview for Nontechnical Readers

Date: 2026-06-05

This document explains what is being developed in this workspace, what is
already accepted, what is only planned, and what is still blocked. It is written
for people who do not need to read the code to understand the work.

This is not a release note and not a hardware approval. It summarizes the
current record-backed development lanes. Detailed proof still lives in the task
logs, source ledgers, ADRs, bench records, and validation scripts linked from
[docs/index.md](index.md).

## How Development Works Here

The workspace is run as an evidence-first engineering project. A change is not
treated as accepted just because code exists. Work must name its scope, owner,
risk level, proof needed, validation commands, and any authority it does not
have. Non-trivial work leaves a task record and a source ledger.

The practical meaning is simple:

- A plan is not the same as proof.
- A simulator result is not the same as live hardware behavior.
- A local debug build is not the same as a signed release.
- A reviewed hardware idea is not the same as a safe wiring procedure.
- Future development is described as the next gate to open, not as a promised
  outcome.

The workspace is generally framework-neutral. ESP-IDF v6.0.1 is accepted only
for the project lanes that have accepted ADR coverage, including
`four-relay-xbee-wifi` and `espnow-bbs`. That does not make ESP-IDF a global
workspace-wide default.

## What This Codebase Is Building

At a high level, this repo is a development hub for connected ESP32 devices,
radio communication, operator tools, and evidence systems. The major areas are:

- ESP32 firmware and interface contracts.
- ESP-NOW BBS radio communication and a DOS-C/Win31 operator path.
- XBee Pro 900HP radio planning, read-only evidence, and host-only simulation.
- A four-relay XBee Wi-Fi controller with LCD, encoder, relay, storage, and
  expansion planning.
- React Native and React Native Windows CBBS apps for Client, Sysop, and
  Hardware Tools experiences.
- Hardware rapid-prototyping documentation for fixtures, enclosures, and
  nontechnical build guides.
- Validation scripts, source ledgers, task logs, and public documentation
  hygiene.

## Current Development Areas

| Area | Plain-language purpose | Current verified status | Future planned development | Not yet approved |
| --- | --- | --- | --- | --- |
| Governance and records | Keeps work traceable and prevents hidden scope changes. | Agent rules, task logs, handoffs, ADRs, source ledgers, and scaffold audits are the control system for the workspace. | Keep records current after each non-trivial lane change. | Skipping task/source records for non-trivial work. |
| ESP-NOW BBS | A bulletin-board style communication system using ESP32 wireless devices. | Structured Gate H live acceptance exists for the accepted operator-to-ESP32 path. | Rerun live proof only through a fresh Tier 3 gate with same-session evidence. | Flashing, serial expansion, PCAP, router/admin mutation, BLE, or live mesh without a new gate. |
| DOS-C and Win31 operator system | A retro operator interface that talks through DOSBox-X, a Pi bridge, and ESP32 hardware. | The accepted path is recorded through the structured Gate H proof. Later UI improvements are tracked separately. | Continue host-only UI, legibility, and static/simulated proof work before any new live action. | Treating screenshots alone as live communication proof. |
| Custom wireless protocol | Defines what messages mean and how host-side fixtures should behave. | Gate F is accepted as a host-prototype/design contract with runtime requirements. | Continue design reviews and host-only fixtures before firmware runtime implementation. | Claiming firmware runtime, persistence, or live proof from host-only tests. |
| Full-service mesh discovery | Shows network and service information for operators. | Gate M2-A is host-only and paired with DOS-C support. | Gate M3 is the next design-only firmware mapping review. | Live mesh, BLE pairing, Android behavior, or router/admin changes. |
| LCD and rotary encoder field console | Gives the device a small local display and knob/button menu. | Multiple PF0530 records exist; PF0530V user acceptance records real LCD menu encoder functionality, while later visual-art work remains pending physical acceptance. | Characterize PF0530V telemetry, finish visual acceptance for later art/menu work, and keep live steps gated. | Relay action, XBee/RF action, wiring-under-power, or future flashes without a named gate. |
| Four-relay XBee Wi-Fi controller | The main device lane for controlling four relay channels while preserving safety boundaries. | Source docs, hardware profiles, safe-core host tests, power/safety notes, and accepted project-specific ESP-IDF scope exist. | Finish board identity, power budget, relay-module evidence, TFT/MicroSD/expander records, and safe fixture work before hardware enablement. | Relay/load/mains work, final wiring, relay GPIO output enablement, or broad hardware acceptance. |
| XBee radio integration | Studies and plans XBee Pro 900HP radio use for hub-spoke communication. | The exact recorded part is `XBP9B-DPUT-001`; host-only hub-spoke planning, simulator fixtures, and source-backed API/status corrections exist. | Run read-only bench proof tiers before any future setting-write gate; later range/throughput and field deployment need separate gates. | Serial opens, AT writes, `WR`, `AC`, `KY`, API transmit to hardware, RF tests, or profile writes. |
| Remote LCD XBee solar client | A separate field-device concept for a remote LCD/XBee/solar node. | The parent repo tracks it as design-only and private-submodule based. | Do identity, power, battery, charger, solar, enclosure, and current-limit intake in the private stream first. | Wiring, charging, XBee writes, firmware, or live bench claims. |
| CBBS React Native apps | Mobile/web-style app surfaces for CBBS roles and evidence review. | ADR-0010 accepts the CBBS React Native platform strategy; host-only app and protocol work is tracked. | Continue role-specific Client and Sysop polish, fixture-driven tests, and closed-surface wording. | Live transport, BLE/Web Serial/Web Bluetooth, EAS/App Center, device release, or hardware action. |
| React Native Windows apps | Windows product apps for CBBS Client, CBBS Sysop, and CBBS Hardware Tools. | Native generation, local debug/build/launch records, and cleanup records exist for bounded review gates. | Future gates may prove split app runtime behavior, package identity, signing, and distribution. | Treating local Debug review as final package identity, Store/App Installer readiness, or release. |
| CBBS Hardware Tools | A Windows tool surface for reviewing bench, radio, firmware, fabrication, and safety evidence. | Current work is review-only: saved evidence, firmware catalog metadata, communications analysis, and disabled closed-surface controls. | Future live bridge or firmware execution requires accepted ABI, adapter evidence, transcript proof, rollback, and cleanup. | HostCommandBridge dispatch, shell execution, serial/RF/XBee writes, firmware flash, OTAP, relay/load/mains. |
| Hardware rapid prototyping | Uses 3D printing, scanning, and CAD planning to support device fixtures and guides. | A documentation/status program and provisional low-voltage fixture package exist. | Fill evidence workbooks, verify printer/scanner/material conditions, and keep generated print artifacts gated. | Live printing as acceptance, raw scans, slicer projects, G-code, or hardware fit claims without proof. |
| Public documentation and Pages | Publishes safe, curated documentation when authorized. | Build, manifest, smoke, and publication-hygiene scripts exist. | Run public-site validation before any future publication. | Publishing, release, commit, push, PR, or private-evidence exposure without explicit authority. |
| Scripts, tests, and simulators | Host-side tools that prove contracts without touching hardware. | Scaffold audits, record audits, source audits, React Native audits, XBee study tools, and host-only simulators are active validation surfaces. | Extend tests when a lane adds new contracts or evidence types. | Treating a simulator or audit pass as live hardware proof. |

## Future Planned Development

The next work should stay lane-specific:

- Keep this overview, the consolidated plan, the status ledger, known gaps,
  source index, and docs index aligned after future non-trivial changes.
- Continue ESP-NOW BBS through design-only Gate M3 and static/simulated client
  proof before opening any new live gate.
- Advance CBBS React Native and React Native Windows work through host-only
  fixture tests, split-app runtime proof gates, and later signing/distribution
  gates only when those gates are explicitly opened.
- Continue Hardware Tools as an evidence-review surface until a separate
  HostCommandBridge live gate accepts adapter proof, ABI, rollback, transcript,
  and cleanup evidence.
- Continue XBee radio work with read-only bench proof and source-backed
  planning before any profile write, key write, transmit, range, or deployment
  gate.
- Continue four-relay hardware work by identifying exact boards/modules,
  proving voltage and power boundaries, and keeping relay/load/mains work
  blocked until qualified review.
- Continue LCD/encoder work by characterizing accepted PF0530V behavior and
  proving later visual-art/menu work separately.
- Continue remote LCD XBee solar work in its private identity and power stream
  before parent-repo integration claims.
- Continue rapid-prototyping work through evidence workbooks and bounded CAD
  source, not generated print artifacts or live print claims.
- Continue public documentation only after local Pages build, manifest, smoke,
  and publication-hygiene checks.

## Explicitly Closed Or Blocked Work

The following remain closed unless a later task opens an exact gate with
authority, recovery path, evidence, validation, and cleanup:

- Firmware flash, erase, monitor, runtime migration, or persistence outside a
  named gate.
- HostCommandBridge live dispatch or native adapter execution.
- Serial/RF/XBee writes, XBee profile writes, key writes, API transmit to
  hardware, range tests, throughput tests, or deployment acceptance.
- Relay output enablement, load work, mains work, wiring-under-power, or final
  hardware acceptance.
- BLE, Web Bluetooth, Web Serial, live mesh, PCAP, router/admin mutation, or
  Windows Wi-Fi mutation.
- Signing, Store/App Installer packaging, EAS, App Center, publication,
  release, commit, push, or PR.
- Copying vendor PDFs, raw private evidence, bulky CAD artifacts, slicer
  projects, G-code, or raw scans into the repo.

## Glossary

- ADR: a recorded decision. It says what was accepted and what was not.
- Bench record: a proof note from a hardware or live-system session.
- Bridge: software that passes messages between one system and another.
- Closed gate: work that is not allowed until a later task explicitly opens it.
- ESP32: the microcontroller family used in the device work.
- ESP-NOW: an ESP32 wireless communication method.
- Firmware: software that runs directly on a device.
- Host-only: work that runs on the development computer and does not operate
  live hardware.
- Source ledger: a short record explaining what sources support a task.
- Tier 2: broad docs, protocol, evidence, governance, or code work that needs
  review before mutation.
- Tier 3: live hardware, flashing, serial/radio writes, relay/load/mains,
  release, or similarly risky work.
- XBee: a Digi radio module family used here for planned off-grid radio links.

## Source Backing

This overview is backed by current workspace records, especially:

- `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`
- `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`
- `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`
- `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`
- `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`
- `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`
- `SRC-LOCAL-CBBS-RNW-SPLIT-NATIVE-GENERATION-2026-06-04`
- `SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`
- `SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`
- `SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-HOST-ONLY-IMPROVEMENTS-2026-06-05`
- `SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-CLEANUP-2026-06-05`
- `SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`
- `SRC-LOCAL-WORKSPACE-REVIEW-FOLLOW-UP-HARDENING-2026-06-05`
- `SRC-LOCAL-NONTECHNICAL-DEVELOPMENT-OVERVIEW-2026-06-05`

Unknowns or older status claims should be checked against
[research/known-gaps.md](../research/known-gaps.md),
[research/triage-status.md](../research/triage-status.md), and the latest task
records before new work begins.
