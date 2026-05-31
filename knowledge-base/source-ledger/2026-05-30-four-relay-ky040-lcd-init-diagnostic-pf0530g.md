# Source Ledger - 2026-05-30 Four Relay KY-040 PF0530G LCD Init Diagnostic

## Verified Facts

- PF0530F COM6 flash/verify passed, but the read-only monitor captured
  `PF0530F LCD_INIT_FAILED` and no `MENU_HB`, `MENU_STEP`, or `MENU_SELECT`
  proof.
- User confirmed same-session safe state, live flash authority, and LCD
  connected as before for the PF0530G diagnosis gate.
- PF0530G keeps the diagnostic XBee bridge closed and uses I2C0 GPIO21/GPIO22
  at 100 kHz with internal pullups disabled.
- PF0530G emits stage-specific serial proof for bus creation, PCF8574/PCF8574A
  probe ranges, device add, HD44780 init steps, final init status, and
  periodic diagnostic heartbeats.
- The COM6 live gate evidence is under
  `research/bench-records/xbee-readonly/local-ky040-pf0530g-lcd-init-diag-live-20260530T223218Z/`.
- COM6 identity matched ESP32-D0WDQ6 MAC `78:e3:6d:0a:90:14`, detected 4 MB
  flash, and a 3.3 V flash-voltage strap.
- The 4 MB pre-flash rollback image is
  `com6-pre-pf0530g-lcd-init-diag-4mb.bin`, size `4194304`, SHA256
  `b60f8ac3951ce333d9d1a4d318beef1fd57419374fe1ae77b07fd8e34a79c546`.
- The staged PF0530G app image SHA256 is
  `85839de510dc167f703950fc1501d8309bb844e1b76d90a3cea95b054781cbaa`.
- PF0530G write-flash succeeded, and separate verify-flash matched bootloader,
  partition table, and app digests.
- The read-only monitor recorded `writes_sent=false`, exactly one LCD probe ACK
  at `0x27`, `LCD_PROBE_SUMMARY count=1 selected=0x27`,
  `LCD_DEVICE result=ok addr=0x27`, all nine HD44780 init steps as ok,
  `LCD_INIT_OK addr=0x27`, and 15 `LCD_DIAG_HB status=ok` lines.
- Transcript scan recorded `acceptance=lcd_diag_pass`,
  `crash_fault_marker_count=0`, and `closed_surface_violation_count=0`.

## Assumptions

- COM6 remains the intended ESP32 target until identity evidence proves
  otherwise.
- The LCD remains on the previously accepted GPIO21/GPIO22 level-shifter and
  common-ground path.
- The LCD is HD44780-compatible with a PCF8574/PCF8574A-class backpack using
  the prior P0/P1/P2/P3/P4-P7 mapping.

## Unknowns

- Exact LCD module/backpack IC, pullup voltage, contrast, backlight current,
  rail-current margin, and physical LCD visual state.
- Why PF0530F emitted `LCD_INIT_FAILED` while the PF0530G diagnostic path
  completed LCD init successfully.
- Whether the later encoder menu proof will work after LCD init is diagnosed.

## Closed Surfaces

- No encoder menu acceptance in this gate.
- No relay GPIO writes or relay-expander writes.
- No XBee setting writes, RF/range/throughput/API transmit, or XBee bridge
  forwarding proof.
- No MicroSD or TFT action.
- No relay/load/mains action.
- No erase, wiring mutation, commit, or push.

## Decision Footer

- Decision: PF0530G serial LCD init diagnosis passed.
- Next gate: separate renewed encoder menu proof only after fresh authority and
  scope confirmation.
- Owner: Firmware with Hardware, QA, Evidence Records, and Live Bench lenses.
- Approved mutation boundary completed: PF0530G LCD init diagnostic
  source/records and named COM6-only write/verify plus read-only UART0
  monitor.
- Authority limits: no encoder menu proof, XBee/RF, relay/load/mains,
  relay GPIO write, relay-expander write, MicroSD/TFT, erase, wiring mutation,
  commit, or push.
