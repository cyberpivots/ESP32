# Task 0001 - Workspace Scaffold

## Task

- ID: 0001-workspace-scaffold
- Owner role: Architect
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Create the initial framework-neutral ESP32 workspace scaffold with governance,
documentation, source-ledger, prompt/model routing, and verification gates.

## Scope

Included: repository initialization, directories, process docs, hardware seed
profiles, knowledge-base structure, and scaffold verification.

Excluded: firmware implementation, framework selection, live hardware flashing,
and physical bench validation.

## Sources

- SRC-OPENAI-LATEST-MODEL
- SRC-ESP-IDF-LATEST
- SRC-ESP32-DATASHEET
- SRC-DIGI-XBP9B-DPUT-001
- SRC-HELTEC-WIFI-LORA-32-V2

## Validation

Run `python3 scripts/verify_scaffold.py`.

## Handoff

Next work should close high-priority gaps in `research/known-gaps.md` before
selecting firmware framework or pin mappings.

