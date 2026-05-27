# Win31 OPCON Pi Desktop Launch Proof Source Ledger

Date: 2026-05-27

Source index ID:
`SRC-LOCAL-WIN31-OPCON-PI-DESKTOP-LAUNCH-PROOF-2026-05-27`

## Sources

- ESP32 task and handoff records:
  `.agents/TASK_LOG/0071-win31-opcon-pi-desktop-launch-proof.md` and
  `.agents/handoffs/0060-win31-opcon-pi-desktop-launch-proof-to-qa.md`.
- DOS-C task and handoff records:
  `/mnt/h/dos-c/.agents/tasks/0041-win31-opcon-pi-desktop-launch-proof.md` and
  `/mnt/h/dos-c/.agents/handoffs/0035-win31-opcon-pi-desktop-launch-proof-to-qa.md`.
- DOS-C implementation files:
  `/mnt/h/dos-c/scripts/ssh/install_pi4_opcon_launchers.sh`,
  `/mnt/h/dos-c/tests/ssh/test_install_pi4_opcon_launchers.sh`, and
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- DOS-C install evidence:
  `/mnt/h/dos-c/artifacts/pi4-poe/ssh-evidence/pi4-opcon-launchers-192.168.200.153-20260527T142600Z.md`.
- DOS-C live proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-opcon-desktop-launch/desktop-launch-20260527T142426Z/`.

## Verified Facts

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- The verified Pi target was `192.168.200.153`, hostname `dos-pi4-poe`,
  Raspberry Pi 4 Model B Rev 1.2, serial `10000000aaaa5b24`.
- The Pi desktop launcher and `dos-c-opcon-win31` icon were installed under
  the `dospi` user profile.
- The Win31 dashboard was launched through the Pi desktop entry.
- Screenshot `desktop-launch-2.png` is `1024x600` and shows the dashboard
  running over `serial-readonly` with three `espnow-enc` peers.
- `bridge-transcript.jsonl` contains 10 serial-nullmodem request records.
- At proof capture time the bridge PID was `10483`, DOSBox-X PID was `10715`,
  and the interface was intentionally left running.

## Assumptions

- Leaving the interface running is the requested endpoint state for this task.

## Unknowns

- Future desktop session restarts may require a normal Raspberry Pi desktop
  refresh before the icon is visually redrawn.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: live Pi installer, desktop-entry launch, screenshot, transcript, and
  left-running proof.
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `/mnt/h/dos-c` `git diff --check`
- PASS: `git diff --check`

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and unsafe controls remain closed.
