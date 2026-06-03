# CBBS Windows Spike

## Verified Facts

- React Native for Windows is versioned and supported separately from Expo and
  React Native Web.
- `ADR-0010` now permits W0/W1 host-only records, TypeScript source models,
  fixtures, UI/protocol tests, audits, and CI validation for Windows
  Client/Sysop planning.
- `ADR-0010` W2 now permits package-only RNW dependency selection for this
  package: `react-native-windows` `0.83.0`, `react-native` `0.83.9`, and React
  `19.2.3`.
- W2.1 adds a package-only Client/Sysop local shell with React Native
  primitives, shared protocol constants, fixture-only intents, disabled closed
  surfaces, and transcript-first evidence wording.
- W3A proves RNW 0.83 package-local Windows prerequisites: Visual Studio 2022,
  Windows SDK, Node, Yarn, .NET 8, and Windows `pnpm`.
- The W3B native generation gate generated the app-local RNW `cpp-app` native
  project after a fresh no-P1/P2 reviewer disposition, package-lock guard,
  pnpm reconciliation, and manifest capability inspection.
- RNW native build/run remains closed.

## Unknowns

- RNW native build behavior.
- RNW build, packaging, signing, and distribution path.
- Windows package identity and capability declarations.

## Host-Only Model

- One role-aware Windows Client/Sysop app is modeled in `src/index.tsx`.
- The shell derives the local-only marker and closed-surface IDs from
  `@cbbs/protocol`.
- Client actions remain local draft, filter, select, proof view, and staged
  request placeholders.
- Sysop actions remain local refresh, filter, select, detail, ack, and proof
  placeholders.
- All intents require `fixture-only-ui-intent`.

## Closed Surfaces

No RNW run, Visual Studio build, Package.appxmanifest capability use, package
identity acceptance, signing, installer packaging, App Center, EAS, live
connectivity, serial, BLE, RF/XBee, relay, flash, erase, monitor, release, PR,
or deploy is authorized in this spike. W3B native generation is complete and
build/run remains closed.
