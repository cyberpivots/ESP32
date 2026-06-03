# CBBS React Native Windows W3A Toolchain Ledger

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-PACKAGE-DEPS-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`

## Scope

Tier 3 Windows host/toolchain preflight for `apps/cbbs-windows`. This record
proves RNW 0.83 package-local prerequisite readiness only. It does not open
native Windows project generation, RNW CLI execution beyond dependency checks,
Windows build/run, live transport, hardware, publication, or release authority.

## Source Coverage

- Official RNW 0.83 System Requirements and CLI docs remain source coverage for
  Windows-only development, Developer Mode, Visual Studio, SDK, Node, RNW CLI
  `--no-telemetry`, and `cpp-app` template planning.
- Package-local RNW 0.83 script coverage is recorded because the public
  `https://aka.ms/rnw-vs2022-deps.ps1` script had drifted to future VS/.NET
  checks during this run.
- Local W3A evidence records the actual host inventory and remediation result.

## Verified Facts

- Host inventory was WSL2 on Windows `10.0.26200.8524` with elevated Windows
  PowerShell available.
- Developer Mode and long paths were already enabled.
- Visual Studio Community 2022 `17.14.37301.10` was installed.
- Windows SDK directories included `10.0.19041.0`, `10.0.22621.0`, and
  `10.0.26100.0`.
- The RNW 0.83 package-local script hash was
  `3579E330746598B44B858DD6DFA919CC11FCA944D3539C42ECA5BA5B8BBF6067`.
- The package-local script required VS 2022 `>= 17.11.0`, Node `>= 22`, Yarn,
  and .NET SDK `8.0`.
- The package-local script initially failed only Yarn.
- The package-local script installed `Yarn.Yarn` via WinGet. WinGet reported
  Yarn `1.22.22` and installer SHA-256
  `ebc1f46891b8d507efad2dd18eec2c4e617457f93e13bc701483cb047a053fa1`.
- Yarn installed under `C:\Program Files (x86)\Yarn\bin`; that directory was
  added to the Windows user PATH.
- Corepack prepared/enabled `pnpm@10.15.0`, matching the repo
  `packageManager`.
- The final package-local RNW dependency check reported all mandatory
  requirements met.
- Package-local RNW 0.83 `cpp-app` template `postInstall` updates
  `package.json` with Windows scripts and `@rnx-kit/jest-preset`, then runs an
  install. This blocks a W3 command plan that promises only
  `apps/cbbs-windows/windows` mutations.
- No app native Windows project was generated.

## Assumptions

- The package-local RNW 0.83 dependency script is more appropriate for this
  repo lane than the floating public `aka.ms` script when the two disagree.
- WSL/Linux validation remains useful for repo checks but cannot prove RNW
  native Windows build or runtime behavior.

## Unknowns

- RNW `init-windows` merge behavior for the scoped package name and missing
  app metadata is not proven.
- A supported way to run `init-windows` while avoiding package/lockfile
  mutations is not proven.
- Generated native manifest capabilities, package identity, signing, and build
  behavior are not proven.
- Runtime screenshots and live CBBS behavior remain separate gates.

## Authority Limits

No RNW CLI `init-windows`, `run-windows`, native `windows/` folder generation,
Visual Studio/MSBuild build, Package.appxmanifest capability declaration,
package identity, signing, installer/store packaging, EAS, App Center,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial write, RF/XBee action, firmware ABI
change, bridge ABI change, serial ABI change, Gate F service-code change,
flash, erase, monitor, relay, load, mains, release, commit, push, PR, or deploy
is authorized by this record.

## Validation

- PASS: package-local RNW dependency script after remediation:
  `All mandatory requirements met`.
- PASS: Windows `node --version`: `v24.12.0`.
- PASS: Windows `pnpm --version`: `10.15.0`.
- PASS: Windows `yarn --version`: `1.22.22`.
- PASS: Windows `.NET` SDK inventory included `8.0.421`.
- PASS: `vswhere` found Visual Studio 2022 `devenv.exe` and `MSBuild.exe`
  under the RNW 0.83 required component set.
- PASS: app native scan found no app native Windows project.

## Decision

Decision accepted: W3A Windows toolchain preflight is complete. W3 native
generation and W4 build remain closed until the next gate records the exact
native-generation boundary and validation plan.
