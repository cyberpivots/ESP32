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
- RNW dependencies, native `windows/` generation, Windows runner/toolchain
  proof, package identity, capabilities, signing, live transport, and release
  work remain closed future gates.
- W2 permits RNW package-only dependency selection inside `apps/cbbs-windows`
  with `react-native-windows` `0.83.0`, `react-native` `0.83.9`, and React
  `19.2.3`; this is package/source validation only.
- The first scaffold is host-only and fixture-backed. No native `android/`,
  `ios/`, or `windows/` project folders are part of this phase.

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
  native build, RNW native build, Windows runner, Windows package
  identity/capabilities, signing, or EAS build has been proven.
- CBBS live acceptance remains a separate proof lane.

## Current Scaffold

- `apps/cbbs-client/`: Expo Router Android/iOS/browser fixture app.
- `apps/cbbs-windows/`: Windows Client/Sysop host source model with W2 RNW
  package dependencies only; no generated Windows project.
- `packages/cbbs-protocol/`: shared role, view, intent, and safety contract.
- `packages/cbbs-fixtures/`: redacted fixture data.
- `packages/cbbs-state/`: local reducer for fixture-only UI intents.
- `packages/cbbs-ui/`: React Native UI shell.
- `packages/cbbs-theme/`: shared design tokens.
- `packages/cbbs-evidence/`: transcript-first evidence wording helpers.
- `tools/react-native/`: scaffold validation notes.

## Closed Surfaces

No native prebuild, native folder generation, EAS, App Center, signing,
release, deploy, simulator/device run, Expo Go proof, live network, BLE, Web
Bluetooth, Web Serial, SoftAP, serial write, RF/XBee action, relay, flash,
erase, monitor, persistent config, router/admin mutation, MicroSD, TFT, wiring,
load, or mains action is authorized by this project page.

Windows W2 also does not authorize RNW CLI execution, Visual Studio/MSBuild,
Package.appxmanifest capability declarations, package identity, installer/store
packaging, or Windows runtime proof.

## Sources

- `ADR-0010`
- `SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`
- `SRC-REACT-NATIVE-VERSIONS-2026-06-02`
- `SRC-EXPO-SDK-56-REFERENCE-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02`
- `SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`
- `SRC-WINDOWS-APP-CAPABILITIES-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02`
- `SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02`
- `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`
