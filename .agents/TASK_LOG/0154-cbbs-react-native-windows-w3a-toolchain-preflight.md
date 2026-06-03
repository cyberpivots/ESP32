# Task 0154: CBBS React Native Windows W3A Toolchain Preflight

Status: completed; W3 native generation and W4 build remain closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-PACKAGE-DEPS-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`

## Goal

Handle the Windows host/toolchain prerequisite gate for the CBBS React Native
Windows app after explicit user authority, without generating native Windows
project files or claiming RNW build/runtime proof.

## Routing Packet

- Verified facts: the user explicitly authorized Windows toolchain download,
  installation, and configuration; W2.1 package-only Windows shell changes were
  already present in the dirty tree; Windows PowerShell was available from WSL2;
  `apps/cbbs-windows` still had no app native `windows/` project.
- Assumptions: the safe W3A mutation was limited to Windows prerequisite
  remediation and durable records; native generation requires a later W3
  amendment, updated audit boundary, and a no-overwrite command plan.
- Unknowns: RNW `init-windows` merge behavior in this monorepo app, generated
  `Package.appxmanifest` contents, package identity, W4 build behavior, and
  runtime UI evidence remain unresolved.
- Selected tier: Tier 3.
- Owner role: Tooling with React Native DevEx/CI, Source Research,
  Security/Safety, and QA.
- Evidence need: official/source refresh, package-local dependency-script hash,
  pre/post Windows inventory, reviewer quorum, install/config log, no-native
  scan, source ledger, task record, handoff, and scaffold/record audits.
- Mutation boundary: Windows host RNW prerequisite installation/configuration
  only, plus W3A governance/source/docs/audit records. No RNW native generation,
  `init-windows`, `run-windows`, MSBuild build, deploy, package, signing, live
  connectivity, firmware/hardware, release, commit, push, PR, or deployment.
- Validation plan: run package-local RNW 0.83 dependency checks, install only
  missing required prerequisites through the versioned RNW script path, refresh
  Windows PATH and Corepack pnpm, re-run toolchain inventory, prove no app
  native folder, update durable records, run scaffold/record audits, and run
  `git diff --check`.
- Gate authority: explicit Tier 3 user authority for Windows toolchain handling
  only. W3 native project generation and W4 build remained rejected by quorum
  until W3A prerequisites, governance, audit, and no-overwrite conditions are
  cleared.
- Trust boundary: W3A proves Windows host prerequisites only; it does not prove
  RNW native generation, build/run, package identity, capability declarations,
  signing, release, live CBBS behavior, or hardware behavior.

## Reviewer Quorum

- Source reviewer, weight 3: approved host inventory/install/config and
  conditional W3 only after same-session prerequisite evidence; flagged public
  docs/source drift risk.
- DevEx/CI reviewer, weight 3: rejected native generation/build readiness;
  approved W3A inventory/install/config only, with W3 blocked on accepted
  amendment, audit update, and same-session proof.
- QA reviewer, weight 3: rejected W3/W4 readiness; approved host remediation
  only and required post-install inventory plus no-native proof.
- Tooling reviewer, weight 3: rejected W3/W4 now; approved source-backed
  prerequisite remediation and required recovery/no-overwrite records.
- Security/Safety reviewer, weight 3: conditionally approved prerequisite and
  later native boundary while keeping live, release, signing, external-service,
  serial/RF/BLE/network, and hardware surfaces closed.

Weighted disposition: 15/15 approval for W3A prerequisite remediation. W3
native generation and W4 build did not pass this quorum.

All reviewer outputs were captured and visible reviewer agents were closed
before the durable W3A decision was recorded.

## Toolchain Evidence

- Host: WSL2 on Windows `10.0.26200.8524`, with elevated Windows PowerShell
  available.
- Developer Mode: `AllowDevelopmentWithoutDevLicense = 1` and
  `AllowAllTrustedApps = 1`.
- Long paths: `LongPathsEnabled = 1`.
- Visual Studio: Visual Studio Community 2022 `17.14.37301.10` found, with RNW
  0.83 required components proven by package-local script and `vswhere`.
- Windows SDK directories: `10.0.19041.0`, `10.0.22621.0`, and `10.0.26100.0`
  found.
- Package-local script:
  `node_modules/react-native-windows/Scripts/rnw-dependencies.ps1`,
  SHA-256 `3579E330746598B44B858DD6DFA919CC11FCA944D3539C42ECA5BA5B8BBF6067`,
  length `25397` bytes.
- Floating public script check:
  `https://aka.ms/rnw-vs2022-deps.ps1`, SHA-256
  `35CF27EC5AD3612F4A50B65B35085E36C4D31172BDEB2C8CB97DC15D92349E70`,
  length `25260` bytes. It had drifted to VS 2026/.NET 10 checks, so it was
  not used for installation.
