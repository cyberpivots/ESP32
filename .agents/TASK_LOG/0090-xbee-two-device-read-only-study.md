# Task 0090 - XBee Two-Device Read-Only Study

## Triage

- Verified facts: The parent worktree was clean before this task; the existing
  XBee tooling supports no-serial `list`, no-serial `inventory`, offline
  `identity-delta`, locked `xctu-discovery-plan`, and gated fixed AT reads
  only through `readonly --confirm-sends-read-commands`.
- Verified facts: Fresh no-serial WSL and Windows inventories were captured in
  an ignored local packet. They show multiple CP210x-style Windows serial
  candidates and legacy WSL serial entries, but do not prove which two
  physical adapters are XBee adapters.
- Assumptions: The user authorizes host-only evidence records and planning for
  a read-only two-device XBee/XCTU study, but not serial opens, XCTU discovery,
  XBee setting writes, firmware tools, API transmit frames, ESP32 carrier
  wiring, relay/load/mains work, or public raw identifiers.
- Unknowns: The two exact XBee adapter ports, adapter markings, antenna state,
  physical isolation, voltage/header/carrier state, DIN/DOUT direction,
  reset/sleep/flow-control exposure, and current radio settings.
- Selected tier: Tier 3 read-only live-radio/XCTU study with Tier 2
  documentation and evidence-record mutation.
- Owner role: QA and Agent Operations, with Hardware, Communications,
  Evidence, and Live Bench review.
- Evidence need: Same-session no-serial inventories, local physical-fact
  placeholders, recovery/cleanup rules, weighted reviewer decision, public
  redacted source/status records, and a stop rule before serial/XCTU action.
- Mutation boundary: ignored
  `research/bench-records/xbee-readonly/local-20260529T063940Z/`, this task
  log, handoff 0079, source ledger/index rows, docs index, development status,
  known gaps, and XBee proof/study docs. No serial port open, no XCTU launch or
  discovery, no Tier B AT read, no write/apply/update/recovery/transmit, no
  ESP32 wiring, no relay/load/mains action, and no public raw identifiers.
- Validation plan: Required no-serial commands and focused tests before public
  edits; full scaffold audit suite, scaffold verification, docs audit, and
  diff checks after records are updated.

## Work Completed

- Captured fresh WSL no-serial `list` and `inventory` records under ignored
  local evidence.
- Captured fresh Windows no-serial `inventory` records under ignored local
  evidence.
- Added local physical-notes placeholders that keep physical facts unknown
  instead of inferring them from host inventory.
- Added local recovery and cleanup rules for wrong port, unstable serial,
  command-mode failure, XCTU update/firmware/recovery prompts, write/apply
  prompts, console transmit surfaces, and range/throughput surfaces.
- Added a local weighted reviewer decision packet and evaluated it with
  `scripts/agent_process_decision.py`.
- Recorded the local Stage A1 decision as `ask_user` because same-session
  physical evidence is missing.
- Added a local SHA-256 manifest for the ignored evidence packet.
- Updated public source/status/index and XBee proof/study docs with redacted
  summaries only.
- After the user reported disconnecting one XBee adapter, captured fresh
  no-serial WSL and Windows inventories and offline identity deltas.
- Recorded that one CP210x-style candidate was removed after the disconnect;
  the exact private host mapping remains in ignored local evidence only.
- Added a Stage A2 decision packet. It still evaluates to `ask_user` because
  the second adapter mapping plus adapter markings, antenna state, and
  isolation notes require physical action.

## Reviewer Quorum

- Coordinator: approved the no-serial evidence/status mutation with conditions
  that public records stay redacted and make no adapter-identity claim.
- Evidence: approved the record shape with conditions that local physical facts
  be explicit placeholders until user-observed evidence exists.
- Live Bench: approved no-serial Stage A1 only; Tier B and XCTU discovery remain
  blocked until exact ports, physical isolation, voltage/carrier, antenna,
  recovery, and cleanup evidence exist.
- QA: approved record/doc mutation only; required scaffold tests, docs audit,
  verification, and diff checks after edits.
- Communications: approved with the closed-surface condition that all-port
  discovery, broad scans, XCTU launch/discovery, writes, updates, transmit,
  wiring, relay/load/mains, and public raw identifiers stay closed.

Weighted local decision result: approval ratio `1.0`, approval weight `17/17`,
no P1/P2 blockers, missing Tier 3 prerequisite `same-session evidence`, and
decision `ask_user`.

## Live Gate Outcome

The study stopped after no-serial Stage A1 evidence. No exact XBee adapter
identity is accepted. No serial port was opened, XCTU was not launched, XCTU
discovery was not run, Tier B AT reads were not run, and no radio write,
firmware, recovery, API transmit, ESP32 carrier wiring, relay/load/mains, range
test, throughput test, or public raw identifier exposure occurred.

The next action is one irreducible physical step: disconnect exactly one XBee
USB adapter, leave the other adapter and all ESP32/relay/load/mains surfaces
untouched, and provide the disconnected adapter marking plus antenna and
isolation notes so the next inventory can produce a one-at-a-time identity
delta.

After the first physical disconnect, the local evidence packet now has one
candidate removal delta. The next action is to reconnect the first disconnected
XBee USB adapter, then disconnect exactly the other XBee USB adapter, leave all
ESP32/relay/load/mains surfaces untouched, and provide both adapters' markings
plus antenna and isolation notes. No Tier B reads or XCTU discovery are
accepted yet.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`:
  PASS, 21/21.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json`:
  PASS; no serial port was opened by the list command.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py inventory --json`:
  PASS; `serialOpenAttempted` was false.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_decision tests.scaffold_audits.test_xbee_radio_study`:
  PASS, 22 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`:
  PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`:
  PASS, 45 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`: PASS.
- `git diff --check`: PASS.
- `git -C submodules/hardware/rlxsc-xbee-pro-s3b diff --check`: PASS.
- Public-diff redaction scan for raw/private COM/PnP and sensitive XBee
  patterns: PASS, no matches.
