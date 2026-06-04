# Task 0167: CBBS RNW Split Commit Push

Status: pre-push gate complete

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-04

Source IDs:
`SRC-LOCAL-CBBS-RNW-SPLIT-COMMIT-PUSH-2026-06-04`

## Routing

- Verified facts: the current branch is `main`, tracking `origin/main`, with no
  ahead/behind divergence before commit. The user explicitly requested
  `git commit + push`. The dirty tree contains the RNW split source/runtime
  records from Tasks 0163-0166 and generated split RNW native source trees.
- Assumptions: the requested push target is the current upstream,
  `origin/main`, and the commit scope is all non-ignored source/record changes
  from the completed RNW split work.
- Unknowns: remote branch protection and network push acceptance remain unknown
  until the push command runs.
- Selected tier: Tier 3 publication gate.
- Owner role: DevEx/release with QA/source-record, coordinator, and
  safety/protocol lenses.
- Evidence need: reviewer quorum outputs, staged manifest, high-risk staged
  artifact scan, publication hygiene output, whitespace check, relevant
  validation evidence, commit hash, and push result.
- Mutation boundary: git staging, one local commit, and push of the current
  branch to `origin/main`. No PR, tag, release, signing, Store/App Installer,
  package publication, live bridge, serial/RF/XBee, firmware, relay/load/mains,
  or hardware action is opened.
- Reviewer quorum: coordinator conditionally approved after publication hygiene;
  QA and DevEx blocked until staged manifest, publication hygiene, staged
  artifact scan, and explicit re-gating of retained runtime outputs. The parent
  captured and closed all reviewers, then resolved those conditions locally.
- Gate authority: user explicitly requested commit and push in this prompt.
- Validation plan: stage non-ignored files, inspect `git diff --cached
  --name-status`, scan staged names for package/signing/build/runtime artifacts,
  run `scripts/git_publication_hygiene.py check --json`, run
  `git diff --cached --check`, run durable-record audit, commit, and push.
- Trust boundary: publication of source and records only. Existing runtime proof
  does not accept release packages, package identities, signing, Store/App
  Installer distribution, live bridge dispatch, or hardware actions.

## Staged Scope

The staged scope is intended to include:

- RNW split native source project trees for Client, Sysop, and Hardware Tools.
- Split app package metadata, Metro resolver configs, Jest configs, and
  NuGet configs.
- ADR/docs/source-index/prompt-registry/known-gaps updates.
- Scaffold audit/test updates.
- Task logs, handoffs, and source ledgers for Tasks 0163-0166.
- This publication task record and source ledger.

The staged scope must exclude ignored runtime/build outputs and proof artifacts:
`node_modules/`, `AppPackages/`, `bin/`, `obj/`, `x64/`, `Generated Files/`,
`.msix`, `.appx`, `.pfx`, `.cer`, `.key`, `.pem`, `.binlog`, `.wrn`, `.log`,
and `Package.StoreAssociation.xml`.

## Authority Limits

This publication gate is limited to one local source/record commit and a push to
the current upstream branch. Closed surfaces remain closed: PR creation, tags,
release publication, Store/App Installer packaging, package signing, live bridge
dispatch, serial/RF/XBee writes or transmit, firmware flash/erase/monitor,
relay/load/mains work, and hardware bench actions.

## Handoff

No handoff is required for this publication-only task.

## Validation

- `git diff --cached --check` passed after correcting trailing whitespace in the
  generated RNW native module source files.
- Staged high-risk artifact scan returned no matches for build, package,
  signing, log, or runtime-proof outputs.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py
  check --json` passed with `ahead=0`, `behind=0`, no open PRs, no extra
  local/remote Codex branches, and upstream `origin/main`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py
  --min-task-id 163` passed.

## Decision

The source/record publication gate is accepted for commit and push. The final
commit hash and remote push result are command evidence outside this committed
record.
