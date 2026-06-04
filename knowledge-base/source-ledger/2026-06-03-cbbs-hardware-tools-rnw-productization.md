# CBBS Hardware Tools RNW Productization Ledger

Date: 2026-06-03

Source ID:
`SRC-LOCAL-CBBS-HARDWARE-TOOLS-RNW-PRODUCTIZATION-2026-06-03`

## Scope

Tier 2 React Native Windows source, test, audit, record, and compatibility
runtime proof work for the `CBBS Hardware Tools` product surface.

This record adds the generated `cbbs_rnw_menu.v1` Hardware Tools product menu
contract and replaces the prior global-action Hardware Tools shell with
page-scoped product workflows. It does not add executable host commands or live
hardware authority.

## Verified Facts

- `tools/react-native/cbbs_rnw_menu.v1.xml` is the product-facing source for
  Hardware Tools pages and actions.
- `tools/react-native/generate_rnw_menu.py` deterministically emits
  `packages/cbbs-product/src/hardwareToolsMenu.generated.ts` and fails closed
  on duplicate IDs, invalid page targets, unknown actions, secret-like fields,
  unsafe visible labels, and raw live-operation wording in visible copy.
- `@cbbs/product` exports generated menu/page/action types and helpers while
  preserving the existing Client, Sysop, and Hardware Tools app profiles.
- `@cbbs/product-ui` renders a page-scoped Hardware Tools desktop utility with
  a menu/dropdown bar, left page list, main workspace, right evidence/safety
  rail, gate phrase field, and transcript strip.
- Hardware Tools execution modes are bounded to `localOnly`,
  `artifactReview`, `bridgePreviewUnavailable`, and `tier3Closed`.
- The UI appends transcript rows only for local/artifact review work and does
  not dispatch native host commands, shell commands, serial/RF/XBee writes,
  firmware flash, relay/load/mains actions, package/signing/release actions, or
  free-form command requests.
- The existing `CbbsWindows` compatibility entry was rebuilt, deployed,
  launched, captured, and cleaned up after proof.

## Assumptions

- Unknown hardware, printer, firmware, enclosure, power, wiring, and radio
  facts should remain rendered as readiness, evidence, or closed-gate states
  until same-session evidence and authority exist.
- Split native app identities, icons, package manifests, signing, and release
  behavior remain future work outside this pass.
- Product copy may reference recorded artifacts and reviewed plans, but not
  live behavior that was not proven in this session.

## Unknowns

- Final native Windows project layout and installed identities for `CBBS
  Client`, `CBBS Sysop`, and `CBBS Hardware Tools`.
- Final HostCommandBridge native module ABI and implementation language.
- Same-session target identity, recovery path, safety evidence, and authority
  for any future executable radio, firmware, relay/load/mains, or live hardware
  action.

## Authority Limits

This record does not authorize separate native split-product build/deploy,
native bridge implementation, free-form shell input, serial writes, radio
writes, XBee setting changes, firmware flash, erase, monitor, relay/load/mains
work, wiring, CAD/G-code generation, package identity acceptance, signing,
Store/App Installer distribution, release, commit, push, PR, deploy, or live
hardware action.

## Runtime Evidence

- PASS: local RNW Debug x64 build/deploy/run for the existing `CbbsWindows`
  compatibility Hardware Tools entry using
  `pnpm --dir apps/cbbs-windows exec react-native run-windows --root . --sln windows\CbbsWindows.sln --proj windows\CbbsWindows\CbbsWindows.vcxproj --arch x64 --no-telemetry`.
- REJECTED: loading-only screenshot
  `research/bench-records/react-native-windows/cbbs-rnw-hardware-tools-productized-menu-20260603.png`,
  SHA-256
  `496223584E4B4F590F3C6369D8ED9A9D93ED0CE2489AF8124DE5CB0BDB60CA15`.
- PASS: accepted screenshot
  `research/bench-records/react-native-windows/cbbs-rnw-hardware-tools-productized-menu-after-wait-20260603.png`,
  SHA-256
  `C4050B275954634EC4D7BD601963894FD5811597EBFC66DF94473FF11A871D4A`,
  process `CbbsWindows` PID `32112`, title `CbbsWindows`, responding,
  `1000x1000`, showing `CBBS Hardware Tools`, the menu bar, page list, Bench
  workspace, evidence rail, gate phrase field, and transcript strip.
- PASS: RNW app and Metro/Node process tree were stopped after capture, the
  RNW tool session was closed, and ignored Debug build/package outputs plus
  MSBuild logs were removed before final audits.

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

Final acceptance is recorded in task log 0160.
