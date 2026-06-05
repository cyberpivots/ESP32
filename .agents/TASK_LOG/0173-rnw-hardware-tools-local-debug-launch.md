# Task 0173: RNW Hardware Tools Local Debug Launch

Status: completed for local review; app and Metro retained

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-LOCAL-DEBUG-LAUNCH-2026-06-05`,
`SRC-LOCAL-CBBS-RNW-SPLIT-BUILD-INSTALL-LAUNCH-2026-06-04`,
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-METRO-INCIDENT-2026-06-04`,
`SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`,
`SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`

## Routing

- Verified facts: `apps/cbbs-hardware-tools-windows` exists with generated
  RNW native source. The retained Debug app registration initially had an empty
  `InstallLocation`; shell activation attempts recorded success but no app
  process. `react-native run-windows --no-telemetry` failed before launch with
  the known Visual Studio discovery error: `The "path" argument must be of type
  string. Received undefined`. The existing app-local Metro server was running
  from `apps/cbbs-hardware-tools-windows` on `127.0.0.1:8081`.
- Assumptions: the user request to launch the RNW Hardware Tools app opens only
  a bounded local Debug review gate for `CbbsHardwareToolsWindows`, including
  local Debug build output and app registration repair when the retained
  registration is stale.
- Unknowns: final package identity, accepted capability use, signing,
  Store/App Installer release path, native HostCommandBridge ABI, live bridge
  dispatch, serial/RF/XBee behavior, and hardware behavior remain unresolved.
- Selected tier: Tier 3 local RNW runtime launch gate.
- Owner role: RNW runtime DevEx with QA evidence, safety/security, and
  protocol/bridge reviewer lenses.
- Evidence need: reviewer quorum outputs, current package/process/Metro state,
  focused host tests, local Debug build/deploy/start transcript, fresh
  process/package proof, Metro inspector proof, screenshot proof, and retained
  state statement.
- Mutation boundary: `apps/cbbs-hardware-tools-windows` local Debug generated
  output under `windows/`, local `CbbsHardwareToolsWindows` package
  unregister/register state, the `CbbsHardwareToolsWindows` process, retained
  app-local Metro process, local evidence artifacts under
  `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/`,
  this task record, source index, source ledger, and docs index.
- Reviewer quorum: four read-only project-local reviewers were spawned, waited,
  captured, and closed. Weighted disposition was 13/13 conditional approval for
  local Debug Hardware Tools launch after applying the user's explicit launch
  authority. Conditions were app-local Metro first, no stale Client/Sysop
  bundle, fresh process/Metro/screenshot proof, and all live/release/hardware
  surfaces closed.
- Gate authority: user requested launch of the RNW Hardware Tools app. This
  opens only local Debug build/register/start for `CbbsHardwareToolsWindows`;
  it does not open release, signing, distribution, live bridge, serial/RF/XBee,
  firmware, relay/load/mains, or publication authority.
- Validation plan: run focused Hardware Tools host checks, repair stale Debug
  registration only as needed, build with `RunAutolinkCheck=false` to avoid
  generated native source rewrites, register the unpacked Debug layout, launch
  the app, capture process/package/Metro/screenshot proof, and retain review
  state.
- Trust boundary: local Windows process, Metro inspector, package registration,
  and screenshot evidence only. This is not release evidence and not hardware
  evidence.

## Reviewer Quorum

| Role | Weight | Vote | Conditions |
| --- | ---: | --- | --- |
| RNW runtime operations coordinator | 5 | approve after explicit launch authority | Keep boundary to app-local Metro plus Hardware Tools app process unless stale registration requires local Debug repair. |
| RNW QA evidence reviewer | 3 | approve evidence requirements | Fresh process, Metro, and loaded screenshot proof required; no redbox or loading-only state. |
| React Native safety/security reviewer | 3 | approve local Debug review launch | Reject HostCommandBridge dispatch, serial/RF/XBee, hardware, credentials, external service, signing, release, and publication surfaces. |
| React Native DevEx reviewer | 2 | approve launch path | Prefer `run-windows`; if blocked and Debug package is installed, use app-local Metro plus installed app. |

## Launch Record

