# Handoff 0013 - Scaffold QA Contracts to Role Lanes

## From

QA

## To

Firmware, Hardware, Communications, Release

## Status

Open

## Context

The scaffold QA cycle is hardening local contracts without opening live hardware
mutation. The verifier is now expected to stay modular, safe-core tests are
split by subsystem, and public Pages output has explicit smoke/link/integrity
checks.

## Continue With

- Firmware: keep additions inside pure C safe-core or explicitly accepted
  project-local ESP-IDF work. Do not add live GPIO, UART writes, storage mounts,
  or flash/monitor steps without a new gate.
- Hardware: use `research/bench-records/TEMPLATE.md` before closing board,
  shield, relay, MicroSD, TFT, mux, expander, power, or instrument blockers.
- Communications: keep XBee bench work inside the existing read-only proof
  boundary unless a later accepted task authorizes setting writes.
- Release: preserve the allowlist Pages artifact path and require manifest,
  link, asset, and smoke checks before publish.

## Validation To Preserve

- `python3 scripts/verify_scaffold.py`
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py`
- `python3 tests/four_relay_safe_core/run_host_tests.py`
- `python3 scripts/audit_public_manifest.py`
- `python3 scripts/smoke_github_pages.py`
- `python3 tests/scaffold_audits/test_source_image_scan.py`

## Open Gaps

- Hardware evidence remains unresolved until exact physical/source records are
  captured.
- Live firmware, relay wiring, XBee setting writes, storage mounting, TFT
  wiring, and load/mains procedures remain out of scope.
