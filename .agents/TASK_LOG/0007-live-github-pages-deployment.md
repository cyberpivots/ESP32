# Task 0007 - Live GitHub Pages Deployment

## Task

- ID: 0007-live-github-pages-deployment
- Owner role: Release, QA
- Status: In Progress
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

## Assumptions

- Publishing the full non-ignored workspace is authorized by the user-provided
  deployment plan.
- The repository should be created as public under `cyberpivots/ESP32`.
- GitHub Pages should use GitHub Actions as the publishing source.

## Unknowns

- Final live Pages URL and deployment run ID are unknown until the first
  remote workflow completes.
- Browser smoke status for the live Pages URL is unknown until the site is
  published.

## Validation

- Local validation is complete and passing.
- Remote deployment validation is pending.

