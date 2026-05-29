# Source Ledger - 2026-05-29 XCTU Download And Install

## Scope

Tier 2 host-tooling evidence for downloading and installing Digi XCTU as a GUI
reference tool. This task installed host software only. It did not open serial
ports, discover/add XBee devices, read radio settings, write radio settings,
send API transmit frames, update/recover firmware, run range tests, wire an
ESP32 carrier, or touch relay/load/mains hardware.

## Verified facts

- Digi's official XCTU support path listed `XCTU v. 6.5.13 Windows x86:x64`,
  Windows asset detail size 230.5 MB, version `v. 6.5.13`, version date
  2023-07-17, and direct download filename `40003026_AL.exe`. Source ID:
  `SRC-DIGI-XCTU-SUPPORT-2026-05-29`.
- The downloaded `40003026_AL.exe` file was 241,696,728 bytes and had SHA-256
  `9b6acd16927ee17d4f3a728768cd1c559e09ab6b12470fd6da08e7106fb308e1`.
  Source ID: `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- Windows file metadata on the installer reported product `XCTU`, product
  version `6.5.13.2`, company `Digi International Inc.`, and original filename
  `XCTU.exe`. Authenticode status reported signature verified for Digi
  International Inc. Source ID: `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- Silent NSIS-style install attempts returned exit code 1 and did not install
  XCTU. The GUI installer completed with the default per-user path under
  `%LOCALAPPDATA%\Digi\XCTU-NG\XCTU.exe`. Source ID:
  `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- The GUI install launched the bundled Digi USB RF Device Drivers setup.
  Windows Security prompted for Digi International device software; the
  persistent trust checkbox was kept off and the driver components were
  installed once. Source ID: `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- First XCTU launch showed the XCTU 6.5.13 change-log window headed
  `XCTU 6.5.13 - June 2nd, 2023`; no separate application update prompt was
  observed. Source ID: `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- Post-install `scripts/xbee_radio_study.py inventory --json` found the
  per-user `XCTU-NG` executable path and still reported
  `serialOpenAttempted: false`. Source ID:
  `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.

## Evidence records

- Local-only ignored evidence directory:
  `research/bench-records/xctu-install/local-20260529T033010Z/`.
- Key local files include pre/post inventory JSON, HTTP download headers,
  installer hash, Authenticode summary, Windows uninstall record, installer
  screenshots, first-run screenshot, and `install-summary.txt`.
- The installer binary, screenshots, raw inventories, and local prompt captures
  are not committed to the repository.

## Closed gates

- No serial port was opened by the repo inventory command.
- No XCTU Add/Discover action was clicked.
- No AT console, API console, firmware explorer, firmware update/recovery,
  range test, profile write, or API transmit operation was used.
- No `WR`, `AC`, setting-value AT command, radio reset, or factory restore was
  attempted.
- No ESP32 DIN/DOUT wiring, relay/load/mains action, or live RF evidence was
  performed.

## Remaining blockers

- Any local XBee adapter identity remains unresolved until disconnect/delta
  evidence or an explicit read-only identification gate proves it.
- Any radio settings backup/readback, profile target review, setting write,
  firmware operation, range test, or transmit exercise remains blocked behind a
  future Tier 3 gate with same-session evidence, rollback, reviewer quorum, and
  explicit operator authority.
