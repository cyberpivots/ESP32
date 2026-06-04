# CBBS React Native Windows Build Launch Integrated Ledger

Date: 2026-06-03

Source IDs:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-BUILD-LAUNCH-INTEGRATED-2026-06-03`,
`SRC-REACT-NATIVE-WINDOWS-RUN-WINDOWS-2026-06-03`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`,
`SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`,
`SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`,
`SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`

## Scope

Local Windows PC RNW build/deploy/launch evidence plus app-surface integration
for mesh discovery, XBee radio configuration/readback, XBee OTA link, and
firmware flash evidence.

## Verified Facts

- `react-native run-windows` was executed from the Windows host side with
  `--no-telemetry`, the generated solution, generated vcxproj, and `x64`.
- RNW restore, autolinking, Debug x64 build, deploy, loopback exemption, and app
  start completed successfully.
- Live Metro served the Windows bundle at 5,133,923 bytes, SHA-256
  `FDD80512D04989C0A8F83FC4BD16181A5BCAE38ACFFE0DA5D5A944EB72633BC9`, with RNW
  Windows module markers and the `CbbsWindows` registration marker.
- Windows process verification found process `CbbsWindows`, PID `29964`, window
  title `CbbsWindows`, and `Responding=true`.
- Focused screenshot evidence was captured at
  `research/bench-records/react-native-windows/cbbs-windows-window-final.png`
  and shows the integrated mesh, XBee, and firmware flash app surface without
  the previous RNW redbox.
- Windows package verification found package
  `CbbsWindows_1.0.0.0_x64__2g54mg31548kg` installed from the app-local Debug
  AppX output path.
- The app source exposes `mesh_discovery.v1` request names, XBee selected-port
  programming/readback records, XBee OTA link proof records, COM6 bridge
  flash/retest records, and PF0530W live flash evidence records.

## Unknowns

- Final package identity, signing, packaging, Store/App Installer path, public
  distribution, and update policy.
- Current cause of the Jest hang in this session.
- Whether generated native `packages.lock.json` files should be tracked or
  ignored.

## Validation

- `pnpm --filter @cbbs/windows-spike typecheck`
- `git diff --check`
- Live Metro bundle request/hash/marker check
- Windows RNW `run-windows` build/deploy/launch
- Windows process/package verification
- Focused Windows screenshot capture

Note: `scripts/scaffold_audit_react_native.py` fails immediately after
`run-windows` because the successful Debug build creates `obj`, `x64/Debug`,
`bin`, and `AppPackages` outputs under the native project. Those outputs remain
because the app is running from the Debug AppX layout.

## Authority Limits

This ledger proves local Windows debug build/deploy/launch only. It does not
prove signing, Store/App Installer distribution, release, relay/load/mains
operation, new XBee setting writes, new RF range/throughput, firmware update
recovery, or new flash activity beyond previously recorded source evidence.
