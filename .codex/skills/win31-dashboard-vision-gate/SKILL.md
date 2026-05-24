---
name: win31-dashboard-vision-gate
description: Use when reviewing copied Win31 OPCON screenshots, OCR/CV JSON, and bridge transcript evidence for ESP-NOW BBS completion gates.
---

# Win31 Dashboard Vision Gate

1. Operate only on copied screenshots, transcripts, and cleanup files. Do not drive DOSBox-X, the Pi desktop, serial ports, or live hardware.
2. Run the DOS-C vision gate first when available:
   `python3 scripts/win31_dashboard_vision_gate.py --screenshot-dir <dir> --bridge-transcript <json> --cleanup-proof <txt-or-json> --out <json>`.
3. Require the output status to be `pass` before using screenshots as corroboration.
4. Keep OCR/CV evidence secondary to bridge transcript behavior. If OCR is weak or views are missing, mark the visual result `needs_manual_review`.
5. Preserve the accepted serial-nullmodem path and closed unsafe lanes.

For visible-state expectations, read `references/opcon-visible-states.md`.
