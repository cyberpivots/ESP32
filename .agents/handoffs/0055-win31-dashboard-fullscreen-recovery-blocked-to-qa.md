# Handoff 0055 - Win31 Dashboard Fullscreen Recovery Blocked To QA

Task:
[../TASK_LOG/0066-win31-dashboard-fullscreen-recovery.md](../TASK_LOG/0066-win31-dashboard-fullscreen-recovery.md)

## Status

Superseded by
[0056-win31-dashboard-fullscreen-fix-to-qa.md](0056-win31-dashboard-fullscreen-fix-to-qa.md).
This file preserves the earlier failed copied-config-only result before the
X11 fullscreen and compact OPCON layout fix.

## Earlier Verified Facts

- DOS-C failing-state proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-recovery/fullscreen-recovery-20260527T010201Z/`.
- Pi proof packet:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-recovery/fullscreen-recovery-20260527T010201Z/`.
- `wlr-randr`: `HDMI-A-2 "TXD Display"` current/preferred `1024x600`.
- Current dashboard bbox: `(0,0)-(639,479)`.
- Tested Program Manager `win`, current `win /s`, OPCON `win /3`, and OPCON
  `win /3` plus explicit DOSBox-X display config; all remained 640x480.

## Superseding Result

The later X11 fullscreen config plus rebuilt compact OPCON layout produced the
final live proof at
`/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/final-live-20260527T014831Z/`.
