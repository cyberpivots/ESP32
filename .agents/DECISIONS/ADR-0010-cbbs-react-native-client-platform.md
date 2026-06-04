# ADR-0010: CBBS React Native Client Platform Strategy

Status: Accepted

Date: 2026-06-02

## Context

The workspace remains framework-neutral for firmware except where accepted
firmware ADRs explicitly narrow that scope. `ADR-0003` accepts ESP-IDF only for
the ESP-NOW BBS coordinator/client firmware lane. It does not select a mobile
or browser client framework.

The project now needs a separate CBBS client/operator app lane for host-only
fixture UI work across Android, iOS, browser, and a later Windows spike. This
lane must not replace the accepted Win31/DOSBox-X/Pi/ESP32 path and must not
create live hardware authority from UI intent.

## Verified Facts

- React Native `0.85` is the latest stable line as of 2026-06-02, and Expo SDK
  `56.0.0` maps to React Native `0.85`, React `19.2.3`, React Native Web
  `0.21.0`, and minimum Node.js `22.13.x`.
- React Native documentation recommends using a framework for new React Native
  apps, and Expo is documented as a production-grade React Native framework.
- Expo supports monorepos with workspace package managers including `pnpm`.
- Expo Router is a file-based router for React Native and web apps and supports
  shared Android, iOS, and web navigation.
- Expo SDK 55 and later run entirely on React Native's New Architecture; SDK 56
  cannot disable it.
- React Native for Windows is versioned and supported separately from Expo and
  React Native Web. RNW `0.83` is the current active line as of 2026-06-02.
- EAS Build is a hosted build/signing service for Expo and React Native app
  binaries. No EAS build proof is created by this ADR.
- Visual Studio App Center reached its lifecycle retirement date on
  2025-03-31. Microsoft separately extended App Center Analytics and
  Diagnostics support beyond the original retirement window; App Center is not
  selected for build, test, distribution, or CodePush in this project.
- Android and iOS local-network/Bluetooth behavior has platform-specific
  permission and privacy requirements. This ADR records those requirements for
  later planning only.

## Accepted Decision

Accept a CBBS client/operator app platform strategy using:

- Expo SDK 56 and React Native 0.85 for the Android, iOS, and browser
  client/operator app lane.
- React Native Web through Expo for browser export proof.
- Expo Router for shared Android, iOS, and web route structure.
- `pnpm` workspaces for the modular client scaffold.
- A separate React Native for Windows spike lane that remains docs/stub only
  until a future Windows toolchain gate proves runner support.

This decision applies only to CBBS client/operator apps. It does not select or
change firmware framework, firmware ABI, coordinator serial ABI, bridge ABI,
Gate F service codes, RF transport, BLE transport, ESP-WIFI-MESH transport,
router/admin behavior, persistent device configuration, or release tooling.

## Initial Shared Contract

Stable app roles:

- `client`
- `sysop`
- `monitor`
- `devconfig`

Stable view IDs:

- `home`
- `messages`
- `downloads`
- `peers`
- `network`
- `diagnostics`
- `safety`
- `config`
- `evidence`

Initial UI intent whitelist:

- `navigate`
- `refresh`
- `filter`
- `select_row`
- `open_detail`
- `compose_draft`
- `queue_file_request`
- `ack_local`
- `view_proof`

All initial intents are local fixture/UI intents. They do not send bridge
messages, write files, acknowledge live packets, discover networks, connect to
devices, mutate configuration, or trigger hardware actions.

## Scaffold Boundary

After this ADR is accepted, the approved scaffold boundary is:

- `apps/cbbs-client/`: Expo SDK 56 Android/iOS/browser fixture app.
- `apps/cbbs-windows/`: RNW spike docs/stub package only; no generated
  `windows/` native project.
- `packages/cbbs-ui/`, `packages/cbbs-state/`, `packages/cbbs-protocol/`,
  `packages/cbbs-fixtures/`, `packages/cbbs-theme/`, and
  `packages/cbbs-evidence/`.
- `tools/react-native/`, `research/cbbs-react-native/`, and a repo-local
  React Native client skill/reviewer profile set.

