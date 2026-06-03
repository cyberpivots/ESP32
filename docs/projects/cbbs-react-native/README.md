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
- RNW native `windows/` generation, package identity, capabilities, signing,
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
  native build, RNW native generation/build, Windows package
  identity/capabilities, signing, runtime proof, or EAS build has been proven.
- CBBS live acceptance remains a separate proof lane.

## Current Scaffold

- `apps/cbbs-client/`: Expo Router Android/iOS/browser fixture app.
- `apps/cbbs-windows/`: Windows Client/Sysop source model with W2 RNW package
  dependencies, W2.1 local shell source/tests, W3A Windows prerequisite proof,
  and W3B generated native project files. W3B is not build/run/runtime proof.
- `packages/cbbs-protocol/`: shared role, view, intent, and safety contract.
- `packages/cbbs-fixtures/`: redacted fixture data.
- `packages/cbbs-state/`: local reducer for fixture-only UI intents.
- `packages/cbbs-ui/`: React Native UI shell.
- `packages/cbbs-theme/`: shared design tokens.
- `packages/cbbs-evidence/`: transcript-first evidence wording helpers.
- `tools/react-native/`: scaffold validation notes.

## Closed Surfaces

No native prebuild outside the accepted Windows W3B gate, EAS, App Center,
signing, release, deploy, simulator/device run, Expo Go proof, live network, BLE, Web
Bluetooth, Web Serial, SoftAP, serial write, RF/XBee action, relay, flash,
erase, monitor, persistent config, router/admin mutation, MicroSD, TFT, wiring,
load, or mains action is authorized by this project page.

Windows W3B authorizes only reviewed native generation for
`apps/cbbs-windows`. It does not authorize RNW `run-windows`,
Visual Studio/MSBuild build, Package.appxmanifest capability use, package
identity acceptance, installer/store packaging, or Windows runtime proof.

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
