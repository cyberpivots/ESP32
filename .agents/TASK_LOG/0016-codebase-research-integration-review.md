# Task 0016 - Codebase Research Integration Review

## Task

- ID: 0016-codebase-research-integration-review
- Owner role: Architect, Hardware, Communications, Firmware, QA, Release
- Status: Complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Run the next M0/M1 integration cycle for `four-relay-xbee-wifi`: reconcile
code/docs contracts, keep hardware research evidence-gated, and tighten public
artifact QA without adding live hardware behavior.

## Scope

Included: public relay-channel contract alignment, host-test negative-path
coverage, XBee parser vectors, public manifest audit helper, known-gap updates,
task record, and role-lane handoff.

Excluded: relay/load wiring, relay GPIO writes, expander writes to relay
hardware, XBee setting writes, XBee API transmit frames to hardware, ESP32
DIN/DOUT carrier wiring, TFT wiring, MicroSD wiring, firmware flashing,
monitoring, live bench mutation, private bench-data publication, and
mains/load procedures.

## Sources

- `SRC-ESP-IDF-STABLE-ESP32`
- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`
- `SRC-GITHUB-PAGES-WHAT-IS`
- `SRC-GITHUB-PAGES-LIMITS`

## M0 Contract Findings

- Firmware/API lane: `POST /api/relay/{channel}` now accepts public channels
  `1..4`, rejects `0` and `5`, and keeps internal desired-state arrays
  zero-based behind `safe_core`.
- Firmware/QA lane: host tests now cover public-to-internal relay mapping,
  invalid payloads, missing admin, closed safety lock, open hardware gate,
  invalid channels, replay, all-off behavior, and storage/log failure paths.
- Communications/QA lane: host vectors now include escaped API2 frames, bad
  checksum, bad length, truncated escape, short frame, and transmit-status
  frame handling.
- Release/QA lane: `scripts/audit_public_manifest.py` audits
  `build/github-pages/public-file-manifest.json` for blocked source paths,
  blocked suffixes, and non-allowlisted image assets.

## M1 Hardware Evidence Disposition

| Item | Disposition | Notes |
| --- | --- | --- |
| Board/shield power path | blocked | Needs exact board/shield identity, regulator, jumper, rail, and continuity evidence. |
| Relay module behavior | blocked | Needs exact module source or measured input voltage, current, polarity, isolation, and `JD-VCC`/`VCC` behavior. |
| MicroSD reader | blocked | Needs exact module identity, level/power behavior, pullups, card-detect/write-protect, and continuity evidence. |
| XBee adapter/carrier | approved_with_gaps | Read-only PC-dock proof tooling is bounded; ESP32-mounted carrier wiring remains blocked. |
| TFT pin pressure | blocked | Needs exact module inspection and shared pin-budget review with relay, storage, XBee, ADC, boot, and UART0 constraints. |
| Expander/mux boards | approved_with_gaps | CD74HC4067 remains input-only planning; latched expander proof is LED/logic-analyzer only until relay evidence exists. |
| Bench instruments | approved_with_gaps | Instrument classes are identified, but exact local instruments and records remain open. |
| Load/enclosure gates | blocked | Requires separate qualified-review package before any mains/load design. |

## Validation

- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 -m py_compile scripts/verify_scaffold.py scripts/build_github_pages.py scripts/xbee_read_only_probe.py tests/four_relay_safe_core/run_host_tests.py scripts/audit_public_manifest.py`: PASS.
- `python3 tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 scripts/xbee_read_only_probe.py self-test`: PASS.
- `python3 scripts/build_github_pages.py`: PASS.
- `python3 scripts/audit_public_manifest.py`: PASS.
- `git diff --check`: PASS.
- Browser QA: PASS for `index.html`, `blueprints.html`, and
  `demos/admin-hmi/index.html` at desktop and mobile widths.

## Handoff

Continue through `.agents/handoffs/0012-codebase-research-integration-to-role-lanes.md`.
