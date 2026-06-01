# Four Relay KY-040 BBS LCD Menu PF0530O Real-Menu Calibration

Status: PF0530O real-menu calibration built, flashed to COM6, verify-flashed,
and read-only monitored; encoder/button interaction remains unaccepted pending
user visual/input report

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 for firmware/menu source calibration, followed by the
  user-authorized Tier 3 COM6 write/verify/read-only monitor gate.
- Owner role: Firmware owner with LCD UX, Hardware-safety, QA, and Evidence
  Records lenses.
- Evidence need: PF0530N attended retry transcript counts, source diff,
  ESP-IDF no-flash build result, artifact hashes, rollback backup, COM6
  write-flash transcript, separate verify-flash transcript, read-only monitor
  transcripts, marker scans, cleanup proof, and this task/source record.
- Mutation boundary: firmware/menu source, generated menu metadata, records,
  docs index, and COM6-only PF0530O write/verify/read-only monitor after the
  user safe-state gate. No erase-flash, serial command writes, XBee/RF,
  relay/load/mains, wiring, DMM/current, persistent config, commit, or push.
- Reviewer disposition: local role-lens quorum approved 17/17 for the bounded
  source calibration and the named COM6 Tier 3 PF0530O write/verify/read-only
  monitor gate after the user provided `SAFE STATE VERIFIED` and
  `Allow flash on COM6`. Subagents were not spawned because the active tool
  contract requires an explicit user request for subagents.

## Verified Facts

- The user explicitly required the real LCD menu to be used for review and
  rejected dummy, simulated, or mock acceptance.
- The PF0530N attended retry captured 489 `ENC_RAW`, 316 `ENC_EV`, 12
  `BBS_MENU_STEP`, five short `BBS_MENU_SELECT`, zero long
  `BBS_MENU_SELECT`, 129 `BBS_LCD_RENDER`, 75 `BBS_MENU_HB`, and zero
  crash/unsafe markers.
- PF0530O sets the active firmware ID to `PF0530O`.
- GPIO13/GPIO14/GPIO32 remain encoder inputs. LCD remains display-only on
  GPIO21/GPIO22. The bridge, XBee/RF, relay, load, mains, and serial-write
  surfaces remain closed.
- PF0530O changes encoder calibration to `FR_ENCODER_TRANSITIONS_PER_STEP=1`,
  `FR_ENCODER_AB_STABLE_SAMPLES=2`, `FR_ENCODER_SW_GUARD_MS=75`, and
  `FR_ENCODER_LONG_PRESS_MS=650`.
- PF0530O moves quadrature decoding to the stable-level change path instead
  of decoding before the stable A/B samples are updated.
- PF0530O disables automatic menu cycling at boot with
  `FR_MENU_AUTO_CYCLE_ENABLED=0`, so the LCD menu remains operator-controlled.
- PF0530O readiness output reports the real-menu calibration constants in
  `BBS_INPUT_READY`.
- Visible menu text no longer uses `Mesh simulator mode`, `Edit demo value`,
  `gauge_demo`, or `MESH sim`; the firmware/menu sources now use runtime/local
  wording and the `gauge` glyph-bank name.
- The COM6 live gate captured a full 4 MB rollback backup before programming.
- Windows esptool write-flash completed for the PF0530O bootloader, partition
  table, and app offsets, with per-segment hash verification.
- A separate Windows esptool verify-flash pass matched all three PF0530O
  artifacts.
- A reset boot monitor captured `PF0530O BBS_LCD_READY`,
  `PF0530O BBS_INPUT_READY`, `LCD_INIT_OK addr=0x27`, `auto_cycle=off`,
  `cal=real-menu-v1`, `step=1`, `stable=2`, `sw_guard_ms=75`, and
  `long_ms=650`.
- The attended 150 second read-only monitor captured 75 `BBS_MENU_HB`, 75
  `BBS_LCD_RENDER`, 75 `BBS_CURSOR`, zero crash/unsafe markers, and zero bad
  20-character render row lengths.
