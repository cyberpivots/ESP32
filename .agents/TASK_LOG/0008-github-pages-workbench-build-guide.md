# Task 0008 - GitHub Pages Workbench Build Guide

## Task

- ID: 0008-github-pages-workbench-build-guide
- Owner role: Release, QA
- Status: In progress
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Improve the public GitHub Pages site into a workbench-style technical build
guide for the four-relay XBee Wi-Fi controller, with user-customizable relay
labels and a hard qualified-review gate for load or mains wiring.

## Scope

Included: landing-page redesign, `site-data.json` relay-channel defaults,
local browser relay-label editing, static admin HMI relay-label fallback,
source-backed public build guide, generated artifact allowlist update, docs
index/project README links, and validation/deployment evidence.

Excluded: firmware source, framework changes, hardware-profile factual changes,
relay wiring, relay load switching, XBee setting writes, raw media publishing,
vendor PDF publishing, and any mains wiring procedure.

## Sources

- `SRC-GITHUB-PAGES-WHAT-IS`
- `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`
- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`
- `SRC-GITHUB-PAGES-LIMITS`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`
- `SRC-SONGLE-SRD-05VDC-SL-C`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-NIOSH-ELECTRICAL-SAFETY`
- `SRC-OSHA-DEENERGIZED-WORK`
- `SRC-OSHA-GFCI`
- `SRC-OSHA-AEGCP`
- `SRC-OSHA-GROUNDING-OVERCURRENT`
- `SRC-NEMA-ENCLOSURES`

## Decisions

- Relay labels are UI aliases stored under localStorage key
  `esp32.relayLabels.v1`; they are not hardware facts.
- Public load and mains content remains a qualified-review checklist only, with
  no relay-contact wiring procedure.
- The generated Pages artifact remains allowlist-only.

## Validation

- `python3 -m json.tool site/github-pages/site-data.json`: PASS.
- `python3 scripts/build_github_pages.py --out build/github-pages`: PASS,
  generated 39 public files.
- `python3 -m py_compile scripts/build_github_pages.py scripts/verify_scaffold.py`:
  PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `git diff --check`: PASS.
- Local Playwright landing smoke: PASS on desktop and mobile, no horizontal
  overflow, build guide and admin HMI links return HTTP 200, manifest includes
  `bundle/docs/projects/four-relay-xbee-wifi/build-guide.md`, 39 public files,
  relay label edit persists across reload, and reset returns `Output A`.
- Local Playwright admin HMI smoke: PASS on desktop and mobile, four relay
  cards and four label inputs render, edited labels persist across reload,
  reset returns `Output A`, zero console errors, zero page errors, and zero
  `/api/` requests in static mode.
- GitHub Actions deployment and live Pages smoke checks are pending after the
  content commit is pushed.

## Handoff

No handoff is required if the local and live validation steps pass. Remaining
hardware unknowns stay with the hardware and QA owners through the existing
project gates.
