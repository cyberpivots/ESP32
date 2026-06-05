# Source Ledger - 2026-06-05 Nontechnical Development Overview

## Scope

Tier 2 documentation/status update adding a nontechnical codebase development
overview, docs-index discoverability, and durable Task 0177 records. This
source ledger covers only record-backed documentation. It does not authorize or
claim live hardware, serial/RF/XBee writes, firmware execution, bridge
dispatch, relay/load/mains, release, publication, commit, push, PR, or deploy.

## Source IDs

- `SRC-LOCAL-NONTECHNICAL-DEVELOPMENT-OVERVIEW-2026-06-05`
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

## Verified facts

- The overview groups the checked-in workspace into plain-language
  development lanes: governance/records, ESP-NOW BBS, DOS-C/Win31,
  custom wireless protocol, mesh discovery, LCD/encoder, four-relay XBee
  Wi-Fi, XBee radio integration, remote LCD XBee solar client, CBBS React
  Native apps, React Native Windows apps, Hardware Tools, rapid prototyping,
  public docs/Pages, scripts/tests/simulators, and shared packages/protocols.
- The overview treats `research/development-plan.md` and
  `research/development-status-ledger.md` as older anchors and reconciles them
  with June 3-5 task/source records.
- The overview separates current verified status, future planned development,
  and explicitly closed or blocked surfaces.
- The documentation links back to the source index, known gaps, triage status,
  and latest task/source records rather than copying private or bulky evidence.

## Assumptions

- The user wanted a durable in-repo explanation rather than a chat-only
  summary.
- The target audience is nontechnical stakeholders, operators, and future
  contributors.
- Public-site publication is not opened by this task.

## Unknowns

- Whether a later public-facing version should be added to the Pages bundle is
  unspecified.
- Owner-specific preferences for a longer narrative, diagrams, or per-lane
  nontechnical handbooks remain open.
- Hardware identity, wiring, voltage, relay/load/mains, XBee live settings,
  live bridge dispatch, signing, and release claims remain governed by their
  existing known gaps and task/source records.

## Validation

Passed on 2026-06-05:

- `git diff --check` exited `0` with the pre-existing CRLF normalization
  warning for
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.cpp`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 177`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.

## Decision

Decision: accept the nontechnical overview as a documentation/status artifact
only. All live hardware, RF/XBee write, firmware, bridge-dispatch, release,
publication, commit, push, PR, and deploy surfaces remain closed.
