# LCD BBS Menu Simulator

This host-only simulator renders compact `bbs_lcd_state.v1` snapshots through
the build-time `bbs_lcd_menu.v1` XML menu into four 20-character LCD lines plus
an eight-slot HD44780 custom-glyph bank. It is for ESP-NOW BBS field-console
planning and PF0530N non-live menu-state testing only.

The renderer output schema is `bbs_lcd_render.v2`. It adds software cursor
tracking, HD44780 DDRAM row/column metadata, dirty-row/cell metadata, a named
glyph bank, host-rendered widget previews, selected-item/viewport metadata,
visible item IDs, physical indicator row, horizontal marquee offsets, and the
source XML version.

## Boundaries

- No hardware access.
- No serial commands.
- No firmware build, flash, erase, monitor, XBee/RF, ESP-NOW runtime, relay,
  TFT, MicroSD, load, mains, or wiring action.
- Rotary events produce local UI intents only: scroll-list item movement,
  XML-defined page navigation, detail view, local edit value changes, local
  acknowledgement, back, or home.
- The browser mirror is an inert host request shim/static HTML generator. It
  opens no socket and does not add firmware, Wi-Fi, or persistent endpoints.
- `POST /api/lcd/intent` accepts only an `intent` field and rejects unknown or
  secret-bearing payload fields before applying local UI state.
- The static HTML mirrors cursor row/column/DDRAM/focus, selected item,
  viewport top line, marquee offsets, source XML version, and the active glyph
  bank through inert markup/data attributes only.

## Build-Time XML

`bbs_lcd_menu.v1.xml` is the source of truth for pages and items. Run the
generator after editing it:

```sh
python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py
python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check
```

The generator writes `generated_menu.py` for host tests and
`firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h` for
firmware static definitions. The ESP32 firmware does not parse XML at runtime.
The generator rejects unknown fields, duplicate IDs, bad targets, unsafe glyph
banks, table rows wider than the 19-column content area, unknown text tokens,
secret-bearing field names, DOCTYPE, and external entities.

## Snapshot Fields

The renderer accepts only these top-level fields:

`schema`, `mode`, `link`, `peers`, `queue`, `custody`, `messages`, `files`,
`telemetry`, `mesh`, `xbee`, `bridge`, `errors`, `locks`, `last_event`, and
`uptime_ms`.

Missing values render as `?` except closed surfaces, which render as `CLOSED`.
Secret-bearing field names are rejected recursively.

The current host page set is generated from XML: `HOME`, `MESSAGES`, `PEERS`,
`QUEUE`, `FILES`, `MESH`, `XBEE`, `DIAG`, `LOCKS`, `BARS`, `CHART`, `DIGITS`,
`GAUGE`, and `ROUTES`.

Run:

```sh
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page MESH
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page ROUTES
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page GAUGE
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page MESSAGES --now-ms 1000
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME --browser-html
```
