# ESP-NOW BBS ML Live Completion Gate

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

Date: 2026-05-23

## Scope

This gate adds project-scoped agent configuration and a completion audit for
the accepted Windows 3.1 ESP-NOW BBS proof path:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

The gate does not change firmware, the bridge wire protocol, flashing
authority, or any unsafe bench lane. It evaluates copied evidence after a live
run: manifest, flash evidence, bridge transcript, cleanup proof, and the
paired DOS-C screenshot vision-gate JSON.

## Verified Facts

- Codex project config can use `.codex/config.toml` with project-local skills
  and custom-agent config files. Source IDs:
  `SRC-CODEX-PROJECT-CONFIG-2026-05-23`,
  `SRC-CODEX-CUSTOM-AGENTS-2026-05-23`.
- The project-local `.codex` setup added read-only default agents with explicit
  reasoning levels and lean skills for ESP32 live-gate coordination and Win31
  dashboard CV/OCR proof. Source ID:
  `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`.
- Local Python and Tesseract probes found `cv2`, `PIL`, `pytesseract`, `numpy`,
  `onnxruntime`, and Tesseract 5.3.4 available in the current shell. Source ID:
  `SRC-LOCAL-ML-OCR-PROBE-2026-05-23`.
- OpenCV and Tesseract provide documented image-processing/OCR references for
  deterministic preprocessing and recognition checks. Source IDs:
  `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`,
  `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`.
- The first implementation keeps PaddleOCR and OpenAI vision as documented
  future comparison options; no new runtime dependency or hosted vision API is
  selected by this gate. Source IDs:
  `SRC-PADDLEOCR-OCR-PIPELINE-2026-05-23`,
  `SRC-OPENAI-VISION-LIMITATIONS-2026-05-23`.
- The bridge transcript remains authoritative for BBS behavior. The screenshot
  gate corroborates visible OPCON/Program Manager state and fails closed as
  `needs_manual_review` when OCR/CV evidence is weak. Source ID:
  `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`.

## Assumptions

- Live acceptance evidence will be copied into ignored local evidence paths
  before the DOS-C vision gate and ESP32 completion gate run.
- Screenshot filenames may provide operator labels, but visible OCR/CV evidence
  must still support required dashboard state.
- Future OCR alternatives may be evaluated only after labeled live screenshots
  show the current deterministic gate is insufficient.

## Unknowns

- No new live screenshots, flash evidence, or bridge transcript were captured
  by this task.
- No PaddleOCR accuracy comparison has been run on project screenshots.
- No OpenAI vision model is approved for live acceptance of this bench lane.
- OCR thresholds may need tuning after the next copied live OPCON screenshot
  set is reviewed.

## Required Inputs

`scripts/espnow_bbs_live_gate.py complete` requires:

- A prepare manifest with device identities, build hashes, backup hashes,
  recovery commands, and flash-gate metadata.
- Flash evidence proving all four roles completed write and verification steps.
- The authoritative bridge transcript showing `hello`, `state_get`,
  `peer_list`, `diag_get`, `fw_inventory`, `msg_post`, `msg_pull`,
  `msg_search`, and `msg_ack`.
- Cleanup proof for DOSBox-X, warning/quit modals, the Pi bridge process, and
  listeners on `31331`, `31332`, and `8080`.
- DOS-C `win31_dashboard_vision_gate.py` JSON with screenshot hashes,
  required-view classification, transcript audit, cleanup audit, and
  fail-closed status.

## Required Visible States

The screenshot gate must corroborate:

- OPCON splash or dashboard.
- Peers view with `peer01`, `peer02`, `peer03`, and `espnow-enc`.
- Message Board view.
- Network view.
- Diagnostics and Safety views.
- Disabled unsafe controls.
- Program Manager item when that screenshot is present.

## Stop Gates

Keep these lanes closed unless a later explicit gate opens them:

- PCAP, packet-driver, router admin, BLE, ESP-WIFI-MESH live action, relay,
  XBee, TFT, MicroSD, load, mains, erase, monitor, and serial write expansion.
- Live hardware mutation when fresh identity, preflight, manifest, backups,
  build hashes, recovery commands, physical USB-only state, and cleanup
  conditions are not confirmed in the same session.
- ML acceptance when OCR/CV output does not independently support visible
  dashboard states.

## Validation

This task validates the gate with local fixture tests and scaffold checks only.
Live acceptance remains a separate same-session bench run.
