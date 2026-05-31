# LCD BBS Menu Simulator

This host-only simulator renders compact `bbs_lcd_state.v1` snapshots into
four fixed 20-character LCD lines plus an eight-slot HD44780 custom-glyph bank.
It is for ESP-NOW BBS field-console planning only.

The renderer output schema is `bbs_lcd_render.v1`. It adds software cursor
tracking, HD44780 DDRAM row/column metadata, dirty-row/cell metadata, named
glyph banks, and host-rendered widget previews.

## Boundaries

- No hardware access.
- No serial commands.
- No firmware build, flash, erase, monitor, XBee/RF, ESP-NOW runtime, relay,
  TFT, MicroSD, load, mains, or wiring action.
- Rotary events produce local UI intents only: page navigation, row selection,
  local notification acknowledgement, or home.
- The browser mirror is an inert host request shim/static HTML generator. It
  opens no socket and does not add firmware, Wi-Fi, or persistent endpoints.

## Snapshot Fields

The renderer accepts only these top-level fields:

`schema`, `mode`, `link`, `peers`, `queue`, `custody`, `messages`, `files`,
`telemetry`, `mesh`, `xbee`, `locks`, `last_event`, and `uptime_ms`.

Missing values render as `?` except closed surfaces, which render as `CLOSED`.
Secret-bearing field names are rejected recursively.

Run:

```sh
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page MESH
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME --browser-html
```
