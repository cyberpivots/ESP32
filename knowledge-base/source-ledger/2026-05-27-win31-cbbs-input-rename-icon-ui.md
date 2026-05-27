# Win31 CBBS Input, Rename, Icon, And UI Source Ledger

Date: 2026-05-27

Source index ID:
`SRC-LOCAL-WIN31-CBBS-INPUT-RENAME-ICON-UI-2026-05-27`

## Sources

- DOS-C knowledge record:
  `/mnt/h/dos-c/knowledge-base/win31-cbbs-input-rename-icon-ui-2026-05-27.md`.
- DOS-C task and handoff:
  `/mnt/h/dos-c/.agents/tasks/0043-cbbs-input-rename-icon-ui.md` and
  `/mnt/h/dos-c/.agents/handoffs/0037-cbbs-input-rename-icon-ui-to-qa.md`.
- DOS-C implementation and tests:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`,
  `/mnt/h/dos-c/software/win31-operator/src/operator.rc`,
  `/mnt/h/dos-c/software/win31-operator/src/opcon.ico`,
  `/mnt/h/dos-c/software/win31-progman-helper/src/progman_opcon.c`,
  `/mnt/h/dos-c/scripts/ssh/install_pi4_opcon_launchers.sh`,
  `/mnt/h/dos-c/scripts/package_win31_opcon_bundle.sh`,
  `/mnt/h/dos-c/scripts/win31_dashboard_vision_gate.py`,
  `/mnt/h/dos-c/tests/test_win31_dashboard_vision_gate.py`,
  `/mnt/h/dos-c/tests/win31_operator/test_win31_launcher_sources.sh`,
  `/mnt/h/dos-c/tests/win31_operator/test_package_win31_opcon_bundle.sh`,
  and `/mnt/h/dos-c/tests/ssh/test_install_pi4_opcon_launchers.sh`.
- Ignored same-session input inventory:
  `/mnt/h/dos-c/artifacts/pi4-poe/ssh-evidence/cbbs-input-inventory-20260527T161148Z.md`.
- Ignored same-session ESP32/Pi read-only preflight:
  `research/bench-records/live-bench/cbbs-input-rename-preflight-20260527T161004Z.json`.
- External input/focus references recorded in DOS-C source index:
  DOSBox-X mouse support, DOSBox-X reference full configuration, labwc config,
  libinput helper tools, SDL environment variables, and Program Manager DDE
  references.

## Verified Facts

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- DOS-C user-facing Win31 title and Pi launcher name are now `CBBS`.
- Internal Win31 binary names remain `OPCON.EXE`, `OPCONPC.EXE`, and
  `PMOPCON.EXE`.
- `PMOPCON.EXE` stays DDE-only and now best-effort deletes the stale
  `RETRO-CBBS-NOW Dashboard` item before replacing/adding `CBBS`.
- Active package/launcher artifact prefixes now use `cbbs-win31`.
- The copied-screenshot gate now fails closed on stale `RETRO` branding or
  `OPCON Dashboard` Program Manager text when those screenshots are present.
- The tracked Win31 icon is one `16x16`, `16-color`, `4 bits/pixel` original
  `.ico`, SHA-256
  `1259ba746bdb4cfd69ace76bd208137c15f58c2d969d8e99bac13cc6201af8b8`.
- The same-session input inventory found `ZY.Ltd ZY Control Mouse` at
  `/dev/input/event5` and touch input at `/dev/input/event8`.
- The same-session preflight verified current host/serial/peer identities but
  returned `ok:false` due to stale listener `127.0.0.1:31332` and stale
  bridge/DOSBox-X runtime from the previous proof.

## Assumptions

- `CBBS` is the accepted user-facing interface name.
- The visible `ZY.Ltd ZY Control Mouse` is the candidate physical pointer path,
  but device enumeration alone does not prove movement through DOSBox-X/Win31.

## Unknowns

- Wireless pointer root cause is not proven.
- Permanent pointer fix is not accepted.
- No physical movement/click A/B matrix was captured for Pi desktop,
  DOSBox-X focus, Program Manager, and CBBS.
- No fresh live screenshot proves the new Program Manager `CBBS` item/icon.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `python3 tests/test_win31_dashboard_vision_gate.py`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: `python3 scripts/verify_scaffold.py`

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
tracked Pi DOSBox-X mouse config mutation, and unsafe controls remain closed.