- App-local Metro was already running from `apps/cbbs-hardware-tools-windows`
  and returned `packager-status:running`.
- Initial shell activation failed to leave a process because the retained
  package registration was stale and had an empty `InstallLocation`.
- `pnpm --dir apps/cbbs-hardware-tools-windows exec react-native run-windows
  --root . --sln windows\\CbbsHardwareToolsWindows.sln --proj
  windows\\CbbsHardwareToolsWindows\\CbbsHardwareToolsWindows.vcxproj --arch
  x64 --no-telemetry` failed before launch in Visual Studio discovery with the
  known `path` argument error.
- Direct MSBuild with autolink checking enabled failed because RNW reported
  generated auto-link files would need regeneration. The accepted build used
  `/p:RunAutolinkCheck=false` to avoid rewriting generated native source files.
- The local Debug build succeeded and produced the unpacked Debug layout under
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows.Package/bin/x64/Debug`.
- Unsigned Debug MSIX installation was rejected by Windows unsigned namespace
  rules, so the MSIX was not accepted as an install or release artifact.
- Removed only the stale `CbbsHardwareToolsWindows` local Debug registration,
  registered the unpacked Debug layout, and launched
  `CbbsHardwareToolsWindows_2g54mg31548kg!App`.
- Final process proof: `CbbsHardwareToolsWindows` PID `47248`, responding
  `True`, path
  `H:\esp32\apps\cbbs-hardware-tools-windows\windows\CbbsHardwareToolsWindows.Package\bin\x64\Debug\CbbsHardwareToolsWindows\CbbsHardwareToolsWindows.exe`.
- Final package proof: `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`,
  install location
  `H:\ESP32\apps\cbbs-hardware-tools-windows\windows\CbbsHardwareToolsWindows.Package\bin\x64\Debug`,
  signature kind `None`.
- Final Metro proof: `/status` returned `packager-status:running`, and
  `/json/list` reported app ID
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`.
- Screenshot proof:
  `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/hardware-tools-launch-screen.png`,
  6400x3497, SHA-256
  `CB80E4401A8BF66146BAF253205B2D926B72CDD4501C6B374D571090F293EF8B`.
  Visual inspection showed the Hardware Tools window loaded with no redbox and
  no loading-only state.

## Validation

Passed:

- `pnpm --filter @cbbs/hardware-tools-windows typecheck`.
- `pnpm --filter @cbbs/hardware-tools-windows test:windows`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`.
- `curl -fsS http://127.0.0.1:8081/status`.
- `curl -fsS http://127.0.0.1:8081/json/list`.
- Windows process/package proof captured in
  `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/process-package.json`.
- Screenshot metadata captured in
  `research/bench-records/react-native-windows/hardware-tools-launch-20260605T151725Z/hardware-tools-launch-screenshot-meta.json`.

Not claimed:

- Scaffold-clean audit is not claimed because this launch intentionally
  retained local Debug build output and package registration for review.
- Release/package/signing/capability acceptance is not claimed.

## Retained Local State

- `CbbsHardwareToolsWindows` is left running for user review.
- App-local Metro on `127.0.0.1:8081` is left running for the Debug app.
- Local Debug generated output under
  `apps/cbbs-hardware-tools-windows/windows/` is retained for the launched app.
- The local Debug package registration for
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg` is retained.

## Cleanup Note

Task 0175 subsequently cleaned the intentionally retained review state from
this task: it stopped the matching Hardware Tools Debug process, stopped the
app-local Hardware Tools Metro chain, unregistered only
`CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`, deleted only the named
generated Debug output directories, and restored the React Native scaffold
audit to scaffold-clean mode. The launch facts above remain historical local
Debug review evidence only.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee/radio writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, commit, push, PR, deploy, and release.

## Handoff

No handoff is required for the launch. A future cleanup gate can stop the app,
stop Metro, unregister the local Debug package if desired, remove generated
Debug outputs, and rerun `scripts/scaffold_audit_react_native.py`.

## Decision

Decision: accept the bounded Tier 3 local Debug launch for
`CbbsHardwareToolsWindows` review only. All live bridge, hardware, release,
publication, signing, and external-service surfaces remain closed.
