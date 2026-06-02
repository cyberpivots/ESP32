# Four Relay KY-040 BBS LCD Menu PF0530V PCNT Source Build

Status: source/build prepared; no COM6 flash or live proof in this task

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Selected tier: Tier 2 because this continuation mutates firmware source,
  tests, docs, and records but does not perform COM6 flash, monitor, serial, or
  hardware actions.
- Owner role: Firmware owner with coordinator, QA, LCD UX, hardware-safety, and
  evidence-record lenses.
- Evidence need: source diff, generated menu proof, focused tests, scaffold
  audits, ESP-IDF no-flash build, `git diff --check`, and durable records.
- Mutation boundary: PF0530V firmware/menu/test/docs/source records only. No
  COM6 identity query, flash, verify-flash, monitor, serial command writes,
  XBee/RF writes or tests, relay GPIO writes, relay-expander writes, ESP-NOW
  runtime expansion, wiring changes, DMM/current/load/mains, persistent config,
  external services, release, commit, or push.
- Reviewer disposition: prior read-only quorum approved the named source-only
  PF0530V boundary at 20/20 weight with no P1/P2 blockers. Current sidecar
  reviewers are read-only QA/evidence support.

## Verified Facts

- PF0530U is the last recorded written and verify-flashed COM6 image; its
  post-flash monitors captured no physical input events.
- PF0530V changes firmware identity and generated menu metadata to `PF0530V`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only, and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530V switches rotation from the software detent-return decoder to
  ESP-IDF PCNT quadrature counting with `esp_driver_pcnt`.
- Switch handling remains poll/debounce based, with a 40 ms switch guard.
- PF0530V reports `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`,
  `poll_decoder=0`, and PCNT heartbeat/counter telemetry.

## Unknowns

- Live PCNT count direction and counts-per-detent behavior on the attached
  KY-040 module are unproven until a future Tier 3 gate.
- Live responsiveness, runaway tolerance, and short/long press behavior remain
  unaccepted until COM6 flash/read-only interaction proof is collected.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_hooks tests.scaffold_audits.test_admin_policy_hooks tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu`
  ran 60 tests.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-pf0530v-pcnt-build build`.
- PASS: final `git diff --check`.

## Decision Footer

Decision: `continue`. Next gate: separate Tier 3 PF0530V live proof only if
explicitly opened. Owner: Firmware with QA, LCD UX, hardware-safety, and
evidence records. Evidence: PF0530V source-only tests, audits, scaffold
verification, and ESP-IDF no-flash build passed; live PCNT behavior remains
unproven. Approved mutation boundary: PF0530V source/docs/tests/records only.
Authority limits: no COM6 flash/monitor/serial, XBee/RF, relay/load/mains,
wiring, DMM/current, persistent config, external services, release, commit, or
push.
