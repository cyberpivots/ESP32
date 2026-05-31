# Known Gaps

## High priority

- Use [development-status-ledger.md](development-status-ledger.md) as the
  current canonical status record. Historical blocked task logs and handoffs
  remain historical; the structured Gate H live acceptance and Gate G
  local-admin export records supersede earlier blocked Gate H and simulator-only
  analytics status where noted.
- Confirm exact firmware framework requirements and constraints for projects not
  covered by ADR-0002.
- Keep ESP-IDF v6.0.1 activation evidence current for
  `four-relay-xbee-wifi`: the 2026-05-21 cycle installed and built the
  disabled skeleton, but `idf.py` still requires sourcing the local activation
  script and OpenOCD udev rules were not installed without elevated
  permissions.
- Identify exact photographed ESP32 development board vendor/revision, USB-UART
  bridge, regulator, expansion-shield schematic, jumper position, and GPIO
  continuity for `four-relay-xbee-wifi`.
- Define source-backed power-entry/protection requirements for
  `four-relay-xbee-wifi`: single selected input source, rail budget, current
  limit, brownout behavior, reverse-protection need, overcurrent protection,
  TVS/ESD placement, and test points.
- Identify exact four-channel relay module manufacturer/model, input voltage,
  trigger polarity, 3.3 V compatibility, `JD-VCC`/`VCC` behavior, isolation
  method, coil/load ratings, and current requirements.
- Close or explicitly block the relay direct-GPIO 3.3 V/current gate for
  `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`.
- Verify the exact Open-Smart R61509V TFT module, pinout, power/backlight,
  touch interface, driver path, and conflict with relay, MicroSD, XBee, ADC,
  boot, flash, and UART0 pins.
- Verify exact CD74HC4067 breakout, select/enable wiring, ADC1 input path,
  voltage protection, source impedance, and input-only scan behavior.
- Select and verify exact MCP23017 or TCA9555 expander board, I2C address pins,
  pullups, inactive defaults, output latch behavior, and readback policy.
- Select a relay driver stage only after exact relay-module trigger polarity,
  input current, voltage compatibility, and isolation behavior are verified.
- Confirm Heltec WiFi LoRa 32(V2) physical revision and radio chip variant.
- Verify Waveshare XBee USB Adapter serial port, UART voltage, DIN/DOUT routing,
  and whether it is only a PC dock or also a possible ESP32-mounted carrier.
- Run the XBee read-only bench proof Tier A, then optionally Tier B with
  `--confirm-sends-read-commands`, to capture `VR`, `HV`, `SH`, `SL`, `AP`,
  `AO`, `BD`, and `NP` without setting writes.
- Fresh two-device XBee/XCTU Stage A1/A2 no-serial evidence is recorded under
  `SRC-LOCAL-XBEE-TWO-DEVICE-READONLY-STUDY-2026-05-29`, including one
  local-only candidate removal delta after the first physical disconnect. Exact
  two-adapter identity remains open until the second adapter delta, adapter
  markings, antenna state, and isolation notes are recorded.
