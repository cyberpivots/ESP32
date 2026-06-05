# Tests

Tests will be added as firmware, tools, and protocol implementations are
introduced. The current scaffold validation entrypoint is
`scripts/verify_scaffold.py`.

Project-local host tests:

- `python3 tests/four_relay_safe_core/run_host_tests.py`
- `python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'`
- `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `python3 -m unittest discover -s tests/custom_wireless_protocol -p 'test_*.py'`
- `python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `python3 -m unittest discover -s tests/rnw_menu -p 'test_*.py'`
- `python3 -m unittest discover -s tests/esp32_gateway_tcp -p 'test_*.py'`
- `python3 -m unittest discover -s tests/live_bench -p 'test_*.py'`
- `python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`
- `python3 -m unittest tests.scaffold_audits.test_agent_scheduler`
- `python3 scripts/agent_scheduler.py self-test`
- `python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
- `python3 scripts/scaffold_audit_agent_process.py`
- `python3 tests/scaffold_audits/test_source_image_scan.py`
- `python3 scripts/audit_public_manifest.py` after
  `python3 scripts/build_github_pages.py`
- `python3 scripts/smoke_github_pages.py` after
  `python3 scripts/build_github_pages.py`
