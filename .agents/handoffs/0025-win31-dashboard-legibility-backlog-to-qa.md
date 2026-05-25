# Handoff 0025 - Win31 Dashboard Legibility Backlog To QA

Task:
[../TASK_LOG/0035-win31-dashboard-legibility-research-backlog.md](../TASK_LOG/0035-win31-dashboard-legibility-research-backlog.md)

## Continue With

- Use the accepted baseline packet for before/after comparison:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-viewfinder-full-completion/full-completion-20260524T135020Z/`.
- Use the tracked advisory outputs:
  [../../research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json](../../research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json)
  and
  [../../docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md](../../docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md).
- Treat the top ranked backlog as implementation order unless a later copied
  packet changes the evidence: full Win31 console fit, contrast,
  bottom/status quiet zone, ASCII decoration density, novice wording,
  hierarchy, plain task labels, disabled-control explanations, and revision
  comparison.
- The first DOS-C source pass for full console fit now shortens the OPCON
  Win16 layout and stops forcing a maximized window.
- A revised Pi screenshot packet was captured at
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-opcon-visual-fit/visual-fit-20260524T175101Z/`.
  The advisory analyzer measured 11 screenshots, mapped 10/10 target views,
  reported lowest bottom margin `135 px`, lowest right margin `6 px`, and no
  `console_fit_risk` or `log_region_overflow`.
- DOS-C `win31_dashboard_vision_gate.py` on the revised packet returned
  `status: needs_manual_review` only because counters did not move between
  captured screenshots. Treat visual-fit evidence separately from that
  telemetry-refresh gate.

## Required Evidence Before UI Acceptance

- A copied before/after screenshot packet for every changed target view.
- Advisory analyzer JSON and Markdown for both baseline and revised packet.
- DOS-C `win31_dashboard_vision_gate.py` still passing or explicitly marked
  `needs_manual_review` with reviewer acceptance. The current revised packet
  is in this state because of `counters_not_moving`.
- ESP32 `scripts/espnow_bbs_live_gate.py complete` still passing when the
  revision is part of a live completion packet.
- No weakening of transcript-first acceptance or cleanup evidence.

## Closed Gates

This backlog does not authorize firmware changes, bridge wire-protocol
changes, live hardware mutation, live mesh file delivery, live flashing, relay,
XBee, TFT, MicroSD, load, mains, erase, monitor, serial writes, PCAP,
packet-driver, router-admin work, PaddleOCR, or hosted vision.

Any future UI implementation must preserve the accepted
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`
proof path unless a later accepted ADR changes that path.
