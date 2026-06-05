# CBBS RNW Hardware Tools Debug Metro Incident Ledger

Date: 2026-06-04

Source ID:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-METRO-INCIDENT-2026-06-04`

## Scope

Tier 3 local RNW runtime incident response for the retained
`CbbsHardwareToolsWindows` Debug package, plus Tier 2 guardrail updates for
project instructions and skills.

This ledger records local debug runtime repair only. It does not authorize live
bridge dispatch, serial/RF/XBee, firmware, relay/load/mains, wiring, signing,
Store/App Installer packaging, release, PR, push, deploy, or hardware action.

## Verified Facts

- The retained Debug `CbbsHardwareToolsWindows` package exists as
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`.
- The generated Debug app loads `index` from Metro when `BUNDLE` is not set.
- Before recovery, same-session checks found no Metro server on `8081`, no
  Windows `node` process, and no live Hardware Tools process.
- A retry of the approved `run-windows --no-telemetry` command failed in RNW's
  Visual Studio discovery before relaunch.
- Starting the matching app-local Metro server and then launching the installed
  Debug package produced a loaded Hardware Tools UI.

## Evidence

- Failing state: `Invoke-WebRequest http://127.0.0.1:8081/status` failed and
  process inventory showed no `CbbsHardwareToolsWindows` process.
- Recovery Metro command: `pnpm --dir apps/cbbs-hardware-tools-windows exec
  react-native start --port 8081 --reset-cache --no-interactive --verbose`.
- First recovery screenshot:
  `C:\Users\cyber\AppData\Local\Temp\cbbs-hardware-tools-repair-screenshot.png`,
  2560x1600, SHA-256
  `73D69C7C9365C49E3BCDF55655B3DF83E51E1D115AE66875BE69C69B51B0E848`,
  rejected because it showed loading-only UI.
- Accepted recovery screenshot after app restart against detached Metro:
  `C:\Users\cyber\AppData\Local\Temp\cbbs-hardware-tools-repair-screenshot-clean-2.png`,
  2560x1600, SHA-256
  `8E2121FA9F885726EDB94B1B2075EF4316292B1FF45859FA1C5F7ABB9192DA83`,
  visible Hardware Tools UI, no redbox, no loading-only state.
- The prior warning strip was traced through the Metro inspector to stale
  `Cannot connect to Metro` state from the bad direct launch. Restarting the app
  with detached Metro already running cleared the warning strip; the final
  inspector check showed only React Native debugger info/log entries.
- Final app process: PID `46928`, title `CbbsHardwareToolsWindows`,
  responding `True`.
- Final Metro proof: WSL and Windows returned `packager-status:running` for
  `http://127.0.0.1:8081/status`.
- Final Metro inspector proof listed `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`
  as connected to the detached Metro server.
- Detached Metro process retained for review: PID `935586`.

## Recurrence Guardrail

Do not direct-launch retained RNW Debug packages for review unless the matching
app-local Metro server is already proven live. Prefer the app-local
`run-windows --no-telemetry` command. If `run-windows` is unavailable but the
Debug package is already installed, start app-local Metro first, launch the app
registration second, and accept only a fresh loaded UI screenshot with no redbox
and no loading-only state.

Run only one split RNW app/Metro pairing at a time. Stop stale Metro/Node
workers before switching between Client, Sysop, and Hardware Tools.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, commit, push, PR, deploy, and release.

## Final Result

The local Debug Hardware Tools app is repaired for review with app-local Metro
running. The app and detached Metro server remain running intentionally.
