# Win31 Dashboard Fullscreen Recovery Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-WIN31-DASHBOARD-FULLSCREEN-RECOVERY-2026-05-26`
- `SRC-WIN31-WIN-COM-SWITCHES-2026-05-26`
- `SRC-SUNFOUNDER-7INCH-HDMI-1024X600-2026-05-26`
- `SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-ADAPTIVE-VISUAL-QUALITY-2026-05-26`

## Scope

Source-backed paired ESP32 record for the DOS-C/Pi fullscreen recovery and fix
on the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Evidence

- DOS-C failing-state proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-recovery/fullscreen-recovery-20260527T010201Z/`.
- DOS-C fix proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/`.
- Pi final live proof:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/final-live-20260527T014831Z/`.
- ESP32 ignored evidence summary:
  `research/bench-records/live-bench/win31-dashboard-fullscreen-recovery-20260527T010201Z/`.
- Paired DOS-C record:
  `/mnt/h/dos-c/knowledge-base/win31-dashboard-fullscreen-recovery-2026-05-26.md`.

## Verified Facts

- Pi identity matched `dos-pi4-poe`, Raspberry Pi 4 Model B Rev 1.2, serial
  `10000000aaaa5b24`, root `/dev/mmcblk0p2`.
- `wlr-randr` reported `HDMI-A-2 "TXD Display"` current/preferred
  `1024x600`; DRM reported connected/enabled HDMI-A-2; `grim` captures were
  `1024x600`.
- Original Win31 dashboard capture bbox was `(0,0)-(639,479)`, with `384 px`
  right and `120 px` bottom margin.
- Initial Program Manager/current `win /s`/OPCON `win /3`/explicit DOSBox-X
  display config tests all remained about 640x480.
- The accepted fix uses DOSBox-X X11 video with explicit `1024x600`
  fullscreen resolution.
- DOS-C `devices/pi4-poe/win31.conf` and
  `devices/pi4-poe/win31-serial-nullmodem.conf` were updated with
  `fullresolution=1024x600`, `windowresolution=1024x600`, and
  `videodriver=x11`.
- DOS-C `software/win31-operator/src/operator.c` was updated to compact the
  status, navigation, action, and disabled-control rows for the 640-logical-pixel
  Win31 surface.
- Rebuilt staged `OPCON.EXE` SHA-256:
  `49676aac972602388bfafede944bb82cb8971b09845dda8a51820193251761aa`.
- Final live capture was `1024x600`, bbox `(0,1)-(1023,599)`, right margin
  `0 px`, bottom margin `0 px`, `X11 main window is 1024 x 600`, no
  `switched to window mode`, and ten bridge transcript lines.
- The fixed dashboard was intentionally left open with bridge PID `7332`,
  DOSBox-X PID `7333`, and listener `127.0.0.1:31332`.

## Assumptions

- SunFounder remains the user-stated display class; the active HDMI output is
  locally identified as `TXD Display`.
- The active fix relies on XWayland in the current Pi labwc session.

## Unknowns

- Human usability confirmation on the physical touchscreen.

## Validation

- PASS: Fresh identity/display/process/log/screenshot capture.
- PASS: Failed copied-config A/B runs preserved.
- PASS: DOS-C host tests passed: `bash tests/win31_operator/run_host_tests.sh`.
- PASS: DOS-C Open Watcom build passed: `bash software/win31-operator/build-watcom.sh`.
- PASS: Final live proof captured the rebuilt dashboard at full panel size and
  left it open for human confirmation.

## Closed Surfaces

Firmware flashing, erase, monitor, serial-write expansion, PCAP, packet-driver,
router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load, mains, Gate G
export, and forced tracking of ignored runtime artifacts remain closed.
