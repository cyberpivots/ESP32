# Handoff 0121: CBBS RNW Split Runtime Proof And Agents To QA

From: RNW remediation coordinator

To: QA, RNW DevEx, RNW UI/layout, protocol/bridge, safety/security, KB records

Task:
[../TASK_LOG/0162-cbbs-rnw-split-runtime-proof-and-agents.md](../TASK_LOG/0162-cbbs-rnw-split-runtime-proof-and-agents.md)

## Summary

Task 0162 remediates the Tier 2 blockers found before any future split RNW
runtime proof. The expected result is stronger source/test/audit/profile
readiness, not native runtime acceptance.

## QA Focus

- Confirm RNW-specific read-only profiles are registered and audited.
- Confirm `@cbbs/product-ui` uses React Native peer dependencies and does not
  force Expo RN 0.85 into RNW 0.83 consumers.
- Confirm split Client, Sysop, and Hardware Tools source app packages declare
  the RNW 0.83 package lane and pass direct host-only tests.
- Confirm HostCommandBridge secret-like keys fail for string, number, boolean,
  object, array, and null values.
- Confirm unavailable bridge results have exact `boundsProof.actualBytes` and
  stale byte proofs fail.
- Confirm `apps/cbbs-windows` current docs default to Sysop and do not expose a
  runnable `react-native run-windows` command.
- Confirm host-only tests do not claim native runtime proof.

## Validation Evidence

- Review task 0162 for the full command list and outputs summary.
- Passed: RNW generator checks, RNW menu/parity unit tests, focused protocol
  Jest, focused product/product-ui/split-app host-only Jest, package
  typechecks, split app `test:windows`, root `pnpm typecheck`, `pnpm lint`,
  `timeout 180s pnpm test`, agent/skill/record/React Native scaffold audits,
  React Native audit unit tests, `scripts/verify_scaffold.py`, and
  `git diff --check`.
- `pnpm install --frozen-lockfile` passed; pnpm ignored build scripts for
  `msgpackr-extract` and `unrs-resolver`.
- No Tier 3 runtime proof was run. Native RNW launch, live bridge dispatch,
  serial/RF/XBee write, firmware flash/erase/monitor, signing, Store/App
  Installer release, commit, push, PR, deploy, and release stayed closed.

## Closed Surfaces

No RNW `run-windows`, native build/deploy/launch, Metro/process cleanup,
generated Debug/AppPackages cleanup, native bridge execution, shell execution,
serial/RF/XBee write, firmware flash, erase, monitor, relay/load/mains work,
wiring, signing, Store/App Installer release, commit, push, PR, deploy, or
release is authorized by this handoff.