- RNW 0.83 package-local checks required VS 2022 `>= 17.11.0`, Node `>= 22`,
  Yarn, and .NET SDK `8.0`.

## Implementation Summary

- Ran the RNW 0.83 package-local dependency check before installation. It
  passed Windows version, Developer Mode, long paths, Visual Studio 2022
  components, Node, and .NET 8, and failed only Yarn.
- Ran the package-local RNW 0.83 dependency script with `-Install -NoPrompt
  -Verbose`; it installed `Yarn.Yarn` through WinGet and reported all mandatory
  requirements met.
- Added `C:\Program Files (x86)\Yarn\bin` to the Windows user PATH because the
  Yarn MSI install did not expose `yarn` to new WSL-launched PowerShell
  processes until PATH was refreshed.
- Activated the repo-pinned `pnpm@10.15.0` through Corepack so Windows `pnpm`
  resolves to `C:\Program Files\nodejs\pnpm.CMD`.
- Re-ran the package-local RNW 0.83 dependency script with a refreshed
  Machine+User PATH; all mandatory requirements passed.
- Inspected package-local RNW 0.83 `cpp-app` template behavior and found that
  `postInstall` updates `package.json` with Windows scripts and
  `@rnx-kit/jest-preset`, then runs an install. This means W3 native
  generation is not confined to `apps/cbbs-windows/windows` under the default
  CLI path.
- No native app Windows project was generated.

## Validation

- PASS: package-local RNW 0.83 dependency script after remediation:
  `All mandatory requirements met`.
- PASS: Windows `node --version`: `v24.12.0`.
- PASS: Windows `pnpm --version`: `10.15.0`.
- PASS: Windows `yarn --version`: `1.22.22`.
- PASS: Windows `.NET` SDK inventory includes `8.0.421`.
- PASS: `vswhere` found Visual Studio 2022 `devenv.exe` and `MSBuild.exe` with
  the RNW 0.83 required component set.
- PASS: app native scan found no app native Windows project; the only
  `react-native.config.js` hit was under `apps/cbbs-windows/node_modules`.

Follow-up validations are recorded in the source ledger and must remain green:
React Native scaffold audit, durable-record audit, agent-process audit,
scaffold verification, no-native app scan, and `git diff --check`.

Validation note: `verify_scaffold.py` initially failed because
`research/skills/available-skills.md` referenced stale GitHub/Canva plugin
cache hash `bd80d7d9`. The skill inventory was refreshed to same-session cache
hash `5e86d584` and source row
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-03` before rerunning the gate.

## Authority Limits

No RNW CLI `init-windows`, `run-windows`, native `windows/` project generation,
MSBuild build, Visual Studio launch, Package.appxmanifest capability
declaration, package identity, signing, installer/store packaging, EAS,
App Center, simulator/device launch, live network, BLE, Web Bluetooth,
Web Serial, local-network discovery, SoftAP, serial write, RF/XBee action,
firmware ABI change, bridge ABI change, serial ABI change, Gate F service-code
change, flash, erase, monitor, relay, load, mains, release, commit, push, PR,
or deploy is authorized by this task.

## Handoff

Handoff:
[../handoffs/0114-cbbs-react-native-windows-w3a-toolchain-to-qa.md](../handoffs/0114-cbbs-react-native-windows-w3a-toolchain-to-qa.md)

## Decision

Decision accepted: `cbbs_react_native_windows_w3a_toolchain_preflight`.
Windows host prerequisites are proven for the RNW 0.83 package-local check.
Next gate: W3 native generation requires accepted W3 governance/audit boundary,
same-session no-native baseline, explicit no-overwrite command plan, an
approved package/lockfile mutation boundary or a source-backed way to avoid
those mutations, and a fresh no-P1/P2 reviewer disposition before any
`init-windows` command.
