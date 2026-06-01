# PF0530N BBS LCD Menu Scrolling/XML Handoff To QA

PF0530N is a non-live source/test continuation after PF0530M. It does not
replace flashed PF0530L evidence and does not open any live hardware surface.
It adds build-time XML menu definitions, generated static firmware/simulator
data, scroll-list navigation, selected-row marquee, grouped multi-row items,
and table glyph formatting.

## Review Focus

- Confirm the active firmware ID is `PF0530N`.
- Confirm `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with pullups and no relay/XBee
  GPIO output path is added.
- Confirm LCD writes remain display-only on GPIO21/GPIO22.
- Confirm firmware consumes `bbs_lcd_menu_generated.h` static definitions and
  does not parse XML at runtime.
- Confirm the host generator fails closed for duplicate IDs, bad targets,
  unknown glyph banks, too-wide table rows, unknown tokens, secret-bearing
  fields, DOCTYPE, and external entities.
- Confirm `bbs_lcd_render.v2` exposes selected item, visible item IDs,
  physical indicator row, viewport top line, horizontal scroll offsets, and
  source XML metadata.
- Confirm selected overlong rows marquee at 750 ms hold and 250 ms steps, while
  non-selected overlong rows clip.
- Confirm the `table` glyph bank stays within eight slots and row bytes
  `0..31`, and is not mixed with bar/chart/big-digit/gauge pages.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- Broader source/docs/agent/data/verify scaffold validation, full scaffold
  audit unittest discovery, `git diff --check`, and ESP-IDF v6.0.1 no-flash
  build passed before handoff.
- ESP-IDF v6.0.1 no-flash build generated `four_relay_xbee_wifi.bin` size
  `0x2d3c0`, with `0xd2c40` bytes (82 percent) free in the smallest app
  partition.

## Closed Surfaces

- No COM6 access, flash, monitor, or serial write.
- No XBee/RF transmit or configuration write.
- No ESP-NOW live runtime or bridge ABI expansion.
- No firmware HTTP, SoftAP, WebSocket, or persistent configuration endpoint.
- No relay GPIO or relay-expander write.
- No MicroSD/TFT action.
- No wiring, DMM, current measurement, load, mains, erase, commit, push,
  publication, or release.
