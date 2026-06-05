# Task 0169: RNW Hardware Tools Evidence Loop

Status: source/test validation complete; scaffold-clean audit deferred

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-04

Source IDs:
`SRC-LOCAL-CBBS-RNW-PRODUCT-SPLIT-HARDWARE-TOOLS-BRIDGE-CONTRACT-2026-06-03`,
`SRC-LOCAL-CBBS-HARDWARE-TOOLS-RNW-PRODUCTIZATION-2026-06-03`,
`SRC-LOCAL-CBBS-RNW-SOURCE-UI-MUTATION-2026-06-03`,
`SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`

## Routing

- Verified facts: Hardware Tools already used the product Windows shell,
  generated page-scoped actions, disabled closed controls, an inert gate
  phrase, and unavailable bridge transcript rows. The current protocol
  validator required result booleans by type but did not require
  `noSecretScan === true`. `ADR-0010` and the React Native project page keep
  native bridge dispatch, serial/RF/radio writes, firmware device operations,
  relay/load/mains, signing, release, deploy, and publication closed.
- Assumptions: the requested improvement loop is limited to source/test/UI
  evidence work, not runtime proof, RNW build/launch, native bridge work,
  hardware action, or release work.
- Unknowns: final native HostCommandBridge ABI, live adapter behavior, package
  identity acceptance, capability use, signing, release packaging, and runtime
  proof remain unknown.
- Selected tier: Tier 2 source/UI/protocol/evidence mutation.
- Owner role: RNW Product UI with Protocol/Bridge ABI, QA evidence, and
  Safety/Security lenses.
- Evidence need: protocol negative tests, product catalog/preview tests, UI
  render/accessibility/layout tests, focused app host tests, typechecks, lint,
  generator checks, scaffold audit disposition, and this durable record.
- Mutation boundary: `packages/cbbs-protocol`, `packages/cbbs-product`,
  `packages/cbbs-product-ui`, focused RNW app host-test mocks needed for the
  shared shell, and this task record. No native source, generated build output,
  lockfile, source-ledger, source-index, runtime, hardware, or release mutation
  is included.
- Reviewer quorum: read-only subagents were attempted and then closed. The
  coordinator, protocol/bridge, product UI, and QA reviewers approved the
  source/test boundary with conditions. The safety/security reviewer blocked
  scaffold-clean acceptance because ignored RNW native build/package outputs
  already exist under split Windows native trees. The parent accepted only the
  source/test mutation and records scaffold-clean validation as deferred.
- Gate authority: Tier 2 source/test/UI evidence mutation only. Tier 3 is
  closed.
- Validation plan: run package typechecks, focused Jest, Hardware Tools app
  host test, generator checks, root typecheck, root lint, React Native scaffold
  audit for disposition, record audit, and `git diff --check`.
- Trust boundary: source and host-test evidence only. No Metro/app runtime,
  RNW native build/run, bridge dispatch, shell/DOS-C execution, serial/RF/radio
  write, firmware device operation, relay/load/mains, signing, release, commit,
  push, PR, or deploy authority is opened.

## Changes

- Hardened `validateHostCommandBridgeResult` so unavailable bridge results now
  require `noSecretScan === true`, while still forcing unavailable status,
  `accepted:false`, `executed:false`, `available:false`, and
  `reason:adapter_unavailable`.
- Added protocol regressions for `noSecretScan:false`, all non-unavailable
  result statuses, exact byte bounds, secret-like fields, and forbidden host
  command fields.
- Added a typed Hardware Tools evidence catalog keyed by the generated
  `evidenceRef` aliases, with provenance, redaction notes, and authority notes.
- Added a dry-run preview helper for enabled bridge-backed artifact reviews.
  The helper builds and validates a bounded `dryRun:true` request with
  `appId:hardware-tools`, `actorRole:sysop`, `targetRef:review-target`,
  primary redaction, non-secret params, no dispatch path, and the existing
  unavailable result. Tier 3 closed actions return blocked-gate metadata only.
- Added a closed-work matrix derived from `CLOSED_SURFACE_IDS` with sanitized
  visible labels, disabled state, and safety-gate evidence.
- Updated the shared product shell to render Hardware Tools evidence
  provenance, bridge preview, closed-work matrix, compact layout branches, and
  accessibility labels/hints/state for closed work, previews, evidence rows,
  actions, menus, and the gate phrase.
- Updated split app host-test mocks to provide deterministic
  `useWindowDimensions` for the shared shell.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee/radio writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, runtime proof, commit, push, PR, deploy, and
release.

## Validation

- PASS: `pnpm --filter @cbbs/protocol typecheck`.
- PASS: `pnpm --filter @cbbs/product typecheck`.
- PASS: `pnpm --filter @cbbs/product-ui typecheck`.
- PASS: `pnpm --filter @cbbs/hardware-tools-windows typecheck`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_win31_parity.py --check`.
- PASS: focused Jest for protocol, product, product-ui, and Hardware Tools app:
  4 suites, 50 tests.
- PASS: `pnpm --filter @cbbs/hardware-tools-windows test:windows`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm lint` after fixing the unconditional hook call and host mocks.
- PASS: focused Jest for product-ui plus Client/Sysop/Hardware Tools/legacy
  Windows app host tests: 5 suites, 22 tests.
- FAIL, deferred: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
  found pre-existing ignored RNW native build/package outputs under
  `apps/cbbs-client-windows/windows/`, `apps/cbbs-sysop-windows/windows/`, and
  `apps/cbbs-hardware-tools-windows/windows/`, including `obj`, `bin`,
  `x64/Debug`, AppX/AppPackages-style outputs, binaries, symbols, and package
  recipes. No cleanup was performed under this source/test gate.

## Handoff

No handoff is required for this source/test improvement. A future cleanup gate
can remove ignored RNW native build/package outputs and rerun the scaffold audit
before any scaffold-clean claim.

## Decision

Decision: accept the Tier 2 source/test/UI evidence improvements. The
HostCommandBridge remains unavailable-only and non-dispatching. Scaffold-clean
acceptance is not claimed in this task because the read-only scaffold audit is
blocked by pre-existing generated RNW outputs.
