# Tier 3 COM6 Attended Interaction Proof Ledger

Source ID:
`SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31`

## Verified Facts

- The proof was run after explicit user Tier 3 COM6 attended interaction
  authority and safe-state confirmation.
- The previous PF0530L rollback record remained available at
  `<redacted-local-evidence-path>`
  with SHA256
  `<redacted-sha256>`.
- Same-session Windows esptool read-only identity on COM6 passed for
  `chip_id`, `read_mac`, and `flash_id`: ESP32-D0WDQ6 revision v1.0, MAC
  `<redacted-mac>`, detected 4 MB flash, 40 MHz crystal, and 3.3 V flash
  strap.
- WSL `/dev/ttyS6` pyserial monitor setup failed with an input/output error;
  the accepted transcript artifact for this proof is the Windows COM6 pyserial
  monitor, not the failed WSL attempt.
- The initial Windows COM6 monitor ran for 90 seconds at 115200 baud with
  `writes_sent=false`, captured 23,667 bytes, and saved transcript plus raw
  byte artifacts.
- The initial transcript scan counted 45 `BBS_MENU_HB`, 45 `BBS_LCD_RENDER`,
  and 45 `BBS_CURSOR` lines. It found zero watchdog, backtrace, panic,
  LCD-init-failure, `unsafe-open`, `UNSAFE_OPEN`, or
  `FR_DIAG_XBEE_BRIDGE_OPEN` markers, but zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero input-event lines.
- The user reported missing the initial start cue and requested a restarted
  attended proof.
- The retry COM6 identity checks passed for `chip_id`, `read_mac`, and
  `flash_id`.
- The retry Windows COM6 monitor ran for 120 seconds at 115200 baud with
  `writes_sent=false`, captured 137,059 bytes and 3,445 metadata-counted lines,
  and saved transcript plus raw byte artifacts.
- The retry transcript scan counted 768 `ENC_RAW`, 456 `ENC_EV`, six
  `BBS_MENU_STEP`, 11 `BBS_MENU_SELECT`, seven `BBS_MENU_AUTO`, 59
  `BBS_MENU_HB`, 135 `BBS_LCD_RENDER`, 135 `BBS_CURSOR`, one `LCD_INIT_OK`,
  one `PF0530L BBS_LCD_READY`, and one `BBS_INPUT_READY`.
- The retry transcript included both `BBS_MENU_STEP dir=-` and
  `BBS_MENU_STEP dir=+`, plus `BBS_MENU_SELECT kind=short` and
  `BBS_MENU_SELECT kind=long`.
- The retry scan found zero watchdog, backtrace, panic, LCD-init-failure,
  `unsafe-open`, `UNSAFE_OPEN`, or `FR_DIAG_XBEE_BRIDGE_OPEN` markers, so the
  serial/menu physical interaction proof is accepted on retry.
- Cleanup proof found zero lingering monitor/esptool/idf.py processes after
  the retry run.

## Assumptions

- The retry capture reflects the user's physical encoder/button actions during
  the attended 120 second window.
- Heartbeat cumulative counters are not treated as fresh physical interaction
  proof without timestamped event lines in the attended transcript.

## Unknowns

- Physical LCD/glyph readability, custom glyph appearance, encoder direction,
  switch behavior, rail-current margin, LCD backpack pullup voltage, and
  boot-held switch behavior remain unaccepted.
- Hardware/electrical acceptance still needs continuity, idle/toggle levels,
  pullup behavior, and rail-current evidence.

## Evidence

- Evidence directory:
  `<redacted-local-evidence-path>`
- Identity summary:
  `<redacted-local-evidence-path>`
- Windows monitor metadata:
  `<redacted-local-evidence-path>`
- Windows monitor transcript:
  `<redacted-local-evidence-path>`
- Transcript scan:
  `<redacted-local-evidence-path>`
- Cleanup proof:
  `<redacted-local-evidence-path>`
- SHA256 manifest:
  `<redacted-local-evidence-path>`
- Retry evidence directory:
  `<redacted-local-evidence-path>`
- Retry transcript scan:
  `<redacted-local-evidence-path>`
- Retry SHA256 manifest:
  `<redacted-local-evidence-path>`

## Authority Limits

This record proves only COM6 read-only identity, read-only attended monitor
capture, and serial/menu physical interaction on PF0530L. It does not
authorize or prove flashing, erase, serial writes, XBee/RF transmit, XBee
setting writes, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
wiring mutation, MicroSD/TFT action, relay/load/mains work, persistent
configuration writes, credential access, external service changes, GitHub
publication, release gates, LCD visual acceptance, electrical acceptance, or
hardware acceptance.