- Corrected ESP32/XBee evidence is recorded under
  `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`: `COM6` is
  the ESP32 serial target and `COM15` is the healthy XBee peer, but `COM6` did
  not expose XBee API frames before the bridge firmware. The bridge
  implementation is recorded under
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`; the named COM6
  bridge flash/retest gate now has same-session wiring/no-load confirmation,
  rollback backups, artifact hashes, COM6-only flash output, redacted bridge
  local-AT readback, and corrected bidirectional benign `link_probe` proof.
- Four-relay LCD I2C test firmware and COM6-only write/verify evidence are
  recorded under `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`. The
  mutation preserves the COM6 bridge and assumes one 20x4
  HD44780/PCF8574-class LCD on GPIO21/GPIO22, but exact LCD identity, pullup
  voltage, logic voltage, exact detected address value, contrast, backlight
  current, and rail-current margin remain open. User visual proof passed for
  page cycling, detected-address line display, and clean four-row rendering. No
  monitor, XBee/RF, relay/load/mains, encoder, or future flash authority is
  opened by that record.
- The four-relay rotary encoder LCD menu plan is recorded under
  `SRC-LOCAL-FOUR-RELAY-ROTARY-ENCODER-MENU-PLAN-2026-05-30`. It keeps
  GPIO21/GPIO22 reserved for the LCD, GPIO17/GPIO16 reserved for the XBee
  bridge, and GPIO25/GPIO26/GPIO27/GPIO33 reserved as relay candidates. Exact
  encoder/module identity, pinout, PPR/detents, switch option, pullups,
  voltage, debounce/noise behavior, header continuity, rail-current impact,
  and boot behavior remain open. No final pin assignment, wiring, firmware,
  flash, serial/RF action, relay/load/mains work, or live encoder proof is
  authorized.
- The four-relay encoder LCD menu firmware is prepared under
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`. It assigns
  GPIO34/GPIO35/GPIO36 as input-only encoder lines for the user-selected COM6
  menu gate and keeps relay pages as locked UI text only. The named COM6
  write/verify gate recorded same-session facts, rollback backup hashes, COM6
  artifact write-flash, and separate verify-flash. Exact encoder/module
  identity, pullup values, rail-current impact, rotation direction, boot
  behavior, and user-observed live LCD/encoder proof remain open. No further
  flash, monitor, XBee/RF action, relay/load/mains work, or hardware acceptance
  is authorized by this record.
- The four-relay encoder raw diagnostics firmware preparation is recorded
  under `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`. It changes
  LCD page 0 to show raw GPIO34/GPIO35/GPIO13 `A/B/SW` levels plus raw A/B and
  SW transition counters after the user reported GPIO36 is not exposed,
  preserving the COM6 bridge, LCD path, locked relay UI text, and no
  XBee/RF/relay/load/mains behavior. The named COM6-only GPIO13
  backup/write/verify gate is recorded; user LCD raw observation, monitor,
  hardware acceptance, and future flash gates remain closed.
- The four-relay KY-040 diagnostic refactor is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`. It records the
  user-identified ASIN `B06XQTHDRR` as a Cylewet KY-040 branch using an
  independent Manuals+ mirror, keeps GPIO34/GPIO35 internal pulls disabled,
  enables only the GPIO13 internal pullup for active-low `SW`, and records the
  user-observed raw LCD no-change symptom as hardware/electrical/pinout-first.
  The later same-session COM6 user-test flash recorded safe-state authority,
  refreshed validation, COM6 identity, rollback backups, artifact hashes,
  recovery command, write-flash, and separate verify-flash. LCD raw proof,
  serial monitor, XBee/RF, relay/load/mains, hardware acceptance, decoder
  changes, and future live gates remain closed.
- The four-relay KY-040 pin-finder diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`. It adds
  firmware ID `PF0530A`, keeps the raw page, and adds input-only level/count
  probes for GPIO34/GPIO35/GPIO13/GPIO14/GPIO32/GPIO33. The image has been
  written/verified to COM6; the user reported only pin 34 was displayed, so
  lower-row pin-finder evidence was not usable without encoder navigation.
- The four-relay KY-040 row-0 diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`. It adds firmware
  ID `PF0530B` and cycles raw levels, transition counts, and each candidate
  GPIO level/count on LCD row 0 after the user reported only pin 34 was
  displayed on `PF0530A`. The image was later written/verified to COM6 and
  the user reported no displayed pins changed.
- The four-relay KY-040 GPIO sweep contact tracer is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`. It adds
  firmware ID `PF0530C`, locks the LCD to page 0, shows row-0 `HIT` on any
  watched GPIO change, sweeps GPIO34/GPIO35/GPIO36/GPIO39/GPIO13/GPIO14/
  GPIO18/GPIO19/GPIO23/GPIO32, enables internal pullups only on GPIO13/GPIO14,
  excludes flash/LCD/UART0/XBee/strapping-risk/relay-candidate pins, and
  closes the diagnostic XBee bridge loop. A later same-session COM6 gate
  recorded safe-state authority, refreshed validation, identity, rollback,
  hashes, recovery command, write-flash, and separate verify-flash. User LCD
  observation remains pending.
