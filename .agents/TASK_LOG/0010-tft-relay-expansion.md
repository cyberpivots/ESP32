# Task 0010 - TFT Relay Expansion Revision

## Task

- ID: 0010
- Owner role: Architect, Hardware, Firmware, QA
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Implement the revised TFT plus relay expansion plan: keep the Open-Smart
R61509V TFT planning branch, reject CD74HC4067 as a direct relay-output surface,
and move relay pin relief to a latched GPIO expander plus verified driver-stage
path.

## Scope

Included:

- Source-index and source-ledger updates for TFT, mux, GPIO expander, and
  relay-driver planning sources.
- Project architecture, pin plan, firmware task model, web contract, protocol,
  safety, build, prototype, and bench-runbook updates.
- Static admin HMI mock-state support for `relayExpander` and `mux` health.
- Hardware planning profiles for Open-Smart R61509V, CD74HC4067,
  TCA9555/MCP23017, and TPIC6B595.
- Public Pages allowlist and site-data updates for the new expansion package.

Excluded:

- Firmware implementation files, framework project files, live ESP32 flashing,
  TFT wiring, relay-expander wiring to relay inputs, relay switching, XBee
  setting writes, and mains/load wiring.

## Sources

- `SRC-TI-CD74HC4067`
- `SRC-TI-TCA9555`
- `SRC-ESPRESSIF-MCP23017-COMPONENT`
- `SRC-TI-TPIC6B595`
- `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`
- `SRC-LCDWIKI-R61509V-MRB2802`
- Existing project sources cited in the edited package files.

## Decisions

- CD74HC4067 is allowed only for slow input routing and is rejected for direct
  relay state holding, TFT bus reduction, or safety-critical output selection.
- Relay output pin relief uses the planned
  `ESP32 I2C -> MCP23017/TCA9555 -> verified driver stage -> relay module input`
  branch.
- TFT touch and mux-derived inputs remain UI intents only; relay state changes
  still pass through `relay_manager` and `safety_supervisor`.
- Expander init/write/readback failure keeps `hardwareGateClosed=false` and maps
  relay commands to `hardware_gate_open`.

## Validation

- `python3 scripts/verify_scaffold.py` -> pass.
- `python3 -m json.tool site/github-pages/site-data.json` -> pass.
- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js` -> pass.
- `git diff --check` -> pass.
- `python3 scripts/build_github_pages.py` -> pass, built 45 public files.
- All referenced `SRC-*` IDs in checked text files resolve to
  `knowledge-base/source-index.md` -> pass.

## Handoff

Next owners: Hardware, Firmware, QA.

Next actions:

- Hardware: identify exact Open-Smart R61509V module, CD74HC4067 breakout,
  MCP23017/TCA9555 expander board, and relay module input behavior.
- Firmware: keep future implementation aligned to `relay_expander` and
  `mux_scan` task contracts without adding framework files until the
  implementation gate is open.
- QA: prove mux inputs with ADC1 test voltages and expander outputs on LEDs or a
  logic analyzer before any relay-module input connection.

Unresolved gaps remain recorded in `research/known-gaps.md`.
