# Task 0015 - Public Wow Factor Workbench

## Task

- ID: 0015-public-wow-factor-workbench
- Owner role: Release, QA
- Status: Complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Upgrade the public GitHub Pages artifact and bundled admin HMI demo into a
premium technical workbench presentation while preserving the allowlisted static
artifact model and hard public safety gates.

## Scope

Included: generated public-safe WebP backplates, richer Pages home and blueprint
surfaces, expanded R&D loop and hardware-research links, polished static admin
HMI styling, disabled default command controls, build allowlist updates,
manifest-missing fallback behavior, scaffold verification markers, local build,
and browser QA.

Excluded: relay/load wiring, mains wiring, exact pinout or terminal diagrams,
raw user-upload photos, vendor PDFs, private bench notes, radio ID publication,
XBee setting writes, ESP32 flashing/monitoring, live hardware control, firmware
behavior changes, and publishing to GitHub Pages.

## Sources

- `SRC-GITHUB-PAGES-WHAT-IS`
- `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`
- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`
- `SRC-GITHUB-PAGES-LIMITS`
- `SRC-ESP-IDF-STABLE-ESP32`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-NIOSH-ELECTRICAL-SAFETY`
- `SRC-OSHA-DEENERGIZED-WORK`
- `SRC-OSHA-GFCI`
- `SRC-OSHA-AEGCP`
- `SRC-OSHA-GROUNDING-OVERCURRENT`
- `SRC-OSHA-1910-305`

## Decisions

- New artwork is deterministic, label-free, non-photoreal WebP backplate art
  under `site/github-pages/assets/workbench/`.
- Factual labels remain HTML text so reviewers can audit copy without relying
  on pixels.
- The public build allowlist remains explicit; adding a new image requires both
  `scripts/build_github_pages.py` and `scripts/verify_scaffold.py` coverage.
- The admin HMI demo keeps relay commands disabled by default and keeps mock
  state behavior visible as static demo mode.

## Validation

- `python3 -m py_compile scripts/verify_scaffold.py scripts/build_github_pages.py scripts/xbee_read_only_probe.py tests/four_relay_safe_core/run_host_tests.py`:
  PASS.
- `python3 -m json.tool site/github-pages/site-data.json`: PASS.
- `node --check site/github-pages/app.js`: PASS.
- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js`: PASS.
- `python3 tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 scripts/build_github_pages.py`: PASS, generated 56 public files.
- `python3 scripts/verify_scaffold.py`: PASS after QA screenshots were moved
  under ignored `build/qa-screenshots/`.
- `git diff --check`: PASS.
- Public manifest allowlist audit: PASS, all three workbench WebP backplates
  are present; no `.agents/`, `user_uploads/`, or
  `research/bench-records/` source path is present.
- Playwright QA from `http://127.0.0.1:8876/`: PASS for desktop and mobile
  screenshots of `index.html`, `blueprints.html`, and
  `demos/admin-hmi/index.html`; same-origin links returned non-error
  responses; images loaded; no horizontal overflow was detected; no console
  warnings or errors were reported.

## Handoff

No downstream role is blocked by this presentation pass. Continue with Release
or QA review before any live public deployment setting changes.
