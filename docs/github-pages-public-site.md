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

- The public site is a project site and must use relative links because this
  repository does not hard-code an owner, repository name, custom domain, or
  final deployed URL.
- The public audience needs a credibility-first entry point to the DIY concept
  package, not a hardware operation guide.
- Public review should start from a generated artifact so the repository root,
  `.agents/`, private uploads, raw photos, and unrelated docs are not exposed by
  default.

## Deployment Model

The source site lives under `site/github-pages/`.

The generated publish artifact is built with:

```bash
python3 scripts/build_github_pages.py --out build/github-pages
```

The build script copies:

- static site files from `site/github-pages/`;
- explicitly allowlisted Markdown files into `build/github-pages/bundle/`;
- the existing static admin HMI demo into
  `build/github-pages/demos/admin-hmi/`;
- a generated `public-file-manifest.json` with paths, byte counts, and hashes.

GitHub Actions deploys only `build/github-pages` through
`.github/workflows/pages.yml`.

## Public Content Policy

Allowed public content:

- curated Markdown documentation that is already source-backed or clearly
  marked as an assumption or unresolved gap;
- static HTML, CSS, JavaScript, and JSON for the landing page and admin HMI
  demo;
- generated manifest metadata for the allowlisted public files.

Excluded public content:

- `.agents/` records and internal handoffs;
- `user_uploads/` and raw photo archives;
- generated screenshots and bulky media;
- copied vendor PDFs or source artifacts;
- private bench notes or files not listed in `scripts/build_github_pages.py`.

## Safety Boundary

The public site is DIY concept/prototype documentation only. It does not approve
mains wiring, relay load wiring, live firmware flashing, relay switching, or
XBee setting writes.

The public site must keep hardware blockers visible, including power-source
selection, voltage compatibility, boot-pin effects, relay trigger polarity,
relay input current, isolation behavior, XBee read/write readiness, enclosure
selection, overcurrent protection, grounding/bonding, GFCI/de-energization
process, strain relief, and qualified review.

## Manual Repository Setting

Before a live deployment can succeed, a repository admin or maintainer must set
the repository Pages source to `GitHub Actions` in the repository settings.
Source ID: `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`.

Unknowns:

- final repository owner/name and project-site URL;
- whether Pages permissions are enabled in the eventual remote repository;
- whether deployment protection rules will be added to the `github-pages`
  environment.

## Validation

Run these checks before handoff:

```bash
python3 scripts/build_github_pages.py --out build/github-pages
python3 -m py_compile scripts/build_github_pages.py scripts/verify_scaffold.py
python3 scripts/verify_scaffold.py
find . -path './.git' -prune -o \( -name 'CMakeLists.txt' -o -name 'sdkconfig*' -o -name 'platformio.ini' -o -name 'idf_component.yml' -o -name 'arduino-cli.yaml' \) -print
```

Local browser verification should confirm that the landing page renders on
desktop and mobile, no horizontal overflow appears, public bundle links resolve,
the admin HMI demo opens from `demos/admin-hmi/`, safety disclaimers are
visible, no console errors are emitted, and no external network requests occur.
