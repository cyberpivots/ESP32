# Task Log 0020 - GitHub Pages Expert Panels

## Task

- ID: 0020-github-pages-expert-panels
- Owner role: Release, QA, Agent operations
- Status: complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Use the `$expert-agent-panels` workflow to improve the public GitHub Pages
artifact while preserving the curated allowlist model, source-backed safety
boundaries, and no-live-hardware claims.

## Scope

Included:

- Public-safe expert review panel section on the homepage.
- Quality-page panel method section.
- Safer wording for artifact checks, host software contract tests, and
  candidate GPIO labels.
- Workflow validation steps before Pages artifact upload.
- Scaffold and smoke markers for the new public sections.
- Local build and browser validation.

Excluded:

- Firmware, framework, relay/load wiring, live GPIO, XBee setting writes,
  MicroSD mount behavior, TFT wiring, deployment push, and live hardware
  validation.
- Publishing private `.agents/` records or screenshots into the public Pages
  artifact.

## Sources

- `SRC-LOCAL-GITHUB-PAGES-EXPERT-PANELS-2026-05-19`
- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`
- `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`
- `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`
- `SRC-OPENAI-REASONING`
- `SRC-CODEX-SUBAGENTS`

## Panel findings addressed

- Reworded homepage and quality-page status from broad "proof" language to
  artifact-check language.
- Reworded public relay labels from bare GPIO names to candidate GPIO labels.
- Reworded safe-core claims as host software contract tests, not electrical
  safety testing.
- Reworded the blueprint proof ladder as an evidence ladder.
- Removed generated root screenshot artifacts that violated the source-image
  gate.
- Added workflow checks for JSON/JS syntax, public manifest audit, smoke
  checks, scaffold verification, Python compilation, and host-side contract
  tests before artifact upload.

## Validation

- `python3 -m json.tool site/github-pages/site-data.json`
- `python3 -m json.tool docs/projects/four-relay-xbee-wifi/ui/manifest.json`
- `node --check site/github-pages/app.js`
- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js`
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py`
- `python3 tests/four_relay_safe_core/run_host_tests.py`
- `python3 scripts/build_github_pages.py`
- `python3 scripts/audit_public_manifest.py`
- `python3 scripts/smoke_github_pages.py`
- `python3 scripts/verify_scaffold.py`
- `git diff --check`
- Playwright browser checks against `http://127.0.0.1:8877/` at desktop,
  tablet, and mobile viewports for homepage, quality page, blueprints page,
  and admin HMI demo. Checked required expert-panel and safety markers,
  horizontal overflow, image loading, console warnings/errors, page errors, and
  failed requests.

## Handoff

No downstream role is blocked. A future QA task can turn the Playwright browser
checks into a checked-in script if CI browser coverage becomes required.
