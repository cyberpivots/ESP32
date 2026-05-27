# Task Log 0068 - Win31 OPCON Dual Style Plan

- ID: 0068-win31-opcon-dual-style-plan
- Date: 2026-05-27
- Contract: [../../AGENTS.md](../../AGENTS.md)
- Status: planning complete; implementation not authorized

## Goal

Plan a source-backed dual visual style system for the DOS-C Windows 3.1 OPCON
dashboard while preserving the accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C OPCON source is under
  `/mnt/h/dos-c/software/win31-operator/`.
- The current dashboard uses hard-coded owner-drawn ANSI colors, fixed-font
  controls, black shell brushes, black `WM_CTLCOLOR`, and current fields
  `g_theme_name` / `g_layout_name` without a real style selector.
- The Settings view currently displays the active theme name and says
  persistence is a later local INI slice.
- The most recent paired ESP32 record reports a copied live proof at
  `1024x600` with visual-only analyzer status `visual_only_pass`, target views
  `10/10`, no `console_fit_risk`, no `log_region_overflow`, and no
  `proof_capture_size_mismatch`.
- Transcript-first DOS-C vision/completion gates remain authoritative;
  screenshot/OCR/CV evidence remains corroborating.

## Sources Inspected

- Local DOS-C source:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`,
  `/mnt/h/dos-c/software/win31-operator/src/operator.rc`,
  `/mnt/h/dos-c/software/win31-operator/include/resource.h`,
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- Local DOS-C records:
  `/mnt/h/dos-c/.agents/tasks/0036-win31-opcon-ui-refinement.md`,
  `/mnt/h/dos-c/.agents/handoffs/0033-win31-opcon-ui-refinement-to-qa.md`,
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-1024x600-gate-h-live-proof-2026-05-26.md`,
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-adaptive-visual-quality-2026-05-26.md`,
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-fullscreen-recovery-2026-05-26.md`.
- Local ESP32 records:
  `.agents/TASK_LOG/0064-win31-dashboard-1024x600-gate-h-live-proof.md`,
  `.agents/TASK_LOG/0065-win31-dashboard-adaptive-visual-quality.md`,
  `.agents/TASK_LOG/0067-win31-opcon-ui-refinement.md`,
  `.agents/handoffs/0057-win31-opcon-ui-refinement-to-qa.md`,
  `knowledge-base/source-ledger/2026-05-27-win31-opcon-ui-refinement.md`.
- External research:
  Microsoft Press, *The Windows Interface: An Application Design Guide*
  (1992); Microsoft Windows 3.1 Programmer's Reference, Volume 1 (1992);
  Microsoft Windows for Workgroups 3.11 User's Guide (1993);
  Microsoft KB 90285; Microsoft Learn `GetSysColor`.

## Assumptions

- v1 should avoid local INI persistence unless implementation explicitly opens
  and tests that risk.
- Win16/Open Watcom feasibility for a menu command and in-session repaint is
  high because the app already handles menu commands, owner-draw buttons,
  `WM_CTLCOLOR`, brush lifetime, and full-window invalidation.

## Unknowns

- Exact Windows 3.1 system color values on the live Win31 installation remain
  runtime facts; implementation should use `GetSysColor`/system brushes rather
  than hard-code them.
- Human operator preference for default Windows 3.1 style versus ANSI style
  remains unmeasured.

## Closed Surfaces

Protocol, transport, PCAP, firmware flashing, relay/XBee, MicroSD, load,
mains, router/admin, BLE, mesh, serial-write expansion, and unsafe control
authority remain closed.
