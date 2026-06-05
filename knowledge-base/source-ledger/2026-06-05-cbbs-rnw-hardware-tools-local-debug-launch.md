# CBBS RNW Hardware Tools Local Debug Launch Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-LOCAL-DEBUG-LAUNCH-2026-06-05`

## Scope

Tier 3 local RNW runtime launch for `CbbsHardwareToolsWindows` only. This
ledger records local Debug build output, package registration repair, app
launch, Metro proof, and screenshot proof for user review.

This ledger does not authorize release packaging, signing, Store/App Installer
distribution, native HostCommandBridge dispatch, shell/DOS-C execution,
serial/RF/XBee writes, firmware flash/erase/monitor, relay/load/mains work,
wiring, BLE/Web Serial/Web Bluetooth, SoftAP/local-network discovery, commit,
push, PR, deploy, or release.

## Verified Facts

- The retained `CbbsHardwareToolsWindows` registration initially had an empty
  `InstallLocation` and did not produce a running process after shell
  activation.
- App-local Hardware Tools Metro was already running on `127.0.0.1:8081`.
- `react-native run-windows --no-telemetry` failed before launch with the known
  Visual Studio discovery error: `The "path" argument must be of type string.
  Received undefined`.
- Direct MSBuild with `RunAutolinkCheck=false` built the local Debug layout
  without rewriting generated native auto-link source files.
- Windows rejected unsigned Debug MSIX installation because the package
  publisher was not in the unsigned namespace.
- The unpacked Debug layout registered successfully after removing the stale
  local Debug registration.
- `CbbsHardwareToolsWindows` launched and remained responding as PID `47248`.
- Metro inspector reported the connected app ID
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`.
- Fresh screenshot proof exists at
  `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/hardware-tools-launch-screen.png`,
  6400x3497, SHA-256
  `CB80E4401A8BF66146BAF253205B2D926B72CDD4501C6B374D571090F293EF8B`.

## Assumptions

- The user's launch request authorized only the local Debug review launch
  needed to make the app visible, not release packaging or hardware action.
- Retaining the app, Metro server, package registration, and generated Debug
  output is useful for immediate review.

## Unknowns

- Final Windows package identity, capability acceptance, signing, distribution,
  and release path remain unresolved.
- Native HostCommandBridge implementation, live adapter behavior, and recovery
  path remain unresolved.
- Serial/RF/XBee behavior and hardware behavior remain unresolved.

## Evidence Artifacts

- `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/hardware-tools-launch-screen.png`
- `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/hardware-tools-launch-screenshot-meta.json`
- `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/process-package.json`
- `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/metro-status.txt`
- `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/metro-inspector.json`

## Retained Local State

- `CbbsHardwareToolsWindows` app process remains running for review.
- App-local Metro remains running on `127.0.0.1:8081`.
- Local Debug generated output under
  `apps/cbbs-hardware-tools-windows/windows/` remains for the running app.
- Local Debug app registration remains installed.

## Decision

Decision: accept local Debug launch for review only. Do not treat this as
scaffold-clean, signing, release, Store/App Installer distribution, live bridge,
or hardware evidence.
