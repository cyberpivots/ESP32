# Task Log 0066 - Win31 Dashboard Fullscreen Recovery

## Task

- ID: 0066-win31-dashboard-fullscreen-recovery
- Owner role: QA, Communications
- Status: fixed and left open for panel confirmation
- Created: 2026-05-26
- Updated: 2026-05-26
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Coordinate the paired ESP32 record for the DOS-C/Pi Win31 1024x600 fullscreen
recovery while preserving the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C failing-state proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-recovery/fullscreen-recovery-20260527T010201Z/`.
- DOS-C fix proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/`.
- Pi final live proof:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-fullscreen-fix/final-live-20260527T014831Z/`.
- Pi identity, SSH fingerprints, `wlr-randr`, DRM, and `grim` evidence were
  captured fresh.
- The active panel/capture path is `1024x600`; the original Win31 content bbox
  was `(0,0)-(639,479)`.
- Initial copied config tests remained about 640x480.
- The fixed DOS-C path uses X11 video with explicit 1024x600 DOSBox-X
  fullscreen config and a compact OPCON layout for the 640x480 Win31 logical
  surface.
- No ESP32 firmware or protocol surface was changed.
- Final live capture was `1024x600`, bbox `(0,1)-(1023,599)`, right margin
  `0 px`, bottom margin `0 px`, `X11 main window is 1024 x 600`, no
  `switched to window mode`, and ten bridge transcript lines.
- The fixed dashboard was intentionally left open with bridge PID `7332`,
  DOSBox-X PID `7333`, and listener `127.0.0.1:31332`.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-FULLSCREEN-RECOVERY-2026-05-26`
- `SRC-WIN31-WIN-COM-SWITCHES-2026-05-26`
- `SRC-SUNFOUNDER-7INCH-HDMI-1024X600-2026-05-26`
- `SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26`

## Assumptions

- The user-stated SunFounder panel class remains relevant, but exact installed
  product identity is not independently proven by this task.
- The active fix relies on XWayland in the current Pi labwc session.

## Unknowns

- Human usability confirmation on the physical panel.

## Validation

- PASS: Fresh capture and copied-config A/B evidence generated.
- PASS: DOS-C host tests and Open Watcom build passed.
- PASS: Final live proof captured the rebuilt dashboard at full panel size and
  left it open for human confirmation.

## Handoff

Continue with
[../handoffs/0056-win31-dashboard-fullscreen-fix-to-qa.md](../handoffs/0056-win31-dashboard-fullscreen-fix-to-qa.md).

## Stop Surfaces

Do not reopen flash, erase, monitor, serial-write expansion, PCAP,
packet-driver, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD,
load, mains, Gate G export, or forced tracking of ignored runtime artifacts
from this task.
