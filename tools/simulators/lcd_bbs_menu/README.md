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

The host art compiler emits `bbs_lcd_art.v1` metadata for image-like LCD
panels. It compiles deterministic 100x32 ASCII PBM `P1` bitmaps or direct
4x20 tile maps into 5x8 HD44780 glyph rows, reuses identical nonblank tiles,
and fails closed when a panel needs more than eight custom glyphs. The normal
`lines` field stays ASCII-safe; compiled art exposes `preview_lines`,
`cell_slots`, a deterministic `bbs_lcd_pixel_preview.v1` 100x32 `.`/`#`
preview, and its own eight-slot glyph bank as metadata only. The ART page also
exposes a host-only catalog of candidate panels for comparison before any
firmware or physical LCD gate.

## Boundaries

- No hardware access.
- No serial commands.
- No firmware build, flash, erase, monitor, XBee/RF, ESP-NOW runtime, relay,
  TFT, MicroSD, load, mains, or wiring action.
- The art compiler is host-only metadata. It does not write raw CGRAM control
  codes into `lines` and does not prove physical LCD readability or flicker.
- Pixel previews and catalog panels are host-rendered planning evidence only;
  they do not prove contrast, transient CGRAM redraw behavior, or physical
  ART-page readability.
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
`GAUGE`, `ROUTES`, and `ART`.

Run:

```sh
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page MESH
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page ROUTES
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page GAUGE
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page ART
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page MESSAGES --now-ms 1000
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page HOME --browser-html
python3 tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py --page ART --browser-html
```

The sample render output includes an `art_panel` widget with
`bbs_lcd_art.v1` metadata. It is suitable for host tests and browser mirror
inspection only. The `ART` page output includes `art_catalog`,
`art_active_name`, `art_active_index`, `art_panel_count`, and
`bbs_lcd_pixel_preview.v1` metadata for five host candidate panels:
`bbs_badge`, `mesh_radar`, `packet_flow`, `signal_skyline`, and `link_heat`.
Rotary events on the ART page cycle those panels locally without changing the
selected menu item. A future physical LCD acceptance gate must collect
same-session visual evidence before claiming any art panel is readable.
