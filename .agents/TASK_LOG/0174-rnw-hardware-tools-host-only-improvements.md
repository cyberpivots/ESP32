# Task 0174: RNW Hardware Tools Host-Only Improvements

Status: completed for host-only source/test scope; scaffold-clean blocker resolved by Task 0175 cleanup

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-HOST-ONLY-IMPROVEMENTS-2026-06-05`,
`SRC-REACT-NATIVE-USE-WINDOW-DIMENSIONS-2026-06-05`,
`SRC-MICROSOFT-WINDOWS-APPWINDOW-DISPLAYAREA-2026-06-05`,
`SRC-ESPRESSIF-ESPTOOL-FIRMWARE-2026-06-05`,
`SRC-ESP-IDF-OTA-PLANNING-2026-06-05`,
`SRC-ESP-IDF-ESPNOW`,
`SRC-ESP-IDF-WIFI-SNIFFER-2026-06-05`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-05-29`,
`SRC-DIGI-XCTU-FEATURES-2026-05-29`,
`SRC-DIGI-XCTU-LOCAL-DISCOVERY-2026-05-29`,
`SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`

## Routing

- Verified facts: `apps/cbbs-hardware-tools-windows` exists with generated RNW
  native source. `packages/cbbs-product-ui` used `useWindowDimensions` before
  this task but only width drove layout. `packages/cbbs-product` already kept
  Hardware Tools actions in artifact-review or Tier 3 closed modes. The
  `cbbs_host_command_bridge.v1` product/protocol path remains unavailable-only.
  Visible-copy tests reject raw live-operation wording.
- Assumptions: the implementation request authorizes repo edits for the
  approved host-only slice only. Saved fixtures/source records are acceptable
  for catalog and communications review metadata, but not for live operation.
- Unknowns: native AppWindow compile/runtime proof after this source change,
  final package identity/capability acceptance, signing/distribution path,
  target identity, artifact hashes, rollback manifests, target compatibility,
  native bridge adapter ABI, recovery path, transcript proof, and cleanup proof
  remain unresolved.
- Selected tier: Tier 2 host-only RNW Hardware Tools source/UI/audit/record
  work, with Tier 3 execution surfaces closed.
- Owner role: RNW product/UI owner with firmware catalog, communications
  analysis, bridge-safety, and evidence-record QA lenses.
- Evidence need: source-index/ledger coverage, focused Jest tests for product
  and product UI, split-app host tests, React Native scaffold audit, durable
  record audit, and host-only firmware/comms safety checks.
- Mutation boundary: `packages/cbbs-product`, `packages/cbbs-product-ui`,
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.cpp`,
  `scripts/scaffold_audit_react_native.py`, focused tests, this task record,
  `knowledge-base/source-ledger/2026-06-05-rnw-hardware-tools-host-only-improvements.md`,
  `knowledge-base/source-index.md`, and `docs/index.md`.
- Reviewer quorum: previous read-only RNW UI, firmware/device, comms, bridge
  safety, and source-record reviewers were completed and closed. Weighted
  outcome approved host-only implementation only; no live bridge, USB
  operation, firmware execution, serial/RF/XBee writes, relay/load/mains,
  signing, release, commit, push, or PR.
- Validation plan: run focused product/product-ui/hardware-tools Windows Jest
  suites; run `scripts/scaffold_audit_react_native.py`; run
  `scripts/scaffold_audit_records.py --min-task-id 174`; run firmware scaffold,
  XBee study, custom wireless protocol, and four-relay safe-core host checks
  where available without live hardware.
- Trust boundary: local source and host-only tests only. No runtime screenshot,
  device operation, radio operation, firmware execution, release, or
  publication evidence is claimed.

## Implementation

- Added `deriveProductShellLayout(width, height, fontScale)` with compact,
  standard, wide, and short modes plus non-visible layout metadata props.
- Bounded short-layout workspace, evidence, and transcript regions, and widened
  large viewports for page navigation, workspace, evidence, and analysis
  surfaces.
- Replaced the Hardware Tools fixed native startup size with AppWindow
  DisplayArea work-area sizing and maximize behavior.
- Added review-only firmware catalog records and install-preview metadata.
  Imported binaries remain untrusted until source, hash, target compatibility,
  and provenance are recorded.
- Added saved-evidence communications analysis records for ESP-NOW, radio
  profile, bridge, transport, discovery, queues/custody, and evidence views.
- Added React Native scaffold audit checks for forbidden native bridge symbols,
  attributed native module methods, process APIs, transport APIs, browser live
  APIs, and firmware-tool markers in app/native sources.

## Validation

Passed:

- `pnpm --filter @cbbs/protocol exec jest --config ../../jest.config.cjs packages/cbbs-protocol/__tests__/contract.test.ts --runInBand`
  passed: 24 tests.
- `pnpm --filter @cbbs/product exec jest --config ../../jest.config.cjs packages/cbbs-product/__tests__/product.test.ts --runInBand`
  passed: 15 tests.
- `pnpm --filter @cbbs/product-ui exec jest --config ../../jest.config.cjs packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx --runInBand`
  passed: 15 tests.
- `pnpm --filter @cbbs/hardware-tools-windows test:windows` passed: 2 tests.
- `pnpm --filter @cbbs/product typecheck`.
- `pnpm --filter @cbbs/product-ui typecheck`.
- `pnpm --filter @cbbs/hardware-tools-windows typecheck`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/scaffold_audits/test_react_native_scaffold.py::ReactNativeScaffoldAuditTests::test_rnw_native_bridge_surface_audit_blocks_dispatch_symbols`
  passed: 1 test.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 174`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/scaffold_audits/test_xbee_radio_study.py`
  passed: 15 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
  passed: 33 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
  passed the safe-core host suite.

Resolved cleanup blocker:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
  originally failed on retained Task 0173 Hardware Tools Debug build/package
  outputs under
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows.Package/AppPackages`,
  `bin`, `obj`, `CbbsHardwareToolsWindows/obj`,
  `CbbsHardwareToolsWindows/x64/Debug`, and `x64/Debug`. This blocker existed
  as retained local Debug review state and was not cleaned by this host-only
  implementation task.
- Task 0175 subsequently stopped the retained Hardware Tools Debug process,
  stopped the app-local Hardware Tools Metro process chain, unregistered the
  retained local Debug package, removed only the named generated Debug output
  directories, and passed
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
  The new native/live-surface audit remained separately validated by the
  focused scaffold test above.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee radio writes or transmit,
firmware flash/erase/monitor, OTAP execution, relay/load/mains work, wiring,
BLE/Web Serial/Web Bluetooth, SoftAP/local-network discovery, signing
certificates, Store/App Installer distribution, EAS, App Center,
credentials/key material, commit, push, PR, deploy, and release.

## Handoff

No handoff is required for this host-only implementation slice. A future Tier 3
runtime proof, firmware execution, OTAP, radio, or adapter task must open a new
gate with same-session target identity, rollback/hash proof, accepted ABI/ADR,
recovery path, transcript proof, cleanup proof, and explicit live authority.

## Decision

Decision: accept the named host-only implementation boundary with the known
scaffold-clean audit blocker above. All live bridge, hardware, firmware
execution, radio, release, publication, signing, commit, push, PR, and deploy
surfaces remain closed.
