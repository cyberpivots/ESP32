# Handoff 0061 - Win31 OPCON Communications Program Manager Icon To QA

- Date: 2026-05-27
- Task: [../TASK_LOG/0072-win31-opcon-communications-program-manager-icon.md](../TASK_LOG/0072-win31-opcon-communications-program-manager-icon.md)
- Status: ready for QA; runtime intentionally left running

## Summary

The DOS-C Program Manager helper now creates/repairs the Win31 OPCON dashboard
icon in `COMMUNICATIONS`. The live proof shows the group icon, launches the
dashboard from that Program Manager icon, and leaves the accepted
serial-nullmodem path running.

## Evidence

- DOS-C task:
  `/mnt/h/dos-c/.agents/tasks/0042-win31-opcon-communications-program-manager-icon.md`
- Install evidence:
  `/mnt/h/dos-c/artifacts/pi4-poe/ssh-evidence/pi4-opcon-launchers-192.168.200.153-20260527T151415Z.md`
- Live proof:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-opcon-program-manager-icon/program-manager-icon-20260527T150844Z/`
- Screenshot: `communications-group.png`
- Screenshot: `dashboard-launched-from-icon.png`
- Transcript: `bridge-transcript.jsonl`
- Runtime proof: `left-running-proof-clean.md`

## Runtime State At Handoff

- Bridge PID at proof time: `11435`
- DOSBox-X PID at proof time: `12011`
- Listener: `127.0.0.1:31332`
- Modal check: no `zenity` modal process

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and unsafe controls remain closed.
