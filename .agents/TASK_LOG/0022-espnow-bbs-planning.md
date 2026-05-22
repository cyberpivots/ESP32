# Task 0022: ESP-NOW BBS Planning Artifacts

Status: docs and ADR added; firmware and hardware gates remain closed

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Record the ESP32-side project boundary for the DOS-C ESP-NOW BBS integration:
coordinator/client firmware planning, source-backed ESP-NOW constraints, and
safe split between Windows 3.1, Raspberry Pi bridge services, Windows 11
tooling, and future ESP32 firmware.

## Scope Completed

- Project-local framework ADR for `espnow-bbs`.
- Source ledger for ESP-NOW BBS architecture and safety gates.
- Project README and protocol plan under `docs/projects/espnow-bbs/`.
- Documentation index/source-index/known-gap updates.

## Not Performed

- No ESP32 flashing, erasing, monitor attachment, serial writes, relay actions,
  XBee writes, SD imaging, mains/load work, or firmware source implementation.

## Validation

Expected validation:

- `python3 scripts/verify_scaffold.py`
- `git diff --check`
