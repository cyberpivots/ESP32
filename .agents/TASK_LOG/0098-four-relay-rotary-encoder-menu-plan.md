# Task 0098 - Four Relay Rotary Encoder Menu Plan

## Task

- ID: 0098
- Owner role: Hardware with Firmware and QA lenses
- Status: Completed documentation-only plan
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: accepted LCD display-status proof uses GPIO21/GPIO22. Source
  ID: `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- Verified facts: accepted COM6 XBee bridge proof uses UART2 GPIO17/GPIO16.
  Source ID: `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Verified facts: ESP32 GPIO source coverage exists for strapping pins,
  flash-related pins, and input-only pins. Source ID: `SRC-ESP-IDF-GPIO`.
- Verified facts: PEC11R is candidate/reference-only encoder family coverage
  and does not verify the exact encoder. Source ID: `SRC-BOURNS-PEC11R`.
- Assumptions: the user intent is to record a future encoder connection plan
  for LCD menus, not to perform wiring, firmware, flash, serial, RF, relay, or
  load/mains work.
- Unknowns: exact encoder/module, PPR/detents, switch option, pullups,
  debounce, voltage, board/shield continuity, rail margin, and boot-pin impact.
- Selected tier: Tier 1 bounded hardware planning/docs mutation.
- Owner role: Hardware, with Firmware and QA lenses.
- Evidence need: source-index-backed facts, explicit unresolved gaps, and
  documentation-only stop gates.
- Mutation boundary: four-relay documentation/status records plus task/source
  records only. No source code, firmware config, hook/config, live bench,
  serial, radio, flash, relay/load/mains, or wiring mutation.
- Validation plan: documentation/source audits, agent-process audit, scaffold
  verifier, and `git diff --check`.

## Goal

Add a source-backed future rotary encoder plan for LCD menu navigation without
disturbing the accepted LCD GPIO21/GPIO22 path, the accepted XBee bridge
GPIO17/GPIO16 path, or relay candidates GPIO25/GPIO26/GPIO27/GPIO33.

## Scope

Included:

- Documentation-only encoder plan.
- Pin-plan and power/safety gate updates.
- Development status, triage, known-gap, docs-index, source-index, and source
  ledger records.

Excluded:

- Encoder wiring.
- Final encoder GPIO assignment.
- Firmware implementation.
- Build, flash, erase, monitor, or serial writes.
- XBee/RF action or XBee setting writes.
- Relay, load, or mains work.

## Sources

- `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`
- `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`
- `SRC-ESP-IDF-GPIO`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-BOURNS-PEC11R`
- `SRC-LOCAL-FOUR-RELAY-ROTARY-ENCODER-MENU-PLAN-2026-05-30`

## Decisions

- Keep LCD pins GPIO21/GPIO22 reserved.
- Keep XBee bridge pins GPIO17/GPIO16 reserved.
- Keep GPIO25/GPIO26/GPIO27/GPIO33 reserved as relay candidates.
- Do not assign final encoder pins until exact board/shield continuity and
  boot behavior are checked.
- Treat future encoder events as UI intents only:
  `rotate_left`, `rotate_right`, `select`, and optionally `long_press` or
  `back`.

## Validation

Passed checks:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

## Handoff

No immediate handoff is required. Future owner is Hardware for encoder identity,
pinout, pullup-voltage, continuity, rail-margin, and boot-risk evidence before
any wiring. Firmware remains the later owner for input-only debounce and
UI-intent implementation after a separate mutation gate.
