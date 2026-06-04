# Task 0160: CBBS Hardware Tools RNW Productization

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-LOCAL-CBBS-RNW-PRODUCT-SPLIT-HARDWARE-TOOLS-BRIDGE-CONTRACT-2026-06-03`,
`SRC-LOCAL-CBBS-HARDWARE-TOOLS-RNW-PRODUCTIZATION-2026-06-03`,
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-03`

## Routing

- Verified facts: task 0159 created product-facing RNW app packages and an
  inert bridge contract, but Hardware Tools still needed a generated menu
  source, page-scoped command surfaces, dropdown/menu behavior, transcript
  proof, and stronger no-dispatch tests. The existing `CbbsWindows`
  compatibility native project can be refreshed without creating split native
  projects.
- Assumptions: the accepted plan authorizes Tier 2 source, UI, protocol-test,
  audit, records, and compatibility-app proof only. Product copy can describe
  reviewed artifacts and closed gates, but not unverified hardware behavior.
- Unknowns: final split native app identities, native HostCommandBridge ABI,
  exact hardware target evidence, live radio behavior, live firmware update
  behavior, signing, packaging, and release path remain unresolved.
- Selected tier: Tier 2.
- Owner role: React Native Windows/UI product owner with Protocol/Bridge,
  XBee/radio, Safety/Security, and QA lenses.
- Evidence need: XML generator tests, generated TypeScript parity, product/UI
  tests, protocol no-dispatch tests, audit results, runtime screenshot proof,
  SHA-256, window/process proof, dimensions, and cleanup proof.
- Mutation boundary: `tools/react-native/`, `packages/cbbs-product/`,
  `packages/cbbs-product-ui/`, `packages/cbbs-protocol` tests,
  `apps/cbbs-windows` compatibility source/tests/docs,
  `apps/cbbs-hardware-tools-windows` validation, scaffold audits, docs,
  source ledger/index, task log, handoff, and screenshot evidence under
  `research/bench-records/react-native-windows/`.
- Gate authority: user authorized implementation of the Hardware Tools RNW
  productization plan. No Tier 3 live bridge, serial/RF/XBee write, firmware
  flash, relay/load/mains work, package/signing/release, commit, push, PR, or
  deploy authority is granted.
- Validation plan: run XML generator checks, targeted Python unit tests,
  product/product-ui/protocol Jest tests, package and root TypeScript checks,
  Windows package tests, root lint/test, scaffold audits, compatibility
  `CbbsWindows` build/deploy/run proof, screenshot capture, generated-output
  cleanup, record audit, and `git diff --check`.
- Trust boundary: source/test/runtime screenshot proof for the existing
  compatibility entry only. No separate split-app native runtime or hardware
  execution is claimed.

## Reviewer Quorum

- Coordinator, weight 5: accepted the Tier 2 source/test/record boundary after
  reviewer collection and lifecycle cleanup.
- React Native UI parity reviewer, weight 3: rejected the prior global action
  grid and required page-scoped Hardware Tools navigation, menu/dropdown
  behavior, transcript evidence, and removal of scaffold/developer copy.
- Protocol/Bridge reviewer, weight 3: accepted only inert alias-backed
  previews and required the HostCommandBridge validator to remain fail-closed.
- XBee/radio reviewer, weight 3: accepted offline/product-copy radio planning
  surfaces only; Tier 3 radio contact and setting writes remain closed.
- Safety/Security reviewer, weight 3: required redacted visible copy, disabled
  dangerous controls, and generated-output cleanup.
- QA reviewer, weight 3: required generator freshness, UI behavior tests,
  no-dispatch tests, scaffold audits, and compatibility-app proof.

Weighted result: no P1/P2 blocker remained for the named Tier 2 mutation
boundary. Tier 3 live execution prerequisites remain closed.

## Changes

- Added `cbbs_rnw_menu.v1` XML for Hardware Tools and a deterministic stdlib
  Python generator that emits tracked TypeScript menu data for `@cbbs/product`.
- Added generator/unit tests for freshness, fixed Hardware Tools pages, unique
  IDs, page targets, page-scoped actions, and fail-closed unsafe copy.
- Extended `@cbbs/product` with `ProductMenu`, `ProductPage`,
  `ProductSection`, `ProductMenuItem`, `ProductCapabilityGroup`, and
  `ProductExecutionMode` types, generated Hardware Tools menu export, and
  page-scoped action helpers.
- Replaced the Hardware Tools shell with a product-facing desktop utility:
  menu/dropdown bar, left page list, main workspace, right evidence/safety
  rail, gate phrase field, and bottom transcript strip.
