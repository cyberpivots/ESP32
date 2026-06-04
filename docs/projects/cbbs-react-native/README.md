# CBBS React Native Client

## Verified Facts

- `ADR-0010` accepts a CBBS client/operator app lane using Expo SDK 56 and
  React Native 0.85 for Android, iOS, and browser fixture work.
- The lane is scoped to client/operator apps only. It does not select or alter
  firmware framework, firmware ABI, bridge ABI, serial ABI, RF transport, or
  live app transport.
- React Native for Windows is tracked separately. W0/W1 now permits
  host-only records, TypeScript source models, fixtures, UI/protocol tests,
  audit policy, and CI validation for Windows Client/Sysop planning only.
- RNW build/run/runtime, package identity acceptance, capability use, signing,
  live transport, and release work remain closed future gates.
- W2 permits RNW package-only dependency selection inside `apps/cbbs-windows`
  with `react-native-windows` `0.83.0`, `react-native` `0.83.9`, and React
  `19.2.3`; this is package/source validation only.
- W2.1 adds a package-only Windows Client/Sysop local shell using React Native
  primitives and shared protocol constants; it still does not prove Windows
  native runtime behavior.
- W3A proves the Windows host/toolchain prerequisites for the RNW 0.83
  package-local dependency check; it still does not generate a native Windows
  project or prove build/run behavior.
- W3B generated the app-local RNW `cpp-app` native project for
  `apps/cbbs-windows` only. It used an app-scoped no-overwrite/no-telemetry
  command, package-lock suppression, pnpm lock reconciliation, generated
  `run-windows` script removal, and manifest capability inspection before
  acceptance.
- W4A is a pre-release source/record refresh. It registers `CbbsWindows` with
  `AppRegistry`, corrects stale Windows status fields, records app-local RNW
  project metadata, and keeps build/run/package/signing/release proof closed.
- The RNW product split replaces the prior single cockpit source with
  product-facing Windows app shells for `CBBS Client`, `CBBS Sysop`, and
  `CBBS Hardware Tools`. Hardware Tools includes visible but non-executing
  planning controls backed by an unavailable bridge result.
- Hardware Tools now uses a generated `cbbs_rnw_menu.v1` product menu with
  fixed `Bench`, `Radio`, `Mesh`, `Firmware`, `Fabrication`, `Safety`, and
  `Activity` pages. The shell renders page-scoped workflows with a menu bar,
  page list, workspace, evidence rail, gate phrase field, and transcript strip.
- The `CbbsWindows` compatibility entry now defaults to the Sysop product
  surface in source. Earlier local Debug x64 Hardware Tools compatibility
  evidence is historical only; it is not current split-product runtime proof.
- The split native generation gate may generate app-local RNW `cpp-app` source
  projects for `CbbsClientWindows`, `CbbsSysopWindows`, and
  `CbbsHardwareToolsWindows`. Generated manifest identities and capabilities
  remain local debug template facts only.
- The Android/iOS/browser scaffold remains host-only and fixture-backed.

## App Contract

Stable roles:

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

Initial UI intents:

- `navigate`
- `refresh`
- `filter`
- `select_row`
- `open_detail`
- `compose_draft`
- `queue_file_request`
- `ack_local`
- `view_proof`

These are local UI/fixture intents only. `compose_draft`, `queue_file_request`,
and `ack_local` do not send bridge messages, touch files, transmit live ACKs,
or start network/file-transfer behavior.

## Assumptions

- The first useful app proof is browser/host validation against fixtures.
- Transcript-first evidence wording remains authoritative; screenshots and UI
  snapshots are corroboration only.
- Package tests and scaffold audits are the acceptance path for this phase.

## Unknowns

- Live transport, BLE UUIDs, local-network mode, credentials, native
  distribution, and update policy remain unresolved.
- No Android/iOS permission prompt, BLE pairing, local-network discovery,
  split-product native runtime, accepted Windows package identity/capability
  use, signing, release packaging, or EAS build has been proven.
