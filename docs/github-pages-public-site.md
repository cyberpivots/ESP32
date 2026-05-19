# GitHub Pages Public Site

## Purpose

Publish a curated, public, static review site for the ESP32 DIY control
prototype materials without exposing private uploads, agent records, raw photo
archives, vendor PDFs, bulky binaries, or the working `docs/` tree as a direct
Pages source.

## Verified Facts

- GitHub Pages hosts static HTML, CSS, and JavaScript from a repository and can
  optionally run a build process before publishing. Source ID:
  `SRC-GITHUB-PAGES-WHAT-IS`.
- A repository can publish Pages from a branch source or from a custom GitHub
  Actions workflow. Source ID: `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`.
- GitHub's custom workflow documentation lists the Pages action flow using
  `actions/checkout@v6`, `actions/configure-pages@v5`,
  `actions/upload-pages-artifact@v4`, and `actions/deploy-pages@v4`, with
  `pages: write` and `id-token: write` permissions for deployment. Source ID:
  `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`.
- GitHub Pages sites are publicly available and are subject to size, bandwidth,
  build-time, and acceptable-use limits. Source IDs:
  `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`, `SRC-GITHUB-PAGES-LIMITS`.

## Assumptions

- The current public site is a project site under `cyberpivots/ESP32`; source
  links stay relative so forks, custom domains, and local previews can reuse the
  same generated artifact.
- The public audience needs a credibility-first entry point to the DIY concept
  package, not a hardware operation guide.
- Public review should start from a generated artifact so the repository root,
  `.agents/`, private uploads, raw photos, and unrelated docs are not exposed by
  default.

## Current Repository Status

Verified from the local shell on 2026-05-19:

- GitHub Pages API for `cyberpivots/ESP32` reports `build_type` as `workflow`,
  source branch `main`, and public URL `https://cyberpivots.github.io/ESP32/`.
- The latest checked `pages.yml` run completed successfully on `main`.
- `https://cyberpivots.github.io/ESP32/` returned HTTP 200.

Future repository, branch, workflow, or Pages setting changes must be
re-verified before claiming deployment success.

## Deployment Model

The source site lives under `site/github-pages/`.

The generated publish artifact is built with:

```bash
python3 scripts/build_github_pages.py --out build/github-pages
```

The build script copies:

- static site files from `site/github-pages/`, including the landing page,
  visual blueprint page, and quality evidence page;
- named generated public-safe backplates under
  `site/github-pages/assets/blueprints/` and
  `site/github-pages/assets/workbench/`;
- explicitly allowlisted Markdown files, including the XBee read-only bench
  proof, into `build/github-pages/bundle/`;
- the existing static admin HMI demo into
  `build/github-pages/demos/admin-hmi/`;
- a generated `public-file-manifest.json` with paths, byte counts, and hashes.

The landing page and the static admin HMI both use checked-in relay-channel
defaults. Browser-side label edits are stored only in local browser storage
under `esp32.relayLabels.v1` and do not become hardware facts.

GitHub Actions deploys only `build/github-pages` through
`.github/workflows/pages.yml`.

## Public Content Policy

Allowed public content:

- curated Markdown documentation that is already source-backed or clearly
  marked as an assumption or unresolved gap;
- static HTML, CSS, JavaScript, and JSON for the landing page and admin HMI
  demo;
- the named generated WebP backplates used by the public visual blueprint and
  workbench pages, with factual labels rendered in HTML instead of inside the
  image;
- generated manifest metadata for the allowlisted public files.
- a public-safe expert review panel section that describes workspace,
  source, risk, QA, and knowledge-record review lanes without publishing
  private `.agents/` records.

Excluded public content:

- `.agents/` records and internal handoffs;
- `user_uploads/` and raw photo archives;
- generated screenshots and bulky media except the two named blueprint
  backplates;
- copied vendor PDFs or source artifacts;
- private bench notes or files not listed in `scripts/build_github_pages.py`.

## Safety Boundary

The public site is DIY concept/prototype documentation only. It does not approve
mains wiring, relay load wiring, live firmware flashing, relay switching, XBee
setting writes, XBee API transmit frames, or ESP32 DIN/DOUT carrier wiring.

The visual blueprint page is a conceptual schematic, not a wiring diagram.
Relay/load wiring, mains wiring, TFT wiring, and expander-to-relay wiring remain
blocked until the documented gates close.

The public site must keep hardware blockers visible, including power-source
selection, voltage compatibility, boot-pin effects, relay trigger polarity,
relay input current, isolation behavior, XBee read/write readiness, enclosure
selection, overcurrent protection, grounding/bonding, GFCI/de-energization
process, strain relief, XBee read-only proof status, and qualified review.

## Deployment Re-Verification

The current repository is configured for GitHub Actions Pages deployment, but
that status is not a permanent assumption. Re-check the Pages API, latest
workflow result, and public URL after any remote, branch, workflow, permission,
or Pages setting change.

Known open deployment question:

- Whether future deployment protection rules will be added to the
  `github-pages` environment.

## Validation

Run these checks before handoff:

```bash
python3 scripts/build_github_pages.py
python3 scripts/audit_public_manifest.py
python3 scripts/smoke_github_pages.py
python3 scripts/verify_scaffold.py
python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py
git diff --check
```

The GitHub Actions Pages workflow runs the non-browser subset before uploading
the Pages artifact: JSON and JavaScript syntax checks, build, manifest audit,
smoke checks, scaffold verification, Python compilation, and host-side contract
tests.

Local browser verification should confirm that the landing page renders on
desktop and mobile, `blueprints.html`, `quality.html`, and
`demos/admin-hmi/index.html` render without horizontal overflow, public bundle
links resolve, safety disclaimers are visible, and no console errors are
emitted.
