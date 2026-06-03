# CBBS React Native Client Platform Ledger

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`

## Scope

Tier 2 governance, source-record, tooling, and host-only scaffold work for a
CBBS React Native client/operator app lane. The work accepts `ADR-0010`, adds
source-backed records, and prepares a fixture-only Expo/RN workspace without
opening native build, external service, live device, or hardware surfaces.

## Source Coverage

- React Native latest/current line and framework recommendation are sourced by
  `SRC-REACT-NATIVE-VERSIONS-2026-06-02` and
  `SRC-REACT-NATIVE-ENV-SETUP-2026-06-02`.
- Expo SDK 56, monorepo, router, New Architecture, web, and EAS boundaries are
  sourced by `SRC-EXPO-SDK-56-REFERENCE-2026-06-02`,
  `SRC-EXPO-MONOREPOS-2026-06-02`, `SRC-EXPO-ROUTER-2026-06-02`,
  `SRC-EXPO-NEW-ARCHITECTURE-2026-06-02`,
  `SRC-EXPO-EAS-BUILD-2026-06-02`, and
  `SRC-REACT-NATIVE-WEB-2026-06-02`.
- React Native for Windows separate support scope is sourced by
  `SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02`.
- Android/iOS network and Bluetooth permission planning is sourced by
  `SRC-ANDROID-NETWORK-OPS-2026-06-02`,
  `SRC-ANDROID-BLUETOOTH-PERMISSIONS-2026-06-02`,
  `SRC-ANDROID-WIFI-PERMISSIONS-2026-06-02`,
  `SRC-APPLE-LOCAL-NETWORK-PRIVACY-2026-06-02`, and
  `SRC-APPLE-CORE-BLUETOOTH-2026-06-02`.
- App Center retirement wording is sourced by
  `SRC-MICROSOFT-APP-CENTER-RETIREMENT-2026-06-02`.

## Verified Facts

- `ADR-0010` is accepted and scoped only to CBBS client/operator apps.
- The accepted app lane uses Expo SDK 56 and React Native 0.85 for
  Android/iOS/browser host-only fixture work.
- The Windows lane is a separate RNW spike and remains docs/stub only.
- The initial shared app roles are `client`, `sysop`, `monitor`, and
  `devconfig`.
- The stable view IDs are `home`, `messages`, `downloads`, `peers`, `network`,
  `diagnostics`, `safety`, `config`, and `evidence`.
- The initial intent whitelist is `navigate`, `refresh`, `filter`,
  `select_row`, `open_detail`, `compose_draft`, `queue_file_request`,
  `ack_local`, and `view_proof`.
- The scaffold is fixture-only and does not add native `android/`, `ios/`, or
  `windows/` project folders.
- EAS and App Center are documented as closed/future surfaces only; no
  `eas.json`, App Center config, token, signing material, deploy, submit, or
  release automation is added.

## Assumptions

- The first app proof is host-only and can be validated through package tests,
  static audits, and browser export planning before any device/simulator gate.
- React Native and Expo version facts are current for 2026-06-02; future SDK
  releases may require a new source-review pass.
- Local fixture intent handling is sufficient for UI parity planning and does
  not imply live CBBS or ESP32 acceptance.

## Unknowns

- Exact live client transport, BLE UUIDs, SoftAP/LAN behavior, credentials,
  OTA/update policy, and native distribution path are unresolved.
- No Android/iOS permission prompts, local-network prompts, BLE pairing,
  simulator/device runs, native app builds, Windows native builds, EAS builds,
  or store submissions are proven.
- RNW Windows runner/toolchain support is unresolved.
- CBBS live acceptance remains separate and unproven by this record.

## Authority Limits

No native prebuild, native folders, native builds, simulator/device runs,
Expo Go proof, EAS cloud/local builds, EAS Submit, EAS Update, EAS Hosting,
App Center SDKs or automation, signing credentials, store upload, GitHub
publication, release, BLE pairing, Web Bluetooth, Web Serial, local-network
discovery, SoftAP probing, live bridge traffic, serial writes, firmware ABI
changes, bridge ABI changes, Gate F service-code changes, flash, erase,
monitor, RF/XBee action, router/admin mutation, relay, MicroSD, TFT, wiring,
load, mains, commit, push, PR, or deploy is authorized by this record.

## Validation

- PASS: `pnpm install`.
- PASS: `pnpm install --frozen-lockfile`.
  - Note: pnpm reported ignored dependency build scripts for
    `msgpackr-extract` and `unrs-resolver`; no native project, EAS, App
    Center, or device command was run.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` (3 suites, 10 tests).
- PASS: `pnpm doctor:expo` (21/21 Expo Doctor checks).
- PASS: `pnpm --filter @cbbs/client export:web`.
- PASS: temporary static smoke check using `python3 -m http.server 4173
  --directory apps/cbbs-client/dist` plus `curl -fsS` to
  `http://127.0.0.1:4173/`; the server was stopped in the same command.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold tests.scaffold_audits.test_agent_process_classifiers`
  (11 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`
  (command passed; dirty tree reflects this task; branch `main` is aligned
  with `origin/main`; no open PRs reported).
- PASS: `git diff --check`.

## Decision

Decision: `ADR-0010` accepts the CBBS React Native client/operator app
platform strategy, and the named host-only scaffold is validated for QA review
with web export/static smoke proof. Future live app, native build,
external-service, or release work requires a separate gate.
