# Four Relay KY-040 BBS LCD Menu PF0530U Responsive V7

Status: PF0530U written and verify-flashed on COM6; post-flash actuation proof pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Selected tier: Tier 3 because this continuation includes firmware mutation
  and a COM6 write/verify/read-only proof.
- Owner role: Firmware owner with coordinator, QA, LCD UX, hardware-safety, and
  evidence-record lenses.
- Evidence need: source diff, generated menu proof, focused tests, scaffold
  audits, ESP-IDF build, artifact hashes, COM6 identity, rollback backup,
  write-flash, separate verify-flash, reset boot transcript, attended read-only
  transcript, cleanup proof, and durable records.
- Mutation boundary: PF0530U firmware/menu/test/docs/source records plus COM6
  bootloader, partition table, and app write only. No erase, serial command
  writes, XBee/RF writes or tests, relay GPIO writes, relay-expander writes,
  ESP-NOW runtime expansion, wiring changes, DMM/current/load/mains, persistent
  config, external services, release, commit, or push.
- Reviewer disposition: subagent spawning was not used because the discovered
  multi-agent tool contract allows spawn only when the user explicitly asks for
  subagents. Local coordinator, firmware, QA, LCD UX, hardware-safety, and
  evidence-record lenses approved the named PF0530U boundary with no unresolved
  P1/P2 blockers. Weighted disposition was 17/17.
- Gate authority: the user's same-session instruction to do what it takes to
  leave the rotary encoder responsive is treated as explicit authority for this
  named COM6-only responsiveness gate, with all closed surfaces preserved.

## Verified Facts

- PF0530T restored raw input proof and button/select proof but remained too
  conservative for rotation: the attended transcript recorded `ENC_EV=446`,
  `MAX_RAW_AB=905`, `MAX_RAW_SW=60`, `SELECT=30`, `STEP_PLUS=2`, and
  `STEP_MINUS=2`.
- PF0530U changes firmware identity and generated menu metadata to `PF0530U`.
- PF0530U keeps GPIO13/GPIO14/GPIO32 input-only with pullups; LCD GPIO21/GPIO22
  remains display-only; `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- PF0530U keeps polling authoritative at 2 ms, disables interrupt-fed decoding
  and per-edge raw serial logging, keeps detent-gated stepping, and changes
  `FR_ENCODER_TRANSITIONS_PER_STEP` from `2` to `1`.
- PF0530U reports `cal=responsive-v7`.

## Unknowns

- Whether one-transition detent-return stepping gives the desired live
  one-detent/one-row feel without runaway.
- Whether fast scrolling remains controlled with the 25 ms step lockout.

## Validation

- PASS: focused tests, generated menu freshness check, firmware scaffold audit,
  scaffold verification, ESP-IDF build, and `git diff --check`.
- PASS: COM6 identity and flash ID recheck.
- PASS: fresh 4 MB rollback backup, staged artifact hashes, write-flash, and
  separate parameter-matched verify-flash.
- PASS: reset monitor showed `PF0530U`, `LCD_INIT_OK`, `BBS_LCD_READY`,
  `BBS_INPUT_READY cal=responsive-v7`, `step=1`, GPIO config, and heartbeat.
- PASS: two post-flash read-only monitors showed stable heartbeat/render output
  and zero crash markers.
- OPEN: both PF0530U post-flash monitors captured no physical input events, so
  final PF0530U knob/switch actuation proof remains pending.

## Decision Footer

Decision: `continue`. Next gate: focused validation and COM6
identity/rollback/write/verify/read-only proof. Owner: Firmware with Hardware
QA and Evidence Records. Evidence: PF0530T live counts justify the threshold
change; PF0530U must prove the final live condition. Approved mutation
boundary: PF0530U source/docs/records plus COM6 bootloader, partition, and app
write only. Authority limits: no erase, serial command writes, XBee/RF,
relay/load/mains, wiring, DMM/current, persistent config, external services,
release, commit, or push.
