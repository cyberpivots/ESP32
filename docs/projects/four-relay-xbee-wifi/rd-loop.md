# R&D Loop

This document defines the milestone-based R&D loop for
`four-relay-xbee-wifi`. It moves source-backed research into prototype
development without weakening hardware, safety, or public-release gates.

## Verified facts

- The workspace remains framework-neutral, but ADR-0002 accepts ESP-IDF stable
  v6.0.1 for this project only. Source IDs: `SRC-ESP-IDF-STABLE-ESP32`,
  `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF stable v6.0.1 documentation covers the project surfaces needed for a
  future implementation: Wi-Fi, HTTP server, GPIO, UART, NVS, FatFS/VFS, and
  SDSPI. Source IDs: `SRC-ESP-IDF-WIFI`, `SRC-ESP-IDF-HTTP-SERVER`,
  `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-NVS`,
  `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- The photographed hardware set and XBee read-only boundary are already
  documented in the project package. Source IDs:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBP9B-DPUT-001`, `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Mains/load work remains blocked by qualified-review and safety gates. Source
  IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-OSHA-1910-305`,
  `SRC-NEMA-ENCLOSURES`, `SRC-NEMA-250-ENCLOSURES`.
- ESP-IDF v6.0.1 is installed locally for this project and the disabled
  skeleton build passes after sourcing
  `/home/cyber/.espressif/tools/activate_idf_v6.0.1.sh`. Source ID:
  `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`.

## Assumptions

- The loop is milestone-based, not weekly timeboxed.
- The role lanes are Architect, Hardware, Communications, Firmware, QA, and
  Release.
- Each non-trivial cycle creates or updates its own task record and handoff.
- The first prototype milestone is a disabled-by-default ESP-IDF skeleton under
  this project only.
- Host tests are required before any future hardware-facing implementation is
  considered.

## Unknowns

- Exact board, shield, relay-module, MicroSD, TFT, mux, expander, XBee carrier,
  enclosure, and load evidence remain unresolved.
- Flashing tools are present only as toolchain evidence; flashing remains
  blocked until physical no-load evidence and recovery records are complete.
- OpenOCD udev rules were not installed during EIM setup because copying to
  `/etc/udev/rules.d/` needs elevated permissions.
- Final pins, relay polarity, driver stage, XBee carrier wiring, storage
  wiring, authentication format, and release packaging remain open.

## Non-negotiable gates

- No relay/load wiring, relay-expander wiring to relay inputs, mains/load
  design, or public load wiring procedure.
- No XBee setting writes, `WR`, `AC`, firmware update, factory reset, API
  transmit frames, relay commands over XBee, or ESP32 DIN/DOUT carrier wiring.
- No relay GPIO writes, expander writes to relay hardware, TFT wiring, firmware
  flashing, monitor automation, or live bench mutation until the matching
  milestone gate closes.
- No `.agents/` records, private upload archives, raw photos, vendor PDFs,
  private bench records, unredacted radio identifiers, or bench-record paths in
  public artifacts.

## Milestones

| Milestone | Goal | Entry gate | Exit gate |
| --- | --- | --- | --- |
| M0 intake | Build the evidence map from current docs, source index, known gaps, and task records. | Current worktree reviewed and AGENTS reading complete. | Open gaps, sources, task record, and handoff are updated. |
| M1 hardware evidence | Close evidence for board/shield power, relay module, XBee dock/carrier, MicroSD, TFT, mux, expander, tools, and enclosure gates. | M0 complete and source-index entries exist or gaps are explicit. | Hardware lane marks each item `approved`, `approved_with_gaps`, or `blocked`. |
| M2 disabled skeleton | Add host-testable ESP-IDF skeleton with all hardware outputs disabled by default. | ADR-0002 accepted and M1 gaps remain treated as closed gates only when measured. | Host tests pass; static scan proves no relay GPIO writes, XBee writes, flash path, or live carrier assumption. |
| M3 simulated integration | Simulate HTTP state, storage status, XBee parser/telemetry framing, safety supervisor, and UI mock behavior. | M2 host tests and API contracts pass. | QA approves positive and negative simulated flows, including rejected unsafe transitions. |
| M4 bench-gated enablement | Enable one hardware path at a time only after measured evidence closes that gate. | M1 evidence for the selected path is complete and reviewed. | Bench record, stop conditions, rollback plan, and private/public evidence classification are recorded. |
| M5 release/public package | Review public artifacts, Pages allowlist, changelog/readiness notes, and private-evidence exclusion. | Role-lane disposition recorded for the cycle. | Release and QA approve public bundle manifest and source-path audit. |

## Role lanes

| Lane | Owns | Required review output |
| --- | --- | --- |
| Architect | Architecture consistency, ADR fit, interfaces, and milestone sequence. | `approved`, `approved_with_gaps`, or `blocked` plus architecture notes. |
| Hardware | Verified facts, measurements, pin/power risks, and unresolved gaps. | Gate table for board, relay, XBee, storage, TFT, mux, expander, tools, enclosure, and load. |
| Communications | XBee/API frame boundaries, read-only/write gates, parser vectors, and radio evidence handling. | Parser/test-vector status and XBee mutation boundary. |
| Firmware | ESP-IDF skeleton, disabled-by-default hardware gates, state machine, config, parser, storage, and host tests. | Test results and static safety scan. |
| QA | Validation scripts, acceptance checks, negative tests, artifact safety checks, and stop conditions. | Reproducible command log and pass/fail disposition. |
| Release | Docs index, public bundle allowlist, changelog/readiness notes, and publish safety. | Public manifest audit and release-readiness disposition. |

## Cycle review rule

A cycle is not accepted until every role lane records one of:

- `approved`
- `approved_with_gaps`
- `blocked`

The integrator then records the final disposition in the task record. A blocked
lane does not disappear; the blocker must remain in `research/known-gaps.md`
or in the active task handoff.

## M2 prototype boundaries

The first skeleton may add project-local ESP-IDF files under
`firmware/projects/four-relay-xbee-wifi/` because ADR-0002 is accepted for this
project only. It must expose host-testable modules for:

- relay state manager with relay outputs disabled while the hardware gate is
  open, using the stable `hardware_gate_open` reject reason,
- safety supervisor,
- config store abstraction,
- XBee API frame parser/encoder tests without transmit-to-hardware behavior,
- HTTP/API contract stubs,
- storage status abstraction.

The skeleton must not add `sdkconfig`, flash/monitor automation, GPIO output
enablement, relay expander writes, XBee setting writes, XBee API transmit to
hardware, or bench-mutation scripts.

## Acceptance checks

- `python3 scripts/verify_scaffold.py`
- `python3 -m py_compile scripts/verify_scaffold.py scripts/build_github_pages.py scripts/xbee_read_only_probe.py tests/four_relay_safe_core/run_host_tests.py`
- `python3 tests/four_relay_safe_core/run_host_tests.py`
- `python3 scripts/build_github_pages.py`
- `git diff --check`
- Source-ID audit for each new `SRC-*` reference.
- Public manifest audit for blocked private or bulky paths.
- Static scan for flash commands, relay GPIO writes, XBee writes, and live
  carrier assumptions.
