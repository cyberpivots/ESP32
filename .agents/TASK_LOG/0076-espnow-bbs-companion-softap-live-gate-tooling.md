# Task 0076: ESP-NOW BBS Companion SoftAP Live-Gate Tooling

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-27

## Goal

Implement the tooling-only portion of the ESP32 BBS companion SoftAP Gate 1
plan: prepare-time companion HTTP config, redacted manifest metadata, Windows
proof collection script, and completion-audit enforcement.

This task does not run `prepare`, `flash`, live SoftAP proof, Windows Wi-Fi
mutation, radio proof, serial writes, DOSBox-X, dummy GPIO/output, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, release gates, or cleanup claims.

## Verified Facts

- The paired DOS-C companion firmware source already has a disabled-by-default
  SoftAP HTTP API and volatile dummy-output-disabled state model.
- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- The ESP32 worktree had unrelated full-service mesh changes before this task;
  those files are outside this mutation boundary.
- Current live bench identity and Windows Wi-Fi state were not re-proved in
  this Tier 2 task.

## Assumptions

- Companion HTTP Gate 1 uses a generated SSID/passphrase under the ignored DOS-C
  live directory.
- Completion should require a companion proof JSON only when the prepare
  manifest records companion HTTP as enabled.
- Gate 1 must keep physical dummy output disabled.

## Unknowns

- No current live preflight, backup, flash, SoftAP gateway, Windows Wi-Fi,
  bridge transcript, vision gate, companion proof, or cleanup proof exists in
  this session.
- No exact GPIO, no-load fixture, observation method, or recovery evidence
  exists for Gate 2.

## Reviewer Quorum

Read-only local reviewer lenses used before mutation; no subagents were spawned
because this session did not include explicit subagent authority.

- Coordinator/governance reviewer: Tier 2 tooling only; Tier 3 live gates stay
  closed.
- Firmware/communications reviewer: preserve serial-nullmodem and ESP-NOW peer
  continuity; no firmware runtime behavior change in ESP32 repo.
- Evidence auditor: manifests must redact passphrases and completion must fail
  closed without required companion proof.
- UI/protocol analyst: companion proof validates JSON API semantics, not
  physical output.
- QA reviewer: add focused unit/source tests for new flags, redaction, proof
  auditing, and script cleanup intent.
- Live bench gate reviewer: no live mutation without same-session authority and
  fresh identity/recovery evidence.

## Mutation Boundary

- `scripts/espnow_bbs_live_gate.py`
- `scripts/companion_softap_windows_proof.ps1`
- `tests/live_bench/test_espnow_bbs_live_gate.py`
- this task record and paired handoff

## Validation Plan

- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 scripts/verify_scaffold.py` where practical
- `python3 scripts/scaffold_audit_agent_process.py` where practical
- `git diff --check`
- ESP-IDF readiness probe from DOS-C before any later live `prepare`

## Validation

- PASS: `python3 tests/live_bench/test_espnow_bbs_live_gate.py` (15 tests)
- PASS: `python3 -m py_compile scripts/espnow_bbs_live_gate.py`
- PASS: `python3 scripts/scaffold_audit_agent_process.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `git diff --check`
- PASS: paired DOS-C generator test and companion bridge suite
- PASS: paired DOS-C no-flash temporary ESP-IDF build of companion-enabled
  coordinator and peer01 using generated ignored live config
- SKIPPED: PowerShell parse because `pwsh` is not installed in this environment.
- Not run: live `prepare`, `flash`, Windows Wi-Fi proof, bridge proof,
  vision gate, completion gate, or cleanup proof.

## Handoff

Continue with
[../handoffs/0065-espnow-bbs-companion-softap-live-gate-tooling-to-qa.md](../handoffs/0065-espnow-bbs-companion-softap-live-gate-tooling-to-qa.md).

## Stop Gates

Do not use this tooling task to authorize flash, erase, monitor, physical serial
writes, live SoftAP/API proof, Windows Wi-Fi mutation, dummy GPIO/output proof,
relay, XBee, TFT, MicroSD, load, mains, PCAP, router-admin, release gating, or
cleanup acceptance.