- The attended monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- Linux and Windows cleanup checks found no lingering COM6/esptool/Python
  monitor process after the run.

## Assumptions

- One accepted quadrature transition should map to one intended tactile menu
  step for the current encoder after PF0530N showed sparse menu movement under
  attended actuation.
- If the live PF0530O review shows double-stepping, the next source-only
  calibration should raise `FR_ENCODER_TRANSITIONS_PER_STEP` rather than
  changing pins or hardware.
- COM6 remained connected to the intended target through write/verify/monitor.
- If the user confirms they operated the encoder/button during the attended
  PF0530O window, the zero input events should be treated as a physical/input
  capture gap before further debounce or transitions-per-step tuning.

## Unknowns

- User visual report for the PF0530O LCD menu after flash is still pending.
- Whether physical encoder/button actuation occurred during the 150 second
  attended monitor is not confirmed in this record.
- Physical direction, per-detent behavior, quick-rotation behavior, short
  button behavior, and long-button behavior under PF0530O remain unaccepted
  because the attended transcript captured no input events.

## Validation

- PASS: `git diff --check`
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530o-real-menu-cal-build build`
- PASS: build generated `/tmp/esp32-pf0530o-real-menu-cal-build/four_relay_xbee_wifi.bin`
  size `0x2d390`; smallest app partition is `0x100000`, leaving `0xd2c70`
  bytes free.
- Artifact hashes:
  - bootloader:
    `7c4061b011b1d8812653906ca2f9cb95fee1ca687f057119bacb8a508f3f9dcb`
  - partition table:
    `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  - app:
    `301e6bed800d0d644a32da6512efadf08f14b540139c4e78a7b385e054f9db7b`
- PASS: COM6 full rollback backup captured before programming; backup hash is
  retained in the ignored local evidence directory.
- PASS: Windows esptool write-flash completed for PF0530O bootloader,
  partition table, and app artifacts.
- PASS: Separate Windows esptool verify-flash matched all three PF0530O
  artifacts.
- PASS: reset boot monitor proved PF0530O runtime readiness and LCD init on
  the real device.
- PASS: attended read-only monitor proved continued LCD rendering and
  heartbeats with zero crash/unsafe markers and zero bad render-row lengths.
- GAP: attended monitor did not prove encoder/button interaction because it
  captured zero input events.
- NOT RUN: host simulator, mock, or unit tests, per user instruction that real
  firmware/menu operation is the acceptance surface.

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `docs/projects/four-relay-xbee-wifi/rotary-encoder-menu-plan.md`
- `docs/prompt/comprehensive-bench-development-process.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `research/development-status-ledger.md`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-cal.md`
- `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530o-live.md`
- `.agents/handoffs/0094-four-relay-ky040-bbs-lcd-menu-pf0530o-input-report-to-hardware-qa.md`
- `docs/index.md`

## Next Gate

Ask the user what the physical LCD did during the PF0530O attended window and
whether they rotated/pressed the encoder during the timed cues. If the user
confirms actuation occurred and the LCD did not respond, the next gate should
focus on physical/input capture evidence for GPIO13/GPIO14/GPIO32 before any
more debounce or transitions-per-step tuning.

## Decision Footer

Decision: `programmed_but_input_gap_pending_user_report`. Next gate: user
visual/input report for PF0530O, then a COM6 read-only physical/input capture
gate if the user confirms actuation occurred without LCD/menu response. Owner:
Firmware live-gate owner with LCD UX, Hardware-safety, QA, and Evidence
Records lenses. Evidence: PF0530N attended retry transcript counts, PF0530O
source diff, ESP-IDF no-flash build, artifact hashes, rollback backup, COM6
write-flash success, separate verify-flash digest matches, PF0530O reset boot
monitor, PF0530O attended monitor, marker scans, cleanup proof, source ledgers,
and this task record. Approved mutation boundary for this task: PF0530O
source/build/records and COM6-only write/verify/read-only monitor. Authority
limits: no erase-flash, serial command writes, XBee/RF, relay/load/mains,
wiring, DMM/current, persistent configuration, commit, or push.
