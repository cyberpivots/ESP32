# Task 0158: CBBS RNW High-Contrast Live-Control Cockpit

Status: completed for app-local source/test cockpit; scaffold audit remains
post-clean only

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-BUILD-LAUNCH-INTEGRATED-2026-06-03`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`,
`SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`,
`SRC-DIGI-XBP9B-DPUT-001`,
`SRC-DIGI-XBEE-900HP-AP`,
`SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`,
`SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`,
`SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`,
`SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`

## Goal

Replace the raw text RNW Windows operations screen with a high-contrast
operations cockpit while keeping all live-control surfaces app-local,
redacted, and non-executable.

## Routing Packet

- Verified facts: `ADR-0010` accepts the CBBS React Native Windows lane and
  W4 records exist for RNW project metadata, mesh discovery evidence, XBee
  radio evidence, and firmware evidence. `@cbbs/protocol` allows only local UI
  intents and rejects live-action intent names. The previous running
  `CbbsWindows` process existed before this task.
- Assumptions: the requested `Live Controls` direction means visible controls
  with local transcript behavior only, not a host-command bridge or live
  serial/RF/flash execution.
- Unknowns: package identity, signing, release path, future host-command bridge
  ABI, and final production update policy remain unresolved. RNW scaffold audit
  status remains post-clean because Debug build outputs are present.
- Selected tier: Tier 2, because the UI exposes hardware-adjacent evidence and
  disabled live-control affordances, but this task does not run hardware,
  serial/RF, flash, signing, release, or a host-command bridge.
- Owner role: React Native Windows/UI with QA, protocol/state, and
  safety/security lenses.
- Evidence need: source/test proof for shell regions, accessibility states,
  redaction, disabled controls, local-only intent validation, no host dispatch,
  and refreshed visual evidence if safely available from the already-running
  app.
- Mutation boundary: `apps/cbbs-windows/src/index.tsx`,
  `apps/cbbs-windows/__tests__/windowsHostOnly.test.tsx`, this task record,
  and generated screenshot evidence under
  `research/bench-records/react-native-windows/`.
- Validation plan: Windows package typecheck/test, root typecheck/lint,
  `git diff --check`, source-only dispatch scan, Metro bundle marker check,
  and screenshot inspection without starting a new RNW deploy/run command.
- Trust boundary: app-local React Native source/test and already-running
  Windows UI proof only. No live hardware, serial/RF/XBee write, firmware
  flash, relay/load/mains, signing, packaging, release, or external service
  action is accepted.

## Reviewer Disposition

- React Native UI parity reviewer, weight 3: no P1; required selected
  accessibility state, stronger disabled-surface tests, and no command
  dispatch tests.
- React Native protocol/state reviewer, weight 3: no P1; required the
  dot-separated action IDs to remain Windows-only catalog IDs, not protocol
  `IntentId` values or emitted payload strings.
- QA validation reviewer, weight 3: no P1; required the package Windows Jest
  run to become clean and noted scaffold audit as post-clean only.
- Safety/security reviewer, weight 3: blocked acceptance until typed
  confirmation, redacted primary COM details, disabled dangerous controls, no
  raw command strings, and evidence-only wording were implemented. Those
  source/test conditions are now covered. The scaffold audit condition remains
  post-clean because existing Debug RNW outputs are still present and were not
  changed by this task.
- Coordinator, weight 5: accepted only the app-local source/test and
  already-running-window visual proof boundary.

## Implemented Changes

- Refactored `apps/cbbs-windows/src/index.tsx` into a high-contrast cockpit
  using app-local React Native primitives and `StyleSheet`.
- Added left role/view rail, top safe-state banner, main operations workspace,
  right safety/evidence rail, and bottom transcript/preview console.
- Added Windows-only action IDs:
  `mesh.discoverySnapshot`, `mesh.serviceCatalog`, `xbee.inventory`,
  `xbee.readonlyQuery`, `xbee.profileDiff`, `xbee.writePlan`,
  `firmware.build`, and `firmware.flashCom6`.
- Kept enabled live controls local-only: enabled actions append transcript rows
  and emit safe `view_proof` intents only. XBee write-plan and firmware flash
  controls are visually armed but disabled.
- Added inert typed confirmation text. Typing does not enable closed actions.
- Redacted primary dashboard port details; `COM6`/`COM15` are visible only in
  the right evidence/detail rail.
- Replaced raw command strings with sanitized previews and evidence-only
  wording.
- Updated Windows tests with a local host-render mock to avoid the RNW Jest
  `Text` mock failure while still testing component behavior.

## Validation

- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `timeout 180s pnpm --filter @cbbs/windows-spike test:windows`
  (17 tests passed).
- PASS: `pnpm typecheck`.
- PASS: `pnpm lint`.
- PASS: `git diff --check`.
- PASS: source-only dispatch scan found no matches in `apps/cbbs-windows/src`
  for `HostCommandBridge`, `runAction`, `child_process`, `SerialPort`,
  `navigator.serial`, `idf.py`, `react-native run-windows`, `esptool`, or
  `powershell`.
- PASS: Metro bundle probe returned length `5165176`,
  `HasCockpit=true`, `HasLiveControls=true`, and `HasHostBridge=false`.
- PASS: running Windows process proof found `ProcessId=29964`,
  `Title=CbbsWindows`, `Responding=true`.
- PASS: refreshed screenshot captured after a direct Reload click:
  `research/bench-records/react-native-windows/cbbs-windows-high-contrast-cockpit-reload-click-20260603.png`,
  SHA-256
  `ABAB5591618A8A0CA3031C914E74F6101F61EF88426876A8B3E0B87D0A363B36`.
  Visual inspection shows the high-contrast cockpit with left rail, safe-state
  banner, main evidence cards, right evidence/safety rail, and disabled closed
  surfaces.

Notes:

- Two earlier screenshots,
  `cbbs-windows-high-contrast-cockpit-20260603.png` and
  `cbbs-windows-high-contrast-cockpit-reload-20260603.png`, showed an RNW
  `HMRClient.setup` error dialog and were not accepted as cockpit proof.
- `scripts/scaffold_audit_react_native.py` was not run as an acceptance gate in
  this task because the existing RNW Debug build output tree remains present.
  Per the prior W4 record, that audit is post-clean only until generated Debug
  outputs are removed or separately handled.
- No new RNW `run-windows`, deploy, package, signing, serial/RF, XBee write,
  firmware flash, or hardware command was run by this task.

## Authority Limits

This task accepts only app-local RNW source/test UI changes and screenshot
evidence from the already-running Windows app after UI reload. It does not
authorize or prove a host-command bridge, serial/RF/XBee writes, firmware
flash/erase/monitor, relay/load/mains operation, package identity acceptance,
signing, Store/App Installer distribution, release, commit, push, PR, or
external-service automation.

## Decision

Decision accepted:
`cbbs_rnw_high_contrast_live_control_cockpit_source_test`.

No handoff is required for continuation from this task. Future executable
controls require a separate Tier 3 host-command bridge gate with same-session
authority, recovery path, and closed-surface review.
