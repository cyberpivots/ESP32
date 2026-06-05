# RNW Hardware Tools Debug Cleanup Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-CLEANUP-2026-06-05`

## Scope

Tier 3 bounded local RNW Debug cleanup for `CbbsHardwareToolsWindows`, plus
Tier 2 durable-record updates. This ledger records cleanup of the intentionally
retained Task 0173 local Debug review state so the React Native scaffold audit
can return to scaffold-clean mode.

This ledger does not authorize release packaging, signing, Store/App Installer
distribution, native HostCommandBridge dispatch, shell/DOS-C execution,
serial/RF/XBee writes, firmware flash/erase/monitor, relay/load/mains work,
wiring, BLE/Web Serial/Web Bluetooth, SoftAP/local-network discovery, commit,
push, PR, deploy, or release.

## Source Coverage

- `SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-LOCAL-DEBUG-LAUNCH-2026-06-05` records
  the retained local Debug launch state being cleaned by this task.
- `SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-HOST-ONLY-IMPROVEMENTS-2026-06-05`
  records that Task 0174 was blocked only by the retained Task 0173 Debug
  output state.
- Same-session local process, package, Metro, filesystem, audit, and test
  outputs are recorded in Task 0175.

## Verified Facts

- Task 0173 retained the Hardware Tools Debug app process, app-local Metro,
  local Debug Appx registration, and generated Debug outputs for review.
- Before cleanup, same-session checks showed `CbbsHardwareToolsWindows` PID
  `47248`, package
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`, Hardware Tools Metro
  inspector app ID on `127.0.0.1:8081`, eleven `.msix`/`.appx` artifacts, and
  1,912 generated files in the approved output directories.
- The read-only reviewer quorum approved starting the bounded cleanup mutation
  after Task 0175 record creation, with final acceptance gated on fresh
  negative cleanup proof and validation.
- Task 0175 stopped only the matching Hardware Tools Debug process, stopped
  only the app-local Hardware Tools Metro process chain, unregistered only
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`, and deleted only the
  six approved generated output directories.
- Post-cleanup proof showed no `CbbsHardwareToolsWindows` process, no
  `CbbsHardwareToolsWindows` Appx registration, no port `8081` listener, no
  app-local Hardware Tools Metro process, no generated output groups, and no
  `.msix`/`.appx` artifacts under the Hardware Tools Windows tree.

## Assumptions

- The cleanup plan authorizes only local Debug review cleanup for Hardware
  Tools.
- Future review relaunch will use a new RNW runtime gate rather than retaining
  this Debug output state.

## Unknowns

- Future Hardware Tools runtime review relaunch is unresolved and requires a
  separate RNW runtime gate.

## Validation

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 173`.
- `pnpm --filter @cbbs/hardware-tools-windows typecheck`.
- `pnpm --filter @cbbs/hardware-tools-windows test:windows`.
- `git diff --check` exited `0` with a CRLF normalization warning for the
  existing RNW C++ source file.

## Decision

Decision: accept the bounded cleanup of the Task 0173 retained local Debug
review state. The React Native scaffold audit is restored to scaffold-clean
mode without authorizing RNW relaunch, build, deploy, signing, release,
publication, live bridge dispatch, firmware execution, radio action, or
hardware action.
