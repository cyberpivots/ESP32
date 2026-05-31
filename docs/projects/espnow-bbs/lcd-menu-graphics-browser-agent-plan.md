# ESP-NOW BBS LCD Menu Graphics, Browser Mirror, And Agent Plan

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This is a Tier 2 host-only continuation of the LCD/encoder field-console work.
It improves the simulator renderer, custom-glyph planning surface, navigation
model, static browser mirror, tests, and recallable agent/skill records for a
20x4 HD44780-class BBS field console.

This plan does not authorize live bench action, flash, erase, monitor, serial
writes, XBee/RF writes, ESP-NOW runtime mutation, relay GPIO writes,
relay-expander writes, TFT, MicroSD, wiring mutation, load, mains, persistent
configuration endpoints, release gating, commit, or push.

## Verified Facts

- `bbs_lcd_state.v1` remains the production input snapshot schema for the
  host renderer. Source ID:
  `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`.
- The renderer now emits `bbs_lcd_render.v1`, including four 20-character
  lines, eight glyph slots, cursor metadata, dirty-cell metadata, widgets, and
  local view state. Source ID:
  `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`.
- The current PF0530K live gate passed flash and verify-flash but captured zero
  `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, and `BBS_MENU_SELECT`; it is not
  accepted as proven interactive. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`.
- HD44780 CGRAM planning is limited to eight 5x8 custom-character types.
  Source ID: `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`.
- The local 20x4 cursor tracker uses row bases `0x00`, `0x40`, `0x14`, and
  `0x54`, matching the existing firmware lineage and the source-backed 20x4
  row-address planning reference. Source IDs:
  `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`.
- Luma.LCD, Espruino, vrEmuLcd, and LcdMenu are design references only for
  progress-bar/custom-character examples, browser/emulator precedent, and
  rotary-menu control mapping. Source IDs:
  `SRC-LUMA-LCD-HD44780-2026-05-31`,
  `SRC-ESPRUINO-HD44780-2026-05-31`,
  `SRC-VREMULCD-2026-05-31`,
  `SRC-LCDMENU-ROTARY-ENCODER-2026-05-31`.
