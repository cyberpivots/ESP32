# Task Log 0070 - Win31 Dashboard Interface Improvement Phase 0

- ID: 0070-win31-dashboard-interface-improvement-phase0
- Date: 2026-05-27
- Contract: `AGENTS.md`
- Status: implemented; validated

## Goal

Record the Phase 0 cross-repo planning state and ranked backlog for improving
the Windows 3.1 OPCON dashboard interface, then coordinate DOS-C Phase 1
packaging and Phase 2 launcher implementation slices while preserving the
accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- The new ESP32 backlog is
  [../../docs/projects/espnow-bbs/win31-dashboard-interface-improvement-backlog.md](../../docs/projects/espnow-bbs/win31-dashboard-interface-improvement-backlog.md).
- The paired DOS-C Phase 0 record is
  `/mnt/h/dos-c/.agents/tasks/0038-win31-dashboard-interface-improvement-phase0.md`.
- DOS-C Phase 1 packaging is recorded in
  `/mnt/h/dos-c/.agents/tasks/0039-win31-opcon-package-bundle.md`.
- DOS-C Phase 2 launch is recorded in
  `/mnt/h/dos-c/.agents/tasks/0040-win31-opcon-launchers.md`.
- Phase 1/2 are deployment and launch improvements only; no ESP32 firmware,
  bridge protocol, transport client, live-gate authority, or unsafe-control
  surface was opened.

## Sources

- [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)
- [../../knowledge-base/source-ledger/2026-05-27-win31-dashboard-interface-improvement.md](../../knowledge-base/source-ledger/2026-05-27-win31-dashboard-interface-improvement.md)
- DOS-C record:
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-interface-improvement-2026-05-27.md`

## Assumptions

- Generated OPCON package output remains ignored and untracked.
- Live Pi install/run proof is separate from this documentation and tooling
  implementation.

## Unknowns

- Live Pi launcher installation and screenshot proof remain pending.
- Future persistence and shortcut mapping need a separate accepted file-format
  decision.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: `/mnt/h/dos-c` `git diff --check`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0059-win31-dashboard-interface-improvement-phase0-to-qa.md](../handoffs/0059-win31-dashboard-interface-improvement-phase0-to-qa.md).

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and forced tracking of ignored runtime artifacts remain closed.