- CBBS live acceptance remains a separate proof lane.

## Current Scaffold

- `apps/cbbs-client/`: Expo Router Android/iOS/browser fixture app.
- `apps/cbbs-windows/`: Windows Client/Sysop source model with W2 RNW package
  dependencies, W2.1 local shell source/tests, W3A Windows prerequisite proof,
  W3B generated native project files, and W4A pre-release source/record
  metadata. It now acts as a Sysop compatibility entry while separate product
  app packages carry the forward source model. Separate split-product native
  runtimes remain unproven.
- `apps/cbbs-client-windows/`: product-facing Windows client source app with
  RNW 0.83 package-lane dependencies and host-only render/operation tests.
- `apps/cbbs-sysop-windows/`: product-facing Windows sysop source app with
  RNW 0.83 package-lane dependencies and host-only render/operation tests.
- `apps/cbbs-hardware-tools-windows/`: product-facing Hardware Tools source
  app with generated page-scoped workflows, disabled dangerous controls, and
  user-facing artifact reviews. It has RNW 0.83 package-lane dependencies and
  host-only render/operation tests.
- `packages/cbbs-product/`: shared product profiles, product states, and
  generated Hardware Tools menu/action definitions.
- `packages/cbbs-product-ui/`: high-contrast React Native product shell shared
  by the Windows product apps, including menu/dropdown, page list, evidence
  rail, and transcript behavior.
- `packages/cbbs-protocol/`: shared role, view, intent, and safety contract.
  It also contains the inert `cbbs_host_command_bridge.v1` validator and
  unavailable-result helper for future Hardware Tools bridge planning.
- `packages/cbbs-fixtures/`: redacted fixture data.
- `packages/cbbs-state/`: local reducer for fixture-only UI intents.
- `packages/cbbs-ui/`: React Native UI shell.
- `packages/cbbs-theme/`: shared design tokens.
- `packages/cbbs-evidence/`: transcript-first evidence wording helpers.
- `tools/react-native/`: scaffold validation notes plus the Hardware Tools
  `cbbs_rnw_menu.v1` XML source and generator.

## Closed Surfaces

No native prebuild outside the accepted Windows W3B gate, EAS, App Center,
signing, release, deploy, simulator/device run, Expo Go proof, live network, BLE, Web
Bluetooth, Web Serial, SoftAP, serial write, RF/XBee action, relay, flash,
erase, monitor, persistent config, router/admin mutation, MicroSD, TFT, wiring,
load, or mains action is authorized by this project page.

Windows W3B authorizes only reviewed native generation for
`apps/cbbs-windows`; W4A authorizes only source/record refresh, app component
registration, and inert metadata. They do not authorize RNW `run-windows`,
Visual Studio/MSBuild build, Package.appxmanifest capability use, package
identity acceptance, installer/store packaging, or Windows runtime proof.

The product split and `cbbs_host_command_bridge.v1` contract are source/test
work for the three split product packages. Hardware Tools productization adds a
generated menu contract and host-only operation proof. It does not authorize
native bridge implementation, free-form shell input, serial/RF/XBee writes,
firmware flashing, monitor, relay/load/mains work, split-product native
runtimes, or any live hardware execution.

## Sources

- `ADR-0010`
- `SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`
- `SRC-REACT-NATIVE-VERSIONS-2026-06-02`
- `SRC-EXPO-SDK-56-REFERENCE-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-PACKAGE-DEPS-2026-06-03`
- `SRC-REACT-NATIVE-WINDOWS-CPP-APP-TEMPLATE-2026-06-03`
- `SRC-WINDOWS-APP-CAPABILITIES-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02`
- `SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W21-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`
- `SRC-LOCAL-CBBS-RNW-PRODUCT-SPLIT-HARDWARE-TOOLS-BRIDGE-CONTRACT-2026-06-03`
- `SRC-LOCAL-CBBS-HARDWARE-TOOLS-RNW-PRODUCTIZATION-2026-06-03`
