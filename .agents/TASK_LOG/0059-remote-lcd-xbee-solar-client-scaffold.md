# Task 0059: Remote LCD XBee Solar Client Scaffold

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-26

## Goal

Create a framework-neutral, documentation-only scaffold for a new project lane
named `remote-lcd-xbee-solar-client`.

## Verified facts

- The initial scaffold created parent documentation and hardware profile stubs.
- Follow-on task 0060 creates real private Git submodules for the same lane.
- Existing XBee source/profile coverage for `XBP9B-DPUT-001` is reused.
- New unsupported hardware classes are documented as candidate/reference-only
  sources or unresolved gaps.
- No firmware source, framework files, XBee writes, battery/solar bench actions,
  wiring instructions, or accepted pin assignments are added.

## Assumptions

- The project is distinct from `four-relay-xbee-wifi`.
- The first pass used internal module lanes; current submodule status is tracked
  by task 0060.

## Unknowns

- Exact LCD module, encoder part, ESP32 board, 18650 cell, BMS board, solar
  panel, charger module, XBee carrier, antenna, fuse/protection, and enclosure.
- Power budget, pin plan, firmware framework, radio settings, and live proof
  status.

## Implementation

- Added project docs under
  `docs/projects/remote-lcd-xbee-solar-client/`.
- Added hardware profile stubs under `hardware-profiles/displays/`,
  `hardware-profiles/inputs/`, `hardware-profiles/power/`, and
  `hardware-profiles/esp32/`.
- Added source ledger and source-index coverage.
- Updated docs index, device matrix, known gaps, and research triage status.

## Validation

- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0048-remote-lcd-xbee-solar-client-to-hardware-qa.md](../handoffs/0048-remote-lcd-xbee-solar-client-to-hardware-qa.md).

## Stop gates

Do not start firmware implementation, framework selection, XBee writes, API
transmit frames, ESP32 DIN/DOUT wiring, battery charging, solar connection,
battery pack assembly, or power-path wiring from this scaffold.
