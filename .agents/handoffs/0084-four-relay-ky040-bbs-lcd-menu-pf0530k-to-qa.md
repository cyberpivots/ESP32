# PF0530K BBS LCD Menu Handoff To QA

PF0530K supersedes PF0530J. PF0530J fixed the PF0530I task-watchdog backtrace
symptom, but its first read-only monitor did not capture encoder/button input
events. PF0530K keeps the PF0530J delay fix and adds GPIO any-edge interrupt
queueing for GPIO13/GPIO14/GPIO32, while keeping the XBee bridge and relay
surfaces closed.

## Review Focus

- Confirm the active firmware ID is `PF0530K`.
- Confirm required proof strings are source-visible: `PF0530K BBS_LCD_READY`,
  `BBS_INPUT_READY`, `irq=anyedge queue=64`, `ENC_RAW`, `ENC_EV`,
  `BBS_LCD_RENDER`, `BBS_MENU_HB`, `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with internal pullups and no
  GPIO outputs are added.
- Confirm GPIO interrupts are any-edge only for the encoder inputs and feed a
  queue consumed by the input task.
- Confirm LCD rendering remains dirty-row or slow idle refresh only.
- Confirm `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- If live gate completes, confirm the evidence packet has no watchdog,
  backtrace, panic, guru-meditation, LCD init failure, closed-surface marker,
  or serial-write expansion.

## Closed Surfaces

- No XBee/RF transmit or configuration writes.
- No ESP-NOW runtime.
- No relay GPIO or relay-expander writes.
- No MicroSD/TFT action.
- No wiring, load, mains, erase, commit, or push.
