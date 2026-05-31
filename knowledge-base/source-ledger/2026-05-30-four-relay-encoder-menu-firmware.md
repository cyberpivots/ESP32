# Source Ledger - 2026-05-30 Four Relay Encoder Menu Firmware

## Scope

Tier 2 firmware/docs/audit preparation plus Tier 3 COM6-only write/verify for
replacing the auto-cycling LCD test pages with an input-only rotary encoder LCD
menu on `four-relay-xbee-wifi`. User-observed LCD/encoder acceptance remains
pending after the write/verify gate.

## Sources

- Accepted COM6 XBee bridge proof:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Accepted LCD display-status proof:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- Previous encoder menu planning record:
  `SRC-LOCAL-FOUR-RELAY-ROTARY-ENCODER-MENU-PLAN-2026-05-30`.
- ESP-IDF GPIO, UART, and I2C API context: `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-I2C`.

## Verified Facts

- Firmware preserves UART0 host `115200`, UART2 XBee `9600`, TX GPIO17, RX
  GPIO16, no hardware flow control, and app logging disabled after startup.
- Firmware preserves LCD I2C0 GPIO21/GPIO22 at 100 kHz and PCF8574/PCF8574A
  candidate-address probing.
- Firmware defines `FR_ENCODER_CLK_GPIO GPIO_NUM_34`,
  `FR_ENCODER_DT_GPIO GPIO_NUM_35`, and `FR_ENCODER_SW_GPIO GPIO_NUM_36`.
- Encoder GPIOs are configured input-only with internal pullups and pulldowns
  disabled.
- Menu polling is 1 ms, quadrature requires four valid transitions per menu
  step, switch debounce is 30 ms, and long press threshold is 800 ms.
- Relay pages are locked UI text only and show no relay output state change.
- Firmware does not add relay GPIO writes, relay expander writes, XBee setting
  strings, Wi-Fi start, storage mounting, erase, flash, or monitor behavior.
- Same-session user confirmation recorded COM6 available, LCD visible on
  GPIO21/GPIO22, encoder wired CLK=34, DT=35, SW=36, `+`=3V3, GND=GND with SW
  capacitor, relay/load/mains disconnected, and explicit COM6 flash authority.
- COM6 identity was recorded as a Silicon Labs CP210x USB to UART Bridge
  (VID_10C4/PID_EA60) connected to ESP32-D0WDQ6 revision v1.0, MAC
  `78:e3:6d:0a:90:14`, with 4 MB flash and 3.3 V flash voltage.
- COM6-only write-flash and a separate COM6-only verify-flash passed for the
  encoder-menu bootloader, partition table, and app image.

## Assumptions

- Direction reversal is not a blocker for the first live proof.
- Encoder module or external pullups hold all encoder lines in the ESP32 3.3 V
  domain; firmware intentionally does not enable internal pullups on GPIO34-36.
- Direction reversal is not a blocker for the first live proof.

## Unknowns

- Exact encoder/module identity, onboard pullup values, PPR/detents, switch
  bounce, rail-current impact, rotation direction, and boot behavior remain
  unresolved until live proof.
- User-observed LCD/encoder acceptance remains pending after write/verify.

## Local Reviewer Quorum

- Coordinator/architecture-risk lens, weight 5: approves Tier 2 mutation only;
  Tier 3 flash remains closed.
- Firmware lens, weight 3: approves input-only GPIO reads and menu rendering
  while preserving bridge/LCD behavior.
- Hardware lens, weight 3: approves only the recorded wiring assumption and
  unresolved-gap wording; live electrical acceptance remains pending.
- Communications lens, weight 3: approves because firmware does not parse or
  generate XBee commands/settings.
- QA lens, weight 3: approves source/task/status records plus pre-flash static
  validation before any live gate.

Weighted local decision: approved for Tier 2 repo mutation, no P1/P2 blockers
for the named boundary. No subagents were spawned because the available
delegation tool requires explicit subagent authorization.

Live Tier 3 continuation used local reviewer lenses only; no subagents were
spawned because no safe delegation tool was available in this session. Weighted
local decision: 19/19 approved for the named COM6 encoder-menu write/verify
gate after same-session facts, rollback backups, recovery path, and explicit
authority were recorded; no P1/P2 blockers.

## Validation Plan

- Host safe-core tests.
- Firmware, documentation, source, and agent-process audits.
- Scaffold audit unit tests.
- `scripts/verify_scaffold.py`.
- `git diff --check`.
- ESP-IDF v6.0.1 no-flash build when the local toolchain is available.

## Validation Results

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-encoder-menu-build build`

The ESP-IDF build generated
`/tmp/esp32-four-relay-xbee-wifi-encoder-menu-build/four_relay_xbee_wifi.bin`
and did not run flash or monitor.

Live COM6 gate evidence directory:

- `research/bench-records/xbee-readonly/local-encoder-menu-flash-20260530T053004Z/`

Live gate passed:

- COM6 Windows inventory and esptool flash identity.
- 2 MB rollback backup SHA-256:
  `b64b69d1f2ce3ff5dd3f5fbb6b4c0576a00e0c62f73433cfe70c6c5dbbeb88cc`.
- 4 MB rollback backup SHA-256:
  `d0e193b60e8184d13a26cd008fb6c70789b7869a5fea1adff1ead7c5151511f0`.
- Artifact hashes in `build-artifacts.sha256`.
- COM6-only write-flash with esptool per-segment hash verification.
- Separate COM6-only verify-flash with digest matches for all images.
- Evidence manifest hash:
  `6ca4dd24c74811b25bbbc107614ecc9eafaffe1ce337d85ac23197064b1e613e`.

## Closed Surfaces

- No further COM6 flash or verify without a fresh Tier 3 live gate.
- No serial monitor, XBee local-AT, RF link probe, range, throughput, relay,
  load, or mains test.
- No relay GPIO writes, relay expander writes, XBee setting writes, Wi-Fi,
  storage, erase, or persistent configuration writes.
