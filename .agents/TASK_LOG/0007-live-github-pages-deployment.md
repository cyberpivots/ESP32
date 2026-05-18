# Task 0007 - Live GitHub Pages Deployment

## Task

- ID: 0007-live-github-pages-deployment
- Owner role: Release, QA
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Publish this ESP32 workspace as the public `cyberpivots/ESP32` GitHub
repository and deploy the curated generated GitHub Pages artifact.

## Scope

Included: local Pages build verification, scaffold gate verification, ignored
file verification, initial repository creation, push to `main`, GitHub Pages
workflow-source configuration, live Actions deployment, and browser smoke
verification of the published site.

Excluded: firmware implementation, framework changes, hardware-profile factual
changes, protocol changes, raw upload publishing, generated build artifact
tracking, and any bench or electrical action.

## Verified Facts

- Local branch before deployment: `main`.
- Existing local remote before deployment: none configured.
- `gh` is installed: version 2.89.0.
- `gh auth status` reports the active account as `cyberpivots`.
- `gh repo view cyberpivots/ESP32` did not resolve an existing repository
  before creation.
- `python3 scripts/build_github_pages.py --out build/github-pages`: PASS,
  generated 38 public files.
- `python3 -m py_compile scripts/build_github_pages.py scripts/verify_scaffold.py`:
  PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `git status --ignored --short` reports `build/`, `scripts/__pycache__/`,
  and `user_uploads/` as ignored.
- Public repository created: `https://github.com/cyberpivots/ESP32`.
- Pages API reports `build_type` as `workflow` and `html_url` as
  `https://cyberpivots.github.io/ESP32/`.
- Initial deployment run `26058438714`: PASS.
- Admin HMI static-demo path fix committed as `4f11d3e`.
- Post-fix deployment run `26058571425`: PASS.

## Assumptions

- Publishing the full non-ignored workspace is authorized by the user-provided
  deployment plan.
- The repository should be created as public under `cyberpivots/ESP32`.
- GitHub Pages should use GitHub Actions as the publishing source.

## Unknowns

- GitHub Actions reports a Node.js 20 deprecation warning for current Pages
  actions. The workflow passed, but the warning should be reviewed before
  GitHub's 2026 runner cutoff dates.

## Validation

- Local validation is complete and passing.
- `gh run watch --repo cyberpivots/ESP32 26058438714 --exit-status`: PASS.
- `gh run watch --repo cyberpivots/ESP32 26058571425 --exit-status`: PASS.
- `curl -fsSIL https://cyberpivots.github.io/ESP32/`: PASS, HTTP 200.
- `curl -fsSI https://cyberpivots.github.io/ESP32/public-file-manifest.json`:
  PASS, HTTP 200.
- `curl -fsSI https://cyberpivots.github.io/ESP32/demos/admin-hmi/`: PASS,
  HTTP 200.
- `curl -fsSI https://cyberpivots.github.io/ESP32/user_uploads/`: PASS, HTTP
  404 expected.
- `curl -fsSI https://cyberpivots.github.io/ESP32/build/github-pages/`: PASS,
  HTTP 404 expected.
- Playwright live landing smoke with cache disabled: PASS, title and H1 loaded,
  safety text present, manifest count 38, and 17 same-site public links checked
  with no failures.
- Playwright live admin HMI smoke with cache disabled: PASS, title and H1
  loaded, prototype-mode message present, four relay records loaded, scenario
  control visible, zero console errors, zero page errors, and zero `/api/`
  requests.
