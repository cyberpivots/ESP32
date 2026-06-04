# Task 0157: CBBS React Native Windows Build Launch Integrated

Status: completed; local Windows build/deploy/launch succeeded

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-RUN-WINDOWS-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`,
`SRC-DIGI-XBP9B-DPUT-001`,
`SRC-DIGI-XBEE-900HP-AP`,
`SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`,
`SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`,
`SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`,
`SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`

## Goal

Build and launch the RNW app on the local Windows PC, and integrate mesh
network device, XBee radio configuration/readback, XBee OTA link, and firmware
flash evidence surfaces into the Windows app.

## Routing Packet

- Verified facts: `apps/cbbs-windows/windows/CbbsWindows.sln` and
  `windows/CbbsWindows/CbbsWindows.vcxproj` exist; the JS app registers
  `CbbsWindows`; RNW `run-windows` builds, deploys, and starts by default;
  source records exist for `mesh_discovery.v1`, selected-port XBee programming,
  bidirectional XBee link proof, COM6 XBee bridge flash/retest, and PF0530W
  COM6 live flash evidence.
- Assumptions: the user's same-session safe-state and repeated build/launch
  instructions are explicit local operator authority for W4B/W4C build,
  deploy, launch, and app-surface integration.
- Unknowns: final package identity, signing, Store/App Installer distribution,
  production update policy, and any new live hardware action not performed by
  the RNW build command.
- Selected tier: Tier 3, because local deploy/launch and radio/flash evidence
  surfaces are hardware-adjacent.
- Owner role: React Native Windows with Communications, Firmware, XBee/radio,
  Live Bench, QA, and Evidence lenses.
- Evidence need: same-session RNW command transcript, Windows package/process
  proof, source/test validation, and durable task/handoff/source records.
- Mutation boundary: `apps/cbbs-windows/src/index.tsx`,
  `apps/cbbs-windows/__tests__/windowsHostOnly.test.tsx`,
  `apps/cbbs-windows/README.md`, React Native scaffold audit/tests, this task
  record, matching handoff, and matching source ledger. The native Windows
  build also generated app-local NuGet `packages.lock.json` files.
- Validation plan: Windows package typecheck, React Native scaffold audit,
  `git diff --check`, RNW `run-windows`, process/package verification, and
  cleanup of hung Jest processes.
- Trust boundary: local Windows debug build/deploy/launch proof only. No
  signing, Store, App Installer, public release, relay/load/mains operation, or
  new radio/flash command execution is claimed beyond the RNW build command.

## Reviewer Disposition

- RNW DevEx/CI reviewer, weight 3: approved the app-local
  `react-native run-windows` command and found no P1/P2 blocker in native
  config.
- Protocol/Bridge ABI reviewer, weight 3: approved fixture/simulator-summary
  mesh integration and identified the source-backed command names.
- XBee radio/protocol reviewer, weight 3: approved inert read-only app/test
  planning conditioned on no executable radio command dispatch and no raw
  identifier exposure.
- Firmware/device reviewer, weight 3: required the PF0530W live flash source ID
  in the flash panel; that source ID is now pinned in source/tests.
- Live-bench reviewer, weight 5: rejected treating this as live mesh/hardware
  acceptance without fresh hardware evidence. This task accepts only local RNW
  build/deploy/launch plus source-backed evidence UI.

## Implemented Changes

- Converted the Windows shell into a CBBS Windows operations console.
- Added integrated panels for `mesh_discovery.v1`, XBee radio
  configuration/readback, XBee OTA link proof, and firmware flash evidence.
- Added an inert operator command catalog that displays the RNW build command,
  mesh discovery request names, XBee study/programming surfaces, and firmware
  build/flash evidence command text without dispatching serial/RF/flash UI
  intents.
- Updated Windows tests and scaffold audit markers for the integrated surfaces.
- Updated the Windows README with the build and launch command plus
  mesh/XBee/flash integration notes.

## Validation

- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `git diff --check`.
- PASS: live Metro bundle request for
  `http://127.0.0.1:8081/index.bundle?platform=windows&dev=true&minify=false`;
  saved to
  `research/bench-records/react-native-windows/live-index.bundle`, 5,133,923
  bytes, SHA-256
  `FDD80512D04989C0A8F83FC4BD16181A5BCAE38ACFFE0DA5D5A944EB72633BC9`, with
  RNW `index.windows.js`, RNW `NativeDeviceInfo`, and `CbbsWindows` markers.
- PASS: `powershell.exe ... pnpm --dir apps/cbbs-windows exec react-native run-windows --root . --sln windows\CbbsWindows.sln --proj windows\CbbsWindows\CbbsWindows.vcxproj --arch x64 --no-telemetry`.
  The transcript reported NuGet restore success, autolinking success, Debug x64
  build success, deploy success, loopback exemption verification, and
  `Starting the app` success.
- PASS: Windows process proof found `ProcessName=CbbsWindows`, window title
  `CbbsWindows`, PID `29964`, and `Responding=true`.
- PASS: Windows package proof found `CbbsWindows_1.0.0.0_x64__2g54mg31548kg`
  installed from
  `H:\ESP32\apps\cbbs-windows\windows\CbbsWindows.Package\bin\x64\Debug\AppX`.
- PASS: focused window screenshot captured at
  `research/bench-records/react-native-windows/cbbs-windows-window-final.png`;
  the rendered app shows mesh discovery, XBee radio configuration, firmware
  flash evidence, and no RNW redbox.

Notes:

- Direct `pnpm --dir apps/cbbs-windows exec jest --config jest.config.windows.js --runInBand`
  and root `pnpm test` hung without output in this session and were terminated.
- A post-launch rerun of `scripts/scaffold_audit_react_native.py` failed
  because the successful RNW build generated native `obj`, `x64/Debug`, `bin`,
  and `AppPackages` outputs. Generated Debug outputs were left in place because
  the app is running from the Debug AppX layout.
- No lingering Jest, MSBuild, or `run-windows` process remained after launch.

## Authority Limits

This task authorizes and records only local Windows debug build, deploy, launch,
and inert app-surface integration. It does not authorize signing, package
identity acceptance, Store/App Installer distribution, public release,
relay/load/mains operation, new XBee setting writes, new RF range/throughput,
firmware update recovery, erase, or new flash activity beyond previously
recorded source evidence.

## Decision

Decision accepted:
`cbbs_react_native_windows_local_build_launch_integrated_surface`.
The app was built, deployed, launched, and verified running on the Windows PC.

## Handoff

Handoff:
[../handoffs/0117-cbbs-react-native-windows-build-launch-integrated-to-qa.md](../handoffs/0117-cbbs-react-native-windows-build-launch-integrated-to-qa.md)
