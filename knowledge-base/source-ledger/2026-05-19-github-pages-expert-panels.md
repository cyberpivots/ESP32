# Source Ledger - 2026-05-19 GitHub Pages Expert Panels

## Scope

Expert-panel improvement pass for the public GitHub Pages artifact. This pass
adds a public-safe review-panel surface, tightens artifact/safety wording,
labels relay signals as candidate GPIOs, and moves Pages workflow validation
earlier in the deployment job. It does not change firmware behavior, framework
status, relay wiring, XBee radio settings, live hardware operation, or
load/mains procedures.

## Verified facts

- `SRC-LOCAL-GITHUB-PAGES-EXPERT-PANELS-2026-05-19`: Local validation records
  the updated static Pages source, generated artifact checks, host-side
  contract tests, browser rendering checks, and no-horizontal-overflow checks.
- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`: GitHub Pages is deployed from the
  checked-in workflow, so moving local validation before artifact upload keeps
  the generated artifact gate inside the deployment path.
- `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`: Public Pages availability remains a
  repository setting and workflow outcome; this pass does not claim future
  deployments stay valid without re-verification.
- `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`: Host software contract
  tests validate safe-core API and parser behavior only. They are not
  electrical safety tests and do not validate live relay hardware.
- `SRC-OPENAI-REASONING` and `SRC-CODEX-SUBAGENTS`: The panel method follows
  the local expert-panel skill's reasoning and subagent boundary guidance.

## Assumptions

- Public site improvements should stay dense, technical, and source-backed
  rather than becoming a marketing page.
- The visible expert-panel section is safe to publish because it describes
  review lanes and links to public-safe sources without exposing private
  `.agents/` records.
- Browser QA through the current Playwright tool is valid local render
  evidence, but it is not yet a checked-in CI script.

## Unresolved gaps

- A reusable checked-in browser QA script is still open. Current workflow
  validation runs syntax, build, manifest, smoke, scaffold, and host tests, but
  not full browser rendering assertions.
- Future GitHub Actions runner changes may require updating the current Pages
  Actions versions and Node runtime behavior.

## Workspace updates

- Updated `site/github-pages/index.html`, `quality.html`, `blueprints.html`,
  `site-data.json`, `app.js`, and `styles.css`.
- Updated `.github/workflows/pages.yml` and `.github/workflows/README.md` so
  validation runs before artifact upload.
- Updated `scripts/scaffold_audit_pages.py` and `scripts/smoke_github_pages.py`
  to cover the new expert-panel and safety wording.
- Updated `scripts/scaffold_audit_data.py`, `docs/index.md`,
  `docs/github-pages-public-site.md`, and `knowledge-base/source-index.md`.
- Added `.agents/TASK_LOG/0020-github-pages-expert-panels.md` and this source
  ledger.