- The four-relay KY-040 DevKitC 13/14/32 diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`. It adds
  firmware ID `PF0530D` for the user-confirmed GPIO13/GPIO14/GPIO32 wiring,
  enables internal pullups on all three pins, locks LCD page 0, shows raw
  levels, transition/position/button counts, and per-pin `HIT` changes, and
  keeps the diagnostic XBee bridge loop closed. It has been written and
  separately verify-flashed to COM6. User LCD observation and hardware
  acceptance remain pending.
- The four-relay KY-040 serial pintrace diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`. It adds
  firmware ID `PF0530E`, watches a DevKitC candidate GPIO set as input-only,
  enables internal pullups only on GPIO13/GPIO14/GPIO32, prints COM6/UART0
  stable change events and periodic summaries, warns that DevKitC physical
  `J2-13` is `IO12` and `J2-14` is `GND`, and closes the diagnostic XBee
  bridge loop. The r4 COM6 write/verify and 10-minute read-only monitor
  completed without watchdog/backtrace lines and without encoder-pin `EV`
  events. The later r5 read-only monitor recorded user-confirmed actuation with
  GPIO13/GPIO14/GPIO32 count increases, `writes_sent=false`, and no watchdog,
  panic, or backtrace scan hits. Hardware acceptance remains pending.
- The four-relay KY-040 encoder menu PF0530F repo update is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`. It changes the
  current diagnostic image to LCD menu proof on GPIO13/GPIO14/GPIO32 with
  input-only pullups, XBee bridge forwarding closed, A/B debounce, switch
  debounce and guard suppression, invalid-transition counting, and serial
  `MENU_*` proof lines. A later user-authorized live attempt under
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30` flashed
  and separately verify-flashed PF0530F on COM6, captured `PF0530F MENU_READY`,
  then captured `PF0530F LCD_INIT_FAILED` with no `MENU_HB`, `MENU_STEP`, or
  `MENU_SELECT` proof. Live menu acceptance, relay/load/mains, XBee/RF,
  hardware acceptance, final pin reassignment, and any further flash or monitor
  action remain closed.
- The PF0530G LCD init diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`. It keeps the
  XBee bridge closed, uses GPIO21/GPIO22 I2C only, and emits stage-specific
  `LCD_*` serial proof lines. The COM6 live gate passed serial LCD init
  diagnosis with one ACK at `0x27`, all HD44780 steps ok, and
  `LCD_INIT_OK addr=0x27`; physical LCD visual confirmation and another
  encoder menu proof remain separate.
- PF0530H source is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`. It combines
  the PF0530G LCD init path with PF0530F GPIO13/GPIO14/GPIO32 input-only menu
  handling and static/simulated BBS pages.