- ESP-IDF HTTP Server and Wi-Fi records support future URI-handler/web-serving
  and AP/SoftAP planning, but this task adds no firmware HTTP server, SoftAP,
  WebSocket, Wi-Fi profile, or selected-board browser proof. Source IDs:
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-WIFI`.

## Assumptions

- Browser mirror work is an inert host-only simulator surface.
- Custom glyph bank changes are host-rendered planning aids until a later live
  LCD gate proves visual behavior on hardware.
- Rotary input remains local UI intent only and cannot directly trigger relay,
  XBee, radio, serial-write, flash/erase, persistent configuration, or bridge
  commands.
- Future ESP32 browser work will use ESP-IDF only in an already accepted
  project lane and will require its own live/security gate.

## Unknowns

- Physical LCD visual behavior with custom glyph bank swaps.
- Encoder direction/select proof after PF0530K.
- Target firmware memory budget for any future browser mirror.
- Whether a future live device should expose SoftAP before a separate network
  and security gate.
- Exact LCD backpack electrical behavior, pullup voltage, and rail margin.

## Routing Packet

- Selected tier: Tier 2.
- Owner role: Lead LCD Menu Developer, with Architecture, Firmware, Hardware,
  Communications, QA, Evidence, and Agent-Ops lenses.
- Evidence need: repo-local source records, host tests, reviewer quorum,
  closed-surface scan, and no-secret-field checks.
- Mutation boundary: LCD simulator/browser host code, tests, this plan, source
  index/ledger rows, docs cross-links, repo-local skill/agent/config, task log,
  and QA handoff.
- Reviewer quorum: read-only reviewers approved mutation start with no P1/P2
  blockers; QA required browser-specific tests before browser acceptance.

## Renderer UX

The host renderer now tracks:

- fixed four-row, 20-column ASCII-safe display lines;
- cursor row/column and DDRAM address;
- dirty rows and dirty cells compared with a prior render;
- focus state for page, row, detail, and edit lab modes;
- local widget previews for progress bars, sliders, signal bars, queue/custody
  indicators, spinner frames, big digits, vertical charts, and a gauge demo.

The cursor tracker is software-owned. It does not depend on HD44780 address
counter reads or R/W wiring.

## Navigation Model

Modes are:

- `page_browse`: rotate changes page; short press enters row browse; long
  press returns home.
- `row_browse`: rotate changes selected row; short press selects; long press
  backs out to page browse.
- `detail`: rotate changes selected row; short press enters the edit lab;
  long press backs out.
- `edit_lab`: rotate changes a local value; short press commits local UI
  state; long press backs out.

`double_click` remains outside v1 and is rejected.

## Custom Graphics

The host `GlyphBankManager` defines these named banks:

- `core_status`
- `horizontal_bar`
- `vertical_chart`
- `big_digits`
- `gauge_demo`

Each bank is capped at eight slots, each glyph has eight rows, and each row
byte must stay in `0x00..0x1F`. Bank swaps are guarded at 250 ms minimum in the
host manager.

## Browser Mirror

The host mirror is a Python request shim and static HTML generator. It opens no
socket and starts no server.

- `GET /api/lcd/state` returns `bbs_lcd_render.v1`.
- `POST /api/lcd/intent` accepts only `rotate_left`, `rotate_right`,
  `short_press`, and `long_press`.
- The intent payload accepts only an `intent` field. Unknown or secret-bearing
  payload fields are rejected before local UI state changes.
- Unknown routes and methods return closed errors.
- Secret-bearing fields are rejected before rendering.
- The static HTML mirrors the active glyph-bank name plus cursor row, column,
  DDRAM address, and focus through inert markup/data attributes.
- The static HTML includes no `fetch`, WebSocket, EventSource, serial,
  Bluetooth, relay, XBee, flash, erase, or GPIO behavior.

## Browser QA Hardening Continuation

Task 0117 continues this host-only plan by tightening the inert browser mirror
contract:

- `bbs_lcd_render.v1` now includes `glyph_bank_name` alongside the eight-slot
  `glyph_bank` list.
- Static HTML exposes cursor and glyph-bank mirror metadata without opening
  network, browser device, GPIO, serial, RF, flash, relay, or persistent
  surfaces.
- Focused tests now cover all four allowed UI intents, method closure,
  malformed JSON, non-object JSON, unknown intent payload fields,
  secret-bearing intent payload fields, cursor HTML metadata, and glyph-bank
  HTML metadata.

This continuation remains Tier 2 host-only. It does not open the future ESP32
browser path, live browser proof, firmware HTTP server, SoftAP, WebSocket,
serial-write, RF, relay, flash, monitor, or wiring gates.

## Future ESP32 Browser Path

A future firmware browser mirror may use ESP-IDF HTTP Server URI handlers and,
if separately reviewed, WebSocket support. That future work requires a new gate
covering selected board, identity, network/security policy, rollback, memory
budget, endpoint allowlist, closed-surface scan, and same-session proof. This
Tier 2 slice does not open that gate.

## Recallable Agent

The repo-local `lcd-menu-operations` skill and
`lcd-menu-ux-reviewer` read-only agent profile capture the repeatable LCD
workflow. They are advisory operating aids only; they do not install system
requirements, override operator launch intent, mutate firmware, or authorize
hardware actions.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Closed-surface scan.
- `git diff --check`

## Stop Gates

Stop before live flash, prepare/flash/complete, monitor, serial writes,
serial-write expansion, XBee/RF, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, TFT, MicroSD, wiring mutation, load, mains, erase,
firmware ABI changes, bridge ABI changes, coordinator serial ABI changes, Gate
F service-code changes, `mesh_discovery.v1` changes, Win31 transport changes,
persistent configuration endpoints, framework changes outside accepted ADRs,
release gating, commit, or push.
