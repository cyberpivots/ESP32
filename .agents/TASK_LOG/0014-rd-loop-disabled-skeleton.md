# Task 0014 - R&D Loop And Disabled Skeleton

## Task

- ID: 0014-rd-loop-disabled-skeleton
- Owner role: Architect, Firmware, QA, Release
- Status: Complete
- Created: 2026-05-19
- Updated: 2026-05-19

## Goal

Create the canonical milestone-based role-lane R&D loop for
`four-relay-xbee-wifi` and add the first project-local ESP-IDF skeleton with
all hardware outputs disabled by default.

## Scope

Included: R&D loop document, project/doc index links, project-local ESP-IDF
skeleton shell, host-testable safe core, host tests, public bundle allowlist
update for the loop document, scaffold verification updates, task record, and
handoff.

Excluded: relay/load wiring, mains/load design, XBee setting writes, XBee API
transmit frames to hardware, relay GPIO writes, expander writes to relay
hardware, ESP32 DIN/DOUT carrier wiring, TFT wiring, flashing, monitoring, live
bench mutation, `sdkconfig`, vendor PDF copies, raw upload copies, private bench
notes, and public bench records.

## Sources

- `SRC-ESP-IDF-STABLE-ESP32`
- `SRC-ESP-IDF-GET-STARTED`
- `SRC-ESP-IDF-WIFI`
- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP-IDF-NVS`
- `SRC-ESP-IDF-FATFS`
- `SRC-ESP-IDF-SDSPI`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-NIOSH-ELECTRICAL-SAFETY`
- `SRC-OSHA-DEENERGIZED-WORK`
- `SRC-OSHA-GFCI`
- `SRC-OSHA-AEGCP`
- `SRC-OSHA-GROUNDING-OVERCURRENT`
- `SRC-OSHA-1910-305`
- `SRC-NEMA-ENCLOSURES`
- `SRC-NEMA-250-ENCLOSURES`

## Decisions

- The role-lane loop uses M0 through M5 milestones with Architect, Hardware,
  Communications, Firmware, QA, and Release review lanes.
- This skeleton is project-local under
  `firmware/projects/four-relay-xbee-wifi/`; workspace-level framework
  neutrality remains unchanged.
- The skeleton uses pure C `safe_core` modules so relay state, safety, config,
  HTTP route classification, storage status, and XBee API-frame parsing can be
  tested without ESP-IDF tools or hardware.
- `app_main` initializes in-memory defaults only and performs no GPIO, UART,
  I2C, Wi-Fi, HTTP, storage, flash, monitor, or bench-mutation action.

## Validation

- `python3 -m py_compile scripts/verify_scaffold.py scripts/build_github_pages.py scripts/xbee_read_only_probe.py tests/four_relay_safe_core/run_host_tests.py`:
  PASS.
- `python3 tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 scripts/build_github_pages.py`: PASS, generated 53 public files.
- `git diff --check`: PASS.
- Source-ID audit for the new loop, skeleton README, and task record: PASS,
  no unresolved `SRC-*` references.
- Public artifact source-path audit: PASS, no `.agents/`, `user_uploads/`, or
  `research/bench-records/` sources in
  `build/github-pages/public-file-manifest.json`.
- Static skeleton scan: PASS, no forbidden firmware mutation markers in
  `firmware/projects/four-relay-xbee-wifi/` source files.
- ESP-IDF build/flash validation: NOT RUN. `idf.py` and `cmake` are not
  available on PATH in this shell, and the gate forbids flash/monitor steps.

## Handoff

Continue through `.agents/handoffs/0011-rd-loop-disabled-skeleton-to-role-lanes.md`
after validation is recorded here.
