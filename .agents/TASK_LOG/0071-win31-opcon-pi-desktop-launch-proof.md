# Task Log 0071 - Win31 OPCON Pi Desktop Launch Proof

- ID: 0071-win31-opcon-pi-desktop-launch-proof
- Date: 2026-05-27
- Contract: `AGENTS.md`
- Status: implemented; validated; left running

## Goal

Coordinate the DOS-C live Raspberry Pi 4 desktop launcher proof for the Win31
OPCON dashboard while preserving the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C task:
  `/mnt/h/dos-c/.agents/tasks/0041-win31-opcon-pi-desktop-launch-proof.md`.
- The verified Pi target was `192.168.200.153`, hostname `dos-pi4-poe`,
  Raspberry Pi 4 Model B Rev 1.2, serial `10000000aaaa5b24`.
- The Pi launcher installer now installs a trusted desktop entry and
  `dos-c-opcon-win31` icon, and stages generated root `OPCON.EXE`,
  `WINDOWS/OPCON.EXE`, and `PMOPCON.EXE`.
- The dashboard was launched through
  `/home/dospi/Desktop/dos-c-opcon-win31.desktop`.
- The DOS-C proof packet is
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-opcon-desktop-launch/desktop-launch-20260527T142426Z/`.
- Screenshot `desktop-launch-2.png` is `1024x600` and shows the Win31 OPCON
  dashboard running over `serial-readonly`.
- `bridge-transcript.jsonl` contains 10 serial-nullmodem request records.
- At proof capture time the bridge PID was `10483`, DOSBox-X PID was `10715`,
  listener `127.0.0.1:31332` was active, and the interface was intentionally
  left running.

## Sources

- [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)
- [../../knowledge-base/source-ledger/2026-05-27-win31-opcon-pi-desktop-launch-proof.md](../../knowledge-base/source-ledger/2026-05-27-win31-opcon-pi-desktop-launch-proof.md)
- DOS-C record:
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-interface-improvement-2026-05-27.md`

## Assumptions

- The requested endpoint state is to leave the Pi interface open after proof,
  not to run the normal cleanup/modal-close sequence.

## Unknowns

- Future desktop session restarts may require the Raspberry Pi desktop to
  refresh `~/Desktop`; the launcher file, trusted metadata, and icon asset are
  installed and verified.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: live Pi launcher install with expected serial guard
- PASS: desktop-entry launch screenshot, transcript, and left-running proof
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `/mnt/h/dos-c` `git diff --check`
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0060-win31-opcon-pi-desktop-launch-proof-to-qa.md](../handoffs/0060-win31-opcon-pi-desktop-launch-proof-to-qa.md).

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and unsafe controls remain closed.
