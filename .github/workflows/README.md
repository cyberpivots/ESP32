# GitHub Workflows

- `scaffold-ci.yml` is non-deploy CI for pull requests and manual validation.
  It runs diff whitespace checks, syntax checks, full scaffold-audit unittest
  discovery, scaffold audits, publication hygiene reporting, scaffold
  verification, Python compilation, and host-side contract tests. It does not
  upload Pages artifacts or deploy.
- `pages.yml` builds the curated public DIY site with
  `scripts/build_github_pages.py` and deploys only `build/github-pages` through
  GitHub Pages on `main` push or manual dispatch.
- Before upload, the workflow now runs JSON and JavaScript syntax checks,
  `git diff --check`, public manifest audit, Pages smoke checks, full
  scaffold-audit unittest discovery, scaffold verification, Python compilation,
  and host-side contract tests.
- Current repository Pages settings use the GitHub Actions source for
  `https://cyberpivots.github.io/ESP32/`; re-verify the Pages API and latest
  workflow result after any repository, branch, workflow, permission, or Pages
  setting change.
- The workflow intentionally does not publish the repository root or the
  working `docs/` tree.