- PF0530H live flash/verify/read-only monitor is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`. Physical
  LCD visual confirmation, encoder direction, `BBS_MENU_STEP`, and
  `BBS_MENU_SELECT` remain user-test evidence items.
- XCTU host install evidence is recorded, but live XCTU behavior remains
  blocked. Complete XBee Studio host evidence separately if it becomes the
  selected GUI, and do not rely on GUI discovery until exact ports, physical
  isolation, voltage/carrier evidence, recovery, and cleanup criteria are
  recorded.
- Identify the SPI MicroSD reader module, 3.3 V power path, pull-ups,
  card-detect/write-protect behavior, and shield continuity for candidate
  `GPIO18`, `GPIO19`, `GPIO23`, and `GPIO32` before any storage wiring.
- Define MicroSD card capacity, FAT preparation process, low-space behavior,
  log rotation, and fallback web-serving behavior for
  `four-relay-xbee-wifi`.
- Inventory required bench instruments and fixtures for `four-relay-xbee-wifi`:
  DMM, current-limited supply, logic analyzer or LED proof fixture, USB serial
  tools, labeled harnesses, low-voltage dummy loads, and completed records
  based on `research/bench-records/TEMPLATE.md`.
- Create a separate qualified-review package before any mains switching design:
  load type, enclosure, overcurrent protection, grounding/bonding, strain
  relief, GFCI/de-energization, separation, labels/disconnect, and test record.
- Define first flashing target board and recovery method.
- Incorporate the Windows COM6 DevKitC-class board into the hardware evidence
  package: local DOS-C evidence identifies ESP32-D0WDQ6 MAC
  `78:e3:6d:10:4d:6c` behind a CP210x bridge, but this workspace still needs
  physical carrier-board inspection before pin or flashing decisions.
- Complete DOSBox-X SLIRP proof from the Windows 3.1 operator console to the
  simulator at `10.0.2.2:31331`; current bridge proof is host-side protocol
  tests only.
- ESP-NOW BBS lane now has a project-local ESP-IDF v6.0.1 ADR, accepted
  coordinator USB serial proof, encrypted one-peer firmware/bridge/OPCON
  implementation, Windows COM6 peer identity/backup/flash/send-loop proof,
  accepted live encrypted one-coordinator/one-peer RX/TX/ACK OPCON proof, and
  accepted 2026-05-23 USB-only three-peer live completion evidence.
- ESP-NOW BBS three-peer live gate tooling exists for COM4/COM5/COM6 and Pi
  `/dev/ttyUSB0`. The 2026-05-23 run first stopped at coordinator full-flash
  backup due a Pi-side esptool CRC/checksum error, then completed after the
  gate switched coordinator backup/flash to the proven Pi esptool venv/stub
  runtime, translated Windows peer artifact paths, resolved activated ESP-IDF
  `idf.py`, and isolated per-role `SDKCONFIG`. Corrected evidence records
  complete backups, manifest, flash/verify, three `espnow-enc` peers, moving
  RX/TX/ACK counters, Win31 runtime captures, and cleanup.
- Custom wireless protocol Gate B and Gate C now have simulator-only proof for
  direct messages, file chunks, interval telemetry, node status, custody ACKs,
  duplicate suppression, TTL, compact reporting, non-executing control intents,
  compact simulated bridge-request translation, Gate D DOS-C fixture replay
  through the ESP32 Gate C adapter, a Gate E draft bridge ABI freeze candidate,
  and Gate G simulator-only analytics report generation. A 2026-05-25
  authorized Gate H attempt first stopped at read-only preflight, then passed
  after the Pi/router path was restored at `192.168.137.105` and the current
  `COM9`/`COM6`/`COM7` peer remap matched accepted peer MACs. A later
  structured Gate H live rerun captured `bridge-transcript.jsonl` and passed
  the DOS-C vision gate plus ESP32 completion gate. That Gate H remap is
  historical live-proof lineage; the later LAN DHCP/current-remap record
  identifies the current read-only mapping as Pi `192.168.200.153`,
  `peer01=COM6`, `peer02=COM10`, and `peer03=COM12` without bridge, Win31,
  BBS, prepare, flash, erase, monitor, or radio proof. `ADR-0005` is now
  accepted for local-admin redacted Gate G JSON export only; firmware ABI
  runtime behavior, Win31 export controls, and bridge export request types
  still need separate owner review.
- Gate F firmware ABI has an accepted design contract only. ESP32 now has
  accepted `ADR-0006`,
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`,
  and
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
  plus host-only packet golden vectors in
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`.
  Gate F runtime requirements are accepted only as requirements planning in
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`;
  this sets volatile-only queue/custody/scheduler requirements for a future
  implementation but does not approve firmware runtime code or firmware
  persistence. Phase 5/6 runtime design is accepted only as host simulator work
  in
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`;
  its balanced queue/retry/expiry defaults are not measured firmware memory
  budgets.
  Do not treat Gate E bridge ABI fixtures, Gate G export policy, Gate H live
  acceptance, the Gate F design contract, or the Gate F runtime requirements as
  firmware runtime implementation approval.
- Gate M1 full-service mesh discovery is accepted only as a host simulator and
  design contract in `ADR-0009` and
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`. It adds
  `mesh_discovery.v1` summaries, service/capability/BLE-Android metadata,
  healing-event shape, 512-byte bridge bounds, and recursive secret-field
  rejection. Gate M2-A adds host-only paired DOS-C bridge/operator support in
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`.
  These gates do not close live ESP-WIFI-MESH, BLE pairing, Android app,
  router/admin, firmware mapping, flash, serial-write, PCAP, or live proof
  gaps.
- The BBS UI System Operation Improvement Program is recorded in
  `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`; UI-0 and M2-B now
  have host-only source/test proof under
  `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`. It still needs M3 firmware
  mapping design review, Client-1 static/simulated browser evidence, copied
  screenshot/OCR/CV corroboration for later UI changes, and a future separate
  Tier 3 Client-2 selected-board read-only Wi-Fi gate before any live client
  proof is accepted.
- Select and verify agricultural telemetry hardware profiles before treating
  center-pivot controllers, soil probes, SDI-12 adapters, Modbus adapters, GPS
  pivot positioning, or GPS asset tracking as implementation targets. Required
  records must include source links, power, voltage, boot-pin, isolation,
  connector, protocol, and calibration/units notes.
- Select and verify all `remote-lcd-xbee-solar-client` hardware before any
  wiring, charging, firmware, or radio work: exact ESP32 board, 20x4 LCD,
  rotary encoder, 18650 cell, BMS/protection board, solar panel, charger/power
  path, XBee carrier, antenna, fuse/protection, and enclosure. Current
  PCF8574/74A, PEC11R, BQ25185, BQ2970, BQ27441-G1, and UL lithium-ion safety
  entries are candidate/reference-only or broad safety context.
- The `remote-lcd-xbee-solar-client` private hardware submodules now exist and
  are docs-only evidence lanes. They do not close exact hardware identity,
  wiring, charging, radio-write, firmware, or live bench gaps.
- The Hardware Rapid Prototyping Program is recorded under
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28` as planning/status only.
  It still needs same-session K1, Kobra 2 Max, CR-30, and CR-Scan Lizard
  identity and condition records; K1 hardened-nozzle physical proof; filament
  SDS and dry-state evidence; ventilation/exposure controls; printer/material
  calibration coupons; CR-30 belt adhesion proof; CR-Scan Lizard
  known-dimension/caliper validation; and lane-specific measurement packets
  before any guide becomes a repeatable build procedure.
