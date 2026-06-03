# Task 0152: CBBS React Native W0-W2 Publication

Status: validated for publication; commit/push gate open only for current source tree

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

Source coverage: source-ledger records
`knowledge-base/source-ledger/2026-06-02-cbbs-react-native-client-platform.md`,
`knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w0-w1.md`,
and `knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w2.md`.

## Goal

Commit and push the current CBBS React Native W0-W2 scaffold and governance
records after the user explicitly requested `git commit + push all`.

## Routing Packet

- Verified facts: W0-W2 scaffold validation passed before publication; current
  branch is `main`; remote is `origin`
  `https://github.com/cyberpivots/ESP32.git`; `main` tracks `origin/main`;
  the requested publication boundary is one normal Git staging pass, one
  commit, and one push.
- Assumptions: "all" means all non-ignored tracked and untracked Git-visible
  changes in `/mnt/h/esp32`.
- Unknowns: remote authentication and final push result remain unknown until
  `git push` completes.
- Selected tier: Tier 3 because commit and push publish repository state.
- Owner role: Agent Operations and Architect with DevEx/CI, QA, and
  Security/Safety reviewers.
- Evidence need: reviewer quorum, dirty-tree review, publication hygiene,
  validation commands, normal staging proof, commit hash, and push result.
- Mutation boundary: Git index, one local commit, and push of current `main`
  to `origin/main`. No PR, release, tag, package publication, native Windows
  generation, native build/run, simulator/device launch, live network, serial,
  RF/XBee, flash, erase, monitor, relay, load, mains, EAS, App Center, or
  deployment.
- Validation plan: patch QA publication blocker, rerun React Native scaffold
  audit, audit unit tests, records audit, agent-process audit, full scaffold
  verify, publication hygiene, no-native-folder scan, `git diff --check`,
  stage with normal `git add -A`, review staged summary, commit, and push.
- Gate authority: explicit user authority for commit and push only.
- Trust boundary: publication records source and scaffold work only; it does
  not prove RNW native build/run, Windows runtime, live CBBS behavior, release
  readiness, or hardware behavior.

## Reviewer Quorum

- DevEx/CI/release reviewer, weight 3: approved normal staging, commit, and
  push with conditions: no forced ignored files, no release/native/live claims,
  and package-only commit wording.
- QA validation reviewer, weight 3: rejected publication until
  `apps/cbbs-windows/README.md` stopped claiming no RNW dependency was
  authorized and audit coverage covered that contradiction.
- Security/safety reviewer, weight 3: approved normal staging, commit, and
  push; no P1/P2 blockers, no credential values found, ignored generated files
  remain outside the publication candidate.

Weighted disposition before blocker fix: 6/9 approve with one QA P2 blocker.
Final disposition after the README/audit fix: 9/9 approve with no P1/P2
blockers. All reviewer outputs were captured and all visible agents were
closed before publication.

## Implementation Summary

- Fixed the QA publication blocker in `apps/cbbs-windows/README.md` by
  replacing stale W0/W1 wording with W2 package-only RNW dependency authority
  and preserving native/build/run/release closures.
- Added React Native scaffold audit coverage for the Windows README W2 markers
  and a regression check against the stale `No RNW dependency` claim.
- Added this publication record and linked it from `docs/index.md`.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
  (`5` tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `find apps packages -maxdepth 3 -type d \( -name android -o -name ios -o -name windows -o -name macos \) -print`
  returned no native app directories.
- PASS: `git diff --check`.
- PASS: QA re-check confirmed the stale Windows README claim is gone, the audit
  catches its reintroduction, and this task has durable-record markers.

Final `git commit` and `git push` results are reported in the assistant
close-out because this record is part of the commit being published.

## Authority Limits

This task authorizes only normal Git staging of non-ignored files, one commit,
and one push of current `main` to `origin/main`. No PR creation, release, tag,
package publication, native Windows generation, native build/run,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial write, RF/XBee action, firmware ABI
change, bridge ABI change, serial ABI change, Gate F service-code change,
flash, erase, monitor, relay, load, mains, EAS, App Center, store upload, or
deployment is authorized.

## Handoff

No handoff required.

## Decision Footer

Decision accepted: `cbbs_react_native_w0_w2_publication`.
Next gate: W3 native Windows project generation only after explicit authority
and same-session Windows toolchain proof. Owner: Agent Operations and
Architect with DevEx/CI, QA, and Security/Safety. Evidence: reviewer quorum,
publication hygiene, scaffold audits, staged diff summary, commit hash, and
push result.
