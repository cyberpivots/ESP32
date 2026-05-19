# Task 0011 - GitHub Pages Blueprints And Schematics

## Task

- ID: 0011-github-pages-blueprints-schematics
- Owner role: Release, QA
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Create a beginner-friendly public visual blueprint experience for the
four-relay XBee Wi-Fi controller Pages site while preserving the safety
boundary that the diagrams are conceptual and not verified wiring
instructions.

## Scope

Included: dedicated `blueprints.html` page, generated label-free WebP
blueprint backplates, homepage links, site data links, public text blueprint
explanations, build allowlist update, scaffold verifier update, and local
Pages validation.

Excluded: firmware source, framework changes, relay wiring, relay load
switching, mains wiring, TFT wiring, expander-to-relay wiring, raw photo
publishing, vendor PDF publishing, and edits to the unrelated untracked
`0009` task log.

## Sources

- `SRC-GITHUB-PAGES-WHAT-IS`
- `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`
- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`
- `SRC-GITHUB-PAGES-LIMITS`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`
- `SRC-SONGLE-SRD-05VDC-SL-C`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-NIOSH-ELECTRICAL-SAFETY`
- `SRC-OSHA-DEENERGIZED-WORK`
- `SRC-OSHA-GFCI`
- `SRC-OSHA-AEGCP`
- `SRC-OSHA-GROUNDING-OVERCURRENT`
- `SRC-NEMA-ENCLOSURES`
- `SRC-TI-CD74HC4067`
- `SRC-TI-TCA9555`
- `SRC-ESPRESSIF-MCP23017-COMPONENT`
- `SRC-TI-TPIC6B595`
- `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`
- `SRC-LCDWIKI-R61509V-MRB2802`

## Decisions

- The public blueprint backplates are generated as label-free WebP images under
  `site/github-pages/assets/blueprints/`; factual labels remain HTML text.
- The build script allows only the two named generated image assets and keeps
  raw uploads, `.agents/`, vendor PDFs, bulky binaries, private notes, and
  unrelated image binaries excluded.
- Every public blueprint panel states that relay/load wiring, mains wiring,
  TFT wiring, and expander-to-relay wiring remain blocked until the documented
  gates close.

## Validation

- `python3 -m json.tool site/github-pages/site-data.json`: PASS.
- `node --check site/github-pages/app.js`: PASS.
- `python3 -m py_compile scripts/build_github_pages.py scripts/verify_scaffold.py`:
  PASS.
- `python3 scripts/verify_scaffold.py`: PASS before and after building.
- `python3 scripts/build_github_pages.py`: PASS, generated 48 public files.
- Manifest check: PASS, `blueprints.html`,
  `assets/blueprints/system-overview.webp`, and
  `assets/blueprints/safety-proof-ladder.webp` are present; no other image
  assets are in the manifest.
- `git diff --check`: PASS.
- Local Playwright preview from `build/github-pages` on
  `http://127.0.0.1:8058/`: PASS on desktop `1440x1000` and mobile
  `390x844` for `index.html` and `blueprints.html`; images load, labels are
  nonempty, blocked wiring text is visible, no horizontal overflow appears, and
  zero console errors were reported.
- Local link check from `blueprints.html`: PASS, `index.html`,
  `blueprints.html`, text blueprint, build guide, mains gate, and power gates
  returned HTTP 200.

## Handoff

Release and QA should continue from
`.agents/handoffs/0008-github-pages-blueprints-to-release-qa.md` after local
validation is recorded here.
