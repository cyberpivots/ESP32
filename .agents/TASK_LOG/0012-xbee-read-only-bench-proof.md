# Task 0012 - XBee Read-Only Bench Proof

## Task

- ID: 0012-xbee-read-only-bench-proof
- Owner role: Hardware, Communications, QA
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Add a source-backed, read-only bench proof lane for identifying the Digi
`XBP9B-DPUT-001 RevF` radio through the Waveshare XBee USB Adapter without
setting writes, firmware updates, relay commands, ESP32 carrier wiring, or load
wiring.

## Scope

Included: dedicated XBee read-only proof doc, two-tier passive/read-query bench
workflow, local Python probe with hardware-free self-test, source and ledger
updates, project/profile links, public bundle allowlist update, and scaffold
verification updates.

Excluded: firmware source, framework files, ESP32 flashing, XBee setting
writes, `WR`, `AC`, API transmit frames, relay commands, relay switching,
ESP32 DIN/DOUT wiring, adapter carrier selection, mains/load wiring, vendor PDF
copies, package installs, and edits to unrelated dirty-tree work.

## Sources

- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`

## Decisions

- Tier A is passive discovery: serial listing, adapter inspection, voltage
  measurement, and optional read-only byte observation.
- Tier B is explicitly gated with `--confirm-sends-read-commands`; it sends the
  command-mode guard sequence and only allows `VR`, `HV`, `SH`, `SL`, `AP`,
  `AO`, `BD`, and `NP`.
- `SH` and `SL` are redacted by default. Unredacted address evidence is
  local-only and must stay out of the public Pages artifact.
- Bench JSON records may be written only under
  `research/bench-records/xbee-readonly/`.

## Validation

- `python3 -m py_compile scripts/xbee_read_only_probe.py scripts/verify_scaffold.py`:
  PASS.
- `python3 scripts/xbee_read_only_probe.py self-test`: PASS, 21/21 hardware-free
  checks.
- `python3 scripts/xbee_read_only_probe.py list --json`: PASS, WSL2/Python
  3.12.3/pyserial 3.5 environment reported, no `xctu` on PATH, `/dev/ttyS0`
  and `/dev/ttyS1` pyserial candidates.
- `python3 scripts/xbee_read_only_probe.py passive --port /dev/does-not-exist --baud 9600 --duration 1 --json`:
  PASS for negative-path validation, returned structured `serial_open_failed`
  and attempted no serial writes.
- `python3 -m json.tool site/github-pages/site-data.json`: PASS.
- `node --check site/github-pages/app.js`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 scripts/build_github_pages.py`: PASS, generated 50 public files.
- Manifest spot check: PASS, public bundle includes the XBee proof doc and
  source ledger; no `.agents/`, `user_uploads/`, or `research/bench-records/`
  source path was added.
- `git diff --check`: PASS.

## Handoff

Continue through `.agents/handoffs/0009-xbee-read-only-proof-to-hardware-comms-qa.md`
after validation is recorded here.
