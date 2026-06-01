# PF0530M BBS LCD Menu Handoff To QA

PF0530M is a non-live source/test continuation after the PF0530L LCD visual,
glyph, serial/menu, and electrical gate was accepted. It does not replace the
flashed PF0530L evidence. It turns the LCD/menu surface into a more useful BBS
operator UI and adds host-side state-machine tests before any future hardware
action.

## Review Focus

- Confirm the active firmware ID is `PF0530M`.
- Confirm `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with pullups and no relay/XBee
  GPIO output path is added.
- Confirm LCD writes remain display-only on GPIO21/GPIO22.
- Confirm `BBS_INPUT_READY` advertises `actions=detail,edit,back`.
- Confirm operational page strings are source-visible: `BBS FIELD STATUS`,
  `BRIDGE LOCAL CLOSED`, `DIAG ERRORS:0`, and `GAUGE STATUS`.
- Confirm only `BARS` row 3 and `GAUGE` row 1 enter edit mode.
- Confirm host tests cover step/select behavior, long-press back/home behavior,
  page wrapping, glyph-bank selection, and 20-character display bounds.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- Broader source/docs/agent/data/verify scaffold validation, full scaffold
  audit unittest discovery, `git diff --check`, and the ESP-IDF v6.0.1
  no-flash build passed after record/index updates. See the task log for the
  exact command list.

## Closed Surfaces

- No COM6 access, flash, monitor, or serial write.
- No XBee/RF transmit or configuration write.
- No ESP-NOW live runtime or bridge ABI expansion.
- No firmware HTTP, SoftAP, WebSocket, or persistent configuration endpoint.
- No relay GPIO or relay-expander write.
- No MicroSD/TFT action.
- No wiring, DMM, current measurement, load, mains, erase, commit, push,
  publication, or release.
