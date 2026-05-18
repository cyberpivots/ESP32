# Handoff 0006 - GitHub Pages Public DIY Site

## From

Release, QA

## To

Release, QA

## Summary

The workspace now has a generated GitHub Pages public-site lane:

- `site/github-pages/index.html`
- `site/github-pages/styles.css`
- `site/github-pages/app.js`
- `site/github-pages/site-data.json`
- `site/github-pages/404.html`
- `site/github-pages/.nojekyll`
- `scripts/build_github_pages.py`
- `.github/workflows/pages.yml`
- `docs/github-pages-public-site.md`

The build script publishes only explicitly allowlisted static site files,
curated Markdown docs under `bundle/`, the static admin HMI demo under
`demos/admin-hmi/`, and a generated `public-file-manifest.json`.

## Required next checks

- Repository admin or maintainer must set Pages source to `GitHub Actions`
  before live deployment.
- Release must confirm the eventual remote repository permits Pages deployment
  and uses the intended `main` branch.
- QA must review `scripts/build_github_pages.py` before any new public file is
  added to the allowlist.
- QA must keep the local no-framework-file and no-bulky-artifact scans in the
  release gate.

## Blockers

- Final owner/repository URL is unknown and intentionally not hard-coded.
- Live GitHub Pages deployment was not attempted in this implementation pass.
- The public site remains documentation-only and does not approve firmware
  flashing, relay switching, XBee writes, or mains/load wiring.

## Evidence

- GitHub Pages source IDs are recorded in `knowledge-base/source-index.md`.
- Deployment model and content policy are recorded in
  `docs/github-pages-public-site.md`.
- Validation results are recorded in
  `.agents/TASK_LOG/0006-github-pages-public-diy-site.md`.
