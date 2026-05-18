# GitHub Workflows

- `pages.yml` builds the curated public DIY site with
  `scripts/build_github_pages.py` and deploys only `build/github-pages` through
  GitHub Pages.
- Repository settings must use Pages source `GitHub Actions` before live
  deployment.
- The workflow intentionally does not publish the repository root or the
  working `docs/` tree.
