# Task 0183: Remote LCD XBee Solar Client Hardware Intake Audit

Status: completed-records-only; exact hardware identity remains open

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-HARDWARE-INTAKE-AUDIT-2026-06-05`,
`SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`,
`SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`,
`SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26`,
`SRC-NXP-PCF8574-74A`,
`SRC-BOURNS-PEC11R`,
`SRC-TI-BQ25185`,
`SRC-TI-BQ2970`,
`SRC-TI-BQ27441-G1`,
`SRC-UL-LIION-SAFETY`,
`SRC-ESP32-WROOM-32-DATASHEET`,
`SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`,
`SRC-ESP-IDF-GPIO`,
`SRC-ESP-IDF-UART`,
`SRC-ESP-IDF-I2C`,
`SRC-DIGI-XBP9B-DPUT-001`,
`SRC-DIGI-XBEE-PRO-900HP`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`,
`SRC-DIGI-XBEE-900HP-TO-2026-06-05`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`,
`SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`,
`SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`,
`SRC-LOCAL-XBEE-TIER-A-NO-SERIAL-IDENTITY-EVIDENCE-2026-06-05`,
`SRC-LOCAL-AGENTIC-PLANNING-GUIDE-2026-06-05`

## Routing

- Verified facts: `remote-lcd-xbee-solar-client` is a separate hardware-device
  stream with seven private `rlxsc-*` docs-only submodules. Parent docs and
  submodule README files keep the lane framework-neutral, evidence-first, and
  closed to firmware, wiring, charging, battery/solar connection, XBee writes,
  API transmit frames, ESP32 DIN/DOUT wiring, pin assignments, and live bench
  action. Current `git submodule status --recursive` was captured for this
  task and shows all seven submodules on `heads/main`; it records current
  status only and does not claim the older 2026-05-26 seed-ledger pins are
  current.
- Assumptions: this packet is a parent repo records/status audit. It does not
  edit submodule contents, submodule pointers, hardware profiles, firmware,
  communication protocols, live tools, or public publication state.
- Unknowns: exact ESP32 board, module, carrier, regulator, USB-UART bridge,
  power input, boot/recovery method, 20x4 LCD module/backpack, I2C address,
  pullups, backlight current, rotary encoder, 18650 cell, BMS/protection board,
  solar panel, charger/power-path module, fuel gauge, XBee carrier, antenna,
  fuse/protection, enclosure, power budget, rail/current limits, pin map,
  framework ADR, remote-client read-only XBee proof, and live bench proof
  remain unresolved.
- Selected tier: Tier 2 records-only hardware intake audit.
- Owner role: Hardware with QA, plus Communications for XBee wording and Agent
  Operations for durable records.
- Evidence need: parent remote-client docs, all seven `rlxsc-*` README files,
  current submodule status, existing source-index rows, research status/gap
  files, and read-only reviewer quorum output.
- Mutation boundary: this task record,
  `.agents/handoffs/0131-remote-lcd-xbee-solar-client-hardware-intake-audit-to-hardware-qa.md`,
  `knowledge-base/source-ledger/2026-06-05-remote-lcd-xbee-solar-client-hardware-intake-audit.md`,
  `knowledge-base/source-index.md`, `docs/index.md`,
  `docs/projects/remote-lcd-xbee-solar-client/hardware-intake.md`,
  `docs/projects/remote-lcd-xbee-solar-client/development-stream.md`,
  `research/development-plan.md`, `research/development-status-ledger.md`,
  `research/triage-status.md`, and `research/known-gaps.md`.
- Reviewer quorum: read-only project-local subagents were spawned for
  development-panel coordination, power/wiring/isolation, evidence records, QA
  validation, XBee radio/protocol, and source coverage review. All reviewers
  were waited and closed after output capture. Weighted disposition: 17/17
  conditional approval, threshold 70 percent. No P1/P2 blockers remained for
  the named parent docs/records mutation. Conditions required candidate/
  reference-only wording, no selected-hardware claim, fresh submodule status
  wording, no transfer of four-relay XBee COM/RF proof into this lane, a
  non-vacuous Task 0183 file check, and post-mutation validation.
- Gate authority: parent docs/status/source records and validation summaries
  only. No Tier 3 authority is opened.
- Validation plan: run explicit Task 0183 file check, source/docs/path/record/
  agent/skill audits, current submodule status, submodule docs-only static
  check, focused unit tests, Pages build/audit/smoke because docs index is
  touched, scaffold verification, and `git diff --check`.
- Trust boundary: local repo records, private submodule README summaries, and
  source-indexed candidate/reference sources. Raw photos, markings, serial
  identifiers, COM/PnP mappings, `SH`/`SL`, keys, address plans, passive bytes,
  full setting snapshots, and private bench captures remain local/redacted.

## Implementation

- Added this Task 0183 parent records-only hardware intake audit.
- Added source ledger, source-index row, docs-index links, and Hardware/QA
  handoff.
- Updated parent remote-client docs/status files to mark the intake as
  audited but not closed.
- Preserved submodule content and pointers; no `rlxsc-*` submodule files were
  edited.
- Preserved dirty-tree boundaries for Tasks 0179-0182 already present in shared
  files.

## Validation

Validation completed on 2026-06-05:

- PASS: `test -f .agents/TASK_LOG/0183-remote-lcd-xbee-solar-client-hardware-intake-audit.md`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 183`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_paths.py`.
- PASS: `git submodule status --recursive`; all seven `rlxsc-*` submodules
  are on `heads/main` at the pins listed in the source ledger.
- PASS: `git diff --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_scaffold_audit_records tests.scaffold_audits.test_source_image_scan tests.scaffold_audits.test_xbee_radio_study`
  (22 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
  built 64 public files.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py build/github-pages`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `timeout 180s env PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.

The reviewer-suggested 60-second timeout was insufficient for this workspace
and exited `124` with no scaffold failure output; the 180-second run passed.

The submodule static check also passed: all seven `rlxsc-*` submodule
worktrees were clean, and no firmware, framework, source, binary, PDF,
setting-write, transmit-procedure, raw COM mapping, serial identifier, AES key,
full setting snapshot, or live discovery claim was added.

## Open Evidence

- Exact physical hardware identity and source links are missing for every
  remote-client component.
- No photo/inspection provenance, voltage/current measurements, pullup
  measurements, charger/BMS/cell compatibility review, panel Voc/Isc record,
  enclosure review, fuse/protection review, rail budget, current-limited supply
  plan, boot/recovery packet, pin-risk closure, remote-client XBee carrier
  proof, remote-client antenna proof, or read-only XBee proof exists.
- No framework ADR, firmware source, payload schema, power-state data model, or
  host-only prototype acceptance exists for this lane.

## Authority Limits

This task does not authorize wiring, charging, battery pack assembly, solar
connection, power-path connection, ESP32 GPIO attachment, ESP32 DIN/DOUT to
XBee, live measurement, bench bring-up, firmware implementation, framework
selection, hardware profile acceptance, pin assignment, charger/BMS/cell
selection, enclosure selection, XBee serial open, Tier B AT reads, XCTU or
XBee Studio live discovery, XBee setting writes, `WR`, `AC`, `KY`, API
transmit, RF/range/throughput tests, firmware update/recovery, flash, erase,
monitor, relay/load/mains work, release, publication, commit, push, PR, deploy,
`/etc/codex/requirements.toml`, or `admin-strict` mutation.

## Handoff

[../handoffs/0131-remote-lcd-xbee-solar-client-hardware-intake-audit-to-hardware-qa.md](../handoffs/0131-remote-lcd-xbee-solar-client-hardware-intake-audit-to-hardware-qa.md)

## Decision

Decision: accept the parent repo records-only hardware intake audit. The lane
remains identity-open and bench-closed. Next gate: collect source-backed
identity intake inside the private `rlxsc-*` submodules, prioritizing cell,
BMS/protection, charger/power path, panel, fuse/protection, enclosure, and
current-limit evidence before board/interface or XBee bench action.
