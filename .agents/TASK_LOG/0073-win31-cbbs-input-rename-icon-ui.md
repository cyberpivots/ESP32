# Task Log 0073 - Win31 CBBS Input, Rename, Icon, And UI

- ID: 0073-win31-cbbs-input-rename-icon-ui
- Date: 2026-05-27
- Contract: `AGENTS.md`
- Status: implemented locally; validated; live input acceptance blocked

## Goal

Coordinate the paired DOS-C CBBS rename/icon/UI implementation and read-only
input diagnosis record while preserving the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C task:
  `/mnt/h/dos-c/.agents/tasks/0043-cbbs-input-rename-icon-ui.md`.
- User-facing Win31/Pi launcher naming is now `CBBS`; internal Win31 binary
  names remain unchanged.
- Program Manager repair remains DDE-only, adds item `CBBS`, and best-effort
  deletes stale item `RETRO-CBBS-NOW Dashboard`.
- Primary CBBS navigation is Status, Messages, Files, Devices, and Help.
- The original tracked icon is Win31-compatible `16x16`, `16-color`,
  `4 bits/pixel`, SHA-256
  `1259ba746bdb4cfd69ace76bd208137c15f58c2d969d8e99bac13cc6201af8b8`.
- Same-session Pi input inventory found `ZY.Ltd ZY Control Mouse` at
  `/dev/input/event5`; this proves Linux input visibility only.
- Same-session read-only preflight returned `ok:false` due stale Pi listener
  and bridge/DOSBox-X processes from the previous Program Manager proof.

## Sources

- [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)
- [../../knowledge-base/source-ledger/2026-05-27-win31-cbbs-input-rename-icon-ui.md](../../knowledge-base/source-ledger/2026-05-27-win31-cbbs-input-rename-icon-ui.md)
- DOS-C record:
  `/mnt/h/dos-c/knowledge-base/win31-cbbs-input-rename-icon-ui-2026-05-27.md`

## Assumptions

- `CBBS` is the current exact user-facing interface name.
- The visible HID pointer is the candidate physical input path, not proof of
  DOSBox-X/Win31 behavior.

## Unknowns

- Wireless pointer root cause and fix remain unproven.
- No physical movement/click A/B matrix was captured.
- No fresh live CBBS Program Manager/icon screenshot was captured.

## Validation

- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-progman-helper/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash tests/ssh/test_install_pi4_opcon_launchers.sh`
- PASS: `/mnt/h/dos-c` `python3 tests/test_win31_dashboard_vision_gate.py`
- PASS: `/mnt/h/dos-c` `bash scripts/package_win31_opcon_bundle.sh --dry-run`
- PASS: `/mnt/h/dos-c` `bash scripts/verify_scaffold.sh`
- PASS: `python3 scripts/verify_scaffold.py`

## Handoff

Continue with
[../handoffs/0062-win31-cbbs-input-rename-icon-ui-to-qa.md](../handoffs/0062-win31-cbbs-input-rename-icon-ui-to-qa.md).

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
tracked Pi DOSBox-X mouse config mutation, and unsafe controls remain closed.
