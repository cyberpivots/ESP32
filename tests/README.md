# Tests

Tests will be added as firmware, tools, and protocol implementations are
introduced. The current scaffold validation entrypoint is
`scripts/verify_scaffold.py`.

Project-local host tests:

- `python3 tests/four_relay_safe_core/run_host_tests.py`
- `python3 tests/scaffold_audits/test_source_image_scan.py`
- `python3 scripts/audit_public_manifest.py` after
  `python3 scripts/build_github_pages.py`
- `python3 scripts/smoke_github_pages.py` after
  `python3 scripts/build_github_pages.py`
