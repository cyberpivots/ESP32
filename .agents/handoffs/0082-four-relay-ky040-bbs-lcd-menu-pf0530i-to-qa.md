# PF0530I BBS LCD Menu Handoff To QA

## Summary

PF0530I is the bounded fix for the PF0530H symptom where encoder rotation and
button presses had no visible LCD menu effect. PF0530I keeps the XBee bridge
closed, keeps GPIO13/GPIO14/GPIO32 input-only, keeps LCD writes display-only,
splits input polling into a higher-priority task, and makes LCD rendering
dirty-row driven instead of periodic full-page redraws.

## QA Focus

- Confirm the active task is `fr_lcd_bbs_menu_task`, with input polling in
  `fr_menu_input_task`.
- Confirm required proof strings are source-visible: `PF0530I BBS_LCD_READY`,
  `BBS_INPUT_READY`, `ENC_RAW`, `ENC_EV`, `BBS_LCD_RENDER`,
  `BBS_MENU_HB`, `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- Confirm `BBS_LCD_RENDER` includes `rows`, `seq`, `dur_ms`, and `reason`
  fields, and that `FR_MENU_REFRESH_MS 250` is gone.
- Confirm nine static/simulated BBS pages render only local status text and
  closed-surface labels.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with internal pullups and no
  relay GPIO, relay-expander, XBee/RF, MicroSD/TFT, erase, or serial-write
  path is opened.
- If live gate completes, confirm the evidence packet contains fresh identity,
  rollback, staged hashes, write-flash, separate verify-flash, read-only
  monitor, transcript scan, `writes_sent=false`, and post-fix `BBS_MENU_STEP`
  and `BBS_MENU_SELECT` proof.

## Boundary

This handoff does not authorize additional live flash, serial-write expansion,
XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
