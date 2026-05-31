# PF0530H BBS LCD Menu Handoff To QA

## Summary

PF0530H is flashed and separately verify-flashed on the four-relay KY-040 COM6
lineage. It combines PF0530G LCD init/probe diagnostics with the PF0530F
GPIO13/GPIO14/GPIO32 input-only encoder loop and keeps the XBee bridge closed.

## QA Focus

- Confirm the active task is `fr_lcd_bbs_menu_task`, not the diagnostic-only
  task.
- Confirm required proof strings are source-visible: `PF0530H BBS_LCD_READY`,
  `BBS_LCD_RENDER`, `BBS_MENU_HB`, `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- Confirm nine static/simulated BBS pages render only local status text and
  closed-surface labels.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with internal pullups and no
  relay GPIO, relay-expander, XBee/RF, MicroSD/TFT, erase, or serial-write
  path is opened.
- Confirm the live evidence packet:
  `research/bench-records/xbee-readonly/local-ky040-pf0530h-bbs-lcd-menu-live-20260531T020501Z/`.
- Next QA focus is user visual confirmation, page changes on rotation,
  encoder direction, and pushbutton `BBS_MENU_SELECT` proof.

## Boundary

This handoff does not authorize additional live flash, serial-write expansion,
XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
