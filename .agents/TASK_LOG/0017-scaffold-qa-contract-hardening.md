# Task Log 0017 - Scaffold QA and Contract Hardening

## Task

- ID: 0017-scaffold-qa-contract-hardening
- Owner role: QA
- Status: complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Reduce scaffold verifier fragility, expand framework-neutral safe-core/API
contract tests, add public artifact smoke/link checks, and convert hardware
blockers into structured evidence-record requirements.

## Scope

Included:

- Modular scaffold audit helpers behind the existing
  `python3 scripts/verify_scaffold.py` entrypoint.
- Source-image audit behavior that ignores generated `build/` outputs while
  still blocking unallowlisted source images.
- Split host tests for relay/safety, HTTP/API contracts, storage contracts, and
  XBee frame parsing.
- Pure-C API payload and snapshot models with no ESP-IDF runtime dependency.
- Public Pages manifest integrity, link/asset checks, and CLI smoke coverage.
- Bench-record template and known-gap next-evidence mapping.

Excluded:

- Live GPIO, relay, XBee setting writes, MicroSD mount, TFT wiring, firmware
  flashing, monitoring, and load/mains procedures.

## Sources

- `SRC-ESP-IDF-STABLE-ESP32`
- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-FATFS`
- `SRC-ESP-IDF-SDSPI`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`

## Decisions

- ADR-0001 remains framework-neutral for the workspace.
- ADR-0002 remains limited to project-local ESP-IDF scaffolding for
  `four-relay-xbee-wifi`.
- Generated public artifacts remain allowlist-only.
- Hardware gaps remain unresolved until supported by a source-index entry,
  physical inspection record, ADR, or test artifact.

## Validation

- `python3 scripts/verify_scaffold.py` - pass.
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py` - pass.
- `python3 tests/four_relay_safe_core/run_host_tests.py` - pass.
- `python3 scripts/xbee_read_only_probe.py self-test` - pass, 21/21 self-tests.
- `python3 tests/scaffold_audits/test_source_image_scan.py` - pass.
- `python3 scripts/build_github_pages.py` - pass, 56 public files.
- `python3 scripts/audit_public_manifest.py` - pass.
- `python3 scripts/smoke_github_pages.py` - pass.
- `git diff --check` - pass.

## Handoff

Next owners:

- QA: keep the modular audits and split host tests wired into future CI.
- Firmware: consume only the pure-C safe-core contracts until a gated ESP-IDF
  implementation task is accepted.
- Hardware/Communications: use `research/bench-records/TEMPLATE.md` for exact
  board, relay, XBee, MicroSD, TFT, mux, expander, and instrument evidence.
