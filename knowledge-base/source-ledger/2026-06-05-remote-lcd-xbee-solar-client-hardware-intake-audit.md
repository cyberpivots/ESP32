# Remote LCD XBee Solar Client Hardware Intake Audit Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-HARDWARE-INTAKE-AUDIT-2026-06-05`

## Scope

Tier 2 parent repo records-only hardware intake audit for
`remote-lcd-xbee-solar-client`. This ledger records reviewer quorum output,
fresh submodule status context, candidate/reference source coverage, and
durable status updates. It does not close hardware identity and does not open
firmware, framework, wiring, charging, serial/RF/XBee, live bench, release,
publication, commit, push, PR, or deploy authority.

## Source Coverage

- Initial remote-client scaffold, private submodule creation, and separate
  hardware stream records are covered by:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`, and
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26`.
- Candidate/reference-only hardware rows include `SRC-NXP-PCF8574-74A`,
  `SRC-BOURNS-PEC11R`, `SRC-TI-BQ25185`, `SRC-TI-BQ2970`,
  `SRC-TI-BQ27441-G1`, and `SRC-UL-LIION-SAFETY`.
- ESP32 and XBee planning rows include `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-I2C`, `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-DIGI-XBEE-PRO-900HP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`,
  `SRC-DIGI-XBEE-900HP-TO-2026-06-05`, and
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Current XBee status context is covered by
  `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`,
  `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`, and
  `SRC-LOCAL-XBEE-TIER-A-NO-SERIAL-IDENTITY-EVIDENCE-2026-06-05`, but those
  records do not prove the remote-client carrier, antenna, settings, wiring,
  or power budget.

## Verified Facts

- The remote-client lane is currently docs-only, framework-neutral, and
  hardware-action closed.
- Seven private `rlxsc-*` submodules are present and were inspected by README
  and current `git submodule status --recursive` output.
- Current submodule status captured during this task:
  - `rlxsc-18650-cell`: `7eb9dede8c3df4d90b11e6dfb0111f0ad4c0eb42`
  - `rlxsc-bms-protection`: `b33fcdfd5bc57fc504e654a4580fda3eeddc386f`
  - `rlxsc-esp32-client-node`: `6b0d6018f17e0e31de9b61e23415d733eb7f5116`
  - `rlxsc-lcd-20x4-i2c`: `8bc2c7fa9e9ee96fdd7f6b41155905da34f4d405`
  - `rlxsc-rotary-encoder`: `b9f66b6d576c2b2f87751b203c5283ded8cc4dcc`
  - `rlxsc-solar-charger-power-path`: `d56b53fd556592fa382b6c6d3f976068b14ef8ff`
  - `rlxsc-xbee-pro-s3b`: `dc6ce28783545f8ca517ae3c61f595ccb482275e`
- The current `rlxsc-xbee-pro-s3b` pointer differs from the historical
  2026-05-26 private-submodule ledger. Treat the older ledger as creation
  evidence only.
- Candidate/reference sources do not select or verify the local LCD backpack,
  encoder, charger, BMS/protection board, fuel gauge, 18650 cell, ESP32 board,
  XBee carrier, antenna, panel, fuse/protection, or enclosure.
- Reviewer quorum approved only this parent records/status boundary with 17/17
  weighted approval and no P1/P2 blockers inside the boundary.

## Assumptions

- Private submodules are evidence lanes; raw photos, markings, serial
  identifiers, keys, raw bytes, and local bench captures remain private unless
  separately redacted and approved.
- Future hardware action requires a later Tier 3 gate with same-session
  evidence, recovery path, cleanup path, reviewer quorum, and no P1/P2
  blockers.

## Unknowns

- Exact ESP32 board, LCD/backpack, encoder, 18650 cell, BMS/protection board,
  solar panel, charger/power path, XBee carrier, antenna, fuse/protection,
  enclosure, power budget, pin map, framework ADR, and read-only bench proof
  remain unresolved.
- No remote-client-specific bench record exists for the lane.
- No voltage/current, pullup, charge-current, panel Voc/Isc, protection
  threshold, rail budget, boot/recovery, antenna/regulatory, DIN/DOUT, or
  enclosure evidence is accepted.

## Authority Limits

This record does not authorize hardware selection, wiring, live measurement,
charging, battery pack assembly, solar connection, power-path connection,
ESP32 GPIO attachment, ESP32-to-XBee DIN/DOUT wiring, framework selection,
firmware source, XBee serial open, Tier B read query, XCTU/XBee Studio live
discovery, XBee setting writes, `WR`, `AC`, `KY`, API transmit, RF/range/
throughput tests, flash, erase, monitor, relay/load/mains, release,
publication, commit, push, PR, deploy, `/etc/codex/requirements.toml`, or
`admin-strict` mutation.

## Validation

Validation completed on 2026-06-05:

- PASS: `test -f .agents/TASK_LOG/0183-remote-lcd-xbee-solar-client-hardware-intake-audit.md`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 183`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_paths.py`.
- PASS: `git submodule status --recursive`.
- PASS: `git diff --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_scaffold_audit_records tests.scaffold_audits.test_source_image_scan tests.scaffold_audits.test_xbee_radio_study`
  (22 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
  built 64 public files.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py build/github-pages`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `timeout 180s env PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: submodule static docs-only check for all seven `rlxsc-*` submodules.

The reviewer-suggested 60-second scaffold timeout exited `124` with no scaffold
failure output; the 180-second run passed.

## Decision

Decision: accept the parent records-only hardware intake audit. Continue with
source-backed identity intake inside private submodules before any bench,
wiring, charging, radio, firmware, or framework gate.