- The four-relay low-voltage fixture kit is recorded under
  `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28` with one
  provisional OpenSCAD source and public guide only. It still needs the
  internal workbook to be filled with printer identity, K1 hardened-nozzle
  proof if needed, filament SDS/dry state, ventilation controls, calibration
  coupon, board/relay/XBee/MicroSD/TFT/expander dimensions, and reviewer
  signoff before any live print, fit, or repeatable build claim.
- Define the cross-project client UI live-gate target before implementation:
  selected board, current identity, Wi-Fi mode, browser support matrix, phone
  and laptop proof packet, safety-supervisor state model, authentication,
  monotonic sequence policy, and command-log retention.
- Select and verify the first dummy-output fixture before any live control:
  exact GPIO, boot-pin risk, inactive state, LED or logic-analyzer fixture,
  observation method, all-off behavior, safety-lock rejection, and proof that no
  relay module, load, or mains path is attached.
- Keep BLE, Web Bluetooth, Web Serial, and raw Serial/UART client work blocked
  behind separate live gates for UUIDs, Android permissions, browser support,
  UART framing, pairing/security, coexistence evidence, rollback, and cleanup.
- Resolved on 2026-05-22 for bounded coordinator scope: live Pi USB serial
  visibility, private flash backup, coordinator flash, `hello`/`state`/`diag`
  UART proof, and Windows 3.1 OPCON physical coordinator dashboard proof passed.
  The later encrypted peer proof closed the first peer/channel/key path for one
  coordinator and one peer only.
