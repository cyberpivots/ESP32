# Task 0013 - Hardware Circuit Improvement Research

## Task

- ID: 0013-hardware-circuit-improvement-research
- Owner role: Hardware, Communications, QA
- Status: Complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Add a source-backed research package for improving the `four-relay-xbee-wifi`
hardware and circuit design while preserving the current safety and mutation
gates.

## Scope

Included: consolidated hardware/circuit research doc, dated source ledger,
source-index additions for protection and bench-tool candidates, known-gap
updates, documentation index updates, public bundle allowlist update, scaffold
verification updates, task record, and handoff.

Excluded: firmware source, framework files, relay/load wiring, mains wiring
design or procedures, XBee setting writes, API transmit frames, relay commands,
ESP32 DIN/DOUT carrier wiring, final wiring diagrams, vendor PDF copies, raw
upload copies, private bench notes, and bench records in the public artifact.

## Sources

- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`
- `SRC-ESP-IDF-FATAL-BROWNOUT`
- `SRC-SD-ASSOCIATION-FORMATTER`
- `SRC-SD-ASSOCIATION-CAPACITY`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-SONGLE-SRD-05VDC-SL-C`
- `SRC-TI-LM66100`
- `SRC-LITTELFUSE-16R-PPTC`
- `SRC-LITTELFUSE-SLVU2-8-TVS`
- `SRC-TI-CD74HC4067`
- `SRC-TI-TCA9555`
- `SRC-ESPRESSIF-MCP23017-COMPONENT`
- `SRC-TI-TPIC6B595`
- `SRC-TI-ULN2003A`
- `SRC-FLUKE-87V`
- `SRC-KEYSIGHT-E36200`
- `SRC-SALEAE-LOGIC-8`
- `SRC-NIOSH-ELECTRICAL-SAFETY`
- `SRC-OSHA-DEENERGIZED-WORK`
- `SRC-OSHA-1910-305`
- `SRC-NEMA-ENCLOSURES`
- `SRC-NEMA-250-ENCLOSURES`

## Decisions

- Protection and driver components are candidates only until exact rail,
  current, relay-input, isolation, and load evidence closes.
- Required component/tool recommendations are grouped as `must buy`,
  `must identify`, `must measure`, `candidate only`, and `blocked`.
- The public Pages bundle can include the new research doc and source ledger,
  but must still exclude `.agents/`, raw uploads, private bench notes, and
  bench records.
- The next implementation step remains evidence collection, not schematic or
  firmware implementation.

## Validation

- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 -m py_compile scripts/verify_scaffold.py scripts/build_github_pages.py scripts/xbee_read_only_probe.py`:
  PASS.
- `python3 scripts/build_github_pages.py`: PASS, generated 52 public files.
- `git diff --check`: PASS.
- Source citation check for new/edited docs: PASS.
- Public artifact source-path check: PASS, no `.agents/`, `user_uploads/`,
  raw uploads, private bench notes, or `research/bench-records/` sources in
  `build/github-pages/public-file-manifest.json`.

## Handoff

Continue through
`.agents/handoffs/0010-hardware-circuit-research-to-hardware-qa.md` when the
next pass collects physical evidence or narrows component selection.
