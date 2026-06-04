# Task 0159: CBBS RNW Product Split Hardware Tools Bridge Contract

Status: completed

## Routing

- Verified facts: `ADR-0010` accepts the CBBS React Native app lane and keeps
  initial UI intents local-only; the previous RNW screen was a single
  developer-facing cockpit; current source and tests can be changed without
  touching firmware or hardware.
- Assumptions: this task implements product source/test surfaces and an inert
  bridge contract only; native product packaging and live execution remain
  future gates.
- Unknowns: final native app identities, HostCommandBridge native ABI, and
  same-session safety evidence for executable actions.
- Selected tier: Tier 2.
- Owner role: React Native Windows/UI with Protocol/Bridge, Safety/Security,
  XBee/radio, and QA review lenses.
- Evidence need: source diff, typecheck/Jest/lint/audit results, no-dispatch
  scans, redaction tests, and durable record.
- Mutation boundary: React Native/RNW source, package manifests, tests, audit
  scripts, docs, source ledger, task log, and handoff only.
- Gate authority: user authorized implementation of the product split plan.
  No Tier 3 live hardware, serial, radio, flash, relay/load/mains, signing,
  release, or native bridge execution authority is granted.
- Trust boundary: host-only source/test proof. No live CBBS, Windows runtime,
  native packaging, or hardware behavior is claimed.

## Reviewer Quorum

- React Native UI parity reviewer, weight 3: rejected the existing cockpit and
  required three product surfaces plus removal of visible developer labels.
- Protocol/bridge reviewer, weight 3: approved only a separate non-executing
  bridge schema/test contract; no UI-intent reuse and no native execution.
- React Native safety/security reviewer, weight 3: required removal of ignored
  RNW build/package outputs and redaction of primary UI identifiers.
- QA reviewer, weight 3: approved inert source/test mutation with package,
  no-dispatch, and audit validation.
- XBee/radio reviewer, weight 3: approved UI-only radio planning surfaces with
  read plans presented as previews and no primary COM/raw identifier display.

Weighted result: conditional Tier 2 mutation accepted after ignored RNW build
outputs were removed and the running `CbbsWindows` debug process was stopped.

## Changes

- Added `@cbbs/product` with product app profiles for `CBBS Client`,
  `CBBS Sysop`, and `CBBS Hardware Tools`.
- Added `@cbbs/product-ui` with a high-contrast product shell that renders
  user-facing controls, status, activity, and Hardware Tools advanced details.
- Added `apps/cbbs-client-windows`, `apps/cbbs-sysop-windows`, and
  `apps/cbbs-hardware-tools-windows` source apps with component registration
  and package-local tests.
- Replaced the old `apps/cbbs-windows` cockpit with a compatibility Hardware
  Tools entry.
- Added `cbbs_host_command_bridge.v1` request/result validation and an
  unavailable-result helper in `@cbbs/protocol`.
- Updated scaffold audit checks for the product split and bridge contract.

## Validation

- PASS: `pnpm --filter @cbbs/product typecheck`
- PASS: `pnpm --filter @cbbs/product-ui typecheck`
- PASS: `pnpm --filter @cbbs/client-windows typecheck`
- PASS: `pnpm --filter @cbbs/sysop-windows typecheck`
- PASS: `pnpm --filter @cbbs/hardware-tools-windows typecheck`
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`
- PASS: `pnpm --filter @cbbs/windows-spike test:windows`
- PASS: `pnpm --filter @cbbs/client-windows test:windows`
- PASS: `pnpm --filter @cbbs/sysop-windows test:windows`
- PASS: `pnpm --filter @cbbs/hardware-tools-windows test:windows`
- PASS: `pnpm typecheck`
- PASS: `pnpm lint`
- PASS: `pnpm test`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- PASS: `python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
- PASS: `git diff --check`
- PASS: targeted RNW product source scan found no live host, serial, RF,
  flash, shell, COM-port, or secret markers in product app/source paths.
- PASS: local RNW Debug x64 build/deploy/run for the `CbbsWindows`
  compatibility entry using
  `pnpm --dir apps/cbbs-windows exec react-native run-windows --root . --sln windows\CbbsWindows.sln --proj windows\CbbsWindows\CbbsWindows.vcxproj --arch x64 --no-telemetry`.
- PASS: accepted runtime screenshot
  `research/bench-records/react-native-windows/cbbs-rnw-product-split-hardware-tools-after-wait-20260603.png`,
  SHA-256
  `5A7D4F130D9A7E3ACCADCC1FB53D07902578A7A4C05D4ACD9F34AA030A3AEC23`,
  captured from process `CbbsWindows` PID `29104`, title `CbbsWindows`,
  `1000x1000`, showing `CBBS Hardware Tools`.
- PASS: post-capture cleanup stopped the RNW app and Metro packager and removed
  ignored Debug build/package outputs before the final scaffold audit rerun.

## Authority Limits

No executable bridge implementation, native product package identities,
signing, release, serial/RF/XBee writes, firmware flash, monitor,
relay/load/mains work, wiring, commit, push, PR, deploy, or live hardware
action is authorized by this record.

## Decision

Accepted as Tier 2 host-only source/test work. The product split, shared
high-contrast shell, inert bridge contract, tests, audit updates, docs, source
ledger, task log, and handoff are complete. Tier 3 live execution, native
bridge implementation, product package identities, build/run/deploy, signing,
release, serial/RF/XBee writes, firmware flash, monitor, relay/load/mains, and
wiring remain closed.
