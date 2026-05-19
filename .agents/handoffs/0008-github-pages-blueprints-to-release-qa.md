# Handoff 0008 - GitHub Pages Blueprints To Release QA

## From

Release, QA

## To

Release, QA

## Summary

The public Pages site now has a dedicated visual blueprint page and two
allowlisted generated WebP backplates:

- `site/github-pages/blueprints.html`
- `site/github-pages/assets/blueprints/system-overview.webp`
- `site/github-pages/assets/blueprints/safety-proof-ladder.webp`

The backplates are intentionally label-free. Factual labels, explanations, and
safety warnings are rendered as HTML/CSS so they can be reviewed and revised
without treating the image pixels as hardware evidence.

## Required next checks

- Release must confirm `scripts/build_github_pages.py` continues to publish
  only the named blueprint image assets.
- QA must verify the built `public-file-manifest.json` includes
  `blueprints.html`, `assets/blueprints/system-overview.webp`, and
  `assets/blueprints/safety-proof-ladder.webp`.
- QA must preview desktop and mobile pages and confirm no horizontal overflow,
  no missing images, readable labels, and resolving links to the blueprint,
  build guide, safety pages, bundle files, and admin HMI demo.

## Blockers

- Relay/load wiring remains blocked.
- Mains wiring remains blocked.
- TFT wiring remains blocked.
- Expander-to-relay wiring remains blocked.
- Exact bench wiring and firmware mutation remain outside this public Pages
  blueprint task.

## Evidence

- Source-backed text blueprint:
  `docs/projects/four-relay-xbee-wifi/prototype-blueprint.md`.
- Public-site policy:
  `docs/github-pages-public-site.md`.
- Task record:
  `.agents/TASK_LOG/0011-github-pages-blueprints-schematics.md`.
