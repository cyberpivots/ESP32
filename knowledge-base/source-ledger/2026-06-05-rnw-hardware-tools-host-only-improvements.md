# RNW Hardware Tools Host-Only Improvements Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-HOST-ONLY-IMPROVEMENTS-2026-06-05`

## Scope

Tier 2 host-only RNW Hardware Tools source update. This ledger records
screen-space layout awareness, Hardware Tools startup-window sizing metadata,
review-only firmware catalog/install-preview records, saved-evidence
communications analysis, and native/live-surface audit hardening.

This ledger does not authorize native HostCommandBridge implementation or
dispatch, shell/DOS-C execution, serial port open/write, RF/XBee radio writes
or transmit, firmware flash/erase/monitor, OTAP execution, relay/load/mains
work, wiring, BLE/Web Serial/Web Bluetooth, SoftAP/local-network discovery,
signing, Store/App Installer distribution, commit, push, PR, deploy, or
release.

## Source Coverage

- `SRC-REACT-NATIVE-USE-WINDOW-DIMENSIONS-2026-06-05`: React Native
  `useWindowDimensions` source for live width/height/font-scale layout inputs.
- `SRC-MICROSOFT-WINDOWS-APPWINDOW-DISPLAYAREA-2026-06-05`: Microsoft
  AppWindow, DisplayArea, and OverlappedPresenter source for startup-window
  sizing and maximize planning.
- `SRC-ESPRESSIF-ESPTOOL-FIRMWARE-2026-06-05`: Espressif esptool source for
  future image artifact/offset planning fields only.
- `SRC-ESP-IDF-OTA-PLANNING-2026-06-05`: ESP-IDF OTA source for future
  rollback/partition/image-validation planning fields only.
- `SRC-ESP-IDF-ESPNOW`: ESP-NOW source for saved frame-budget and
  custody/retry/expiry analysis.
- `SRC-ESP-IDF-WIFI-SNIFFER-2026-06-05`: Wi-Fi sniffer/promiscuous planning
  source for saved-evidence communications analysis only.
- `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-05-29`,
  `SRC-DIGI-XCTU-FEATURES-2026-05-29`, and
  `SRC-DIGI-XCTU-LOCAL-DISCOVERY-2026-05-29`: Digi sources for redacted saved
  radio profile/API-frame/inventory analysis only.
- `SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`: local
  source for keeping `cbbs_host_command_bridge.v1` unavailable-only.

## Verified Facts

- `packages/cbbs-product-ui` already used React Native window dimensions but
  only width drove layout before this task.
- `packages/cbbs-product` already modeled Hardware Tools actions as
  artifact-review or Tier 3 closed, with no dispatch path.
- `cbbs_host_command_bridge.v1` remains unavailable-only and validates only
  non-executing bridge previews.
- Hardware Tools visible copy tests reject raw live-operation terms; app-visible
  communications and firmware labels therefore use redacted review wording.
- The read-only reviewer quorum for this slice approved host-only
  implementation and left all live bridge, hardware, firmware execution, radio,
  and release surfaces closed.

## Assumptions

- The implementation request authorizes repo edits for this host-only slice
  only.
- Saved fixture/source evidence is sufficient for catalog and communications
  analysis records, but not for any live operation.
- Future firmware execution, OTAP, native adapter work, or radio operation will
  require a new ADR/ABI and Tier 3 gate.

## Unknowns

- Native AppWindow build/runtime proof on Windows after the startup-size source
  change remains unverified in this task.
- Final package identity, capability acceptance, signing, and distribution path
  remain unresolved.
- Target device identity, artifact hashes, rollback manifests, and target
  compatibility remain unresolved for any future firmware action.
- Live bridge adapter semantics, recovery path, transcript proof, and cleanup
  proof remain unresolved.

## Implementation Record

- `packages/cbbs-product/src/index.ts`: added review-only firmware catalog and
  install-preview metadata, plus saved-evidence communications analysis records.
- `packages/cbbs-product-ui/src/index.tsx`: added pure
  `deriveProductShellLayout(width, height, fontScale)`, layout metadata props,
  short/wide/compact layout styles, bounded transcript/panel regions, and
  review-only firmware/comms panels.
- `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.cpp`:
  replaced fixed startup size with a DisplayArea/AppWindow work-area sizing
  helper and maximize request.
- `scripts/scaffold_audit_react_native.py`: added required source IDs and an
  audit that fails on app/native HostCommandBridge, attributed native module,
  process, transport, firmware-tool, or browser live-API surfaces.
- Focused Jest and Python tests pin the layout contract, catalog/comms
  records, visible-copy safety, and native/live-surface audit behavior.

## Validation

Validation is recorded in Task 0174. Focused host-only product, product UI,
Hardware Tools split-app, protocol, firmware scaffold, XBee study, custom
wireless protocol, four-relay safe-core, bridge-surface audit, typecheck, and
durable-record checks passed. At Task 0174 completion, the full React Native
scaffold-clean audit was blocked by retained Task 0173 local Debug
build/package outputs. Task 0175 subsequently cleaned that retained output
state and passed `scripts/scaffold_audit_react_native.py`. Runtime screenshot
proof is not claimed by this ledger.

## Decision

Decision: accept this as a bounded Tier 2 host-only source record for RNW
Hardware Tools improvements with the Task 0173 retained-output blocker noted.
All Tier 3 live bridge, hardware, firmware execution, radio, release, and
publication surfaces remain closed.
