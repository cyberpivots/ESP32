# Task 0175: RNW Hardware Tools Debug Cleanup

Status: completed; scaffold-clean audit restored

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-CLEANUP-2026-06-05`,
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-LOCAL-DEBUG-LAUNCH-2026-06-05`,
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-HOST-ONLY-IMPROVEMENTS-2026-06-05`

## Routing

- Verified facts: Task 0173 intentionally retained
  `CbbsHardwareToolsWindows`, app-local Metro, the local Debug Appx
  registration, and generated Debug outputs for review. Same-session checks
  before cleanup showed `CbbsHardwareToolsWindows` PID `47248` responding from
  the Hardware Tools Debug layout, package
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg` registered from
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows.Package/bin/x64/Debug`,
  Metro on `127.0.0.1:8081` reporting app ID
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`, eleven
  `.msix`/`.appx` artifacts under `AppPackages`, and 1,912 files under the
  six generated output directories.
- Assumptions: the user-supplied cleanup plan authorizes only local Debug
  review cleanup for Hardware Tools. Stopping the matching app, app-local
  Metro, and package registration is needed before generated Debug output can
  be removed cleanly.
- Unknowns: process and file-lock state may drift between checks. Final
  scaffold-clean status is unknown until cleanup proof and validation pass.
- Selected tier: Tier 3 bounded local RNW runtime cleanup plus Tier 2
  durable-record updates.
- Owner role: RNW runtime cleanup with QA evidence, safety/security, and
  DevEx/CI review.
- Evidence need: before and after process proof, package-registration proof,
  Metro status and inspector proof, generated-output and package-artifact
  inventory, exact cleanup boundary, React Native scaffold audit, durable
  record audit, and focused Hardware Tools typecheck/Jest validation.
- Mutation boundary: this task record, source ledger, source index, docs index,
  cleanup notes in Tasks 0173 and 0174, only matching
  `CbbsHardwareToolsWindows` Debug process state, only the app-local Metro
  process chain tied to `apps/cbbs-hardware-tools-windows` and the Hardware
  Tools inspector app ID, only Appx package
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`, and only these
  generated output directories:
  `CbbsHardwareToolsWindows.Package/AppPackages`,
  `CbbsHardwareToolsWindows.Package/bin`,
  `CbbsHardwareToolsWindows.Package/obj`,
  `CbbsHardwareToolsWindows/obj`,
  `CbbsHardwareToolsWindows/x64/Debug`, and `windows/x64/Debug`.
- Reviewer quorum: project-local read-only subagents were available. Four
  reviewers were spawned, waited, captured, and closed. Lifecycle listing was
  not available in the exposed tool surface before spawning; all spawned
  reviewers were closed after output capture. The clarified mutation-start
  disposition was 13/13 approval with no P1/P2 blockers: RNW runtime
  coordinator weight 5, RNW QA evidence weight 3, React Native
  safety/security weight 3, and React Native DevEx/CI weight 2.
- Gate authority: the user-supplied cleanup plan opens only the named local
  Debug cleanup. It does not authorize hardware, bridge dispatch, firmware,
  radio/XBee, serial writes, signing, release, commit, push, PR, EAS,
  App Center, Store/App Installer distribution, or device/simulator proof.
- Validation plan: create the durable record first, re-check each target
  immediately before mutation, stop and unregister only matching runtime
  targets, delete only the six generated output directories, prove negative
  cleanup state, run `PYTHONDONTWRITEBYTECODE=1 python3
  scripts/scaffold_audit_react_native.py`, run `PYTHONDONTWRITEBYTECODE=1
  python3 scripts/scaffold_audit_records.py --min-task-id 173`, run
  `pnpm --filter @cbbs/hardware-tools-windows typecheck`, and run
  `pnpm --filter @cbbs/hardware-tools-windows test:windows`.
- Trust boundary: local Windows/WSL runtime state, local generated files,
  local audit/test output, and durable repo records only. This is not hardware,
  release, signing, Store/App Installer, or package-identity acceptance.

## Cleanup Execution

- Stopped only `CbbsHardwareToolsWindows` PID `47248` after confirming its path
  matched
  `H:\esp32\apps\cbbs-hardware-tools-windows\windows\CbbsHardwareToolsWindows.Package\bin\x64\Debug\CbbsHardwareToolsWindows\CbbsHardwareToolsWindows.exe`.
  The after-check returned no `CbbsHardwareToolsWindows` process.
- Stopped only the app-local Metro process chain whose command line was rooted
  at
  `pnpm --dir apps/cbbs-hardware-tools-windows exec react-native start --port
  8081 --no-interactive`. The stopped WSL PIDs were `935586`, `935619`,
  `935631`, and descendant Jest worker PIDs `936230`, `936236`, `936238`,
  `936239`, `936246`, `936251`, `936260`, `936279`, `936280`, `936286`,
  `936288`, `936298`, and `936300`. No PIDs remained after `TERM`; no `KILL`
  was needed.
- Removed only Appx package
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`. The after-check
  returned no `CbbsHardwareToolsWindows` Appx package.
- Deleted only the six generated output directories listed in the routing
  packet. The post-delete generated-output and `.msix`/`.appx` inventory was
  empty.

## Cleanup Proof

- Process proof: `Get-Process -Name CbbsHardwareToolsWindows` returned `[]`.
- Package proof: `Get-AppxPackage -Name CbbsHardwareToolsWindows` returned
  `[]`.
- Metro proof: `curl -fsS http://127.0.0.1:8081/status` and
  `curl -fsS http://127.0.0.1:8081/json/list` both failed to connect with
  curl exit `7`; `ss -ltnp 'sport = :8081'` showed no listener.
- Node process proof: a Node-only process filter for the app-local Metro
  command line and Hardware Tools app ID returned no rows.
- Output proof: `find apps/cbbs-hardware-tools-windows/windows -maxdepth 5`
  for `AppPackages`, `bin`, `obj`, `x64/Debug`, `*.msix`, and `*.appx`
  returned no rows.

## Validation

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 173`.
- `pnpm --filter @cbbs/hardware-tools-windows typecheck`.
- `pnpm --filter @cbbs/hardware-tools-windows test:windows` passed 1 suite,
  2 tests.
- `git diff --check` exited `0` with a CRLF normalization warning for
  `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.cpp`.

Not claimed:

- No RNW relaunch, build, deploy, signing, Store/App Installer package,
  device/simulator proof, live bridge dispatch, firmware execution, radio
  action, release, commit, push, or PR was performed.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee radio writes or transmit,
firmware flash/erase/monitor, OTAP execution, relay/load/mains work, wiring,
BLE/Web Serial/Web Bluetooth, SoftAP/local-network discovery, signing
certificates, Store/App Installer distribution, EAS, App Center,
credentials/key material, commit, push, PR, deploy, and release.

## Handoff

No handoff is required for this cleanup if validation passes. Future relaunch,
runtime proof, firmware execution, radio operation, bridge dispatch, release,
or publication work requires a new gate.

## Decision

Decision: accept the bounded cleanup of Task 0173 retained local Debug review
state. The React Native scaffold audit now passes in scaffold-clean mode. All
live bridge, hardware, firmware execution, radio, release, publication,
signing, commit, push, PR, and deploy surfaces remain closed.
