# Four Relay KY-040 BBS LCD Menu PF0530M Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530M-2026-06-01`

## Verified Facts

- PF0530L serial/menu physical interaction is accepted under
  `SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31`.
- PF0530L LCD visual/glyph readability and user-confirmed low-voltage
  electrical/DMM acceptance are recorded under
  `SRC-LOCAL-LCD-GLYPH-ELECTRICAL-ACCEPTANCE-2026-05-31`.
- PF0530M changes the active firmware ID to `PF0530M`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32 input-only, and
  keeps LCD writes display-only on GPIO21/GPIO22.
- PF0530M changes the LCD/menu content from demo-oriented visual proof pages
  toward operational BBS status pages, including local bridge closed state,
  diagnostics/errors, row/action labels, and editable widget rows.
- PF0530M source-visible proof strings include `PF0530M BBS_LCD_READY`,
  `BBS FIELD STATUS`, `BRIDGE LOCAL CLOSED`, `DIAG ERRORS:0`,
  `GAUGE STATUS`, and `actions=detail,edit,back`.
- The host simulator mirrors the 13-page firmware page set, includes
  `bridge`/`errors` snapshot fields, selects widget glyph banks by page, and
  tests row/detail/edit behavior plus 20-character display bounds.

## Assumptions

- PF0530M remains non-live source/test work until a separately authorized Tier
  3 gate opens any flash, monitor, or hardware action.
- Host simulator tests can lock down menu behavior and LCD text bounds, but do
  not prove physical LCD rendering or encoder behavior.
- Bridge display text remains informational only. It does not authorize XBee/RF
  writes, ESP-NOW runtime, serial-write expansion, or bridge ABI changes.

## Unknowns

- PF0530M runtime behavior on COM6 is unknown because no flash or live monitor
  was performed.
- Final BBS/XBee payload display mapping remains open for a future non-live
  integration lane.
- Future direction-label expectations remain undefined unless the user opens a
  mapping-specific requirement.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (20 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (20 tests)
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
- PASS: `git diff --check`
- PASS: ESP-IDF v6.0.1 no-flash build to
  `<redacted-temp-build-dir>`; app binary size
  `0x2bbf0`, with `0xd4410` bytes free in the 1 MiB factory app partition.

## Files

- `firmware/projects/four-relay-xbee-wifi/main/main.c`
- `firmware/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `docs/prompt/comprehensive-bench-development-process.md`
- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tools/simulators/lcd_bbs_menu/README.md`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `scripts/scaffold_audit_firmware.py`
- `tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `knowledge-base/source-index.md`
- `.agents/TASK_LOG/0123-four-relay-ky040-bbs-lcd-menu-pf0530m.md`
- `.agents/handoffs/0090-four-relay-ky040-bbs-lcd-menu-pf0530m-to-qa.md`

## Authority Limits

This source record does not prove or authorize COM6 access, flash, monitor,
serial writes, XBee/RF writes, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, MicroSD/TFT action, wiring mutation, DMM/current
measurement, load, mains, erase, firmware HTTP/SoftAP/WebSocket runtime,
persistent config, external services, GitHub publication, release, commit, or
push.
