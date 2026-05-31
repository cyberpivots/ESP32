# Source Ledger - 2026-05-30 Four Relay KY-040 PF0530F Live Proof Attempt

## Verified Facts

- User authorized the Tier 3 COM6 PF0530F flash/live proof gate and confirmed
  same-session safe state.
- The evidence directory is
  `research/bench-records/xbee-readonly/local-ky040-pf0530f-encoder-menu-live-20260530T214332Z/`.
- COM6 identified as ESP32-D0WDQ6 revision v1.0, MAC `78:e3:6d:0a:90:14`,
  detected flash size 4 MB, and flash voltage 3.3 V.
- A full 4 MB rollback backup completed and has SHA-256
  `1d2c014462a1fae9521444b9bca7c256bfc358ecea7a37f7b71d7833e0ac784b`.
- PF0530F write-flash completed with per-segment hash verification.
- Separate verify-flash matched the staged bootloader, partition table, and app
  image.
- Read-only monitor captured `PF0530F MENU_READY gpio=13/14/32 pullups=on xbee=closed relay=closed`.
- Read-only monitor captured `PF0530F LCD_INIT_FAILED`.
- Read-only monitor captured no `MENU_HB`, `MENU_STEP`, or `MENU_SELECT` proof.
- Transcript scan reported no crash-fault markers and no closed-surface
  violation markers.

## Assumptions

- COM6 remained the intended ESP32 target because identity matched during
  identity, write-flash, and verify-flash.
- KY-040 wiring and LCD-only I2C safe state remained as user-confirmed during
  the monitor.

## Unknowns

- Cause of `LCD_INIT_FAILED`.
- Whether the LCD issue is power, I2C wiring, address/probe behavior, bus state,
  firmware timing, or another LCD initialization issue.
- PF0530F menu-step, button-select, suppression, and physical rotation-direction
  behavior remain unproven.

## Closed Surfaces

- No relay GPIO writes.
- No relay-expander writes.
- No XBee setting writes, RF/range/throughput/API transmit, or XBee bridge
  forwarding proof.
- No MicroSD or TFT action.
- No relay/load/mains action.
- No erase.
- No wiring mutation, commit, or push.

## Decision Footer

- Decision: blocked for PF0530F live menu acceptance.
- Next gate: diagnose `LCD_INIT_FAILED` before another PF0530F live menu proof
  attempt.
- Owner: Firmware with Hardware and QA; Live Bench for any future COM6 gate.
- Evidence: COM6 identity, rollback backup/hash, recovery command, artifact
  hashes, write-flash log, verify-flash log, monitor transcript, transcript
  scan, cleanup proof, and manifest in the evidence directory above.
- Approved mutation boundary used: COM6-only PF0530F write/verify and read-only
  UART0 monitor.
- Authority limits: no further flash, monitor, serial write, XBee/RF,
  relay/load/mains, relay GPIO write, relay-expander write, MicroSD/TFT, erase,
  wiring mutation, commit, or push without a new explicit gate.
