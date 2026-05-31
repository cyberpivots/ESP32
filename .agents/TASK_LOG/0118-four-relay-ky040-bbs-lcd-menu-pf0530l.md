# Four Relay KY-040 BBS LCD Menu PF0530L

Status: PF0530L source validated, written, verify-flashed, and monitor-scanned for user testing

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Routing

- Selected tier: Tier 3 because the user's priority goal is live flashing for
  user testing.
- Owner role: Lead LCD Menu Developer with Firmware, Live Bench, Hardware-risk,
  QA, Evidence Records, and Governance lenses.
- Evidence need: PF0530K live record, source diff, firmware scaffold tests,
  repo validation, ESP-IDF v6.0.1 no-flash build, source records, fresh COM6
  identity, rollback backup, recovery command, staged hashes, write-flash log,
  separate verify-flash log, read-only monitor transcript, transcript scan, and
  cleanup proof.
- Mutation boundary: PF0530L firmware source, firmware tests/audits,
  firmware/project documentation, ESP-NOW LCD menu plans, source-index/source
  ledger, this task log, QA handoff, and private PF0530L bench evidence.
- Live boundary: COM6-only identity, backup, flash, verify, and read-only
  monitor. No relay, XBee/RF, ESP-NOW runtime, wiring, load, mains, erase,
  SoftAP/browser runtime, persistent configuration, TFT, or MicroSD action.

## Verified Facts

- PF0530K is flashed/verify-flashed for user testing but is not accepted as
  interactive because its monitor captured zero `ENC_RAW`, zero `ENC_EV`,
  zero `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- PF0530L source now uses firmware ID `PF0530L`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32 input-only with
  internal pullups, and keeps LCD writes display-only on GPIO21/GPIO22.
- PF0530L keeps the PF0530K any-edge interrupt queue with
  `FR_ENCODER_EVENT_QUEUE_DEPTH 64` and `FR_ENCODER_IRQ_DRAIN_LIMIT 32`.
- PF0530L adds local page/row/detail/edit modes, software cursor/DDRAM
  tracking, dirty-cell metadata, five named eight-slot glyph banks, custom
  bar/chart/digit/gauge demo pages, and a seven-second auto-demo page cycle.
- PF0530L same-session COM6 identity matched ESP32-D0WDQ6 MAC
  `78:e3:6d:0a:90:14`, 4 MB flash, and 3.3 V flash strap.
- PF0530L write-flash and separate verify-flash passed on COM6, and the
  read-only monitor captured `LCD_INIT_OK`, `PF0530L BBS_LCD_READY`,
  `BBS_INPUT_READY`, all 13 page names, all five glyph banks, 77
  `BBS_LCD_RENDER`, 21 `BBS_MENU_AUTO`, and 74 `BBS_MENU_HB` lines with no
  watchdog/backtrace/panic/LCD-init-failure or unsafe-open markers.

## Assumptions

- The user's `LIVE FLASH AUTHORIZED` and bench `SAFE` statement applies to a
  COM6-only PF0530L flash/verify/read-only-monitor gate.
- The auto-demo path is a visual test surface only. It does not replace
  physical encoder/button acceptance proof.
- Browser mirror records are design inputs only; this task does not open a
  firmware HTTP, SoftAP, WebSocket, persistent config, or network gate.

## Unknowns

- Physical LCD readability, custom glyph appearance, encoder direction, button
  behavior, boot-held switch behavior, rail margin, LCD backpack pullup voltage,
  and attended interaction proof remain unproven.
- The PF0530L monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`, so physical interaction remains
  pending user testing.

## Reviewer Quorum

- Coordinator/Architecture-risk, weight 5: conditional approve for PF0530L
  source mutation and COM6-only live gate after validation; no broader lanes.
- Live Bench, weight 5: approve gate shape; block live-result acceptance until
  fresh identity, rollback, hashes, flash/verify, monitor, interaction proof
  where claimed, and cleanup proof exist.
- QA, weight 3: approve bounded mutation; block live flash until PF0530L
  source/docs/tests/build records and same-session evidence exist.
- Evidence Records, weight 2: approve PF0530L source-record path; block
  pre-populated live-success facts before evidence exists.
- Governance, weight 2: confirm Tier 3 and named boundary.

Weighted disposition: 17/17 conditional pass for source mutation and a named
PF0530L COM6-only live gate after validation. No P1/P2 blocker remains inside
the named mutation boundary; live acceptance remains fail-closed until evidence
exists.

## Implementation

- Changed active firmware ID from `PF0530K` to `PF0530L`.
- Added local menu modes `page_browse`, `row_browse`, `detail`, and
  `edit_lab`; rotate changes page/row/value by mode, short press advances or
  commits local mode, and long press backs out/home.
- Added five named eight-slot HD44780 glyph banks: `core_status`,
  `horizontal_bar`, `vertical_chart`, `big_digits`, and `gauge_demo`.
- Added firmware-side cursor/DDRAM metadata and dirty-cell render metadata to
  `BBS_LCD_RENDER`.
- Added widget pages for bars, vertical charts, big digits, and gauge demo.
- Added `BBS_MENU_AUTO` auto-demo cycling so user testing can inspect pages
  even if physical encoder events still do not reach GPIO13/GPIO14/GPIO32.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `git diff --check`
- ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530l-build build`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py` (4 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (18 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (18 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (49 tests)
- PASS: `git diff --check`
- PASS: ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-four-relay-xbee-wifi-pf0530l-build`, app size `0x2ba60` with
  `0xd45a0` bytes free in the 1 MiB factory app partition.
- PASS: Post-live record audit rerun:
  `scripts/scaffold_audit_firmware.py`, `scripts/scaffold_audit_sources.py`,
  `scripts/scaffold_audit_docs.py`, `scripts/scaffold_audit_agent_process.py`,
  `scripts/verify_scaffold.py`,
  `python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`, and
  `git diff --check`.

## Live Gate Evidence

- Evidence directory:
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/`
- PASS: COM6 identity matched ESP32-D0WDQ6 MAC `78:e3:6d:0a:90:14`,
  detected 4 MB flash, and detected 3.3 V flash strap.
- PASS: Full 4 MB rollback backup saved with SHA256
  `82c99ba16940144f1a3eac1fdceb767f9208c5c9aff76e30623ab44ed08a230f`.
- PASS: Recovery command saved in `pf0530l-recovery-command.txt`.
- PASS: Staged artifact hashes saved in `pf0530l-artifact-sha256.txt`.
- PASS: COM6 write-flash and separate verify-flash both succeeded.
- PASS: Read-only monitor captured `writes_sent=false`, `LCD_INIT_OK`,
  `PF0530L BBS_LCD_READY`, `BBS_INPUT_READY`, six `BBS_GLYPH_BANK`, 77
  `BBS_CURSOR`, 77 `BBS_LCD_RENDER`, 21 `BBS_MENU_AUTO`, and 74 `BBS_MENU_HB`
  lines. The scan covered all 13 page names and all five glyph banks.
- PASS: Transcript scan found no watchdog/backtrace/panic/LCD-init-failure or
  unsafe-open markers.
- PASS: Cleanup proof found no remaining monitor/esptool/idf.py monitor process.
- GAP: The unattended monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`; PF0530L is flashed for user
  visual testing but not accepted as proven physically interactive.

## Closed Surfaces

No XBee/RF transmit or configuration write, ESP-NOW runtime, relay GPIO write,
relay-expander write, MicroSD/TFT action, wiring mutation, load, mains, erase,
firmware HTTP/SoftAP/WebSocket, persistent configuration endpoint, commit, or
push is opened by this gate.