The first scaffold must not create native `android/`, `ios/`, or `windows/`
folders, must not add `eas.json`, and must not run native prebuilds, native
builds, external service builds, signing, deploy, submit, or release commands.

## Windows W0/W1 Host-Only Amendment

Accepted on 2026-06-02.

The Windows lane may advance from docs/stub-only to host-only records,
TypeScript source models, fixture data, UI render tests, protocol tests, audit
policy, and CI validation for one role-aware `apps/cbbs-windows` Client/Sysop
planning app. This amendment authorizes only:

- W0 governance/source records for RNW `0.83` planning, Windows toolchain
  prerequisites, RNW CLI telemetry/`--no-telemetry`, and Windows capability
  manifest planning.
- W1 host-only protocol hardening: exact top-level intent keys, mandatory
  `localOnlyReason === "fixture-only-ui-intent"`, forbidden metadata-key
  rejection, 512-byte payload bounds, and closed-surface parity between
  protocol constants, fixtures, UI labels, and audits.
- W1 local fixture UI for Client and Sysop modes, including role/view parity,
  deterministic accessibility/test IDs, disabled unsafe controls, and
  transcript-first evidence wording.
- W1 TypeScript-only `apps/cbbs-windows` source/tests that model the Windows
  Client/Sysop product shape without adding RNW dependencies or native files.
- CI validation using `pnpm install --frozen-lockfile`, lint, typecheck, Jest,
  lockfile-bound Expo Doctor, Windows spike typecheck, and the React Native
  scaffold audit.

This amendment still does not authorize `react-native-windows` dependencies,
RNW JS package selection, native `windows/` project generation, `init-windows`,
`run-windows`, Visual Studio/MSBuild, Package.appxmanifest capability
declarations, package identity, signing, store packaging, App Center, EAS,
simulator/device launch, live network, BLE, Web Serial, Web Bluetooth, serial,
RF/XBee, firmware/bridge/serial ABI changes, flash, erase, monitor, relay,
load, mains, release, commit, push, PR, or deploy.

Future W2 RNW dependency work must open a separate gate and keep RNW `0.83.x`
isolated from the Expo React Native `0.85.3` lane unless a new source review
proves a different compatibility strategy. Future W3/W4 native Windows work
must prove a Windows host/toolchain in the same session and use explicit
`--no-telemetry` CLI options when any RNW CLI command is authorized.

## Windows W2 RNW JS Dependency Amendment

Accepted on 2026-06-02.

The Windows lane may advance to W2 package-only RNW dependency selection for
`apps/cbbs-windows` after the W2 reviewer quorum. This amendment authorizes
only:

- Exact React Native Windows dependency-lane selection in
  `apps/cbbs-windows/package.json`: `react-native-windows` `0.83.0`,
  `react-native` `0.83.9`, and React `19.2.3`.
- `apps/cbbs-windows` source/tests that import React Native primitives only
  for host-side TypeScript/Jest validation.
- Lockfile update and audit checks proving RNW package ownership remains
  scoped to the Windows package and does not enter `apps/cbbs-client`, root
  tooling, or shared `packages/cbbs-*` packages.
- Import-boundary checks forbidding `@cbbs/ui`, Expo, Expo Router,
  React Native Web, live transports, and native CLI/build/release scripts in
  the Windows lane.

W2 package validation is not Windows native proof. It still does not authorize
RNW CLI execution, `init-windows`, `run-windows`, native `windows/` project
generation, Visual Studio/MSBuild, Package.appxmanifest capability
declarations, package identity, signing, store packaging, App Center, EAS,
simulator/device launch, live network, BLE, Web Serial, Web Bluetooth, serial,
RF/XBee, firmware/bridge/serial ABI changes, flash, erase, monitor, relay,
load, mains, release, commit, push, PR, or deploy.

## Windows W3A Toolchain Preflight Amendment

Accepted on 2026-06-03.

The Windows lane may advance to W3A Windows host/toolchain preflight after
explicit user authority and reviewer quorum. This amendment authorizes only:

