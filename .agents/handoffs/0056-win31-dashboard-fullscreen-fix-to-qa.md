# Handoff 0056 - Win31 Dashboard Fullscreen Fix To QA

Task:
[../TASK_LOG/0066-win31-dashboard-fullscreen-recovery.md](../TASK_LOG/0066-win31-dashboard-fullscreen-recovery.md)

## Status

Fixed live on the Pi panel and intentionally left open for human confirmation.

## Verified Facts

- DOS-C final proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/final-live-20260527T014831Z/`.
- Pi final proof packet:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/final-live-20260527T014831Z/`.
- DOS-C configs now use X11 video with `fullresolution=1024x600` and
  `windowresolution=1024x600`.
- Rebuilt `OPCON.EXE` SHA-256:
  `49676aac972602388bfafede944bb82cb8971b09845dda8a51820193251761aa`.
- Final capture was `1024x600`, bbox `(0,1)-(1023,599)`, right margin `0 px`,
  bottom margin `0 px`, `X11 main window is 1024 x 600`, no
  `switched to window mode`, and ten bridge transcript lines.
- Live state at handoff: bridge PID `7332`, DOSBox-X PID `7333`, listener
  `127.0.0.1:31332`; screen cleanup is intentionally deferred.

## QA Next Steps

Confirm the physical panel visually, then either accept the running state or
request cleanup. If cleanup is requested, close DOSBox-X and the bridge and
capture no-process/no-listener cleanup evidence.

## Closed Surfaces

Flash, erase, monitor, serial-write expansion, PCAP, packet-driver,
router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load, mains, Gate G
export, and forced tracking of ignored runtime artifacts remain closed.
