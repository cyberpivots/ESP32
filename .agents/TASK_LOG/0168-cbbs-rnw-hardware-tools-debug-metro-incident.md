# Task 0168: CBBS RNW Hardware Tools Debug Metro Incident

Status: resolved for local debug review; Metro retained for review

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-04

Source IDs:
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-METRO-INCIDENT-2026-06-04`

## Routing

- Verified facts: after a direct `shell:AppsFolder` launch of the retained
  local Debug package, the user reported a React Native error. Same-session
  checks found no Metro listener on `127.0.0.1:8081`, no Windows `node`
  process, and no live `CbbsHardwareToolsWindows` process. The generated Debug
  app loads `index` from Metro when `BUNDLE` is not set.
- Assumptions: the reported React Native error was caused by launching the
  retained Debug package without the matching app-local Metro server.
- Unknowns: the exact original redbox text was not captured before recovery.
- Selected tier: Tier 3 local RNW runtime incident plus Tier 2 instruction and
  skill update.
- Owner role: RNW runtime DevEx with QA, coordinator, and safety/security
  lenses.
- Evidence need: failing Metro/process state, reviewer outputs, recovery command
  transcript, process/window/package proof, loaded/no-redbox screenshot,
  instruction and skill guardrail updates, and cleanup/retention statement.
- Mutation boundary: local app/Metro process repair, local screenshot evidence,
  project docs/skill/source records, and memory note. No native source behavior
  change was required.
- Reviewer quorum: coordinator, RNW DevEx, and QA reviewers were spawned. The
  RNW DevEx reviewer identified direct app-registration launch without Metro as
  a P1 launch-path blocker. QA blocked any resolution claim until same-session
  failing state and post-fix evidence were captured. Coordinator identified the
  retained Debug package plus stopped Metro as the likely incident cause.
- Gate authority: the user explicitly requested investigation, resolution, and
  instruction/skill improvement after the React Native error report.
- Validation plan: prove current Metro/app state, attempt approved
  `run-windows --no-telemetry`, recover with matching app-local Metro if the
  debug package is already installed, capture loaded UI screenshot, then update
  guardrails and durable records.
- Trust boundary: this proves only local Debug Hardware Tools review readiness.
  It does not accept package identity, capability use, signing, release,
  Store/App Installer distribution, live bridge dispatch, serial/RF/XBee,
  firmware, relay/load/mains, wiring, or hardware action.

## Incident Evidence

- Direct launch state: `Get-AppxPackage -Name CbbsHardwareToolsWindows`
  returned `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`; initial
  process proof after direct launch showed `CbbsHardwareToolsWindows` PID
  `46664`, responding, but no Metro server was proven.
- Failure evidence after user report: no Metro listener on `8081`,
  `Invoke-WebRequest http://127.0.0.1:8081/status` failed, no Windows `node`
  process was running, and no `CbbsHardwareToolsWindows` process remained.
- Approved `run-windows` retry failed before launch in RNW Visual Studio
  discovery with `The "path" argument must be of type string. Received
  undefined`; this did not open release/signing/package surfaces.
- Recovery started the app-local Hardware Tools Metro server with
  `pnpm --dir apps/cbbs-hardware-tools-windows exec react-native start --port
  8081 --reset-cache --no-interactive --verbose`, then launched the installed
  Debug app registration.
- First recovery screenshot was rejected because it showed loading-only UI.
  Metro then completed the initial bundle transform on the Windows-mounted
  workspace.
- Accepted recovery screenshot after app restart against detached Metro:
  `C:\Users\cyber\AppData\Local\Temp\cbbs-hardware-tools-repair-screenshot-clean-2.png`,
  2560x1600, SHA-256
  `8E2121FA9F885726EDB94B1B2075EF4316292B1FF45859FA1C5F7ABB9192DA83`,
  visible `CBBS Hardware Tools`, no redbox, no loading-only state.
- The prior warning strip was traced through the Metro inspector to stale
  `Cannot connect to Metro` state from the bad direct launch. Restarting the app
  with detached Metro already running cleared the warning strip; the final
  inspector check showed only React Native debugger info/log entries.
- Final process proof: `CbbsHardwareToolsWindows` PID `46928`, window title
  `CbbsHardwareToolsWindows`, responding `True`.
- Final Metro proof: WSL and Windows both returned
  `packager-status:running` for `http://127.0.0.1:8081/status`.
- Final Metro inspector proof listed the connected app as
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`.
- Detached Metro PID retained for review: `935586`.

## Prevention

- Updated `.codex/skills/react-native-client-development/SKILL.md` to reject
  direct Start menu/AppFolder Debug launch as acceptance unless the matching
  app-local Metro server is already proven live and the screenshot is loaded.
- Updated `docs/projects/cbbs-react-native/README.md` with the RNW Debug review
  guardrail and stale-Metro split-app warning.
- Added a memory note for this workspace-specific failure mode because the user
  explicitly asked to remember the action and improve future behavior.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, commit, push, PR, deploy, and release.

## Validation

- Same-session failing state, recovery state, process/window proof, Metro proof,
  and screenshot proof were captured.
- `git diff --check` and durable-record audits must pass after the record and
  instruction updates.

## Decision

Decision: the local Debug Hardware Tools app review launch is repaired by
running the matching app-local Metro server and relaunching the installed Debug
app. The app and detached Metro server remain running for user review.

## Handoff

No handoff is required; the incident is resolved for local Debug review.
