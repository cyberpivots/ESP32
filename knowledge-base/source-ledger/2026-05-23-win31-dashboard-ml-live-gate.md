# Win31 Dashboard ML Live Gate Source Ledger

Date: 2026-05-23, updated 2026-05-24

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-CODEX-PROJECT-CONFIG-2026-05-23`
- `SRC-CODEX-CUSTOM-AGENTS-2026-05-23`
- `SRC-OPENAI-VISION-LIMITATIONS-2026-05-23`
- `SRC-OPENAI-PROMPT-OPTIMIZER-2026-05-23`
- `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`
- `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`
- `SRC-PADDLEOCR-OCR-PIPELINE-2026-05-23`
- `SRC-LOCAL-ML-OCR-PROBE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23`
- `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`

## Verified Facts

- Project-local `.codex` agents and skills were added without provider, auth,
  profile, or telemetry keys.
- The ESP32 completion gate now combines manifest, flash-evidence,
  transcript, cleanup, and DOS-C vision-gate JSON checks.
- The DOS-C vision gate hashes copied screenshots, runs deterministic
  preprocessing plus Tesseract OCR, classifies required OPCON views, and fails
  closed when evidence is incomplete.
- The updated acceptance set includes Downloads and gated OTAP visible states,
  plus transcript evidence for `download_list`, `download_status`,
  `otap_status`, and non-executing `otap_intent`.
- The bridge transcript remains authoritative for BBS behavior; screenshots
  corroborate visible UI state only.
- Local fixture tests cover pass, missing-view, weak-OCR,
  transcript-mismatch, and cleanup-failure cases.

## Assumptions

- Future live evidence will be copied from ignored runtime paths before either
  completion gate is run.
- The next live proof will keep the accepted COM1/nullmodem/Pi bridge path.

## Unknowns

- No fresh live screenshot set has been scored by the gate.
- No new board identity, flash, radio, or cleanup evidence was captured by this
  task.
- No live mesh file delivery or live OTAP flashing is proven by the updated
  dashboard/protocol surface.
- PaddleOCR and hosted vision APIs remain unevaluated for this evidence set.

## Stop Gate

Do not claim live ML acceptance unless the authoritative transcript, cleanup
proof, and independent screenshot gate all pass for the same copied evidence
packet.
