# Task 0061: Remote LCD XBee Solar Client Separate Hardware Stream

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-26

## Goal

Record `remote-lcd-xbee-solar-client` as a separate hardware-device development
stream that advances through private `rlxsc-*` evidence submodules without
changing ESP-NOW BBS, Win31/DOS-C, Gate F runtime, Gate G export, Gate H proof,
mesh, BLE, network, relay, TFT, MicroSD, load, or mains plans.

## Verified facts

- The parent scaffold and private submodules already exist and remain
  docs-only.
- The parent ESP32 repo remains the coordination, source-index, status, and
  validation surface.
- No submodule pointer, firmware source, framework file, XBee write, API
  transmit frame, wiring procedure, charging procedure, DOS-C file, or live
  bench record is changed by this task.

## Assumptions

- Hardware submodules are evidence and design ownership lanes, not runtime
  application repositories.
- Future integration with BBS/network or DOS-C work requires a new accepted ADR
  and source-backed interface boundary.

## Unknowns

- Exact hardware identity remains unresolved for the ESP32 board, LCD/backpack,
  encoder, 18650 cell, BMS/protection board, solar panel, charger/power path,
  XBee carrier, antenna, fuse/protection, and enclosure.
- No accepted power budget, pin map, framework ADR, read-only bench proof, or
  implementation gate exists for this lane.

## Implementation

- Added
  [development-stream.md](../../docs/projects/remote-lcd-xbee-solar-client/development-stream.md).
- Updated the project README, submodule map, docs index, source index,
  development status ledger, and triage status.
- Added a source ledger and Hardware QA handoff for this coordination pass.

## Validation

- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `python3 scripts/build_github_pages.py`
- PASS: `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`
- PASS: `python3 scripts/smoke_github_pages.py build/github-pages`
- PASS: `git submodule status --recursive`
- PASS: `git diff --check`
- PASS: Submodule clean status check confirmed all seven `rlxsc-*`
  submodules are on `main...origin/main` with no local changes.
- PASS: Submodule static checks found no unexpected docs-only file-set entries
  and no firmware/framework/source/binary/PDF artifacts.

## Handoff

Continue with
[../handoffs/0050-remote-lcd-xbee-solar-client-separate-hardware-stream-to-hardware-qa.md](../handoffs/0050-remote-lcd-xbee-solar-client-separate-hardware-stream-to-hardware-qa.md).

## Stop gates

Do not start firmware implementation, framework selection, XBee writes, API
transmit frames, ESP32 DIN/DOUT wiring, battery charging, solar connection,
battery pack assembly, power-path wiring, DOS-C changes, submodule runtime
code, or live bench action from this coordination record.
