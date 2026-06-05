# Task 0171: Scaffold Recovery And Tooling Hardening

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-05`,
`SRC-LOCAL-CBBS-RNW-SPLIT-BUILD-INSTALL-LAUNCH-2026-06-04`,
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-METRO-INCIDENT-2026-06-04`,
`SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`,
`SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`

## Routing

- Verified facts: Task 0170 identified two P0 scaffold blockers:
  stale GitHub/Canva plugin skill paths under cache hash `2b564709`, and
  retained RNW generated output under the split Windows app native trees.
  Same-session inventory found current plugin skill paths under cache hash
  `9c1190e4`. Pre-clean `scripts/scaffold_audit_react_native.py` reproduced
  a 6030-line generated-output failure stream. The selected RNW cleanup roots
  were ignored by app-local `windows/.gitignore` rules and had zero tracked
  files by `git ls-files -- <dir>`.
- Assumptions: removing ignored generated output is sufficient to restore RNW
  scaffold cleanliness without deleting generated native source, manifests,
  solution/project files, installed debug packages, app registrations, or Metro
  configs.
- Unknowns: future plugin cache hashes, future RNW generated output after any
  later build/run, final package identities, signing/release path, live bridge
  adapter behavior, XBee write gate evidence, and hardware power/isolation
  facts remain unresolved.
- Selected tier: Tier 2 host-only tooling, records, scaffold audit, and
  generated-output cleanup.
- Owner role: Tooling and QA with RNW DevEx, Evidence Records, Coordinator, and
  Security/Safety review lenses.
- Evidence need: current dirty-tree boundary, same-session skill inventory,
  read-only reviewer quorum, tracked-file and ignore checks for cleanup
  targets, focused audit-reporting and durable-record tests, scaffold audits,
  full scaffold verification, and this task record.
- Mutation boundary: `research/skills/available-skills.md`,
  `knowledge-base/source-index.md`,
  `knowledge-base/source-ledger/2026-06-05-codex-skill-inventory.md`,
  `scripts/scaffold_audit_skills.py`,
  `scripts/scaffold_audit_react_native.py`,
  `scripts/scaffold_audit_records.py`,
  `scripts/verify_scaffold.py`,
  `tests/scaffold_audits/test_scaffold_audit_reporting.py`,
  `tests/scaffold_audits/test_scaffold_audit_records.py`, this task record,
  and ignored generated RNW output directories matching only
  `*.Package/AppPackages`, `*.Package/bin`, `*.Package/obj`, `<App>/obj`,
  `<App>/x64`, and top-level `windows/x64` under the split app Windows trees.
- Reviewer quorum: project-local read-only subagents were spawned, waited,
  their outputs were captured, and all reviewers were closed. The coordinator
  recorded a weighted pass of `17/17`, approval ratio `1.0`, threshold `0.7`,
  and no P1/P2 blockers for this named Tier 2 boundary. Reviewer conditions
  were to refresh the skill source ID and inventory, delete only tracked-zero
  ignored generated-output roots, add focused tests, preserve dirty-tree
  boundaries, and keep live, release, publication, and system-policy surfaces
  closed.
- Gate authority: Tier 2 host-only recovery and tooling hardening only.
  Stopping the retained local `CbbsHardwareToolsWindows` Debug process was
  limited to releasing file locks on the ignored generated-output layout; no
  uninstall, app registration change, build, launch, runtime proof, or package
  identity acceptance was performed.
- Trust boundary: repo-local source, audit, and filesystem cleanup evidence
  only. Hooks are advisory under bypassPermissions.

## Changes

- Refreshed `research/skills/available-skills.md` to current GitHub/Canva
  plugin cache hash `9c1190e4`.
- Added source index and source ledger coverage for
  `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-05`.
- Tightened the skill audit to require the same-session 2026-06-05 skill
  inventory source ID.
- Removed only the pre-checked ignored generated output directories under
  `apps/cbbs-client-windows/windows/`,
  `apps/cbbs-sysop-windows/windows/`, and
  `apps/cbbs-hardware-tools-windows/windows/`.
- Grouped RNW generated-output audit failures by generated-output root instead
  of emitting one line per file.
- Updated `verify_scaffold.py` so failing audit groups are named before detailed
  failure output.
- Added durable-record audit checks for duplicate numeric task IDs and unsafe
  report-only records.
- Added focused unit tests for audit grouping, scaffold failure grouping,
  task-ID collision detection, and report-only durable-record behavior.

## Cleanup Evidence

- Pre-delete candidate checks found 18 top-level cleanup roots across the three
  split app Windows trees. Each candidate had `tracked=0` from
  `git ls-files -- <candidate>` and matched app-local `windows/.gitignore`
  rules with `git check-ignore -v <candidate>/`.
- The first deletion pass removed all selected output roots except locked files
  under `apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows.Package/bin`.
- Process inventory showed only `CbbsHardwareToolsWindows` still running.
  That local Debug process was stopped to release file locks. No package
  uninstall, app registration mutation, build, launch, or runtime proof command
  was run.
- A follow-up candidate scan returned no remaining generated-output directories
  matching the approved cleanup patterns.

## Authority Limits

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee/radio writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, runtime proof, commit, push, PR, deploy,
release, `/etc/codex/requirements.toml`, and `admin-strict` installation.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_scaffold_audit_reporting tests.scaffold_audits.test_scaffold_audit_records`
  (5 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 171`
  after this task record was added.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
  after this task record was added.
- PASS: `git diff --check`.

## Handoff

No handoff is required. Future RNW build/run, HostCommandBridge live dispatch,
XBee writes, hardware power/relay evidence, signing, release, commit, push, and
PR work require separate gates.

## Decision

Decision: accept the Task 0171 Tier 2 scaffold recovery and tooling-hardening
slice. The skill and RNW scaffold blockers from Task 0170 are closed in this
workspace state, audit reporting is hardened, durable-record checks are
broadened, and Tier 3/live/release/publication/system-policy surfaces remain
closed.