- Same-session Windows host inventory for OS version, Developer Mode, long
  paths, Visual Studio, Windows SDK, Node, Yarn, .NET SDK, and Windows package
  manager availability.
- Package-local RNW `0.83.0` dependency-script checks from
  `node_modules/react-native-windows/Scripts/rnw-dependencies.ps1`.
- Source-backed prerequisite remediation through the package-local RNW script
  when the floating public dependency script has drifted from the versioned RNW
  package requirements.
- Narrow Windows PATH/Corepack configuration needed for Yarn and the
  repo-pinned `pnpm@10.15.0`.
- Durable W3A task/source/handoff records and audits proving that no app native
  Windows project was generated.

W3A proves host prerequisite readiness only. It still does not authorize RNW
CLI `init-windows`, `run-windows`, native `windows/` project generation,
MSBuild build, Visual Studio launch, Package.appxmanifest capability
declarations, package identity, signing, store packaging, App Center, EAS,
simulator/device launch, live network, BLE, Web Serial, Web Bluetooth, serial,
RF/XBee, firmware/bridge/serial ABI changes, flash, erase, monitor, relay,
load, mains, release, commit, push, PR, or deploy.

Future W3 native generation must open a separate boundary for
`apps/cbbs-windows/windows`, update the scaffold audit to allow and inspect the
generated native surface, state the exact no-overwrite `init-windows
--no-telemetry` command, stop if the CLI requires `--overwrite`, and preserve
all live, release, signing, and hardware gates.

## Windows W3B Native Generation Gate Amendment

Accepted on 2026-06-03.

The Windows lane may advance to W3B native project generation only after the
same-session W3B record/audit boundary and a fresh no-P1/P2 reviewer
disposition. W3B authorizes only:

- W3B governance/source/handoff records and a W3-aware scaffold audit that
  allows and inspects the generated `apps/cbbs-windows/windows` native surface.
- The app-scoped no-overwrite/no-telemetry command:
  `NPM_CONFIG_PACKAGE_LOCK=false pnpm --dir apps/cbbs-windows exec react-native init-windows --template cpp-app --name CbbsWindows --namespace Cbbs.Windows --no-telemetry`.
- RNW `cpp-app` generated files under `apps/cbbs-windows/windows`, generated
  app-root RNW config files, `apps/cbbs-windows/package.json`, and
  `pnpm-lock.yaml` reconciliation through pnpm only.
- Removal or neutralization of RNW-generated `run-windows` package scripts
  before W3B acceptance, because W4 build/run/deploy remains closed.
- Inspection of generated `Package.appxmanifest` as a template fact only. The
  reviewed template defaults are `internetClient` and restricted
  `runFullTrust`; any additional capability stops W3B.

W3B still does not authorize RNW `run-windows`, Visual Studio/MSBuild build,
deploy, package identity acceptance, capability use, signing, installer/store
packaging, App Center, EAS, simulator/device launch, live network, BLE,
Web Serial, Web Bluetooth, local-network discovery, SoftAP, serial, RF/XBee,
firmware/bridge/serial ABI changes, flash, erase, monitor, relay, load, mains,
release, commit, push, PR, or deploy.

## Windows W4 Pre-Release Planning Amendment

Accepted on 2026-06-03.

The Windows lane may advance to W4 pre-release planning and readiness metadata
only after W3B native generation. This amendment authorizes only:

- W4A source, task, handoff, and docs refresh for a pre-release Windows
  validation lane.
- Registering the generated native component name `CbbsWindows` with
  `AppRegistry` in the app-local Windows source.
- Correcting stale W2/W3 status fields so the app source records that the W3B
  native project exists while W4 build/run/runtime proof is absent.
- App-local metadata that records generated solution/manifest paths, generated
  manifest identity, generated manifest capabilities, and W4 subgate status.
- Audit and test guards that reject package-lock output, package/signing
  artifacts, Store association files, package scripts for build/run/signing,
  and release/deploy command surfaces.

W4 is split into subgates:

- W4A: source/record refresh and package identity/capability review.
- W4B: future build-only proof; no deploy, launch, package, signing, or
  runtime claim.
