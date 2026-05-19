# Task 0018 - Public Quality Evidence Page

## Task

- ID: 0018-public-quality-evidence-page
- Owner role: Release, QA
- Status: complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Refresh the public GitHub Pages artifact so it reflects the live workflow
deployment and recent scaffold/QA hardening work while preserving the
allowlisted static-artifact model and public hardware safety boundaries.

## Verified Facts

- GitHub Pages API for `cyberpivots/ESP32` reports `build_type` as `workflow`
  and public URL `https://cyberpivots.github.io/ESP32/`.
- Latest checked `pages.yml` workflow run on 2026-05-19 completed
  successfully on `main`.
- The public root URL returned HTTP 200 on 2026-05-19.
- Before this task, the generated artifact reported 56 public files.

## Assumptions

- This task updates source files and local generated output only; commit and
  push remain separate unless explicitly requested.
- The public site remains static HTML, CSS, JavaScript, and JSON with no
  framework, CDN, or external runtime dependency.

## Unknowns

- Whether future repository settings, branch protection, or deployment
  protection rules will change after this local update.

## Scope

Included:

- `quality.html` public-safe quality/evidence surface.
- Homepage current-status and quality-gate sections.
- Site data for deployment status and quality gates.
- Build allowlist, smoke checks, scaffold audit markers, workflow copy, and
  public-site documentation updates.
- Local rebuild and validation.

Excluded:

- Live hardware validation, ESP32 flashing, relay switching, relay/load wiring,
  mains wiring, XBee setting writes, raw bench evidence, private uploads,
  copied vendor PDFs, screenshots, and deployment push.

## Sources

- `SRC-GITHUB-PAGES-WHAT-IS`
- `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`
- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`
- `SRC-GITHUB-PAGES-LIMITS`
- `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`

## Validation

- `python3 -m json.tool site/github-pages/site-data.json` - pass.
- `node --check site/github-pages/app.js` - pass.
- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js` - pass.
- `python3 scripts/build_github_pages.py` - pass, generated 57 public files.
- `python3 scripts/audit_public_manifest.py` - pass.
- `python3 scripts/smoke_github_pages.py` - pass.
- `python3 scripts/verify_scaffold.py` - pass.
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py` - pass.
- `python3 tests/four_relay_safe_core/run_host_tests.py` - pass.
- `git diff --check` - pass.
- Playwright browser QA from `http://127.0.0.1:8876/` - pass for
  `index.html`, `blueprints.html`, `quality.html`, and
  `demos/admin-hmi/index.html` at `1440x1000` and `390x844`; no horizontal
  overflow, missing images, broken same-origin links, or console warnings/errors
  were found.

## Handoff

No downstream role is blocked by this public-site refresh. Release should
re-run the Pages API and latest workflow checks after any commit/push or Pages
setting change before claiming the live deployment includes this update.
