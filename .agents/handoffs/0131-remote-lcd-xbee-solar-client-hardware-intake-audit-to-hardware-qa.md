# Handoff 0131 - Remote LCD XBee Solar Client Hardware Intake Audit To Hardware QA

Continuation record for Task 0183
`remote-lcd-xbee-solar-client-hardware-intake-audit`.

## Continue with

- Treat Task 0183 as a parent repo records-only intake audit, not hardware
  identity closure.
- Use
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-HARDWARE-INTAKE-AUDIT-2026-06-05`
  for the current status packet.
- Start source-backed identity intake inside the private `rlxsc-*` submodules.
  Prioritize `rlxsc-18650-cell`, `rlxsc-bms-protection`, and
  `rlxsc-solar-charger-power-path` for cell, BMS/protection, charger, panel,
  fuse/protection, enclosure, and current-limit evidence.
- Then review `rlxsc-esp32-client-node`, `rlxsc-lcd-20x4-i2c`,
  `rlxsc-rotary-encoder`, and `rlxsc-xbee-pro-s3b` for boot/recovery,
  voltage, pullup, DIN/DOUT, antenna, and pin-risk evidence.
- Record fresh submodule status whenever claiming current submodule state. The
  2026-05-26 private-submodule ledger is creation evidence, not a guarantee of
  current pins.

## Stop Gates

- Do not connect battery, BMS/protection, charger, solar panel, ESP32 rail,
  LCD, encoder, XBee carrier, antenna hardware, fuse/protection hardware, or
  enclosure hardware from this handoff.
- Do not infer pinouts, voltages, current limits, charge limits, connector
  labels, DIN/DOUT direction, antenna/regulatory readiness, power budget,
  boot/recovery safety, or enclosure suitability from candidate/reference
  sources.
- No firmware source, framework selection, pin assignment, XBee serial open,
  Tier B read query, XCTU/XBee Studio live discovery, XBee setting write, API
  transmit frame, RF test, relay/load/mains, release, publication, commit,
  push, PR, or deploy is authorized.

## Validation to preserve

```bash
test -f .agents/TASK_LOG/0183-remote-lcd-xbee-solar-client-hardware-intake-audit.md
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 183
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_paths.py
git submodule status --recursive
git diff --check
```