- W4C: future local deploy/run proof against fixture-only UI; no live
  transport.
- W4D: future pre-release packaging choice.
- W4E: future Store or production release gate.

W4A does not accept the generated manifest identity
`Name="CbbsWindows"`, `Publisher="CN=cyber"`, or `Version="1.0.0.0"` as final
package identity. W4A does not accept `internetClient` or restricted
`runFullTrust` for capability use. Self-signed MSIX, unsigned Windows 11 MSIX
smoke testing, App Installer, Microsoft Store, Azure Artifact Signing, and OV
certificate paths are planning alternatives only until a later gate accepts an
exact artifact, credential, trust, install, uninstall, and distribution
boundary.

W4A still does not authorize RNW `run-windows`, Visual Studio/MSBuild build,
deploy, launch, package creation, signing, package identity acceptance,
capability use, Store association, App Installer publishing, EAS, App Center,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial/RF/XBee action,
firmware/bridge/serial ABI change, flash, erase, monitor, relay, load, mains,
release, commit, push, PR, or deploy.

## Windows W5 Split Native Generation Amendment

Accepted on 2026-06-04.

The Windows lane may advance to split-product native source generation for the
three product app packages after a fresh no-P1/P2 reviewer disposition. W5
authorizes only:

- W5 governance/source/handoff records and React Native scaffold audit coverage
  for the generated split native surfaces.
- App-scoped no-overwrite/no-telemetry commands for
  `CbbsClientWindows`, `CbbsSysopWindows`, and `CbbsHardwareToolsWindows`.
- RNW `cpp-app` generated files under
  `apps/cbbs-client-windows/windows`,
  `apps/cbbs-sysop-windows/windows`, and
  `apps/cbbs-hardware-tools-windows/windows`.
- App package metadata and `pnpm-lock.yaml` reconciliation through pnpm only.
- Removal or neutralization of RNW-generated `run-windows` package scripts
  before W5 acceptance.
- Inspection of generated `Package.appxmanifest` files as template facts only.
  The reviewed template defaults remain `internetClient` and restricted
  `runFullTrust`; any additional capability stops W5.

W5 does not authorize RNW `run-windows`, Visual Studio/MSBuild build, deploy,
launch, package identity acceptance, capability use, signing, installer/store
packaging, App Center, EAS, simulator/device launch, live network, BLE,
Web Serial, Web Bluetooth, local-network discovery, SoftAP, native
HostCommandBridge implementation, live bridge dispatch, serial/RF/XBee action,
firmware/bridge/serial ABI changes, flash, erase, monitor, relay, load, mains,
release, commit, push, PR, or deploy.

## Assumptions

- The first app slice is host-only and fixture-backed.
- The client app supplements existing Win31/CBBS/LCD/browser-mirror evidence
  surfaces; it does not supersede them.
- Expo SDK 56 remains the correct current Expo target for React Native 0.85 at
  this decision date.
- Future live mobile connectivity must open a separate Tier 3 gate before
  device, simulator, BLE, Web Serial, Web Bluetooth, LAN, SoftAP, or serial
  actions are attempted.

## Unknowns

- Exact live client transport, BLE UUIDs, SoftAP/LAN mode, credentials,
  native distribution model, and update policy remain unresolved.
- No Android permission prompt, iOS local-network prompt, BLE pairing,
  simulator run, device run, native app build, Windows native build, EAS build,
  or store submission is proven.
- RNW Windows runner/toolchain availability is unverified.
- CBBS live acceptance remains separate from this client scaffold.

## Review Quorum

- Governance reviewer, weight 5: conditional approval after ADR-first ordering;
  rejected framework-dependent mutation before accepted ADR/source records.
- Source research reviewer, weight 3: approved with current official source
  rows and precise App Center wording.
- UI/UX reviewer, weight 3: approved host-only scaffold with stable role, view,
  and intent tests plus transcript-first evidence wording.
- Protocol/state reviewer, weight 3: approved fixture-only protocol package
  with no bridge/serial/RF side effects.
