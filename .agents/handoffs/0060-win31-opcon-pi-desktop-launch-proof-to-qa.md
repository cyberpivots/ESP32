# Handoff 0060 - Win31 OPCON Pi Desktop Launch Proof To QA

- Date: 2026-05-27
- Task: [../TASK_LOG/0071-win31-opcon-pi-desktop-launch-proof.md](../TASK_LOG/0071-win31-opcon-pi-desktop-launch-proof.md)
- Status: ready for QA; runtime intentionally left running

## Summary

The DOS-C Pi desktop launcher was installed on the verified Raspberry Pi 4 and
used to launch the Win31 OPCON dashboard. The proof packet shows the accepted
serial-nullmodem path active, with bridge and DOSBox-X intentionally left
running per user request.

## Evidence

- DOS-C task:
  `/mnt/h/dos-c/.agents/tasks/0041-win31-opcon-pi-desktop-launch-proof.md`
- Install evidence:
  `/mnt/h/dos-c/artifacts/pi4-poe/ssh-evidence/pi4-opcon-launchers-192.168.200.153-20260527T142600Z.md`
- Live proof:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-opcon-desktop-launch/desktop-launch-20260527T142426Z/`
- Screenshot: `desktop-launch-2.png`
- Transcript: `bridge-transcript.jsonl`
- Runtime proof: `left-running-proof.md`

## Runtime State At Handoff

- Bridge PID at proof time: `10483`
- DOSBox-X PID at proof time: `10715`
- Listener: `127.0.0.1:31332`
- Modal check: no `zenity` modal processes found

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and unsafe controls remain closed.

