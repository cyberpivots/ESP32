# Task 0060: Remote LCD XBee Solar Client Private Submodules

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-26

## Goal

Create seven private `cyberpivots` GitHub repositories, seed each with a
docs-only initial commit, and add them as real Git submodules under
`submodules/hardware/`.

## Verified facts

- `gh auth status` was active as `cyberpivots` before repo creation.
- `origin` is `https://github.com/cyberpivots/ESP32.git`.
- No repo-local `.gitmodules` existed before this task.
- All seven target repos were absent before creation, then verified private on
  default branch `main`.
- `.gitmodules` now records seven HTTPS submodules under `submodules/hardware/`.
- Each submodule is docs-only and keeps firmware, framework, wiring, charging,
  radio-write, and live bench gates closed.

## Assumptions

- The existing `remote-lcd-xbee-solar-client` parent scaffold is baseline work.
- The parent ESP32 repo remains the coordination, source-index, and validation
  surface.

## Unknowns

- Exact hardware identity, power budget, pin map, firmware framework, XBee
  carrier, antenna, fuse/protection, enclosure, and live proof status remain
  unresolved.

## Implementation

- Created and seeded private repos:
  `rlxsc-esp32-client-node`, `rlxsc-xbee-pro-s3b`,
  `rlxsc-lcd-20x4-i2c`, `rlxsc-rotary-encoder`, `rlxsc-18650-cell`,
  `rlxsc-bms-protection`, and `rlxsc-solar-charger-power-path`.
- Added each repo as an HTTPS Git submodule under `submodules/hardware/`.
- Updated project docs, source index, source ledger, device matrix, known gaps,
  triage status, task log, and handoff records.

## Validation

- PASS: `git status --short --branch --untracked-files=all`
- PASS: `git submodule status --recursive`
- PASS: `git diff --check`
- PASS: `git diff --cached --check`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: Submodule static check confirmed clean worktrees, expected docs-only
  file sets, HTTPS remotes, and no framework/source/binary/PDF artifacts.

## Handoff

Continue with
[../handoffs/0049-remote-lcd-xbee-solar-client-private-submodules-to-hardware-qa.md](../handoffs/0049-remote-lcd-xbee-solar-client-private-submodules-to-hardware-qa.md).

## Stop gates

Do not start firmware implementation, framework selection, XBee writes, API
transmit frames, ESP32 DIN/DOUT wiring, battery charging, solar connection,
battery pack assembly, power-path wiring, or live bench action from this
submodule scaffold.
