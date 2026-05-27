# Consolidated Development Plan

Source index: [../knowledge-base/source-index.md](../knowledge-base/source-index.md)
Detailed status ledger:
[development-status-ledger.md](development-status-ledger.md)

Date: 2026-05-27

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

## Agent-Optimized Plan

| Lane | Status | Next action | Owner | Tier | Evidence needed | Closed surfaces | Current truth |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan governance | current | Keep this plan aligned with the status ledger, source index, task logs, and handoffs after each non-trivial lane change. | Agent Operations + QA | Tier 2 | `SRC-LOCAL-DEVELOPMENT-PLAN-CONSOLIDATION-2026-05-27` | Live bench, firmware runtime, hardware mutation | This file and `research/development-status-ledger.md` |
| ESP-NOW BBS live baseline | accepted-live | Use structured Gate H transcript proof as the current live baseline; any rerun starts with fresh Tier 3 preflight and authority. | Communications + QA | Tier 3 for live, Tier 2 for docs | `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` | Flash/erase/monitor unless a new live gate opens them | `research/development-status-ledger.md` |
| Custom wireless Gate F | accepted-host-prototype-only | Keep runtime firmware implementation closed; continue only host or owner-review slices until a later implementation gate is accepted. | Communications + Firmware + QA | Tier 2 | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26` | Firmware runtime, persistence, live proof | ADR-0006, ADR-0007, ADR-0008 |
| Full-service mesh discovery | accepted-host-simulator-only | Gate M2: DOS-C companion bridge/operator fixture support and Win31 read-only Network/Services summary. | Communications + Architecture + QA | Tier 2 | `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` | Live mesh, BLE pairing, Android app, router/admin, firmware mapping | ADR-0009 |
| Companion SoftAP Gate 1 | implemented-host-tooling-only | Re-run ESP32 and paired DOS-C host tests before any continuation; live proof needs fresh Tier 3 identity, recovery, Windows Wi-Fi, companion proof, and cleanup evidence. | Communications + QA | Tier 2 tooling; Tier 3 live | `SRC-LOCAL-ESPNOW-BBS-COMPANION-SOFTAP-LIVE-GATE-TOOLING-2026-05-27` | Live SoftAP, Windows Wi-Fi mutation, dummy GPIO/output, flash, cleanup acceptance | Task 0076 and handoff 0065 |
| Win31/OPCON and DOS-C companion | mixed | Treat Gate H and serial-nullmodem path as accepted; keep fullscreen human acceptance, CBBS input proof, and launcher/live proof as separate gated work. | QA + UI/Protocol | Tier 2 or Tier 3 by action | `SRC-LOCAL-WIN31-CBBS-INPUT-RENAME-ICON-UI-2026-05-27`, `SRC-LOCAL-WIN31-DASHBOARD-FULLSCREEN-RECOVERY-2026-05-26` | PCAP, packet-driver replacement, unsafe controls | Status ledger and Win31 task/handoff records |
| Four-relay XBee Wi-Fi | blocked hardware-facing | Complete low-voltage identity, power, relay, XBee adapter, TFT, MicroSD, expander, and instrument records before hardware-facing enablement. | Hardware + Firmware + QA | Tier 2 docs; Tier 3 bench | `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19` | Relay/load/mains, XBee writes, flashing, live output enablement | Four-relay docs and known gaps |
| Remote LCD XBee solar client | private-submodule-scaffolded-design-only | Perform source-backed identity intake inside private `rlxsc-*` submodules, prioritizing cell, BMS, charger/power path, panel, fuse/protection, enclosure, and current limits. | Hardware + QA | Tier 2 docs | `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26` | Wiring, charging, XBee writes, firmware, live bench | `docs/projects/remote-lcd-xbee-solar-client/development-stream.md` |
| Public docs and GitHub Pages | implemented-validated | Run build, manifest audit, and smoke checks before public-site changes. | Release + QA | Tier 2 | `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21` | Private evidence, bulky artifacts, unsupported hardware claims | `docs/index.md` and public-site scripts |
| Blocked future gates | blocked | Reopen only by a source-backed gate naming exact authority, recovery path, validation, and cleanup/rollback. | Relevant owner + QA | Tier 3 when live | Status-ledger source IDs or unresolved gap | Firmware runtime, BLE, live mesh, PCAP, relay, XBee, TFT, MicroSD, load, mains, router/admin, serial-write expansion | `research/development-status-ledger.md` |

## Human-Readable Plan

1. Keep the status system clean.
   Use this file for the next-action plan and
   [development-status-ledger.md](development-status-ledger.md) for detailed
   evidence. Update the task log, handoff, source ledger, source index, docs
   index, and known gaps whenever a lane changes state.

2. Continue ESP-NOW BBS work through host and companion gates first.
   The accepted live path remains
   `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
   The next safe mesh-discovery step is Gate M2 DOS-C companion fixture support
   and a read-only Win31 Network/Services summary. Companion SoftAP remains
   tooling-only until a new Tier 3 live proof opens it.

3. Keep Win31 and DOS-C status precise.
   Gate H and the serial-nullmodem path are accepted. Later Win31 items are not
   globally accepted: fullscreen physical-panel acceptance, CBBS input proof,
   and live launcher proof remain separate gates.

4. Keep hardware streams separate.
   Four-relay work stays blocked for hardware-facing enablement until exact
   board, relay, power, XBee, TFT, MicroSD, expander, instrument, load, and
   safety evidence exists. Remote LCD/XBee/solar work stays in private
   docs-first submodules until identity and power/safety records exist.

5. Publish only after validation.
   Public docs changes require the generated Pages build, manifest audit, smoke
   test, source-ID scan, link check, closed-surface review, and `git diff
   --check`.

## Closed Gates

This consolidation does not authorize firmware runtime migration, firmware
persistence, live SoftAP proof, Windows Wi-Fi mutation, physical output proof,
flash, erase, monitor, physical serial writes, serial-write expansion, BLE
pairing, live ESP-WIFI-MESH, Android app behavior, PCAP, router/admin mutation,
relay, XBee writes, TFT, MicroSD, load, mains, release gating, or cleanup
acceptance.