- DevEx/CI reviewer, weight 3: approved with lockfile-bound validation and
  native-folder absence audit.
- Security/safety reviewer, weight 3: approved with no secrets, no native
  folders, no external services, no live connectivity, and disabled unsafe
  authority.

Weighted disposition: 17/17 approve for the named Phase 0 plus Phase 1/2
host-only boundary after the governance ADR-first condition. No P1/P2 blockers
remain for this boundary.

## Validation Expectations

- Source rows and source ledger for the React Native/Expo/RNW/App Center and
  platform-permission claims.
- `scripts/scaffold_audit_react_native.py`.
- No native-folder audit for `apps/cbbs-client` and `apps/cbbs-windows`.
- Fixture contract tests for roles, views, intent whitelist, no-secret
  recursion, oversize payload rejection, and unsafe action rejection.
- `pnpm install --frozen-lockfile`, `pnpm lint`, `pnpm typecheck`,
  `pnpm test`, and lockfile-bound `pnpm --filter @cbbs/client exec
  expo-doctor` when the local Node/pnpm toolchain supports them.
- Existing scaffold/source/docs/records/skill/agent-process audits.
- No publication or release action without a separate gate.

## Sources

- `SRC-REACT-NATIVE-VERSIONS-2026-06-02`
- `SRC-REACT-NATIVE-ENV-SETUP-2026-06-02`
- `SRC-EXPO-SDK-56-REFERENCE-2026-06-02`
- `SRC-EXPO-MONOREPOS-2026-06-02`
- `SRC-EXPO-ROUTER-2026-06-02`
- `SRC-EXPO-NEW-ARCHITECTURE-2026-06-02`
- `SRC-EXPO-EAS-BUILD-2026-06-02`
- `SRC-REACT-NATIVE-WEB-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02`
- `SRC-ANDROID-NETWORK-OPS-2026-06-02`
- `SRC-ANDROID-BLUETOOTH-PERMISSIONS-2026-06-02`
- `SRC-ANDROID-WIFI-PERMISSIONS-2026-06-02`
- `SRC-APPLE-LOCAL-NETWORK-PRIVACY-2026-06-02`
- `SRC-APPLE-CORE-BLUETOOTH-2026-06-02`
- `SRC-MICROSOFT-APP-CENTER-RETIREMENT-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-PACKAGE-DEPS-2026-06-03`
- `SRC-REACT-NATIVE-WINDOWS-RUN-WINDOWS-2026-06-03`
- `SRC-REACT-NATIVE-WINDOWS-STORE-PUBLISHING-2026-06-03`
- `SRC-WINDOWS-APP-CAPABILITIES-2026-06-02`
- `SRC-MICROSOFT-MSIX-SIGNING-2026-06-03`
- `SRC-MICROSOFT-WINDOWS-CODE-SIGNING-OPTIONS-2026-06-03`
- `SRC-MICROSOFT-WINDOWS-SIDELOADING-2026-06-03`
- `SRC-MICROSOFT-MSIX-UNSIGNED-2026-06-03`
- `SRC-MICROSOFT-MSIX-APP-INSTALLER-2026-06-03`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02`
- `SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`
- `SRC-LOCAL-CBBS-RNW-SPLIT-NATIVE-GENERATION-2026-06-04`
- `SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`
- `SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`

## Stop Gates

This ADR does not authorize native Android/iOS project generation, native
Windows project generation outside the accepted W3B and W5 boundaries, RNW
`run-windows`, Visual Studio/MSBuild build, deploy, launch, package creation,
signing, package identity acceptance, capability use, Store association, App
Installer publishing, simulator/device runs, Expo Go claims, EAS Build, EAS
Submit, EAS Update, EAS Hosting, App Center SDKs or automation, signing
credentials, store upload, GitHub publication, release, BLE pairing, Web
Bluetooth, Web Serial, local-network discovery, SoftAP probing, live bridge
traffic, serial writes, firmware ABI changes, bridge ABI changes, Gate F
service-code changes, flash, erase, monitor, RF/XBee action, router/admin
mutation, relay, MicroSD, TFT, wiring, load, mains, or live proof.
