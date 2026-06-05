# Workspace Review Follow-Up Hardening Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-WORKSPACE-REVIEW-FOLLOW-UP-HARDENING-2026-06-05`

## Scope

Tier 2 host-only workspace review follow-up for durable records, CI/test
coverage, protocol validators, Pages artifact handling, and local generated
evidence audits.

This source ledger does not authorize live bench, flashing, serial/RF/XBee
writes, native HostCommandBridge dispatch, relay/load/mains work, signing,
release, publication, commit, push, PR, deploy, `/etc/codex/requirements.toml`,
or `admin-strict` installation.

## Verified Facts

- Task 0169, Task 0170, and Task 0171 exist as durable task records.
- Task 0172 did not exist before this follow-up.
- Task 0171 closes the stale skill-inventory and RNW generated-output scaffold
  blockers recorded in Task 0170, and current scaffold audits pass. It does
  not close the entire Task 0170 backlog.
- `tests/live_bench` had two path-case expectation failures on this checkout:
  the code returned `H:\esp32\...` while the tests expected `H:\ESP32\...`.
- GitHub `actions/upload-pages-artifact` documents `include-hidden-files` with
  default `false`; `.git` and `.github` remain excluded even when hidden files
  are included. Source ID:
  `SRC-GITHUB-UPLOAD-PAGES-ARTIFACT-HIDDEN-FILES-2026-06-05`.
- `cbbs_host_command_bridge.v1` remains unavailable-only and non-dispatching.
- Host-only simulator bridge requests stay ASCII JSON, newline delimited, and
  bounded to 512 bytes before the newline.

## Reviewer Quorum

| Role | Weight | Vote | P1/P2 disposition |
| --- | ---: | --- | --- |
| Governance cartographer | 5 | approve with conditions | P2: create Task 0172; add discoverability for Tasks 0169-0171; record task-log/source-ledger boundary. |
| DevEx, CI, and release | 3 | approve with conditions | P2: add host-only suite coverage; preserve `.nojekyll` with `include-hidden-files`; fix live-bench path-case tests. |
| Protocol bridge ABI | 3 | approve with conditions | P2: reject HostCommandBridge secret-like neutral values; reject unknown simulator fields. |
| QA validation | 3 | approve | No P1/P2. P3: update `tests/README.md` with current host-only commands. |
| Evidence records | 3 | approve with conditions | P2: add Task 0172, source ledger, and docs/source discoverability without overstating Task 0170 closure. |
| Power, wiring, and isolation | 3 | approve host-only only | No P1/P2 inside host-only scope; all hardware/live gates remain blocked. |

Weighted disposition: 23/23 approved for this named host-only Tier 2 boundary.
Threshold: 70 percent. No P1/P2 blockers remain for the bounded mutation.

## Changes Recorded

- Added Task 0172 as the durable record for this follow-up.
- Added `research/2026-06-05-workspace-review-follow-up.md`.
- Added `research/workspace-review-command-matrix.md`.
- Added docs-index discoverability for Tasks 0169, 0170, 0171, and 0172.
- Added host-only Python suite coverage to scaffold and Pages workflows.
- Set `include-hidden-files: true` for the Pages artifact upload and audited
  `.nojekyll` as a required hidden public artifact.
- Made live-bench path expectations derive from the checkout path case.
- Hardened HostCommandBridge validation against secret-like values in neutral
  fields.
- Added simulator bridge per-type key allowlists and stable error reason
  `field_unknown`.
- Added RNW generated-evidence size, hash, source-record linkage, and
  classification checks.

## Tracked Generated Evidence

These files are tracked generated RNW evidence. They are local review evidence,
not a publication artifact, not release evidence, and not proof of final package
identity, signing, Store/App Installer distribution, live bridge dispatch, or
hardware action.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/bench-records/react-native-windows/cbbs-windows-index.bundle` | 5133785 | `07c301fedfa809e20f8b3b95a891f6090ea2a39d3be2389f18697e0001bbb9a0` |
| `research/bench-records/react-native-windows/cbbs-windows-index.map` | 10328346 | `f64c8a6f20763a6bcd55c7684f8600717fe7462e63b011b22401eaab999100bb` |
| `research/bench-records/react-native-windows/live-index.bundle` | 5133923 | `fdd80512d04989c0a8f83fc4bd16181a5bcae38acffe0da5d5a944eb72633bc9` |

## Assumptions

- Host-only validators and CI coverage can be strengthened without selecting a
  firmware framework or opening live device authority.
- Task 0169 remains a source/test/UI task-log record; Task 0170 remains a
  report-only backlog record; Task 0171 remains the specific scaffold recovery
  record for stale skill inventory and generated-output blockers.

## Unknowns

- Final native HostCommandBridge ABI, adapter allowlist, transcript schema, and
  recovery path remain unknown.
- Final Windows package identities, accepted capability use, signing,
  distribution, and release path remain unknown.
- Hardware power, voltage, boot-pin, isolation, relay/load/mains, battery/solar,
  and XBee carrier/write evidence remain unresolved.

## Validation

Validation is recorded in
`.agents/TASK_LOG/0172-workspace-review-follow-up-hardening.md`.
