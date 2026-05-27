# Win31 OPCON Communications Program Manager Icon Source Ledger

Date: 2026-05-27

Source index ID:
`SRC-LOCAL-WIN31-OPCON-COMMUNICATIONS-PROGMAN-ICON-2026-05-27`

## Sources

- ESP32 task and handoff records:
  `.agents/TASK_LOG/0072-win31-opcon-communications-program-manager-icon.md`
  and
  `.agents/handoffs/0061-win31-opcon-communications-program-manager-icon-to-qa.md`.
- DOS-C task and handoff records:
  `/mnt/h/dos-c/.agents/tasks/0042-win31-opcon-communications-program-manager-icon.md`
  and
  `/mnt/h/dos-c/.agents/handoffs/0036-win31-opcon-communications-program-manager-icon-to-qa.md`.
- DOS-C implementation files:
  `/mnt/h/dos-c/software/win31-progman-helper/src/progman_opcon.c`,
  `/mnt/h/dos-c/software/win31-progman-helper/README.md`,
  `/mnt/h/dos-c/software/win31-operator/README.md`,
  `/mnt/h/dos-c/tests/win31_operator/test_win31_launcher_sources.sh`, and
  `/mnt/h/dos-c/tests/test_win31_dashboard_vision_gate.py`.
- DOS-C knowledge record:
  `/mnt/h/dos-c/knowledge-base/win31-opcon-communications-program-manager-icon-2026-05-27.md`.
- DOS-C install evidence:
  `/mnt/h/dos-c/artifacts/pi4-poe/ssh-evidence/pi4-opcon-launchers-192.168.200.153-20260527T151415Z.md`.
- DOS-C live proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-opcon-program-manager-icon/program-manager-icon-20260527T150844Z/`.
- ESP32 ignored read-only preflight JSON:
  `research/bench-records/live-bench/opcon-program-manager-icon-preflight-20260527T151023Z.json`.

## Verified Facts

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- The verified Pi target was `192.168.200.153`, hostname `dos-pi4-poe`,
  Raspberry Pi 4 Model B Rev 1.2, serial `10000000aaaa5b24`.
- The clean read-only preflight confirmed the current peer remap:
  `peer01=COM6`, `peer02=COM10`, `peer03=COM12`, with coordinator
  `/dev/ttyUSB0`, no stale Pi listeners, and no stale Pi processes.
- DOS-C `PMOPCON.EXE` now creates/repairs uppercase `COMMUNICATIONS` with
  `C:\WINDOWS\OPCOMM.GRP`, item `RETRO-CBBS-NOW Dashboard`, target/icon
  `C:\WINDOWS\OPCON.EXE`, and default directory `C:\WINDOWS`.
- `PMOPCON.EXE` no longer deletes the old `RETRO-CBBS-NOW` group.
- Screenshot `communications-group.png` shows the `COMMUNICATIONS` Program
  Manager group with the dashboard icon selected.
- Screenshot `dashboard-launched-from-icon.png` shows OPCON running after the
  selected Program Manager icon was activated.
- `bridge-transcript.jsonl` contains 10 serial-nullmodem request records.
- At proof capture time the bridge PID was `11435`, DOSBox-X PID was `12011`,
  listener `127.0.0.1:31332` was active, and no `zenity` modal was present.

## Assumptions

- `COMMUNICATIONS` is the requested stable Program Manager group name.
- Leaving the icon-launched dashboard running is the requested endpoint state
  for this proof.

## Unknowns

- This proof does not replace a full Gate H BBS/download/OTAP action run.
- The local vision gate is advisory here because the proof intentionally leaves
  runtime processes running and does not include every full Gate H action/view.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: read-only live preflight on the current remap.
- PASS: live Pi install, `COMMUNICATIONS` group screenshot, icon-launched
  dashboard screenshot, bridge transcript, and left-running proof.
- PASS: `/mnt/h/dos-c` `git diff --check`
- PASS: `git diff --check`
- ADVISORY: `/mnt/h/dos-c` `python3 scripts/win31_dashboard_vision_gate.py ...`
  produced `needs_manual_review` for this narrow icon-launch proof.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and unsafe controls remain closed.
