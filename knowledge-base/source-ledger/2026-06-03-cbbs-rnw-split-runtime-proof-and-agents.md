# CBBS RNW Split Runtime Proof And Agents Ledger

Date: 2026-06-03

Source ID:
`SRC-LOCAL-CBBS-RNW-SPLIT-RUNTIME-PROOF-AND-AGENTS-2026-06-03`

## Scope

Tier 2 remediation before any future split React Native Windows runtime proof.
This record covers RNW-specific read-only expert-agent profiles, protocol and
Product UI hardening, host-only split-app operation tests, audit/CI updates,
documentation corrections, and durable records.

This record does not run RNW native apps. The future split Client, Sysop, and
Hardware Tools runtime proof remains a separate Tier 3 gate.

## Verified Facts

- The current source default for `apps/cbbs-windows` compatibility is Sysop,
  not Hardware Tools.
- Historical `CbbsWindows` Hardware Tools screenshot evidence is a local
  compatibility-entry fact only; it is not current split-product native runtime
  proof.
- `@cbbs/product-ui` imports React Native primitives and is shared by RNW
  consumers, so its package boundary must not force Expo RN `0.85.x` into RNW
  `0.83.x` consumers.
- The HostCommandBridge contract is inert and unavailable by default; UI actions
  must not dispatch native bridge calls, shell commands, DOS-C `type` frames,
  serial/RF/XBee writes, flash/erase/monitor, or relay/load/mains actions.
- The parent coordinator spawned six read-only reviewers, captured outputs with
  `wait_agent`, and closed all six reviewer agents with `close_agent` before
  mutation acceptance.

## Assumptions

- The user plan authorizes Tier 2 source, tests, audits, docs, records, and
  read-only profile changes.
- Split app package-complete source and host-only operation tests are useful
  preparation for a later runtime gate but do not prove runtime behavior.
- Product UI peer dependencies are the least invasive way to support RNW 0.83
  and Expo/RN 0.85 consumers without duplicating the shell package.

## Unknowns

- Whether a future Tier 3 gate will authorize split RNW native build/deploy/run.
- Whether split product native project generation, package identity,
  capabilities, icons, signing, Store/App Installer packaging, or release will
  be accepted later.
- Whether any native HostCommandBridge implementation will ever be accepted.
- Whether the local DOS-C ahead commit referenced by earlier source/UI records
  has been published remains unverified here.

## Reviewer Quorum

- Coordinator, weight 5: selected Tier 2 remediation and kept Tier 3 runtime,
  live bridge, hardware, signing, publication, and release surfaces closed.
- RNW DevEx/CI reviewer, weight 3: blocked on Product UI React Native
  dependency leakage, split app package completeness, and active run command
  docs; approved bounded package/audit/docs/CI remediation.
- RNW UI/layout reviewer, weight 3: blocked on stale Hardware Tools default
  docs and missing deterministic layout/overflow assertions; approved bounded
  host-only UI/docs/test remediation.
- Protocol/bridge reviewer, weight 3: blocked on secret-like `params` keys for
  non-string values and non-exact `boundsProof.actualBytes`; approved focused
  protocol validator/test remediation.
- Safety/security reviewer, weight 3: blocked on active README command surface;
  confirmed no source-side bridge dispatch path or package signing/release
  artifact was accepted.
- QA reviewer, weight 3: blocked acceptance until protocol P1s, RNW profile
  audit coverage, dependency-boundary audit, and split app host-only operation
  proof are added.
- KB/prompt curator, weight 3: blocked on missing task 0162, handoff 0121,
  source ledger/index/docs links, prompt-registry row, and RNW-specific
  read-only profile coverage.

Weighted result: no-P1/P2 acceptance was not available for the original state.
The quorum approved only the bounded Tier 2 remediation boundary named in this
record.

## Authority Limits

This record does not authorize RNW `run-windows`, Visual Studio/MSBuild build,
deploy, launch, Metro/process cleanup, package output cleanup, package identity
acceptance, capability use, signing, Store/App Installer packaging, EAS,
App Center, simulator/device launch, live bridge execution, serial/RF/XBee
writes, firmware flash, erase, monitor, relay/load/mains work, wiring, commit,
push, PR, release, or deploy.

## Validation

- `pnpm install --frozen-lockfile` passed; pnpm ignored build scripts for
  `msgpackr-extract` and `unrs-resolver`.
- RNW generated-source checks passed:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_win31_parity.py --check`,
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`,
  and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.rnw_menu.test_rnw_menu tests.rnw_menu.test_win31_parity`
  (10 tests).
- Protocol/product host-only tests passed:
  `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts`
  (21 tests) and the focused product/product-ui/split-app host-only Jest run
  (6 suites, 28 tests).
- Package checks passed:
  `pnpm --filter @cbbs/product typecheck`,
  `pnpm --filter @cbbs/product-ui typecheck`,
  `pnpm --filter @cbbs/client-windows typecheck`,
  `pnpm --filter @cbbs/sysop-windows typecheck`,
  `pnpm --filter @cbbs/hardware-tools-windows typecheck`,
  `pnpm --filter @cbbs/windows-spike typecheck`, and each split app
  `test:windows` script.
- Scaffold and root validation passed:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`,
  `pnpm typecheck`, `pnpm lint`, `timeout 180s pnpm test`
  (10 suites, 59 tests), `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`,
  and `git diff --check`.

Final disposition: Tier 2 remediation accepted. Split RNW runtime proof remains
a separate closed Tier 3 gate and was not run in this task.
