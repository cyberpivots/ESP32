# Handoff 0058 - Win31 OPCON Dual Visual Style To QA

Task:
[../TASK_LOG/0069-win31-opcon-dual-style.md](../TASK_LOG/0069-win31-opcon-dual-style.md)

## Status

Implemented in DOS-C, locally validated, and live-captured on the Pi
serial-nullmodem path.

## Verified Facts

- Default OPCON style is Windows 3.1; ANSI Terminal remains selectable.
- The accepted serial-nullmodem path remains unchanged.
- Rebuilt ignored DOS-C `OPCON.EXE` SHA-256:
  `ac5d898cf4275548b80e61caddfa3681358f99c90506cdbd600930a14c557620`.
- Rebuilt ignored DOS-C `OPCONPC.EXE` SHA-256:
  `f6c8ae9f227914db53a2c3f91bd861cdbfae5cd9506aebac437e324bffcf5d85`.
- Validation passed in both DOS-C and ESP32 advisory tests.
- Live copied packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-dual-style/live-dual-style-20260527T040008Z/`.
- Packet contents: 14 screenshots at `1024x600`, including 11 Windows 3.1
  default views and ANSI Terminal Settings, Home, and Safety.
- ESP32 visual-only analyzer reported `visual_only_pass`, mapped target views
  `10/10`, lowest layout margins bottom `29 px` and right `15 px`, and no
  `console_fit_risk`, `log_region_overflow`, or
  `proof_capture_size_mismatch`.
- Cleanup proof reports no DOSBox-X process, no quit-warning modal, no bridge
  process, and no listeners on `31331`, `31332`, or `8080`.

## QA Next Steps

QA can review the copied packet directly. If a full transcript-first
acceptance packet is required later, add the DOS-C vision-gate output and ESP32
completion output to the same copied evidence pattern.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP, packet
driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load,
mains, erase, monitor, serial-write expansion, Gate G export, and forced
tracking of ignored runtime artifacts remain closed.
