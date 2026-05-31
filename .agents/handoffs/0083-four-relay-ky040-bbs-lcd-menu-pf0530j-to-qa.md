# PF0530J BBS LCD Menu Handoff To QA

## Summary

PF0530J supersedes PF0530I. PF0530I split input polling from LCD rendering but
its first live monitor showed repeated task-watchdog backtraces because the
higher-priority input task could yield with a zero-tick delay. PF0530J keeps the
split input/render design, changes the poll interval to 10 ms, and adds a
minimum-one-tick delay helper.

Status update: PF0530J live flash and verify succeeded, and its monitor showed
no watchdog/backtrace/panic markers, but it captured no encoder/button input
proof. PF0530J is superseded by PF0530K for interrupt-queued input proof.

## QA Focus

- Confirm the active firmware ID is `PF0530J`.
- Confirm required proof strings are source-visible: `PF0530J BBS_LCD_READY`,
  `BBS_INPUT_READY`, `ENC_RAW`, `ENC_EV`, `BBS_LCD_RENDER`, `BBS_MENU_HB`,
  `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- Confirm `FR_MENU_POLL_MS 10` and `fr_delay_ticks_at_least_one()` are present.
- Confirm `BBS_LCD_RENDER` includes `rows`, `seq`, `dur_ms`, and `reason`
  fields, and that `FR_MENU_REFRESH_MS 250` is gone.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with internal pullups and no
  relay GPIO, relay-expander, XBee/RF, MicroSD/TFT, erase, or serial-write path
  is opened.
- If live gate completes, confirm the evidence packet has no watchdog,
  backtrace, panic, crash, or closed-surface markers and includes post-fix
  `BBS_MENU_STEP` and `BBS_MENU_SELECT` proof if user actuation was captured.

## Boundary

This handoff does not authorize additional live flash, serial-write expansion,
XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
