# Task 0099 - Four Relay Encoder Menu Firmware

## Task

- ID: 0099
- Owner role: Firmware with Hardware, Communications, QA, and Agent Operations
  lenses
- Status: Tier 3 COM6 write/verify complete; user visual acceptance pending
- Created: 2026-05-30
- Updated: 2026-05-30

## Triage

- Verified facts: accepted COM6 bridge uses UART0 host `115200`, UART2 XBee
  `9600`, GPIO17/GPIO16, no app logging after startup. Source ID:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Verified facts: accepted LCD proof uses I2C0 GPIO21/GPIO22 and a
  PCF8574/PCF8574A-class LCD page renderer. Source ID:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- Verified facts: ESP-IDF GPIO source coverage exists for input-only pins and
  GPIO API context. Source ID: `SRC-ESP-IDF-GPIO`.
- Verified facts: same-session user confirmation recorded COM6 available, LCD
  visible on GPIO21/GPIO22, encoder wired CLK=34, DT=35, SW=36, `+`=3V3,
  GND=GND with SW capacitor, relay/load/mains disconnected, and explicit COM6
  flash authority.
- Assumptions: direction reversal is not a blocker for first proof.
- Unknowns: exact encoder/module identity, pullup values, boot behavior, rail
  margin, switch bounce, rotation direction, and user-observed LCD/encoder
  acceptance after write/verify.
- Selected tier: Tier 2 for firmware/docs/audit/source/task mutation; Tier 3
  for any COM6 flash or live proof.
- Owner role: Firmware.
- Evidence need: source-index-backed ESP-IDF facts, local source ledger, task
  record, pre-flash static/build validation, and same-session live evidence
  before flash.
- Mutation boundary: `main.c`, firmware CMake dependency, audit allowlists,
  firmware/project docs, source/status/index/task records. No live hardware
  mutation in this step.
- Validation plan: host/static checks, scaffold audit unit tests, verifier,
  `git diff --check`, and ESP-IDF no-flash build if available.

## Scope

Included:

- Input-only encoder polling on GPIO34/GPIO35/GPIO36.
- LCD menu pages 0 through 7.
- Relay pages as locked UI text only.
- XBee bridge counters on the menu without parsing or generating XBee commands.
- Firmware audit updates allowing encoder reads while preserving output/write
  bans.

Excluded:

- Relay GPIO writes or relay expander writes.
- XBee setting strings/commands, RF tests, range, or throughput.
- Serial monitor.
- Wi-Fi, storage, erase, relay/load/mains expansion.
- Any COM6 action beyond the named encoder-menu write/verify gate.

## Implementation

- Replaced LCD auto-cycling pages with encoder-driven menu rendering.
- Added `driver/gpio.h` and `esp_driver_gpio`.
- Configured GPIO34, GPIO35, and GPIO36 input-only with internal pullups and
  pulldowns disabled.
- Added 1 ms polling, quadrature transition decoding, 4-transition menu steps,
  30 ms switch debounce, 800 ms long-press return to status, short-press
  `SELECT BLOCKED` or `SELECT ACK`, and an encoder test page with position and
  button count.

## Reviewer Quorum

Local read-only lenses only; no subagents were spawned because the available
delegation tool requires explicit user authorization for subagents.

- Coordinator/architecture-risk, weight 5: approve Tier 2 boundary only.
- Firmware, weight 3: approve implementation boundary.
- Hardware, weight 3: approve unresolved-gap wording and live-gate stop.
- Communications, weight 3: approve no XBee command generation.
- QA, weight 3: approve validation plan and task/source records.

Weighted approval: 17/17 for Tier 2 mutation, no P1/P2 blockers.

Live Tier 3 continuation used local reviewer lenses only; no subagents were
spawned because no safe delegation tool was available in this session.

- Coordinator/architecture-risk, weight 5: approve COM6-only write/verify after
  same-session facts, rollback, and authority.
- Firmware, weight 3: approve generated ESP-IDF artifacts and offsets.
- Hardware, weight 3: approve only the disconnected relay/load/mains and
  input-only encoder boundary.
- Communications, weight 3: approve no XBee local-AT, RF probe, or setting
  writes.
- QA/tooling, weight 5: approve pre-flash validation, backup hashes, write-flash,
  verify-flash, and evidence manifest.

Weighted approval: 19/19 for the named COM6 encoder-menu write/verify gate, no
P1/P2 blockers.

## Live Gate Results

Evidence directory:

- `research/bench-records/xbee-readonly/local-encoder-menu-flash-20260530T053004Z/`

Recorded before COM6 flash:

- COM6 available and selected as the only target.
- LCD connected and visible on GPIO21/GPIO22.
- Encoder connected as CLK=34, DT=35, SW=36, `+`=3V3, GND=GND, with 100 nF
  SW-to-GND.
- Relay/load/mains disconnected.
- Rollback backup hashes and recovery path.
- Generated ESP-IDF flash arguments for COM6 only.

Recorded identity and rollback:

- Windows inventory: Silicon Labs CP210x USB to UART Bridge (COM6),
  VID_10C4/PID_EA60.
- esptool identity: ESP32-D0WDQ6 revision v1.0, MAC `78:e3:6d:0a:90:14`, 4 MB
  flash, 3.3 V flash voltage.
- 2 MB rollback backup SHA-256:
  `b64b69d1f2ce3ff5dd3f5fbb6b4c0576a00e0c62f73433cfe70c6c5dbbeb88cc`.
- 4 MB rollback backup SHA-256:
  `d0e193b60e8184d13a26cd008fb6c70789b7869a5fea1adff1ead7c5151511f0`.

Write/verify result:

- COM6-only write-flash completed for bootloader at `0x1000`, partition table at
  `0x8000`, and app at `0x10000`; esptool reported hash verification for all
  written segments.
- Separate COM6-only `verify-flash` completed with digest matches for all three
  images.
- Evidence manifest: `evidence-manifest.md`, hash
  `6ca4dd24c74811b25bbbc107614ecc9eafaffe1ce337d85ac23197064b1e613e`.

Do not run serial monitor, XBee local-AT, RF link probe, range/throughput,
relay, load, or mains tests under this gate. User visual LCD/encoder acceptance
is still pending.

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

No flash, verify-flash, serial monitor, XBee/RF, relay, load, or mains command
was run during this Tier 2 preparation.
