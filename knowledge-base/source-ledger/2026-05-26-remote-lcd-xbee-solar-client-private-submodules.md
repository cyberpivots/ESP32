# Remote LCD XBee Solar Client Private Submodule Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`

## Sources used

- `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-DELIVERY`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-NXP-PCF8574-74A`
- `SRC-BOURNS-PEC11R`
- `SRC-TI-BQ25185`
- `SRC-TI-BQ2970`
- `SRC-TI-BQ27441-G1`
- `SRC-UL-LIION-SAFETY`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`

## Scope

Create seven private `cyberpivots` GitHub repositories, seed each with a
docs-only initial commit on `main`, and add them as HTTPS Git submodules under
`submodules/hardware/`.

No firmware source, framework files, XBee writes, API transmit frames, ESP32
DIN/DOUT wiring, battery charging, solar wiring, power-path wiring, live bench
action, vendor PDFs, binaries, secrets, or bulky artifacts are added by this
task.

## Verified facts

- [github-verified] `gh repo view` reports each target repo is private with
  default branch `main`.
- [repo-verified] `.gitmodules` contains seven HTTPS submodule URLs under
  `https://github.com/cyberpivots/`.
- [repo-verified] `git submodule status --recursive` pins:
  - `rlxsc-esp32-client-node`: `6b0d6018f17e0e31de9b61e23415d733eb7f5116`
  - `rlxsc-xbee-pro-s3b`: `a8b72244b098ca6bcec030d56a81309a97262605`
  - `rlxsc-lcd-20x4-i2c`: `8bc2c7fa9e9ee96fdd7f6b41155905da34f4d405`
  - `rlxsc-rotary-encoder`: `b9f66b6d576c2b2f87751b203c5283ded8cc4dcc`
  - `rlxsc-18650-cell`: `7eb9dede8c3df4d90b11e6dfb0111f0ad4c0eb42`
  - `rlxsc-bms-protection`: `b33fcdfd5bc57fc504e654a4580fda3eeddc386f`
  - `rlxsc-solar-charger-power-path`:
    `d56b53fd556592fa382b6c6d3f976068b14ef8ff`
- [repo-verified] Each submodule seed contains only `README.md`, `AGENTS.md`,
  `docs/index.md`, `docs/hardware-intake.md`,
  `docs/development-boundary.md`, `knowledge-base/source-index.md`,
  `research/known-gaps.md`, `.agents/TASK_LOG/0001-*-scaffold.md`, and
  `.agents/handoffs/0001-*-to-hardware-qa.md`.
- [repo-verified] Antenna review stays inside `rlxsc-xbee-pro-s3b`; fuse,
  protection, and enclosure review stay inside
  `rlxsc-solar-charger-power-path` until exact selected parts justify new
  repos.

## Assumptions

- [assumption] The seven private repos are evidence and ownership lanes, not
  implementation approvals.

## Unknowns

- [unknown] Exact ESP32 board, LCD/backpack, encoder, cell, BMS board, solar
  panel, charger/power path, XBee carrier, antenna, fuse/protection, and
  enclosure remain unresolved.
- [unknown] No power budget, pin map, firmware framework, XBee carrier proof,
  antenna proof, charger/power-path design, or live bench proof exists for this
  lane.

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

## Stop gates

Do not use these private submodules to authorize firmware implementation,
framework selection, XBee writes, API transmit frames, ESP32 DIN/DOUT wiring,
battery charging, solar connection, battery pack assembly, power-path wiring, or
live bench action.
