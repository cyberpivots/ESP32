# CBBS React Native Windows W4 Pre-Release Ledger

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-RUN-WINDOWS-2026-06-03`,
`SRC-REACT-NATIVE-WINDOWS-STORE-PUBLISHING-2026-06-03`,
`SRC-MICROSOFT-MSIX-SIGNING-2026-06-03`,
`SRC-MICROSOFT-WINDOWS-CODE-SIGNING-OPTIONS-2026-06-03`,
`SRC-MICROSOFT-WINDOWS-SIDELOADING-2026-06-03`,
`SRC-MICROSOFT-MSIX-UNSIGNED-2026-06-03`,
`SRC-MICROSOFT-MSIX-APP-INSTALLER-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`

## Scope

Tier 2 W4A pre-release source/record refresh and readiness metadata for
`apps/cbbs-windows`. This ledger records W4 subgates, source coverage, JS
component registration, stale-status correction, app-local generated project
metadata, and closed release/signing/live surfaces. It does not prove or
authorize W4B build-only execution, W4C deploy/run, W4D packaging, or W4E
Store/production release.

## Source Coverage

- RNW `run-windows` is source-covered as build/run/deploy-capable and
  telemetry-on by default unless `--no-telemetry` is passed; it remains closed
  in W4A.
- RNW Store publishing is source-covered as a later Partner Center, Visual
  Studio Store association, package upload, WACK, and Store-submission path.
- Microsoft MSIX signing sources support planning for self-signed internal
  testing, Azure Artifact Signing, OV certificate, and Store signing paths.
- Microsoft sideload/App Installer/unsigned-package sources support planning
  distinctions between controlled trusted-cert installs, local Windows 11
  unsigned smoke tests, and later direct-download/App Installer paths.

## Verified Facts

- W3B generated `apps/cbbs-windows/windows/**` and recorded the manifest
  identity and capabilities as template facts only.
- The generated native shell uses component name `CbbsWindows`.
- W4A registers `CbbsWindows` with `AppRegistry` in
  `apps/cbbs-windows/src/index.tsx`.
- W4A corrects stale Windows status fields so the source says the W3B native
  project exists and W4 build/run/runtime proof is absent.
- W4A records generated solution and manifest paths, generated manifest
  identity, generated capabilities, and explicit non-acceptance of package
  identity, capability use, signing, Store association, and App Installer.
- Package scripts still contain no `run-windows`, `init-windows`, MSBuild,
  MakeAppx, SignTool, signing, App Center, EAS, deploy, Store upload, or
  release command.
- The package-local Windows Jest config uses the React Native Babel preset for
  test transforms; this is host test configuration only, not native build/run
  authority.

## Assumptions

- The near-term audience is local/internal pre-release validation planning, not
  public distribution.
- `Publisher="CN=cyber"` remains generated template output until a later gate
  accepts a matching certificate or package identity.
- Restricted `runFullTrust` remains generated template output and needs later
  source-backed justification before package/release acceptance.

## Unknowns

- RNW native build behavior, runtime behavior, and build output layout.
- Whether the future W4B candidate command is sufficient for build-only proof.
- Final Windows package identity, signing certificate, trust model, update
  policy, and distribution channel.
- Live CBBS transport remains unresolved and closed.

## W4 Subgates

- W4A: source/record refresh and package identity/capability review.
- W4B: future build-only proof; no deploy, launch, package, signing, or
  runtime claim.
- W4C: future local deploy/run proof against fixture-only UI; no live
  transport.
- W4D: future pre-release packaging choice.
- W4E: future Store or production release gate.

## Validation

W4A validation passed:

- `pnpm lint`
- `pnpm typecheck`
- `pnpm test` - 5 suites, 28 tests
- `pnpm --filter @cbbs/client exec expo-doctor`
- `pnpm --filter @cbbs/windows-spike typecheck`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- no package-lock/package/signing artifact scan
- package-script scan for build/run/signing/deploy/release commands
- `git diff --check`

Package-local `pnpm --filter @cbbs/windows-spike test:windows` is not accepted
as W4A evidence. The root Jest suite is the accepted host test path for this
record.

## Authority Limits

No RNW `run-windows`, Visual Studio/MSBuild build, deploy, launch, package
creation, signing, certificate/PFX handling, package identity acceptance,
capability use, Store association, Store upload, App Installer publishing,
App Center, EAS, simulator/device launch, live network, BLE, Web Bluetooth,
Web Serial, local-network discovery, SoftAP, serial/RF/XBee action,
firmware/bridge/serial ABI change, flash, erase, monitor, relay, load, mains,
release, commit, push, PR, or deploy is authorized by this record.

## Decision

Decision: `cbbs_react_native_windows_w4a_pre_release_source_record_refresh`
is accepted as records and app-local metadata only. W4B/W4C/W4D/W4E remain
future gates.
