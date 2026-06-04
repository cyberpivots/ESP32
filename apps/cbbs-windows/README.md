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
- W4A source/record metadata is present. The app registers the `CbbsWindows`
  JS component name expected by the generated native shell and records
  app-local RNW project metadata.
- The legacy `CbbsWindows` entry now opens the Sysop compatibility surface
  while the forward source model is split across `CBBS Client`, `CBBS Sysop`,
  and `CBBS Hardware Tools` product apps.
- Earlier local Debug x64 build/deploy/run evidence remains a historical
  compatibility-entry fact only. It is not split-product runtime proof and is
  not accepted as current Tier 2 runtime authority.

## Unknowns

- Native Windows project layout and installed identities for the three split
  product apps.
- Accepted Windows package identity, capability-use policy, signing, packaging,
  and distribution path.

## Product Model

- `apps/cbbs-client-windows` registers the `CBBS Client` product source app.
- `apps/cbbs-sysop-windows` registers the `CBBS Sysop` product source app.
- `apps/cbbs-hardware-tools-windows` registers the `CBBS Hardware Tools`
  product source app.
- `apps/cbbs-windows/src/index.tsx` keeps the generated native shell compatible
  through `AppRegistry` by registering `CbbsWindows` as a Sysop entry.
- `@cbbs/product` owns user-facing product profiles and generated Hardware
  Tools menu/action definitions.
- `@cbbs/product-ui` owns the high-contrast shared product shell, including
  menu/dropdowns, page list, workspace, evidence rail, and transcript strip.
- Enabled UI actions emit only local `fixture-only-ui-intent` records.

## Closed Surfaces

Package identity acceptance, signing, installer packaging, Store association,
App Installer publishing, App Center, EAS, release, PR, and public deploy remain
closed. Relay/load/mains operation remains closed. Hardware Tools can show
planning controls and command previews, but the app does not dispatch native
host commands, shell commands, serial/RF/XBee actions, relay actions, or firmware
flash actions from UI intents.

## W4 Pre-Release Planning

- W4A source/record refresh is complete.
- W4B build-only proof and W4C local deploy/run proof remain future gates.
- W4D pre-release packaging and W4E Store/production release remain separate.
- The generated manifest identity `CbbsWindows` / `CN=cyber` / `1.0.0.0` and
  capabilities `internetClient` plus restricted `runFullTrust` are recorded as
  generated template facts only.
- Self-signed MSIX, unsigned MSIX, App Installer, Store, Azure Artifact Signing,
  and OV-certificate paths are planning alternatives only until a later
  source-backed gate accepts exact credentials, artifact handling, and
  distribution authority.

## Runtime Gate

Future Tier 3 runtime command stays closed until a same-session gate records
authority, prerequisites, cleanup, and reviewer approval. This README does not
publish a current build, deploy, launch, signing, package, Store, App Installer,
or release command.

## Hardware Tools Contract

- Hardware Tools uses `tools/react-native/cbbs_rnw_menu.v1.xml` as the
  product-facing menu source. Regenerate or check the tracked TypeScript menu
  with `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`.
- Hardware Tools uses user-facing action IDs such as
  `hardware.radioInventory`, `hardware.radioProfileCompare`,
  `hardware.radioChangePlan`, `hardware.firmwareBuildReview`, and
  `hardware.deviceUpdatePlan`.
- `@cbbs/protocol` defines the inert `cbbs_host_command_bridge.v1` request and
  result schema for future Hardware Tools bridge planning.
- The default bridge result is unavailable; no native `HostCommandBridge` module
  is implemented in this pass.

## Mesh And XBee Integration

- Prior mesh, radio, and firmware records remain source evidence for Hardware
  Tools planning views.
- Those records do not make Hardware Tools dispatch live mesh, serial, RF/XBee,
  relay, or firmware flash actions.
