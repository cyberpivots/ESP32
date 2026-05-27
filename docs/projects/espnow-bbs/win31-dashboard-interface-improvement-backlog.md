# Win31 Dashboard Interface Improvement Backlog

Date: 2026-05-27

## Scope

This is the Phase 0 cross-repo backlog for improving the Windows 3.1 OPCON
dashboard interface while preserving the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

The first implementation slices are DOS-C packaging and launch work:

- Phase 0 DOS-C record:
  `/mnt/h/dos-c/.agents/tasks/0038-win31-dashboard-interface-improvement-phase0.md`.
- Phase 1 DOS-C package slice:
  `/mnt/h/dos-c/.agents/tasks/0039-win31-opcon-package-bundle.md`.
- Phase 2 DOS-C launcher slice:
  `/mnt/h/dos-c/.agents/tasks/0040-win31-opcon-launchers.md`.
- Current CBBS rename/icon/input/UI slice:
  `/mnt/h/dos-c/.agents/tasks/0043-cbbs-input-rename-icon-ui.md`.

## Source Basis

- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-GATE-H-LIVE-PROOF-2026-05-26`
  records the accepted 1024x600 Gate H proof and the advisory fit risks that
  make packaging/launch/refinement useful.
- `SRC-LOCAL-WIN31-OPCON-UI-REFINEMENT-2026-05-27` records the current
  computed layout, plain-label, and maximized Win31 OPCON source baseline.
- `SRC-LOCAL-WIN31-OPCON-DUAL-STYLE-2026-05-27` records the default
  Windows 3.1 style, selectable ANSI style, and deferred persistence choice.
- `SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26` and
  `SRC-DOSBOX-SERIAL-CONFIG` support the tracked DOSBox-X config surface.
- `SRC-RASPBERRY-PI-CONFIGURATION` supports keeping Pi identity and SSH
  launcher installation evidence source-backed.
- `SRC-LOCAL-DOSC-WIN31-DASHBOARD-INTERFACE-IMPROVEMENT-2026-05-27` records
  the paired DOS-C Phase 0/1/2 implementation records for this backlog.
- `SRC-LOCAL-WIN31-CBBS-INPUT-RENAME-ICON-UI-2026-05-27` records the current
  CBBS user-facing rename, icon replacement, primary UI plain-language pass,
  stale-branding screenshot guard, and blocked live input diagnosis.

## Ranked Backlog

1. Archive packaging for deployable Win31 OPCON artifacts.
2. Program Manager plus Pi desktop launch.
3. Non-technical plain-language view text and disabled-control explanations.
4. Expanded Settings/Wizard configuration screens.
5. Win16-safe charts, status lamps, bars, and analog gauges.
6. Keyboard shortcuts and later customizable mapping.
7. Future persistence strategy for style/settings/shortcuts after an explicit
   file-format decision.

## Verified Facts

- DOS-C now owns the implementation surface for Win31 OPCON packaging and
  desktop launch scripts.
- The package slice is constrained to generated OPCON binaries, tracked
  DOSBox-X configs, README, manifest, and checksums.
- The launcher slice is constrained to the accepted serial-nullmodem config
  and user-level Pi launch entries.
- Program Manager launch remains DDE-based through `PMOPCON.EXE`; direct
  `.GRP` editing remains out of scope.
- Current user-facing name is `CBBS`; historical OPCON/RETRO records are
  superseded for current UI naming.
- Pointer root cause/fix is not accepted; current evidence is input inventory
  only and live acceptance is blocked by stale runtime plus missing physical
  A/B proof.
- The backlog does not change bridge protocol, ESP32 firmware, live-gate
  authority, PCAP, router/admin, relay/XBee, BLE, mesh runtime, flash, erase,
  monitor, serial-write expansion, or unsafe controls.

## Assumptions

- Generated Open Watcom `.EXE` artifacts may be bundled only in ignored
  package output; generated package directories and archives stay untracked.
- Packaging and launcher installation are deployment ergonomics, not a new
  live proof packet.

## Unknowns

- A live Pi launcher install was not run in Phase 0/1/2 without a same-session
  user request and Pi identity confirmation.
- Future persistence for style/settings/shortcuts still needs an explicit
  file-format decision before implementation.
- A fresh CBBS Program Manager/icon live proof has not been captured after the
  current rename/icon pass.

## Next Implementation Slices

- Complete Phase 1 archive packaging validation in DOS-C and use the package
  only from ignored output.
- Complete Phase 2 live launcher proof only after a fresh Pi identity check
  and explicit user request to install/run it.
- For CBBS live acceptance, start with fresh preflight, resolve or explicitly
  preserve stale runtime, capture physical input A/B proof, and then capture
  Program Manager `COMMUNICATIONS` showing item `CBBS`.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
and forced tracking of ignored runtime artifacts remain closed.
