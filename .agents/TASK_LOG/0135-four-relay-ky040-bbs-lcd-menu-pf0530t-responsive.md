# Four Relay KY-040 BBS LCD Menu PF0530T Responsive Recovery

Status: PF0530T source/build passed; COM6 live proof in progress

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Selected tier: Tier 3 because this continuation includes firmware mutation
  and an intended COM6 write/verify/read-only proof.
- Owner role: Firmware owner with coordinator, QA, LCD UX, hardware-safety, and
  evidence-record lenses.
- Evidence need: source diff, generated menu output, focused tests, scaffold
  audit, scaffold verification, ESP-IDF v6.0.1 no-flash build, artifact hashes,
  COM6 identity, rollback backup, write-flash, separate verify-flash, reset
  boot transcript, attended read-only transcript, cleanup proof, and durable
  records.
- Mutation boundary: PF0530T firmware/menu/test/docs/source records plus COM6
  bootloader, partition table, and app write only. No erase, serial command
  writes, XBee/RF writes or tests, relay GPIO writes, relay-expander writes,
  ESP-NOW runtime expansion, wiring changes, DMM/current/load/mains, persistent
  config, external services, release, commit, or push.
- Reviewer disposition: subagent spawning was not used because the discovered
  multi-agent tool contract allows spawn only when the user explicitly asks for
  subagents. Local coordinator, firmware, QA, LCD UX, hardware-safety, and
  evidence-record lenses approved the named PF0530T boundary with no unresolved
  P1/P2 blockers. Weighted disposition was 17/17.
- Gate authority: the user's same-session instruction to do what it takes to
  leave the rotary encoder responsive is treated as explicit authority for this
  named COM6-only responsiveness gate, with all closed surfaces preserved.

## Verified Facts

- PF0530S recovered raw A/B and switch liveness but did not leave rotary
  stability accepted; its transcript recorded invalid/suppressed transitions
  and final heartbeat `queue_drop=57`.
- PF0530T changes the active firmware ID and generated menu metadata to
  `PF0530T`.
- PF0530T keeps GPIO13/GPIO14/GPIO32 input-only with pullups; LCD GPIO21/GPIO22
  remain display-only; `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- PF0530T makes polling the authoritative decoder path: `FR_MENU_POLL_MS 2`,
  `FR_ENCODER_INTERRUPT_TELEMETRY 0U`, queue depth/drain `0`, and
  `irq=poll`.
- PF0530T disables per-edge raw serial spam with
  `FR_ENCODER_RAW_EVENT_LOG_ENABLED 0U`, while preserving heartbeat counters.
- PF0530T emits steps only on detent return with
  `FR_ENCODER_DETENT_GATED 1U`, `FR_ENCODER_TRANSITIONS_PER_STEP 2`, and
  `FR_ENCODER_STEP_LOCKOUT_MS 25`.
- PF0530T uses one stable A/B sample, 1 ms A/B candidate hold, 0 ms A/B quiet
  time, 30 ms switch debounce, 25 ms switch guard, and 650 ms long press.
- PF0530T reports `cal=responsive-v6`.

## Assumptions

- The GPIO13/GPIO14/GPIO32 and LCD21/22 wiring remains unchanged from the
  PF0530S live proof.
- A detent-gated polling decoder is more likely to feel usable than PF0530S's
  one-transition-per-step diagnostic decoder.

## Unknowns

- Whether PF0530T gives the desired one-detent/one-row physical feel on the
  actual KY-040 module.
- Whether 25 ms lockout is enough to suppress bounce while preserving fast
  scrolling.

## Validation

- PASS: focused LCD/encoder unittest suite.
- PASS: generated menu freshness check.
- PASS: firmware scaffold audit.
- PASS: ESP-IDF v6.0.1 no-flash build at
  `/tmp/esp32-pf0530t-responsive-build`.
- Pending: scaffold verification, `git diff --check`, COM6 identity, rollback,
  artifact hashes, write-flash, separate verify-flash, reset monitor, attended
  monitor, cleanup proof, and final live record updates.

## Decision Footer

Decision: `continue`. Next gate: scaffold verification and COM6
identity/rollback/write/verify/read-only proof. Owner: Firmware with Hardware
QA and Evidence Records. Evidence: source diff, focused tests, generator check,
scaffold audit, ESP-IDF build, pending live proof. Approved mutation boundary:
PF0530T source/docs/records plus COM6 bootloader, partition, and app write
only. Authority limits: no erase, serial command writes, XBee/RF,
relay/load/mains, wiring, DMM/current, persistent config, external services,
release, commit, or push.
