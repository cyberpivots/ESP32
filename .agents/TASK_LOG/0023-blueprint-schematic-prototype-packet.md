# Task 0023 - Blueprint Schematic Prototype Packet

## Task

- ID: 0023-blueprint-schematic-prototype-packet
- Owner role: Release, QA, Hardware, Communications, Agent operations
- Status: complete
- Created: 2026-05-21
- Updated: 2026-05-21

## Goal

Implement a source-backed public Prototype Build Packet for the ESP32
four-relay workbench while keeping unresolved hardware, relay, radio, TFT,
MicroSD, load, and mains facts explicit.

## Scope

Included:

- Dedicated public `prototype.html` packet page.
- Packet Markdown and public-safe XBee boundary summary.
- Label-free WebP backplates for evidence map, low-voltage review sequence,
  and pin-pressure map.
- Build allowlist and manifest audit updates, including Markdown content
  redaction checks.
- Source ledger, source-index updates, docs index updates, known-gaps note,
  and skill inventory refresh.
- Expert-panel findings from workspace cartographer, source researcher,
  architecture risk reviewer, and QA validation reviewer.

Excluded:

- Firmware behavior changes, framework changes, relay GPIO writes, expander
  writes to relay hardware, XBee setting writes, XBee API transmit frames,
  ESP32 DIN/DOUT carrier wiring, MicroSD mount proof, TFT wiring, firmware
  flashing, deployment push, relay/load wiring, and mains/load procedures.

## Sources

- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-21`
- `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-SONGLE-SRD-05VDC-SL-C`

## Decisions

- Public packet means no blockers to finding verified information, source
  links, review order, diagrams, evidence requirements, gaps, and stop
  conditions. It does not remove safety gates.
- The public bundle now publishes `xbee-public-boundary.md` instead of the
  detailed internal XBee protocol contract.
- The public artifact keeps a sanitized source-index copy and a content audit
  so allowlisted Markdown cannot leak raw upload archive names, raw photo
  filenames, local device identifiers, radio identifiers, AES key values, or
  private bench-note breadcrumbs.
- The manifest audit now checks that every `SRC-*` reference in public
  Markdown is present in the generated public source-index copy.
- New raster backplates are label-free. Exact labels and safety facts remain in
  HTML/Markdown.

## Panel findings addressed

- Workspace cartographer: added the missing public packet surface and updated
  allowlists, smoke markers, and docs links.
- Source researcher: refreshed official-source access dates and local skill
  inventory hash to `36878fcb`.
- Architecture risk reviewer: added source-index redaction and kept ADR-0003
  and ESP-NOW work outside this four-relay public packet scope.
- QA validation reviewer: rebuilt from current source before auditing, added
  content-level public Markdown checks, added public source-ID coverage checks,
  and added WebP decode/dimension checks.

## Validation

- `python3 scripts/build_github_pages.py --out build/github-pages`: PASS.
- `python3 scripts/audit_public_manifest.py`: PASS, including public
  source-ID coverage.
- `python3 scripts/smoke_github_pages.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 -m json.tool site/github-pages/site-data.json`: PASS.
- `python3 -m json.tool docs/projects/four-relay-xbee-wifi/ui/manifest.json`: PASS.
- `node --check site/github-pages/app.js`: PASS.
- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js`: PASS.
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 tests/scaffold_audits/test_source_image_scan.py`: PASS.
- `git diff --check`: PASS.
- Local Playwright browser validation: PASS for `index.html`,
  `prototype.html`, `blueprints.html`, `quality.html`, and
  `demos/admin-hmi/` after serving `build/github-pages`.

## Handoff

No downstream role is blocked by this documentation/public-site pass. Hardware,
communications, firmware, and QA should continue using the gaps in
`research/known-gaps.md`; no live hardware, XBee write, relay, TFT, MicroSD,
flash, load, or mains gate was closed.