- Kept execution modes bounded to `localOnly`, `artifactReview`,
  `bridgePreviewUnavailable`, and `tier3Closed`. Only local/artifact review
  actions append UI transcript entries; none call native modules or host
  commands.
- Strengthened product, product UI, protocol, compatibility Windows, and React
  Native scaffold tests so visible copy avoids scaffold/raw live terms and UI
  actions do not dispatch shell, serial/RF/XBee write, flash, relay/load/mains,
  package/signing/release, or free-form command requests.
- Updated the current local Codex plugin skill inventory record from stale
  plugin cache hash `5e86d584` to current hash `2b564709`, because the scaffold
  skill audit failed closed on stale local plugin paths.

## Runtime Proof

- PASS: local RNW Debug x64 build/deploy/run for the existing `CbbsWindows`
  compatibility entry using:
  `pnpm --dir apps/cbbs-windows exec react-native run-windows --root . --sln windows\CbbsWindows.sln --proj windows\CbbsWindows\CbbsWindows.vcxproj --arch x64 --no-telemetry`.
- REJECTED: first screenshot
  `research/bench-records/react-native-windows/cbbs-rnw-hardware-tools-productized-menu-20260603.png`,
  SHA-256
  `496223584E4B4F590F3C6369D8ED9A9D93ED0CE2489AF8124DE5CB0BDB60CA15`,
  because it showed only the RNW loading surface.
- PASS: accepted screenshot
  `research/bench-records/react-native-windows/cbbs-rnw-hardware-tools-productized-menu-after-wait-20260603.png`,
  SHA-256
  `C4050B275954634EC4D7BD601963894FD5811597EBFC66DF94473FF11A871D4A`,
  captured from process `CbbsWindows` PID `32112`, title `CbbsWindows`,
  responding, `1000x1000`. Visual inspection shows `CBBS Hardware Tools`,
  the menu bar, page list, Bench workspace, evidence rail, gate phrase field,
  and transcript strip.
- PASS: post-capture cleanup stopped `CbbsWindows`, stopped the Metro/Node
  process tree, closed the RNW tool session, and removed ignored Debug
  build/package outputs plus MSBuild logs before final audits.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.rnw_menu.test_rnw_menu`
- PASS: `pnpm --filter @cbbs/product typecheck`
- PASS: `pnpm --filter @cbbs/product-ui typecheck`
- PASS: `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts`
- PASS: `timeout 180s pnpm --filter @cbbs/windows-spike test:windows`
- PASS: `timeout 180s pnpm --filter @cbbs/hardware-tools-windows test:windows`
- PASS: `pnpm test -- packages/cbbs-product/__tests__/product.test.ts`
- PASS: `pnpm test -- packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.lcd_bbs_menu.test_lcd_bbs_menu tests.scaffold_audits.test_xbee_radio_study tests.rnw_menu.test_rnw_menu`
- PASS: `pnpm --filter @cbbs/hardware-tools-windows typecheck`
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`
- PASS: `pnpm typecheck`
- PASS: `pnpm lint`
- PASS: `pnpm install --frozen-lockfile`
  - Warning retained: build scripts for `msgpackr-extract` and
    `unrs-resolver` were ignored.
- PASS: `pnpm test`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `git diff --check`
- PASS: post-proof process/output scan found no `CbbsWindows`, Metro,
  `run-windows`, ignored RNW Debug output dirs, AppPackages, MSBuild binlogs,
  or MSBuild warning logs remaining.

## Authority Limits

This task does not authorize or prove separate native product apps,
HostCommandBridge native implementation, free-form shell input, serial/RF/XBee
writes, radio setting changes, firmware flash, erase, monitor, relay/load/mains
work, wiring, CAD/G-code generation, package identity acceptance, signing,
Store/App Installer distribution, release, commit, push, PR, deploy, or live
hardware action.

## Decision

Accepted as Tier 2 host-only RNW Hardware Tools productization. The generated
menu contract, page-scoped product shell, inert execution modes, strengthened
tests/audits, records, and existing `CbbsWindows` compatibility runtime proof
are complete. Future executable bridge or hardware actions require a separate
Tier 3 gate with same-session evidence, explicit authority, recovery path, and
closed-surface review.

## Handoff

Handoff:
[../handoffs/0119-cbbs-hardware-tools-rnw-productization-to-qa.md](../handoffs/0119-cbbs-hardware-tools-rnw-productization-to-qa.md)
