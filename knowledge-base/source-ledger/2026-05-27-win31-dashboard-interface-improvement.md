# Win31 Dashboard Interface Improvement Source Ledger

Date: 2026-05-27

Source index ID:
`SRC-LOCAL-WIN31-DASHBOARD-INTERFACE-IMPROVEMENT-2026-05-27`

## Sources

- ESP32 backlog:
  `docs/projects/espnow-bbs/win31-dashboard-interface-improvement-backlog.md`.
- ESP32 task and handoff records:
  `.agents/TASK_LOG/0070-win31-dashboard-interface-improvement-phase0.md` and
  `.agents/handoffs/0059-win31-dashboard-interface-improvement-phase0-to-qa.md`.
- DOS-C knowledge record:
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-interface-improvement-2026-05-27.md`.
- DOS-C tasks:
  `/mnt/h/dos-c/.agents/tasks/0038-win31-dashboard-interface-improvement-phase0.md`,
  `/mnt/h/dos-c/.agents/tasks/0039-win31-opcon-package-bundle.md`, and
  `/mnt/h/dos-c/.agents/tasks/0040-win31-opcon-launchers.md`.
- DOS-C implementation files:
  `/mnt/h/dos-c/scripts/package_win31_opcon_bundle.sh`,
  `/mnt/h/dos-c/scripts/ssh/install_pi4_opcon_launchers.sh`,
  `/mnt/h/dos-c/software/win31-operator/src/opcon.ico`,
  `/mnt/h/dos-c/software/win31-operator/src/operator.rc`,
  `/mnt/h/dos-c/software/win31-operator/include/resource.h`,
  `/mnt/h/dos-c/software/win31-progman-helper/src/progman_opcon.c`, and
  `/mnt/h/dos-c/software/win31-progman-helper/src/progman_opcon.rc`.
- DOS-C tests:
  `/mnt/h/dos-c/tests/win31_operator/test_package_win31_opcon_bundle.sh`,
  `/mnt/h/dos-c/tests/win31_operator/test_win31_launcher_sources.sh`, and
  `/mnt/h/dos-c/tests/ssh/test_install_pi4_opcon_launchers.sh`.

## Verified Facts

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Phase 0 created a ranked backlog and cross-repo coordination records.
- Phase 1 added DOS-C package tooling for generated Win31 OPCON artifacts.
- Phase 2 added DOS-C launcher tooling for Program Manager and Pi desktop
  launch presentation.
- Program Manager launch remains DDE-based through `PMOPCON.EXE`.
- The Pi launcher script uses the serial-nullmodem DOSBox-X config and
  installs user-level launcher files only.
- Generated package output, generated binaries, licensed Windows files,
  `.GRP` files, secrets, captures, logs, SQLite spools, firmware images, and
  bulky runtime trees remain untracked.

## Assumptions

- Archive packaging may include generated Open Watcom `.EXE` outputs only from
  ignored generated paths.
- Launch installation is a deployment convenience and does not by itself prove
  live dashboard behavior.

## Unknowns

- Live Pi launcher installation and screenshot proof remain pending until the
  user explicitly requests that live action after same-session identity checks.
- Keyboard shortcuts, gauges, expanded configuration screens, and persistence
  remain future backlog items.

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

## Generated Artifact Hashes

- Ignored DOS-C `artifacts/pi4-poe/winroot/OPCON.EXE` SHA-256:
  `321921c1d3f016363fcfe712457dee02c9544b35342289a40132897ad56669ab`.
- Ignored DOS-C `artifacts/pi4-poe/winroot/OPCONPC.EXE` SHA-256:
  `846ad97147c7044b72162ffe274ad3b5064d6c6df301f82b4a491a11bdd3b2fc`.
- Ignored DOS-C `artifacts/pi4-poe/winroot/PMOPCON.EXE` SHA-256:
  `99f9b82d9ee8abe053a746d6605091866041168456bf3c19642f038207d999f3`.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and forced tracking of ignored runtime artifacts remain closed.
