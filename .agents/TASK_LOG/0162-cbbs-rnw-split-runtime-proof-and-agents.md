# Task 0162: CBBS RNW Split Runtime Proof And Agents

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-LOCAL-CBBS-RNW-SPLIT-RUNTIME-PROOF-AND-AGENTS-2026-06-03`

## Routing

- Verified facts: the ESP32 checkout is `/mnt/h/esp32` with a pre-existing
  dirty RNW tree. Split source app packages exist for Client, Sysop, and
  Hardware Tools. `apps/cbbs-windows/src/index.tsx` currently defaults the
  compatibility shell to Sysop. Reviewer quorum found that the current state
  still had protocol, dependency, docs, profile-audit, and host-only proof
  blockers.
- Assumptions: the prior plan is the active user intent and authorizes Tier 2
  remediation only before any future runtime proof.
- Unknowns: split native RNW runtime behavior, accepted package identities,
  capability-use policy, signing, Store/App Installer path, live bridge
  execution, serial/RF/XBee behavior, firmware actions, and release path remain
  unresolved.
- Selected tier: Tier 2 source, tests, audits, docs, records, and read-only
  agent-profile work.
- Owner role: React Native Windows DevEx/Product UI/Protocol with Agent
  Operations, QA, Safety/Security, and KB curator lenses.
- Evidence need: reviewer quorum outputs, protocol negative tests, exact
  byte-boundary tests, package dependency-boundary audit, split app host-only
  operation tests, deterministic layout assertions, RNW profile audit, source
  ledger/index/docs links, and scaffold validation.
- Mutation boundary: `.codex/agents/rnw-*.toml`, `.codex/config.toml`,
  `scripts/scaffold_audit_agent_process.py`,
  `scripts/scaffold_audit_react_native.py`, React Native package metadata,
  `packages/cbbs-protocol`, `packages/cbbs-product-ui`, split app source/tests,
  `apps/cbbs-windows/README.md`, `docs/projects/cbbs-react-native/README.md`,
  `.github/workflows/scaffold-ci.yml`, prompt registry, source/task/handoff
  records, docs index, and lockfile reconciliation.
- Reviewer quorum: six project-local read-only reviewers were spawned, waited,
  captured, and closed. The initial state was blocked by P1/P2 findings; the
  quorum approved only the bounded Tier 2 remediation described here.
- Gate authority: user plan authorizes Tier 2 remediation. Tier 3 runtime
  proof remains closed.
- Validation plan: run focused protocol/product/product-ui/split-app tests,
  package typechecks, root typecheck/lint/test, RNW generators, React Native
  and agent-process scaffold audits, durable-record and skill audits,
  `verify_scaffold.py`, and `git diff --check`.
- Trust boundary: host-only tests, static audits, and records only. No native
  RNW launch, live bridge, hardware action, signing, release, or publication.

## Planned Changes

- Add RNW-specific read-only reviewer profiles for runtime operations,
  split-native DevEx, product UI/layout, protocol/bridge safety, and QA
  evidence review, then audit them for read-only sandboxing and contract
  inheritance.
- Reject secret-like HostCommandBridge `params` keys for every value type.
- Make unavailable HostCommandBridge result byte proof exact and reject stale
  `boundsProof.actualBytes` values.
- Move `@cbbs/product-ui` to a React Native peer dependency boundary and make
  split Windows app packages declare RNW 0.83 dependencies.
- Add dependency-leakage and current-doc command-surface audits.
- Correct stale Hardware Tools compatibility-default docs to Sysop and remove
  current `run-windows` command exposure.
- Add host-only split app operation tests and deterministic layout assertions.
- Add task, handoff, source ledger/index, docs-index, prompt-registry, and CI
  coverage for this remediation.

## Validation

- `pnpm install --frozen-lockfile` passed; pnpm ignored build scripts for
  `msgpackr-extract` and `unrs-resolver`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_win31_parity.py --check`
  passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`
  passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.rnw_menu.test_rnw_menu tests.rnw_menu.test_win31_parity`
  passed: 10 tests.
- `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts` passed:
  21 tests.
- `pnpm test -- packages/cbbs-product/__tests__ packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx apps/cbbs-windows/__tests__/windowsHostOnly.test.tsx apps/cbbs-client-windows/__tests__/app.test.tsx apps/cbbs-sysop-windows/__tests__/app.test.tsx apps/cbbs-hardware-tools-windows/__tests__/app.test.tsx`
  passed: 6 suites, 28 tests.
- Package validation passed:
  `pnpm --filter @cbbs/product typecheck`,
  `pnpm --filter @cbbs/product-ui typecheck`,
  `pnpm --filter @cbbs/client-windows typecheck`,
  `pnpm --filter @cbbs/sysop-windows typecheck`,
  `pnpm --filter @cbbs/hardware-tools-windows typecheck`,
  `pnpm --filter @cbbs/windows-spike typecheck`,
  `pnpm --filter @cbbs/client-windows test:windows`,
  `pnpm --filter @cbbs/sysop-windows test:windows`, and
  `pnpm --filter @cbbs/hardware-tools-windows test:windows`.
- Scaffold audits passed:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`,
  and `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`.
- Root validation passed:
  `pnpm typecheck`, `pnpm lint`, `timeout 180s pnpm test`
  (10 suites, 59 tests), `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`,
  and `git diff --check`.
- Tier 3 runtime proof was not run. No RNW native launch, live bridge,
  serial/RF/XBee, flash, signing, release, commit, push, PR, or deploy action
  was performed.

## Authority Limits

This task does not authorize RNW `run-windows`, native RNW build/deploy/launch,
Metro/process cleanup, generated Debug/AppPackages cleanup, native
HostCommandBridge implementation, shell execution, DOS-C live operation,
serial/RF/XBee writes, firmware flash, erase, monitor, relay/load/mains work,
wiring, package identity acceptance, signing, Store/App Installer release,
commit, push, PR, deploy, or release.

## Decision

Tier 2 remediation accepted for source, tests, audits, docs, read-only RNW
agent profiles, and durable records. Split RNW native runtime proof remains a
separate closed Tier 3 gate.

## Handoff

Handoff:
[../handoffs/0121-cbbs-rnw-split-runtime-proof-and-agents-to-qa.md](../handoffs/0121-cbbs-rnw-split-runtime-proof-and-agents-to-qa.md)
