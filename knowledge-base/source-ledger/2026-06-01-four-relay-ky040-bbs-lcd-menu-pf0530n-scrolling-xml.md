# Four Relay KY-040 BBS LCD Menu PF0530N Scrolling/XML Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-SCROLLING-XML-2026-06-01`

## Verified Facts

- PF0530N is a non-live source/test continuation after PF0530M and the
  accepted PF0530L LCD visual/electrical evidence.
- PF0530N changes the active firmware ID to `PF0530N`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32 input-only, and
  keeps LCD writes display-only on GPIO21/GPIO22.
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml` is the build-time XML
  source of truth for pages and menu items.
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py` validates the XML and
  generates `tools/simulators/lcd_bbs_menu/generated_menu.py` plus
  `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`.
- The ESP32 firmware consumes generated static menu definitions and does not
  parse XML at runtime.
- The host renderer now emits `bbs_lcd_render.v2` with selected item,
  visible item IDs, physical indicator row, viewport top line, horizontal
  scroll offsets, and source XML metadata.
- Rotary movement now drives a generated scroll-list model in source, with a
  bounded page stack for XML-defined page navigation.
- Selected overlong rows use deterministic marquee timing: 750 ms hold, 250 ms
  per step, and two spaces between wrap cycles. Non-selected overlong text
  clips to the 19-column content area.
- The `ROUTES` page uses the `table` glyph bank, which stays within the
  HD44780 eight-slot CGRAM limit and keeps table formatting separate from
  bar/chart/big-digit/gauge banks.

## Assumptions

- PF0530N remains non-live source/test work until a separately authorized Tier
  3 gate opens any flash, monitor, serial-write, DMM, or hardware action.
- Host simulator tests can prove XML parsing, generated-model freshness, menu
  state behavior, and LCD text bounds, but do not prove physical LCD rendering.
- Bridge and lock display text remains informational only. It does not
  authorize XBee/RF writes, ESP-NOW runtime, serial-write expansion, bridge ABI
  changes, relay output, or persistent configuration.

## Unknowns

- PF0530N runtime behavior on COM6 is unknown because no flash or live monitor
  was performed.
- Physical readability of the PF0530N scroll-list and route table remains
  unproven until a fresh Tier 3 live gate opens it.
- Final BBS/XBee payload display mapping remains open for a future non-live
  integration lane.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (22 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (22 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py` (4 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (55 tests)
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B <redacted-temp-build-dir> build`
  generated `four_relay_xbee_wifi.bin` size `0x2d3c0`, with `0xd2c40` bytes
  (82 percent) free in the smallest app partition.
- PASS: `git diff --check`

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `tools/simulators/lcd_bbs_menu/bbs_lcd_menu.v1.xml`
- `tools/simulators/lcd_bbs_menu/generate_lcd_menu.py`
- `tools/simulators/lcd_bbs_menu/generated_menu.py`
- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tools/simulators/lcd_bbs_menu/README.md`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `scripts/scaffold_audit_firmware.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0124-four-relay-ky040-bbs-lcd-menu-pf0530n-scrolling-xml.md`
- `.agents/handoffs/0091-four-relay-ky040-bbs-lcd-menu-pf0530n-scrolling-xml-to-qa.md`

## Authority Limits

This source record does not prove or authorize COM6 access, flash, monitor,
serial writes, XBee/RF writes, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, MicroSD/TFT action, wiring mutation, DMM/current
measurement, load, mains, erase, firmware HTTP/SoftAP/WebSocket runtime,
persistent config, external services, GitHub publication, release, commit, or
push.
