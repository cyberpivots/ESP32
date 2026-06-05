# 2026-06-05 Workspace Review Follow-Up

## Verified Facts

- Task 0169, Task 0170, and Task 0171 existed before this follow-up.
- Task 0172 was created by this follow-up.
- Task 0171 closes the stale skill-inventory and RNW generated-output scaffold
  blockers recorded in Task 0170; it does not close the whole Task 0170
  backlog.
- Current work is host-only. No live bench, flash, serial/RF/XBee write,
  HostCommandBridge dispatch, relay/load/mains, signing, release, publication,
  commit, push, PR, or deploy authority is present.

## Assumptions

- The implementation slice is records, review tooling, host-only CI/test
  hardening, and protocol safety tests only.
- External source research is limited to primary source facts needed for the
  GitHub Pages hidden-file workflow behavior.

## Unknowns

- Final HostCommandBridge native ABI, implementation language, allowlist,
  transcript schema, and recovery path remain unresolved.
- RNW package identity, capability acceptance, signing, distribution, and
  release path remain unresolved.
- Hardware power, voltage, boot-pin, isolation, relay/load/mains, battery/solar,
  carrier, and XBee write evidence remain unresolved.

## Findings By Lane

Governance and records:
Tasks 0169-0171 lacked docs-index discoverability. This follow-up adds index
coverage and records the boundary: Task 0169 is source/test/UI evidence, Task
0170 is report-only backlog analysis, and Task 0171 is the scaffold recovery
for the two stale Task 0170 scaffold blockers.

Tooling and CI:
CI did not run the standalone host-only Python suites for custom wireless
protocol, LCD BBS menu, RNW menu, ESP32 gateway TCP, or live-bench tests. This
follow-up adds those suites to scaffold and Pages workflows.

Pages artifact:
The generated site includes `.nojekyll`. GitHub `actions/upload-pages-artifact`
defaults hidden-file inclusion to false, so this follow-up sets
`include-hidden-files: true` and audits `.nojekyll` as a required artifact.

Protocol and bridge:
HostCommandBridge remains unavailable-only. This follow-up rejects secret-like
values in neutral bridge fields and makes versioned simulator bridge request
types reject unknown fields with `field_unknown`.

RNW and release:
Tracked generated RNW evidence is now pinned by size and SHA-256 and classified
as local review evidence, not a publication artifact. Final package identity,
capability acceptance, signing, Store/App Installer distribution, and release
remain closed.

Hardware and power:
No hardware facts changed. Power, voltage, boot-pin, isolation, relay, load,
mains, battery/solar, XBee carrier/profile-write, flash, monitor, and serial/RF
write gates remain closed.

Dependency research:
Package manifests still contain loose or wildcard-style ranges in some lanes.
This follow-up preserves the existing dependency graph and records that any
dependency update or pinning pass needs a separate source-backed frozen-lockfile
lane.

## Decision

Proceed only with the bounded Tier 2 host-only hardening slice. Defer live
hardware, RNW runtime/release, HostCommandBridge live dispatch, XBee writes,
dependency updates, and publication to separate gated tasks.
