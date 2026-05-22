# Source Ledger - 2026-05-21 Blueprint Schematic Improvement

## Scope

Public Prototype Build Packet implementation for `four-relay-xbee-wifi`. This
pass adds a dedicated public packet page, packet Markdown, label-free
schematic backplates, public bundle text redaction, and a public-safe XBee
boundary summary. It does not change firmware behavior, relay wiring, XBee
settings, live hardware, deployment settings, or load/mains procedures.

## Verified facts

- `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`: GitHub Pages custom workflows use
  Actions artifact upload and deploy actions; the local workflow already
  follows that deployment shape.
- `SRC-ESP-IDF-GPIO`: ESP32 GPIO, strapping-pin, flash/PSRAM, input-only, and
  GPIO-matrix facts remain valid review inputs for the pin-pressure map.
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`: ESP32 schematic checklist material
  remains valid for power, reset, UART, strapping, GPIO, and integration
  review gates.
- `SRC-DIGI-XBP9B-DPUT-001`: Digi's model page supports only the public part
  identity and high-level model description for `XBP9B-DPUT-001`.
- `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-21`: Current local plugin skill
  paths use cache hash `36878fcb`.
- `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21`: Local implementation and validation
  record for the public packet, generated WebP backplates, build allowlist,
  content audit, public source-ID coverage audit, smoke checks, scaffold
  checks, and host-side tests.

## Assumptions

- The phrase "no blockers" means no blockers to finding verified public
  prototype information, source links, diagrams, review sequence, and evidence
  requirements.
- Public diagrams remain conceptual review surfaces. Exact factual labels,
  pins, warnings, and source IDs stay in HTML or Markdown.
- Publishing a public-safe XBee boundary summary is safer than publishing the
  detailed internal protocol contract in the Pages bundle.

## Unknowns

- No hardware gaps were closed by this pass. Exact board/shield, relay module,
  XBee carrier, MicroSD, TFT, mux, expander, driver-stage, and load/mains
  evidence remain unresolved.
- Browser viewport validation remains a local Playwright action rather than a
  checked-in CI script.

## Workspace updates

- Added `docs/projects/four-relay-xbee-wifi/prototype-build-packet.md`.
- Added `docs/projects/four-relay-xbee-wifi/xbee-public-boundary.md`.
- Added `site/github-pages/prototype.html`.
- Added label-free WebP backplates under
  `site/github-pages/assets/blueprints/`.
- Updated Pages build, manifest audit, smoke, and scaffold marker checks,
  including public Markdown `SRC-*` coverage against the generated public
  source index.
- Updated source index, docs index, known gaps, skill inventory, and task log.
- Replaced the detailed XBee protocol file in the public bundle with the
  public-safe XBee boundary summary.