- Keep PCAP bridge acceptance blocked until Pi identity, wired `eth0`,
  `cap_net_raw` setup, rollback, and redacted packet-capture evidence are
  recorded.

## Medium priority

- Keep project-local hook runtime trust and continuous weighted-agent
  enforcement advisory unless the active Codex runtime reports managed hook
  support. `scripts/agent_process_decision.py` proves packet evaluation only;
  it does not replace same-session evidence or Tier 3 live-gate prerequisites.
- Select first protocol only for lanes that do not already have accepted or
  simulator-proven protocol records; ESP-NOW BBS custom wireless work already
  has Gate B/C/D/E/F/G/H and Gate M1/M2-A records.
- Add a checked-in browser QA script for the public Prototype Build Packet so
  desktop/mobile rendering, decoded WebP dimensions, no console errors, no
  failed same-origin requests, keyboard focus visibility, and no horizontal
  overflow are covered by CI instead of local Playwright review only.
- Add XBee API parser test vectors beyond the current escaped-frame,
  bad-length, truncated-escape, checksum, transmit-status, AT-response, and
  receive-packet payload host vectors.
- Decide whether modular scaffold audits should become a CI matrix job after
  the local-only verifier proves stable.
- Define CI matrix after the firmware framework is selected.

## Next evidence record required

