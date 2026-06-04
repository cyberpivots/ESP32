# CBBS RNW Split Build Install Launch Ledger

Date: 2026-06-04

Source ID:
`SRC-LOCAL-CBBS-RNW-SPLIT-BUILD-INSTALL-LAUNCH-2026-06-04`

## Scope

Tier 3 same-session local Windows 11 debug build/deploy/install/launch gate for
the split React Native Windows apps:

- `apps/cbbs-client-windows` / `CbbsClientWindows`
- `apps/cbbs-sysop-windows` / `CbbsSysopWindows`
- `apps/cbbs-hardware-tools-windows` / `CbbsHardwareToolsWindows`

This record is for local review/testing proof only. It does not accept final
package identity, capability use, signing, Store/App Installer distribution,
release, native HostCommandBridge dispatch, serial/RF/XBee, firmware,
relay/load/mains, wiring, commit, push, PR, or deploy.

## Verified Facts

- Task 0163 generated the split RNW native source trees, but explicitly left
  runtime build/deploy/launch closed.
- Tasks 0164 and 0165 keep live HostCommandBridge dispatch and XBee known-profile
  writes blocked.
- The current user request explicitly opens local build/install/launch on this
  Windows 11 PC for review and testing.
- The reviewer lifecycle was closed after capturing quorum outputs.

## Assumptions

- Debug deploy/install through RNW `run-windows` is the requested "install"
  surface.
- The apps may remain running after launch if needed for user review/testing;
  this is not cleanup acceptance.
- Evidence artifacts may be kept as local proof outside source control.

## Unknowns

- Split native runtime behavior before this gate.
- Installed package full names and package family names.
- Whether debug packages should remain installed after user review.
- Whether generated Debug/AppPackages/bin/obj outputs should be removed before
  a later scaffold-clean validation claim.

## Reviewer Quorum

- Coordinator, weight 5: approved bounded local debug build/deploy/launch.
- RNW DevEx/CI, weight 3: approved operator-run Windows debug smoke proof after
  prerequisites and `--no-telemetry` commands.
- Safety/security, weight 3: conditional approval for fixture-only local debug
  runtime; live HostCommandBridge, serial/RF/XBee, signing, distribution, and
  hardware actions remain closed.
- Protocol/bridge, weight 3: rejected live dispatch and required static and
  runtime no-dispatch evidence before accepting launch.
- QA, weight 3: blocked acceptance until same-session task/source records,
  transcript, package/process/window, screenshot, no-dispatch, and cleanup or
  retention evidence are present.
- Live-bench, weight 3: failed closed until same-session preflight, manifest,
  recovery, visual, closed-surface, and cleanup evidence are present.

Disposition: proceed only within the bounded local debug runtime proof gate,
then update this ledger with the same-session evidence and any unresolved
cleanup or retention state.

## Approved Command Boundary

Only these split-app launch commands are approved for runtime proof, one app at
a time, with `--no-telemetry`:

```bash
pnpm --dir apps/cbbs-client-windows exec react-native run-windows --root . --sln windows\\CbbsClientWindows.sln --proj windows\\CbbsClientWindows\\CbbsClientWindows.vcxproj --arch x64 --no-telemetry
pnpm --dir apps/cbbs-sysop-windows exec react-native run-windows --root . --sln windows\\CbbsSysopWindows.sln --proj windows\\CbbsSysopWindows\\CbbsSysopWindows.vcxproj --arch x64 --no-telemetry
pnpm --dir apps/cbbs-hardware-tools-windows exec react-native run-windows --root . --sln windows\\CbbsHardwareToolsWindows.sln --proj windows\\CbbsHardwareToolsWindows\\CbbsHardwareToolsWindows.vcxproj --arch x64 --no-telemetry
```

## Recovery Path

Stop local debug processes if needed:

```powershell
Get-Process CbbsClientWindows,CbbsSysopWindows,CbbsHardwareToolsWindows -ErrorAction SilentlyContinue | Stop-Process
```

Remove local debug packages if package retention is not desired:

```powershell
Get-AppxPackage *CbbsClientWindows* | Remove-AppxPackage
Get-AppxPackage *CbbsSysopWindows* | Remove-AppxPackage
Get-AppxPackage *CbbsHardwareToolsWindows* | Remove-AppxPackage
```

## Evidence

Evidence root:
`research/bench-records/react-native-windows/cbbs-rnw-split-runtime-20260604T052309Z/`

- Host/toolchain preflight: Windows 11 Pro `10.0.26200`, Node `v24.12.0`,
  pnpm `10.15.0`, Yarn `1.22.22`, .NET SDK `8.0.421` plus newer SDKs, and
  Visual Studio 2022 `17.14.37301.10`.
- Source preflight passed before runtime launch: split app typechecks, split app
  `test:windows` suites, static no-dispatch scan, package-script scan, manifest
  capability scan, and React Native scaffold audit.
- Runtime blocker found and fixed: split app Metro configs did not include the
  monorepo resolver settings needed for Windows Metro to resolve workspace
  packages and RNW's Windows `react-native` entry. The fix added the same
  resolver pattern used by the compatibility app plus app-local
  `reactDevToolsSettingsManager.windows.js` shims.
- Accepted Client screenshot:
  `client-screenshot-final.png`, 2560x1600, SHA-256
  `F553980CA92AEF5FAA8C33E81A1CB5D72B6933F6903DF9DEA83CB3E585E1CAC4`.
- Accepted Sysop screenshot:
  `sysop-screenshot-final.png`, 2560x1600, SHA-256
  `8DBF5CDF5854317D84E875065D51B860AC117116D8BDE9E91025E2598F722003`.
- Accepted Hardware Tools screenshot:
  `hardware-tools-screenshot.png`, 2560x1600, SHA-256
  `88295B3D29F34FB0C86C1DD64898F7FAF44D04A261737B2436A48C4CC4B5A9F4`.
- Rejected screenshots are also retained: initial Client loading-only and Sysop
  stale-Metro redbox captures. They are not acceptance evidence.
- Final package proof:
  `CbbsClientWindows_1.0.0.0_x64__2g54mg31548kg`,
  `CbbsSysopWindows_1.0.0.0_x64__2g54mg31548kg`, and
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`.
- Final process proof: all three app processes were responding and their windows
  were left open for user review/testing.
- Final Metro proof: port `8081` was closed and no Metro/worker targets
  remained after cleanup. Metro is not left running.
- Generated output inventory: 5,983 Debug/obj/bin entries are retained under
  the split native roots while the apps remain available for review.
- `git diff --check` passed. Post-run React Native scaffold audit is deferred
  because it intentionally rejects the retained generated Debug output.

## Final Disposition

Local debug build/deploy/install/launch succeeded for all three split RNW apps.
The apps and local debug packages remain on this Windows 11 PC for user review
and testing. This proof does not accept final package identity, capability use,
signing, Store/App Installer distribution, release, native HostCommandBridge
dispatch, serial/RF/XBee, firmware, relay/load/mains, wiring, commit, push, PR,
or deploy.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, commit, push, PR, deploy, and release.
