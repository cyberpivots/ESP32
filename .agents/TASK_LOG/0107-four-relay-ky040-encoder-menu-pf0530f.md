# Task 0107 - Four Relay KY-040 Encoder Menu PF0530F

## Status

- Status: Tier 2 repo-only firmware/docs/tests implementation.
- Date: 2026-05-30.
- Live bench status: closed. No COM6 flash, monitor, serial write, XBee/RF,
  relay/load/mains, MicroSD, TFT, erase, commit, or push authority was used.

## Routing packet

- Verified facts: PF0530E r5 recorded user-confirmed GPIO13 `CLK`, GPIO14 `DT`,
  and GPIO32 `SW` input changes with no writes and no watchdog/panic/backtrace
  scan hits. Current pre-mutation firmware still booted the PF0530E serial
  pintrace branch and the inactive LCD menu path forced `page = 0`.
- Assumptions: GPIO13/GPIO14/GPIO32 remain the intended KY-040 menu-proof
  wiring, KY-040 `+` remains on ESP32 3V3, and closed surfaces remain closed.
- Unknowns: during the later Task 0108 Tier 3 gate, PF0530F flashed and
  verify-flash matched on COM6 but live menu acceptance was blocked by
  `PF0530F LCD_INIT_FAILED`. Exact pullups, rail margin, rotation direction,
  recovered LCD behavior, and final hardware acceptance remain open.
- Selected tier: Tier 2.
- Owner role: Firmware, with Hardware, QA, Agent Operations, and Live Bench
  lenses.
- Evidence need: PF0530E r5 task/source evidence, ESP-IDF GPIO source coverage,
  current source inspection, and repo validation.
- Mutation boundary: `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  firmware audit/tests, project docs/status/source records, source index, and
  this task log.
- Reviewer quorum: Agent Operations weight 5, QA weight 3, Evidence Records
  weight 3, Live Bench weight 5, Firmware/Hardware weight 3. Weighted approval
  19/19, no P1/P2 blockers after audit and record-continuity conditions.
- Gate authority: repo-only mutation. No Tier 3 authority.
- Trust boundary: project-local hooks are advisory; source-backed records and
  explicit live-gate authority remain authoritative.

## Implementation

- Changed firmware ID to `PF0530F`.
- Removed the PF0530E serial pintrace boot branch from the current diagnostic
  image and booted the LCD/menu task while keeping
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- Kept GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with internal
  pullups and pulldowns disabled.
- Added 2 ms A/B polling with three stable samples before accepting a level.
- Kept the 16-state quadrature table and four transitions per accepted menu
  step.
- Counted invalid A/B jumps and reset the transition accumulator on invalid
  transitions.
- Added 30 ms switch debounce and a 150 ms switch guard window on press/release.
  During the guard, raw A/B changes are counted and printed as suppressed and do
  not move the menu.
- Added `printf` proof lines for `MENU_READY`, `ENC_EV`, `MENU_STEP`,
  `MENU_SELECT`, `AB_SUPPRESS`, `AB_INVALID`, and `MENU_HB`.
- Updated the LCD proof pages: `ENCODER`, `RELAY LOCK`, `COMMS LOCK`, `SAFETY`,
  and `COUNTERS`. LCD line 0 always shows `PF0530F`, page, and signed position.
- Updated firmware audit/unit-test expectations to fail if the build remains in
  PF0530E serial-pintrace mode or if the old `fr_menu_poll` page lock returns.
- Preserved the PF0530E serial pintrace helper and r5 evidence as historical
  proof.

## Validation plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
- ESP-IDF v6.0.1 no-flash build for
  `firmware/projects/four-relay-xbee-wifi` if the local toolchain is available.

## Validation results

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
  (`test_relay_safety`, `test_http_api_contracts`, `test_storage_contracts`,
  and `test_xbee_frame_codec`).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
  (49 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.
- PASS: ESP-IDF v6.0.1 no-flash build with
  `idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530f-menu-build build`.
- Build note: the first no-flash build exposed a source-visible
  `-Werror=format-truncation` issue in the LCD encoder level line. The line was
  tightened to fixed-width `0`/`1` characters, the firmware audit/unit-test
  markers were updated, and the no-flash build then passed.
- Live validation was not run in this Tier 2 task. Later Task 0108 flashed and
  verify-flash matched PF0530F on COM6, but live menu acceptance was blocked by
  `PF0530F LCD_INIT_FAILED`.

## Decision footer

- Decision: PF0530F repo-only firmware/docs/tests implementation complete.
  A later Tier 3 COM6 gate is recorded in Task 0108: write/verify passed, but
  live menu acceptance is blocked by `PF0530F LCD_INIT_FAILED`.
- Next gate: diagnose `PF0530F LCD_INIT_FAILED` before another live menu proof;
  any further flash or monitor action needs fresh authority, rollback/recovery
  review as applicable, and closed-surface review.
- Owner: Firmware for source, QA for validation, Live Bench for any future COM6
  gate.
- Evidence: PF0530E r5 transcript/task/source evidence, ESP-IDF GPIO source
  coverage, current `main.c`, and repo validation.
- Approved mutation boundary: firmware menu-proof code, focused audits/tests,
  docs/source/task/status records, and repo-only validation.
- Authority limits: no flash, monitor, serial write, wiring mutation, XBee/RF,
  relay GPIO write, relay-expander write, relay/load/mains, MicroSD, TFT, erase,
  commit, or push until separately authorized.
