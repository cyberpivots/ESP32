# Remote LCD XBee Solar Client Separate Hardware Stream Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26`

## Sources used

- `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`
- `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`
- `SRC-LOCAL-ESPNOW-DEVELOPMENT-STATUS-REVIEW-2026-05-26`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-DIGI-XBP9B-DPUT-001`

## Scope

Record `remote-lcd-xbee-solar-client` as its own hardware-device development
stream, separate from ESP-NOW BBS, Win31/DOS-C, Gate F runtime, Gate G export,
Gate H proof, mesh, BLE, network, relay, TFT, MicroSD, load, and mains work.

No firmware source, framework files, XBee writes, API transmit frames, ESP32
DIN/DOUT wiring, battery charging, solar wiring, power-path wiring, live bench
action, vendor PDFs, binaries, secrets, bulky artifacts, or DOS-C changes are
added by this task.

## Verified facts

- [repo-verified] Added
  `docs/projects/remote-lcd-xbee-solar-client/development-stream.md`.
- [repo-verified] Linked the separate hardware stream from the project README
  and the main docs index.
- [repo-verified] Added this source ledger, source-index entry, task record,
  and Hardware QA handoff.
- [repo-verified] Updated the development status and triage records to keep
  this lane separate from ESP-NOW BBS, Win31/DOS-C, Gate F/G/H, mesh, BLE,
  network, relay, TFT, MicroSD, load, and mains work.
- [repo-verified] No submodule pointers were changed by this task.

## Assumptions

- [assumption] Hardware submodules are evidence and design ownership lanes, not
  application runtime repositories.
- [assumption] Future integration with BBS/network or DOS-C work requires a new
  accepted ADR and source-backed interface boundary.

## Unknowns

- [unknown] Exact ESP32 board, LCD/backpack, encoder, 18650 cell,
  BMS/protection board, solar panel, charger/power path, XBee carrier,
  antenna, fuse/protection, and enclosure remain unresolved.
- [unknown] No accepted power budget, pin map, framework ADR, XBee carrier
  proof, antenna proof, charger/power-path design, read-only bench proof, or
  live implementation gate exists for this lane.

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

## Stop gates

Do not use this coordination record to authorize firmware implementation,
framework selection, XBee writes, API transmit frames, ESP32 DIN/DOUT wiring,
battery charging, solar connection, battery pack assembly, power-path wiring,
submodule runtime code, DOS-C changes, or live bench action.
