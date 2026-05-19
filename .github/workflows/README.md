# GitHub Workflows

- `pages.yml` builds the curated public DIY site with
  `scripts/build_github_pages.py` and deploys only `build/github-pages` through
  GitHub Pages.
- Before upload, the workflow now runs JSON and JavaScript syntax checks,
  public manifest audit, Pages smoke checks, scaffold verification, Python
  compilation, and host-side contract tests.
- Current repository Pages settings use the GitHub Actions source for
  `https://cyberpivots.github.io/ESP32/`; re-verify the Pages API and latest
  workflow result after any repository, branch, workflow, permission, or Pages
  setting change.
- The workflow intentionally does not publish the repository root or the
  working `docs/` tree.
