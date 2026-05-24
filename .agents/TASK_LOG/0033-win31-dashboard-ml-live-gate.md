# Task Log 0033 - Win31 Dashboard ML Live Gate

## Task

- ID: 0033-win31-dashboard-ml-live-gate
- Owner role: Tooling, Communications, QA
- Status: tooling implemented pending copied live evidence
- Created: 2026-05-23
- Updated: 2026-05-23
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Add project-scoped reusable Codex agents/skills and a fail-closed completion
gate that combines the authoritative bridge transcript with local CV/OCR
corroboration of Windows 3.1 OPCON screenshots.

## Scope

Included:

- Project-local `.codex` config, custom agents, and lean skills.
- `scripts/espnow_bbs_live_gate.py complete` for manifest, flash-evidence,
  transcript, cleanup, and DOS-C vision-gate JSON review.
- Paired DOS-C screenshot vision gate and fixture tests.
- Source index, source ledger, project documentation, task record, and handoff.

Excluded:

- Firmware changes, bridge wire-protocol changes, live preflight, backup,
  flashing, monitoring, serial write expansion, PCAP, packet-driver, router
  admin, BLE, ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load, or
  mains work.

## Sources

- `SRC-CODEX-PROJECT-CONFIG-2026-05-23`
- `SRC-CODEX-CUSTOM-AGENTS-2026-05-23`
- `SRC-OPENAI-VISION-LIMITATIONS-2026-05-23`
- `SRC-OPENAI-PROMPT-OPTIMIZER-2026-05-23`
- `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`
- `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`
- `SRC-PADDLEOCR-OCR-PIPELINE-2026-05-23`
- `SRC-LOCAL-ML-OCR-PROBE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`

## Decisions

- Keep transcript proof authoritative for BBS behavior.
- Use local deterministic CV/OCR as corroborating screenshot evidence.
- Fail closed as manual review when visual, transcript, or cleanup proof is
  weak.
- Keep hosted vision and PaddleOCR as future research options, not current
  runtime dependencies.

## Validation

- `python3 -m py_compile scripts/espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_multipeer_preflight.py`
- `python3 scripts/verify_scaffold.py`
- Paired DOS-C validation recorded in
  `/mnt/h/dos-c/.agents/tasks/0013-win31-dashboard-vision-gate.md`.

## Handoff

Continue through
[../handoffs/0023-win31-dashboard-ml-live-gate-to-qa.md](../handoffs/0023-win31-dashboard-ml-live-gate-to-qa.md)
before using this gate for live acceptance.