| Blocker | Required evidence record before closure |
| --- | --- |
| Framework requirements outside ADR-0002 | Accepted ADR or explicit unresolved-gap note naming the project and blocked framework decision. |
| ESP-IDF v6.0.1 toolchain | Closed for the disabled skeleton build by `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`; refresh if shell/toolchain state changes. Future flash/JTAG work still needs physical no-load evidence, recovery record, and OpenOCD/udev review. |
| Exact ESP32 board and expansion shield | Physical inspection record with board markings, USB-UART marking, regulator marking, jumper position, continuity notes, and source links where available. |
| Power entry and protection | Bench power record with selected input source, rail measurements, current-limit setting, brownout observation, reverse-protection decision, overcurrent candidate, TVS/ESD candidate, and test points. |
| Four-channel relay module | Module identity record with manufacturer/model markings, input voltage, trigger polarity, 3.3 V input current measurement, `JD-VCC`/`VCC` behavior, isolation notes, and contact-rating source. |
| Direct GPIO relay gate | Low-voltage proof record for `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33` showing no load/mains connection and measured relay-input behavior. |
| Open-Smart R61509V TFT | Module identity and pin-pressure record with exact pinout, supply/backlight requirements, touch interface, driver path, and shared pin-budget impact. |
| CD74HC4067 mux | Breakout identity and input-only scan record with select/enable wiring, ADC1 path, voltage protection, source impedance, and no relay-output claims. |
| MCP23017 or TCA9555 expander | Expander board identity record with address pins, pullups, inactive default, latch/readback behavior, and driver-stage boundary. |
| Relay driver stage | Driver selection record tied to measured relay input polarity, input current, voltage compatibility, and isolation behavior. |
| Heltec WiFi LoRa 32(V2) | Physical revision record with board photos/markings and radio-chip/source confirmation. |
| Waveshare XBee USB Adapter | Adapter/carrier record with serial port, UART voltage, DIN/DOUT routing, and PC-dock versus ESP32-mounted-carrier decision. |
| XBee read-only bench proof | Superseded for user-selected `COM15`/`COM6` identity by `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`; adapter markings, physical isolation, voltage/carrier, antenna, recovery/cleanup evidence, and full one-at-a-time mapping remain useful before any carrier/wiring work. |
| XBee radio programming study | Selected-port programming is complete for `COM15` and `COM6` under `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`, and bidirectional benign OTA `link_probe` proof is complete under `SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`. Corrected evidence later identified `COM6` as the ESP32 target and `COM15` as the peer under `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`; the permanent bridge implementation and accepted COM6 bridge flash/retest are recorded under `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`. Firmware update/recovery beyond the named bridge gate, reset/restore beyond normal flash hard reset, range tests, throughput tests, relay/load/mains work, future XBee setting changes, relay command payloads, and public key/identifier exposure remain separate closed gates. |
| ESP32 XBee UART bridge flash/retest | Named COM6 bridge gate accepted under `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`: physical wiring/no-load confirmation, backups, artifact hashes, COM6-only flash proof, boot-settle/flush, redacted COM6 local-AT readback, COM15 peer readback, and bidirectional benign `link_probe` proof are recorded. Remaining gaps are measured rail-current margin for broader hardware expansion, deployment range/throughput, source address allowlisting integration, antenna/regulatory deployment review, relay command acceptance, load/mains readiness, future XBee setting writes, and public raw identifier exposure. |
| Four-relay rotary encoder menu input | PF0530E r5 under `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30` proved GPIO-level changes on GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` during user-confirmed actuation. PF0530F under `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30` is the LCD menu-proof image; the later COM6 live attempt under `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30` passed write-flash and verify-flash and captured `PF0530F MENU_READY`, but live menu acceptance is blocked by `PF0530F LCD_INIT_FAILED`. PF0530G under `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30` passed serial LCD init diagnosis with `LCD_INIT_OK addr=0x27`. PF0530H source under `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31` prepares the combined BBS LCD menu image, and PF0530H live under `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31` passed COM6 flash/verify/read-only monitor with BBS ready/render/heartbeat proof. Before acceptance, collect `BBS_MENU_STEP` in both directions, `BBS_MENU_SELECT` events, LCD page changes, suppressed button-window A/B noise, physical LCD visual confirmation, power-off silkscreen/continuity from KY-040 `CLK`/`DT`/`SW`, A/B idle high and toggle-low evidence while rotating, SW idle high and pulls-low evidence when pressed, rail-current margin, rotation direction, and boot behavior. |
| MicroSD reader and card policy | Reader identity and card-prep record with 3.3 V path, pullups, card-detect/write-protect behavior, shield continuity, capacity, FAT preparation, low-space handling, rotation, and fallback behavior. |
| Bench instruments and fixtures | Instrument inventory record covering DMM, current-limited supply, logic analyzer or LED proof fixture, USB serial tools, labeled harnesses, low-voltage dummy loads, and calibration/identity notes. |
| Qualified mains package | Qualified-review package for load type, enclosure, overcurrent protection, grounding/bonding, strain relief, GFCI/de-energization, separation, labels/disconnect, and test record. |
| First flashing target board | Flash target and recovery record with exact board, boot/recovery method, toolchain proof, and rollback path. |
| ESP-NOW BBS coordinator/client lane | Closed for the first one-coordinator/one-peer encrypted proof by `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22`. `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23` adds tooling for the three-peer gate, `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23` records the initial coordinator backup CRC/checksum blocker plus the corrected USB-only three-peer live completion with backups, build hashes, flash/verify evidence, three `espnow-enc` peers, moving RX/TX/ACK counters, and cleanup, and `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23` adds a copied-evidence completion gate only. Future evidence is still required for chunked message delivery, provisioning UX, BLE, ESP-WIFI-MESH, any physical wiring beyond USB-only, or any new live acceptance claim. |
| Custom wireless protocol implementation | Gate B simulator proof exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25`, Gate C bridge-adapter proof exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25`, Gate D DOS-C fixture replay exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25`, Gate E draft bridge ABI candidate exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25`, Gate F owner-review design-contract acceptance exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26` and `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`, Gate F host-only packet golden vectors exist in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`, Gate F requirements-only runtime planning exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`, Gate M1 full-service mesh discovery host contract exists in `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, Gate M2-A DOS-C companion bridge/operator support exists in `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`, Gate G simulator-only analytics exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-G-ANALYTICS-2026-05-25`, Gate G live export policy is accepted in `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`, Gate G local-admin redacted export implementation exists in `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`, Gate H live acceptance exists in `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-H-LIVE-ACCEPTANCE-2026-05-25`, the structured transcript shape exists in `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-TRANSCRIPT-2026-05-25`, and structured Gate H live acceptance exists in `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`; future evidence is still required for firmware runtime implementation, firmware persistence, firmware mesh discovery mapping, Win31 export controls, and any live bridge export request type. |
| BBS UI system operation improvement program | UI-0 ranked improvement packet and M2-B host-only Network/Services source proof now exist under `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`; remaining gaps are M3 firmware mapping design review/fixtures only, Client-1 static/simulated or read-only browser proof with screenshots and logs, copied screenshot/OCR/CV corroboration for later UI changes, and future Client-2 Tier 3 selected-board read-only Wi-Fi proof with same-session identity, power/voltage/boot-pin/isolation, recovery, browser evidence, and cleanup. Dummy-output control needs a later explicit GPIO/fixture/no-load/no-relay/no-mains record. |
| Development status review | Current canonical ledger `research/development-status-ledger.md` plus `SRC-LOCAL-ESPNOW-DEVELOPMENT-STATUS-REVIEW-2026-05-26`; use it to classify planned lanes and superseded blocked evidence without rewriting historical task records. |
| Agricultural telemetry hardware profiles | Source-backed records for selected center-pivot controller, soil probes, SDI-12/Modbus adapter, GPS pivot positioning device, GPS asset tracker, power/voltage/isolation limits, connector pinout, protocol, calibration, units, and live-proof plan. |
| Remote LCD XBee solar client private submodules | Seven private docs-only submodule repos exist under `submodules/hardware/`, but closure still requires exact vendor sources and physical inspection records for ESP32 board, 20x4 LCD/backpack, rotary encoder, 18650 cell, BMS/protection board, solar panel, charger/power path, XBee carrier, antenna, fuse/protection, and enclosure; include power, voltage, boot-pin, isolation, charge/current limit, pullup, and recovery notes before any bench action. |
| Hardware rapid prototyping and CAD | Same-session printer/scanner inventory for K1, Kobra 2 Max, CR-30, and CR-Scan Lizard; K1 hardened-nozzle physical proof; ventilation/exposure record aligned with `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`; filament SDS and dry-state/humidity records; material/printer calibration coupons; CR-30 belt adhesion and slicer-angle proof; CR-Scan Lizard scan-to-caliper/known-dimension validation; CAD source/export packet; and lane-specific measurement packets before any nontechnical build guide is treated as repeatable. |
| Four-relay low-voltage fixture kit | Complete the internal workbook with printer identity, K1 hardened-nozzle proof if needed, filament SDS and dry-state/humidity records, ventilation controls, calibration coupon, board/relay/XBee/MicroSD/TFT/expander dimensions, cable-tie and label-zone review, public-bundle exclusion proof for workbook/CAD, and reviewer signoff before live print, fit, or repeatable guide acceptance. |
| Cross-project client UI live gate | Stage 1 static or simulated phone/laptop UI proof; Stage 2 selected-board Wi-Fi read-only proof with identity, power, voltage, boot-pin, isolation, recovery, browser screenshot, and cleanup evidence; Stage 3 exact dummy-output GPIO/fixture proof with no relay/load/mains path, sequence logs, all-off, safety-lock rejection, and observed dummy output. |
| DOS-C Windows 3.1 TCP bridge | SLIRP acceptance record showing guest ICMP/TCP path to the Pi simulator and operator-console state proof, with generated screenshots and captures kept out of Git. |
| DOSBox-X PCAP bridge | Pi identity record, wired `eth0` evidence, capability setup and restore evidence, redacted packet-flow proof, and rollback result. |

## Closure criteria

Each gap closes only when supported by a source-index entry, physical inspection
record, ADR, or test artifact.
