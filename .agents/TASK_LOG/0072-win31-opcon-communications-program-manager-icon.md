# Task Log 0072 - Win31 OPCON Communications Program Manager Icon

- ID: 0072-win31-opcon-communications-program-manager-icon
- Date: 2026-05-27
- Contract: `AGENTS.md`
- Status: implemented; validated; left running

## Goal

Coordinate the DOS-C live Raspberry Pi 4 Program Manager icon proof for the
Win31 OPCON dashboard while preserving the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C task:
  `/mnt/h/dos-c/.agents/tasks/0042-win31-opcon-communications-program-manager-icon.md`.
- The verified Pi target was `192.168.200.153`, hostname `dos-pi4-poe`,
  Raspberry Pi 4 Model B Rev 1.2, serial `10000000aaaa5b24`.
- The read-only preflight confirmed current remap `COM6`, `COM10`, `COM12` and
  coordinator `/dev/ttyUSB0`, then reported no stale Pi listener/process state
  after cleanup.
- `PMOPCON.EXE` now repairs the `COMMUNICATIONS` Program Manager group and
  leaves old custom groups undeleted.
- The DOS-C proof packet is
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-opcon-program-manager-icon/program-manager-icon-20260527T150844Z/`.
- Screenshot `communications-group.png` shows the `COMMUNICATIONS` group with
  `RETRO-CBBS-NOW Dashboard`.
- Screenshot `dashboard-launched-from-icon.png` shows the Win31 OPCON dashboard
  launched from the selected Program Manager icon.
- `bridge-transcript.jsonl` contains 10 serial-nullmodem request records.
- At proof capture time the bridge PID was `11435`, DOSBox-X PID was `12011`,
  listener `127.0.0.1:31332` was active, and the interface was intentionally
  left running.

## Sources

- [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)
- [../../knowledge-base/source-ledger/2026-05-27-win31-opcon-communications-program-manager-icon.md](../../knowledge-base/source-ledger/2026-05-27-win31-opcon-communications-program-manager-icon.md)
- DOS-C record:
  `/mnt/h/dos-c/knowledge-base/win31-opcon-communications-program-manager-icon-2026-05-27.md`

## Assumptions

- `COMMUNICATIONS` is the requested stable Program Manager group name.
- The requested endpoint state is to leave the icon-launched dashboard open.

## Unknowns

- This proof is not a full Gate H BBS/download/OTAP action run.
- The vision gate is advisory because the proof intentionally left the runtime
  running and did not include all Gate H views/actions.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: read-only live preflight on current remap.
- PASS: live Pi install, Program Manager group screenshot, icon-launched
  dashboard screenshot, transcript, and left-running proof.
- PASS: `/mnt/h/dos-c` `git diff --check`
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0061-win31-opcon-communications-program-manager-icon-to-qa.md](../handoffs/0061-win31-opcon-communications-program-manager-icon-to-qa.md).

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and unsafe controls remain closed.
