# CBBS RNW Product Split And Hardware Tools Bridge Contract Ledger

Date: 2026-06-03

Source ID:
`SRC-LOCAL-CBBS-RNW-PRODUCT-SPLIT-HARDWARE-TOOLS-BRIDGE-CONTRACT-2026-06-03`

## Scope

Tier 2 React Native Windows source, test, audit, and record work that splits
the former single Windows cockpit into three product-facing source apps:
`CBBS Client`, `CBBS Sysop`, and `CBBS Hardware Tools`.

This record also adds an inert `cbbs_host_command_bridge.v1` contract for
Hardware Tools planning. The default result is unavailable and non-executing.

## Verified Facts

- `@cbbs/product` defines three product app profiles and keeps internal
  app/view/action IDs separate from visible product copy.
- `@cbbs/product-ui` renders high-contrast React Native product shells using
  app-local UI intents only.
- `apps/cbbs-client-windows`, `apps/cbbs-sysop-windows`, and
  `apps/cbbs-hardware-tools-windows` register separate Windows product app
  components.
- `apps/cbbs-windows` is now a compatibility entry that opens Hardware Tools
  and does not render the previous developer-facing cockpit text.
- `packages/cbbs-protocol` keeps `cbbs_client_fixture.v1` local UI intents
  unchanged and adds a separate `cbbs_host_command_bridge.v1` validator and
  unavailable-result helper.

## Assumptions

- Separate native packaging, installed app identities, icons, Store metadata,
  signing, and distribution remain future work.
- Hardware Tools bridge requests are schema/test artifacts only until a later
  Tier 3 gate opens native execution.
- Product UI may show user-facing controls for unavailable work, but those
  controls must not call host commands or hardware.

## Unknowns

- Final native Windows project layout for the three product apps.
- Final HostCommandBridge native module ABI and implementation language.
- Same-session hardware identity, recovery, and safety evidence for any later
  executable bridge action.

## Authority Limits

This record does not authorize native build/run/deploy, release packaging,
signing, App Installer, Store publication, shell execution, serial writes,
radio writes, firmware flash, erase, monitor, relay/load/mains work, wiring,
or live hardware action.

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
- PASS: `pnpm test -- packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx packages/cbbs-product/__tests__/product.test.ts packages/cbbs-protocol/__tests__/contract.test.ts`
- PASS: targeted RNW product source scan found no live host, serial, RF,
  flash, shell, COM-port, or secret markers in product app/source paths.
- PASS: local RNW Debug x64 build/deploy/run for the `CbbsWindows`
  compatibility Hardware Tools entry with
  `pnpm --dir apps/cbbs-windows exec react-native run-windows --root . --sln windows\CbbsWindows.sln --proj windows\CbbsWindows\CbbsWindows.vcxproj --arch x64 --no-telemetry`.
- PASS: accepted runtime screenshot
  `research/bench-records/react-native-windows/cbbs-rnw-product-split-hardware-tools-after-wait-20260603.png`,
  SHA-256
  `5A7D4F130D9A7E3ACCADCC1FB53D07902578A7A4C05D4ACD9F34AA030A3AEC23`,
  process `CbbsWindows` PID `29104`, title `CbbsWindows`, `1000x1000`,
  showing `CBBS Hardware Tools`.
- PASS: RNW app and Metro packager were stopped after capture, ignored Debug
  build/package outputs were removed, and final scaffold audit was rerun.

Final acceptance is recorded in task log 0159.
