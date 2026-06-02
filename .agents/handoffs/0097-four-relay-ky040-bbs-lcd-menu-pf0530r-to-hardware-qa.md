# PF0530R Detent Calibration To Hardware QA

Status: PF0530R flashed/verified; readiness OK; input behavior unaccepted

Date: 2026-06-01

## Context

PF0530Q was written and separately verify-flashed on COM6 with LCD/input
readiness proof. The user later reported that PF0530Q works but is not stable.
PF0530R is now the latest written and separately verify-flashed COM6 image.

## Verified Facts

- PF0530R firmware identity/source metadata:
  `PF0530R`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01`.
- PF0530R keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with
  pullups.
- PF0530R keeps LCD GPIO21/GPIO22 display-only and keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- PF0530R uses 8 ms A/B hold, 15 ms quiet time, detent A/B `3`, two accepted
  transitions per step, and 90 ms step lockout.
- PF0530R adds detent return/step/partial telemetry and
  `ENC_FILTER reason=detent_partial`.
- Focused tests, generated-menu freshness, firmware audit, scaffold
  verification, `git diff --check`, and ESP-IDF no-flash build passed before
  the flash.
- The user supplied same-session PF0530R COM6 Tier 3 authority with
  `SAFE STATE CONFIRMED` and `LIVE FLASH APPROVED`.
- COM6 identity was refreshed before write as ESP32-D0WDQ6 with 4 MB detected
  flash and 3.3 V flash-voltage strap evidence.
- A full 4 MB rollback backup was captured and hashed before write; recovery
  command is retained in ignored local evidence.
- PF0530R write-flash and separate verify-flash passed for bootloader,
  partition table, and app.
- Reset boot monitor captured `LCD_INIT_OK addr=0x27`,
  `PF0530R BBS_LCD_READY`, `PF0530R BBS_INPUT_READY`, `cal=detent-v4`,
  `ab_ms=8`, `quiet_ms=15`, `step_lockout_ms=90`, and `detent=3`.
- The 150 second attended read-only monitor completed with `writes_sent=false`,
  zero bad render rows, zero crash/unsafe markers, and continued render/
  heartbeat output.
- The combined scan reported `readiness_ok: true`,
  `no_crash_or_unsafe: true`, `render_rows_ok: true`, and
  `interaction_ok: false`.
- The live transcripts captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero `ENC_FILTER`.

## Assumptions

- The PF0530Q instability is likely bounce/detent-boundary related.
- PF0530R should be evaluated with slow single-detent turns first before fast
  rotation.

## Unknowns

- Whether PF0530R improves physical stability under actual actuation.
- Whether the step lockout is too conservative for fast rotation.
- Direction and button acceptance under PF0530R.

## Current Live Evidence

- Source ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530r-live.md`
- Ignored local evidence:
  `<redacted-local-evidence-dir>/`

## Next Acceptance Need

PF0530R is already flashed. Hardware QA should treat it as readiness-proven but
not interaction-accepted. The next useful evidence is actual physical actuation:
operator report and/or read-only serial monitor showing raw encoder/button
events, decoded events, menu movement, button select events, readable LCD
response, and no runaway/double-step pattern beyond tolerance.

## Suggested Interaction Cues

- idle baseline,
- 5 slow clockwise detents,
- 5 slow counterclockwise detents,
- 10 moderate clockwise detents,
- five single-detent pause checks,
- five short presses,
- one long press,
- final idle.

## Acceptance Evidence

Look for `ENC_RAW > 0`, `ENC_EV > 0`, `BBS_MENU_STEP` in both directions,
short and long `BBS_MENU_SELECT`, readable LCD response, no runaway/double-step
pattern beyond tolerance, no bad render rows, and zero crash/unsafe markers.

## Stop Gates

Do not perform another flash, serial writes, XBee/RF writes, relay/load/mains
work, wiring mutation, DMM/current measurement, erase, persistent config,
release, commit, or push without a separate explicit gate. Read-only observation
of the currently flashed PF0530R image is the narrow next evidence path.
