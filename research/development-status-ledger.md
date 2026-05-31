# Development Status Ledger

Source index: [../knowledge-base/source-index.md](../knowledge-base/source-index.md)

Date: 2026-05-30

This is the canonical planning-status ledger for the ESP32 workspace, with
paired DOS-C evidence included only where ESP32 acceptance depends on DOS-C
bridge, operator, firmware, or live-proof truth.

Current action routing is consolidated in
[development-plan.md](development-plan.md). This ledger remains the detailed
status and evidence table.

## Verified Facts

- Transcript and proof packets are authoritative for live ESP-NOW BBS status.
  Screenshots, CV, and OCR corroborate visible OPCON state only.
- The accepted live BBS path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Three-peer USB-only ESP-NOW BBS completion is accepted by the corrected
  2026-05-23 proof packet.
- Gate H structured live acceptance is accepted by the 2026-05-25
  `bridge-transcript.jsonl` proof packet, DOS-C vision gate, ESP32 completion
  gate, cleanup proof, and pre/post read-only preflights.
- Gate G is open only as a local-admin redacted JSON export from the DOS-C/Pi
  bridge spool under accepted `ADR-0005`.
- Gate F now has an accepted ESP32 firmware ABI design contract under
  `ADR-0006`, accepted runtime requirements under `ADR-0007`, and a host-only
  Phase 5/6 runtime design/prototype under `ADR-0008`, but it does not accept
  runtime firmware implementation or live proof work.
- Gate M1 full-service mesh discovery has an accepted host-only contract under
  `ADR-0009` and source ID
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, but it does not
  accept live ESP-WIFI-MESH, BLE pairing, Android app behavior, router/admin
  mutation, firmware runtime migration, or live proof work.
- Gate M2-A full-service mesh discovery has paired DOS-C host-only
  bridge/operator support under source ID
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`,
  but it does not extend the coordinator serial ABI or accept firmware runtime,
  live mesh, BLE, Android, router/admin, PCAP, or hardware work.
- The BBS UI System Operation Improvement Program is recorded under
  `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`; UI-0 and M2-B now
  have a host-only source/proof slice under
  `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`. The work preserves the
  accepted serial-nullmodem path and does not alter runtime APIs, firmware ABI,
  bridge ABI, coordinator serial ABI, `mesh_discovery.v1`, Gate F radio service
  codes, or Win31 transport.
- The Hardware Rapid Prototyping Program is recorded under
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28` as a Tier 2
  documentation/status/source-record plan for 3D-printed enclosures, brackets,
  fixtures, cable guides, scanner fit checks, parametric CAD workflows, and
  nontechnical guide templates. It does not authorize live printing, live
  scanning, wiring, flashing, serial/radio writes, firmware runtime changes,
  battery/solar charging, relay/load/mains, framework selection, or ABI/API
  changes.
- The four-relay low-voltage fixture kit is recorded under
  `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28` as the first
  concrete package in that lane. It adds one public guide, one internal
  evidence workbook, and one provisional OpenSCAD source model, but it does
  not accept live printing, live scanning, hardware fit, relay/load/mains, or
  hardware gate closure.
- The 2026-05-25 LAN DHCP/current-remap pass ended with a read-only preflight
  `ok:true` for the current Pi/coordinator/peer identities, but it did not run
  bridge, Win31/OPCON, BBS, flash, erase, monitor, or radio proof.
- The 2026-05-26 Win31 fullscreen recovery fixed the active Pi display path:
  DOSBox-X now uses X11 fullscreen at `1024x600`, OPCON was rebuilt with a
  compact 640-logical-pixel layout, and final live proof shows zero
  right/bottom margin.
- Companion SoftAP Gate 1 tooling is implemented and host-validated under
  `SRC-LOCAL-ESPNOW-BBS-COMPANION-SOFTAP-LIVE-GATE-TOOLING-2026-05-27`, but
  it does not accept live SoftAP proof, Windows Wi-Fi mutation, physical dummy
  output, flash, bridge proof, vision proof, completion proof, cleanup
  acceptance, or live hardware work.
- Multi-agentic continuous enforcement is recorded under
  `SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`. The repo now
  has a local weighted-vote decision helper and hook tests that treat missing
  evidence as a continuation condition when safe evidence collection remains.
  It does not authorize live hardware, serial reads, XCTU discovery, XBee
  writes, relay/load/mains work, or system-wide strict policy installation.
- XBee two-device read-only Stage A1 is recorded under
  `SRC-LOCAL-XBEE-TWO-DEVICE-READONLY-STUDY-2026-05-29`. Fresh no-serial WSL
  and Windows inventories, local physical-fact placeholders, recovery/cleanup
  rules, and a weighted `ask_user` decision exist, but exact XBee adapter
  identity, serial reads, and XCTU discovery remain unaccepted.
- XBee selected-port programming is recorded under
  `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`. User-selected
  `COM15` and `COM6` were read, programmed with the redacted project security
  key process, and validated with escaped API local-AT readback showing
  `AP=02`, `AO=00`, and `EE=01` on both selected ports. This does not prove
  over-the-air communication, ESP32 carrier wiring, adapter voltage,
  DIN/DOUT routing, relay command acceptance, range, throughput, or
  relay/load/mains readiness.
- XBee OTA link proof is recorded under
  `SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`. The selected `COM15` and `COM6`
  radios exchanged benign `link_probe` API payloads in both directions, each
  with transmit status and matching destination `0x90` receive packet. This
  does not prove range, throughput, relay command acceptance, ESP32 carrier
  wiring, adapter voltage, DIN/DOUT routing, antenna/regulatory deployment
  readiness, or relay/load/mains readiness.
- XBee ESP32 bridge follow-up evidence is recorded under
  `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30` and
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`. The corrected
  live test proved `COM6` as the ESP32 serial device and `COM15` as a healthy
  XBee peer, then showed the ESP32 did not expose XBee API frames before the
  bridge firmware. The bridge firmware is now flashed on `COM6`; redacted
  bridge local-AT readback and corrected bidirectional benign `link_probe`
  proof passed after same-session physical confirmation and rollback backups.
- Four-relay LCD I2C test firmware preparation is recorded under
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`. It preserves the
  COM6 raw XBee bridge, adds display-status support for one assumed 20x4
  HD44780/PCF8574-class LCD on GPIO21/GPIO22, and now records COM6-only
  backup/write/verify evidence plus user visual PASS. It does not authorize
  monitor, XBee setting writes, RF retest, range/throughput, encoder GPIOs,
  relay/load/mains, future flash gates, or exact LCD hardware/electrical
  acceptance beyond the visual display proof.
- Four-relay encoder raw diagnostics preparation is recorded under
  `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`. It keeps the
  accepted COM6 bridge and LCD paths, changes page 0 to show raw
  GPIO34/GPIO35/GPIO13 `A/B/SW` levels plus raw A/B and SW transition
  counters, and records the named COM6-only GPIO13 backup/write/verify gate.
  User LCD raw observation remains pending; monitor, XBee/RF,
  relay/load/mains, hardware acceptance, and future flash gates remain closed.
- Four-relay KY-040 diagnostic refactor is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`. It records the
  user-identified ASIN `B06XQTHDRR` as a Cylewet KY-040 branch using an
  independent Manuals+ mirror, enables only the GPIO13 internal pullup for
  active-low `SW`, keeps GPIO34/GPIO35 internal pulls disabled, and records the
  user-observed raw LCD no-change symptom as hardware/electrical/pinout-first.
  A later same-session COM6 gate recorded safe-state authority, refreshed
  validation, COM6 identity, rollback backups, build hashes, recovery command,
  write-flash, and separate verify-flash for user LCD testing. It does not
  accept raw LCD behavior, hardware wiring, decoder changes, serial monitor,
  XBee/RF, relay/load/mains, hardware acceptance, or future flash gates.
- Four-relay KY-040 pin-finder diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`. It adds
  firmware ID `PF0530A` and an input-only LCD pin-finder page for GPIO34,
  GPIO35, GPIO13, GPIO14, GPIO32, and GPIO33 live levels and change counts.
  GPIO13 remains the only internally pulled-up probe. A later same-session
  COM6 gate recorded safe-state authority, refreshed validation, COM6
  identity, rollback backups, artifact hashes, recovery command, write-flash,
  and separate verify-flash for user LCD testing.
- Four-relay KY-040 row-0 diagnostic refactor is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`. It adds firmware
  ID `PF0530B` and cycles raw A/B/SW levels, raw A/B and SW transition counts,
  and GPIO34/GPIO35/GPIO13/GPIO14/GPIO32/GPIO33 live level/change-count views
  on LCD row 0 after the user reported only pin 34 was displayed on `PF0530A`
  and encoder navigation could not change pages. A later COM6 write/verify
  gate completed, then the user reported no displayed pins changed.
- Four-relay KY-040 GPIO sweep contact tracer is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`. It adds
  firmware ID `PF0530C`, locks the LCD to page 0, shows row-0 `HIT` when any
  watched GPIO changes, sweeps GPIO34/GPIO35/GPIO36/GPIO39/GPIO13/GPIO14/
  GPIO18/GPIO19/GPIO23/GPIO32, enables internal pullups only on GPIO13/GPIO14,
  excludes flash/LCD/UART0/XBee/strapping-risk/relay-candidate pins, and closes
  the diagnostic XBee bridge loop. A later same-session COM6 gate recorded
  safe-state authority, refreshed validation, identity, rollback, hashes,
  recovery command, write-flash, and separate verify-flash. User LCD
  observation remains pending.
- Four-relay KY-040 DevKitC 13/14/32 diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`. It adds
  firmware ID `PF0530D` for the user-confirmed `CLK` GPIO13, `DT` GPIO14,
  `SW` GPIO32, module `+` on ESP32 3V3, and 100 nF capacitor across `+` and
  `GND`; it locks LCD page 0, enables internal pullups on GPIO13/GPIO14/
  GPIO32, shows raw levels, transition/position/button counts, per-pin `HIT`
  changes, and closes the diagnostic XBee bridge loop. It has been written and
  separately verify-flashed to COM6. User LCD observation and hardware
  acceptance remain pending.
- Four-relay KY-040 serial pintrace diagnostic is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`. It adds
  firmware ID `PF0530E`, watches a DevKitC candidate GPIO set as input-only,
  enables internal pullups only on GPIO13/GPIO14/GPIO32, emits stable `EV`
  changes and periodic `HB`/`ST` summaries on COM6/UART0, warns that DevKitC
  physical `J2-13` is `IO12` and `J2-14` is `GND`, and closes the diagnostic
  XBee bridge loop. The final r4 COM6 write/verify and 10-minute read-only
  monitor completed with no watchdog/backtrace lines and no encoder-pin `EV`
  events. The later r5 read-only monitor recorded user-confirmed actuation with
  GPIO13/GPIO14/GPIO32 count increases, `writes_sent=false`, and no watchdog,
  panic, or backtrace scan hits. Hardware acceptance remains pending.
- Four-relay KY-040 encoder menu PF0530F is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`. It changes the
  current repo firmware ID to `PF0530F`, boots the LCD menu proof path instead
  of PF0530E serial pintrace, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, configures
  GPIO13/GPIO14/GPIO32 input-only with pullups, adds 2 ms A/B debounce,
  30 ms switch debounce, 150 ms switch guard suppression, invalid-transition
  counting, text-only locked pages, and serial `MENU_*` proof lines. The later
  live attempt under
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30` flashed
  and separately verify-flashed PF0530F on COM6 and captured `PF0530F
  MENU_READY`, but live menu acceptance is blocked by `PF0530F
  LCD_INIT_FAILED` with no `MENU_HB`, `MENU_STEP`, or `MENU_SELECT` proof.
- Four-relay KY-040 LCD init diagnostic PF0530G is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`. It keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, uses GPIO21/GPIO22 I2C only, emits
  stage-specific `LCD_*` proof lines, and passed serial LCD init diagnosis with
  one ACK at `0x27`, all HD44780 steps ok, `LCD_INIT_OK addr=0x27`, and
  repeated ok heartbeats. It is diagnostic-only before any renewed encoder menu
  proof.
- Four-relay KY-040 BBS LCD menu PF0530H is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`. It combines
  the PF0530G LCD init/probe path with PF0530F GPIO13/GPIO14/GPIO32 input-only
  encoder handling, renders nine static/simulated BBS pages, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, and adds `BBS_*` serial proof markers. Live
  COM6 flash/verify, LCD visual confirmation, and rotary acceptance remain
  separate gates.
- Four-relay KY-040 BBS LCD menu PF0530H live gate is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`. It
  passed COM6 identity, rollback backup, write-flash, separate verify-flash,
  and read-only monitor with `PF0530H BBS_LCD_READY`, `BBS_LCD_RENDER`, and
  `BBS_MENU_HB`.

## Assumptions

- Historical task logs and handoffs remain immutable historical records.
  Current truth is recorded here and in the 2026-05-26 source ledger.
- If a lane has simulator tests plus draft documents but no accepted live proof,
  it remains `implemented-simulator-only` or `design-only` as classified below.
- If a lane is explicitly closed by a live-gate boundary, it remains closed
  even when a related source or simulator exists.

## Unknowns

- No firmware runtime implementation or live proof is accepted for the custom
  wireless protocol service jobs, scheduler, persistence, recovery, or export
  behavior.
- No Win31/OPCON analytics export control and no live bridge export request type
  are accepted.
- No current same-session physical USB-only/no-load/no-relay/no-XBee/no-TFT/
  no-MicroSD state was captured by this documentation review.
- Except for the selected-port XBee programming gate recorded in
  `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29` and bounded XBee API
  proof attempts recorded in the XBee task logs, no current live proof opens
  BLE, ESP-WIFI-MESH, PCAP, relay, TFT, MicroSD, load, mains, erase, monitor,
  or broad serial-write expansion.
- No firmware mapping from ESP-WIFI-MESH APIs/events into `mesh_discovery.v1`
  is accepted.
- UI-0 and M2-B are accepted only as host-only source/test proof. No M3
  firmware mapping review, Client-1 static/simulated browser proof, Client-2
  selected-board read-only Wi-Fi proof, dummy-output proof, or live browser
  proof is accepted yet.
- No same-session printer/scanner identity, nozzle proof, filament SDS,
  ventilation/exposure record, drying record, calibration coupon, caliper
  validation, slicer packet, print proof, scan proof, or fit acceptance is
  accepted for the hardware rapid-prototyping lane. One provisional OpenSCAD
  source exists for the four-relay low-voltage fixture kit, but it is not
  measurement or fit evidence.
- No same-session LCD module/backpack identity, pullup voltage, logic voltage,
  exact detected address value, contrast, backlight current, or rail-current
  margin is accepted for the four-relay LCD I2C test.
- User-observed encoder raw LCD no-change is recorded, and the KY-040
  GPIO13-pullup diagnostic image has been written/verified to COM6 for user
  testing, but no same-session electrical proof or LCD raw acceptance is
  accepted. Exact bench KY-040 markings, onboard pullups, idle/toggle levels,
  continuity, switch behavior, boot behavior, and rail-current margin remain
  open.
- The row-0 `PF0530B` diagnostic has been written/verified to COM6, and the
  user reported no displayed pins changed. `PF0530C` has been written and
  separately verify-flashed to COM6. PF0530D has also been written and
  separately verify-flashed to COM6, but no same-session user LCD observation
  is accepted. PF0530E r5 is the GPIO-level input proof, and PF0530F is the
  current LCD menu-proof source branch; its COM6 flash/verify gate passed, but
  menu acceptance is blocked by `PF0530F LCD_INIT_FAILED`. PF0530G later passed
  serial LCD init diagnosis at `0x27`; renewed menu acceptance remains
  separate.
- The fullscreen fix did not require Windows 3.1 display-driver/runtime
  mutation.

## Status Ledger

| Lane | Current status | Evidence class | Source IDs | Accepted proof | Remaining gaps | Next gated action |
| --- | --- | --- | --- | --- | --- | --- |
| ESP-NOW BBS one-coordinator/one-peer encrypted proof | accepted-live | live proof packet | `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22` | Win31 OPCON showed peer `peer01`, `espnow-enc`, zero serial errors, and moving RX/TX/ACK counters after private backups and flash/verify evidence. | Superseded as the current breadth by later three-peer proof. | Use only as lineage; cite three-peer or structured Gate H proof for current acceptance. |
| ESP-NOW BBS three-peer USB-only coordinator/client proof | accepted-live | live proof packet | `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`, `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23` | Corrected run produced four full-flash backups, manifest, flash/verify evidence, three `espnow-enc` peers, moving `126/126/126` to `129/129/129` counters, Win31 runtime proof, and cleanup. | Future chunked delivery, provisioning UX, BLE, ESP-WIFI-MESH, physical wiring beyond USB-only, or any new live acceptance claim. | Fresh read-only preflight, same-session physical confirmation, prepare/flash only if a new firmware image is authorized. |
| Gate H structured BBS/download/OTAP live proof | accepted-live | structured transcript proof packet | `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-TRANSCRIPT-2026-05-25`, `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` | `bridge-transcript.jsonl` captured startup telemetry, pre/post telemetry refreshes, BBS post/pull/search/ack, `download_queue`, `otap_intent`, zero serial errors, three `espnow-enc` peers, moving counters, DOS-C vision `pass`, ESP32 completion `pass`, and cleanup. | Firmware ABI, export controls, and bridge export request types remain closed. | Use the same JSONL transcript shape for future completion gates. |
| Earlier Gate H blocked attempt and troubleshooting records | superseded | historical read-only blockers | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-H-LIVE-ATTEMPT-2026-05-25`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-H-TROUBLESHOOTING-2026-05-25`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-H-LIVE-ACCEPTANCE-2026-05-25`, `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` | Later restored Pi/router path and structured live proof supersede the blocked Pi reachability and old transcript-shape caveats. | Historical blocked filenames remain; do not rewrite them. | Link the accepted structured evidence when summarizing current status. |
| LAN DHCP/current peer remap recovery | implemented-validated | read-only preflight and cleanup proof | `SRC-LOCAL-ESPNOW-LAN-DHCP-CURRENT-REMAP-2026-05-25` | Post-cleanup preflight returned `ok:true` for Pi `192.168.200.153`, coordinator `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`, and peers `peer01=COM6`, `peer02=COM10`, `peer03=COM12`. | No bridge, Win31/OPCON, BBS, prepare, flash, erase, monitor, or radio proof was run in this pass. | If a new proof run is requested, start from a fresh read-only preflight on the current LAN mapping. |
| Custom wireless protocol Gate B simulator | implemented-simulator-only | simulator tests | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-SIM-2026-05-25` | Simulator covers packetized direct messages, file chunks, telemetry, node status, custody ACKs, duplicate suppression, TTL, and non-executing control intents. | No live hardware, bridge runtime, firmware ABI, or Win31 proof. | Keep expanding simulator fixtures before any live or firmware gate. |
| Custom wireless protocol Gate C bridge adapter | implemented-simulator-only | simulator tests | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-BRIDGE-SIM-2026-05-25` | Simulated compact bridge requests translate `msg_post`, `download_queue`, telemetry, node status, protocol report, `state_get`, and `control_intent`; blocked requests reject `relay_set`, `flash`, `erase`, and `radio_set`. | Not a final bridge/operator ABI and not live bridge behavior. | Owner review before final ABI or runtime mutation. |
| Custom wireless protocol Gate D DOS-C pairing | implemented-simulator-only | paired simulator fixture replay | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-D-DOSC-PAIRING-2026-05-25` | DOS-C test fixtures replay through the ESP32 Gate C adapter within 512-byte bounds while live `download_queue` remains payload-free. | No live file transfer or final ABI freeze. | Keep DOS-C live operator request shapes payload-free unless a later gate changes them. |
| Gate E bridge ABI candidate | design-only | draft doc plus simulator validation | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-E-BRIDGE-ABI-2026-05-25` | Draft `v:1` ASCII JSON request set and stable error reasons exist for owner review. | Final firmware ABI, runtime migration, bridge mutation, and live proof are not accepted. | Owner ADR/review for final ABI. |
| Gate F firmware ABI and runtime requirements | accepted-host-prototype-only | ADR/source ledger plus host tests | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-GOLDEN-VECTORS-2026-05-26`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-RUNTIME-REQUIREMENTS-2026-05-26`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-PHASE-5-6-RUNTIME-DESIGN-REVIEW-2026-05-26`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27` | Accepted `ADR-0006` mirrors simulator packet budgets, service codes, custody codes, packet header layout, non-executing `control_intent` semantics, and host-only full packet golden vectors. Accepted `ADR-0007` adds requirements-only runtime planning. Accepted `ADR-0008` adds host-only runtime defaults, bounded queue/backpressure behavior, scheduler order, retry/expiry handling, duplicate handling, and visible counters in the simulator. Gate M2-A adds paired DOS-C read-only discovery summaries without changing the coordinator serial ABI. | Firmware runtime implementation, firmware memory budgets, task ownership, firmware persistence, migration, recovery, and live proof are not accepted. | Keep firmware runtime implementation closed until a later implementation gate. |
| Companion SoftAP Gate 1 tooling | implemented-host-tooling-only | task/handoff plus host tests | `SRC-LOCAL-ESPNOW-BBS-COMPANION-SOFTAP-LIVE-GATE-TOOLING-2026-05-27` | ESP32 tooling adds prepare-time companion HTTP config, redacted manifest metadata, Windows proof collection script, and completion-audit enforcement; validation recorded ESP32 live-gate unit tests, py_compile, scaffold checks, paired DOS-C generator/bridge tests, no-flash companion-enabled builds, and PowerShell parser check. | No live preflight, backup, flash, SoftAP gateway, Windows Wi-Fi proof, bridge proof, vision gate, completion gate, cleanup proof, physical dummy output, or Gate 2 GPIO fixture evidence exists. | Before any live continuation, re-run ESP32 and paired DOS-C tests, then open a fresh Tier 3 gate with identity, recovery, Windows Wi-Fi, companion proof, no-output evidence, and cleanup criteria. |
| Gate G simulator analytics | superseded | simulator tests | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-G-ANALYTICS-2026-05-25`, `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25` | Simulator analytics remain useful for test coverage, but policy fields are superseded by accepted ADR-0005 and live export implementation. | Simulator reports are not live export authority. | Treat as fixture coverage only. |
| Gate G local-admin redacted JSON export | accepted-live | policy plus local-admin live proof | `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`, `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25` | Accepted `ADR-0005`, file-backed spool export, redacted `analytics-report.v1.json`, approved ignored roots, existing-destination refusal, raw identifier/body omission, and stale cleanup proof. | No Win31 export UI, firmware export ABI, or live bridge export request type. | Keep export CLI local-admin only until separate owner gates open additional surfaces. |
| Win31 dashboard CV/OCR gate | implemented-validated | corroboration tooling and fixture tests | `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`, `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24` | DOS-C vision gate can corroborate required views and passed the structured Gate H packet. | Screenshots remain secondary to transcript and cleanup evidence. | Use OCR/CV only after transcript proof is present. |
| Win31 dashboard fullscreen recovery | fixed-live-open | live display proof plus tracked DOS-C fix | `SRC-LOCAL-WIN31-DASHBOARD-FULLSCREEN-RECOVERY-2026-05-26`, `SRC-WIN31-WIN-COM-SWITCHES-2026-05-26`, `SRC-SUNFOUNDER-7INCH-HDMI-1024X600-2026-05-26`, `SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26` | Pi identity, SSH fingerprints, `wlr-randr`, DRM, and `grim` proved the display/capture path at `1024x600`; initial copied config-only tests failed; the accepted fix uses DOSBox-X X11 fullscreen at `1024x600` plus a compact OPCON layout for the 640x480 Win31 logical surface; final live capture bbox was `(0,1)-(1023,599)` with zero right/bottom margin and the screen was left open. | Human physical-panel acceptance remains pending. | Keep current bridge/DOSBox-X PIDs open until the user confirms or asks for cleanup. |
| Win31 CBBS rename, icon, UI, and input diagnosis | implemented-local-input-blocked | source build plus read-only input inventory | `SRC-LOCAL-WIN31-CBBS-INPUT-RENAME-ICON-UI-2026-05-27` | DOS-C user-facing title/launcher/package naming is now `CBBS`; Program Manager helper DDE-adds item `CBBS` and best-effort deletes stale `RETRO-CBBS-NOW Dashboard`; the tracked icon is original `16x16` `16-color`; primary UI path is Status, Messages, Files, Devices, and Help; same-session inventory sees `ZY.Ltd ZY Control Mouse` at `/dev/input/event5`. | Wireless pointer root cause and fix are not accepted because the preflight was `ok:false` with stale bridge/DOSBox-X runtime and no physical movement/click A/B matrix. No fresh live CBBS Program Manager/icon screenshot was captured. | Before live acceptance, clean or explicitly preserve stale runtime, re-run read-only preflight, capture physical input A/B proof, then capture CBBS Program Manager/icon screenshots and cleanup/left-running proof. |
| DOS-C bridge/operator default path | accepted-live | paired live proof and source implementation | `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`, `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`, `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` | COM1/nullmodem/Pi bridge path is accepted for BBS status, message, download, and non-executing OTAP intent proof. | Runtime export controls and firmware ABI runtime behavior remain closed. | Continue DOS-C work through companion KB records and host tests before ESP32 claims depend on it. |
| DOSBox-X PCAP/packet-driver path | blocked | historical diagnostic only | `SRC-DOSBOX-SERIAL-CONFIG`, `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20` | No accepted PCAP proof. Serial-nullmodem is the accepted path. | Pi identity, wired `eth0`, capability setup/restore, redacted packet capture, and rollback proof. | Reopen only by explicit PCAP live-gate request. |
| ESP-WIFI-MESH self-healing branch | design-only | source-backed design | `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`, `SRC-ESP-IDF-WIFI-MESH`, `SRC-ESP-IDF-RF-COEXIST` | Optional metadata and Network view are simulator/source-level only. | No mesh route-table, parent, root, healing, coexistence, flash, or cleanup proof. | Accepted ADR plus fresh identity, backups, build hashes, mesh config, route/healing proof, rollback. |
| Full-service mesh discovery Gate M1 | accepted-host-simulator-only | ADR/source ledger plus host tests | `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`, `SRC-ESP-IDF-WIFI-MESH`, `SRC-ESP-IDF-RF-COEXIST`, `SRC-ANDROID-BLE-OVERVIEW`, `SRC-ANDROID-BLE-GATT-CONNECT`, `SRC-ANDROID-BLUETOOTH-PERMISSIONS` | Accepted `ADR-0009` defines `mesh_discovery.v1`, host topology/service/capability/BLE-Android metadata, healing-event shape, compact bridge summaries, recursive secret-field rejection, 512-byte bridge bounds, runtime summary inclusion, and unchanged Gate F radio service codes. | No live mesh proof, BLE proof, Android app proof, router/admin policy, or firmware mapping. | Superseded for DOS-C companion status by Gate M2-A; Gate M3 firmware mapping review remains design-only. |
| Full-service mesh discovery Gate M2-A DOS-C companion | implemented-host-only | paired DOS-C commit, task/handoff, source ledger, and focused host tests | `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` | DOS-C commit `62c4db6` adds read-only `discovery_snapshot`, `discovery_events`, `service_catalog`, and `capability_report` bridge/operator support, Win31 Network/Services summaries, ASCII schema-versioned response parsing, capped event/service rows, 512-byte bridge bounds, and no coordinator serial ABI expansion. Focused Gate M2-A bridge/operator tests passed; full DOS-C Win31/scaffold suites were blocked by unrelated dirty Star Trek fullscreen-fill worktree changes. | No live mesh proof, BLE proof, Android app proof, router/admin policy, firmware mapping, PCAP, serial-write expansion, or hardware proof. | Gate M3 firmware mapping review/design-only; live proof requires a separate future Tier 3 gate with same-session evidence and recovery path. |
| BBS UI system operation improvement program | ui0-m2b-implemented-host-only | Tier 2 plan/source ledger/task/handoff, read-only quorum, and paired DOS-C host proof | `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`, `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`, `SRC-LOCAL-WIN31-DASHBOARD-INTERFACE-IMPROVEMENT-2026-05-27`, `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24`, `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27` | UI-0 now has a ranked source-backed operator packet. M2-B now has host-only Network/Services UX proof tied to DOS-C commit `7f0b5df`; DOS-C `m2a.discovery.v1` companion output is distinguished from ESP32 host `mesh_discovery.v1`, and source tests preserve 512-byte/read-only/no-secret/no-serial-ABI boundaries. | No M3 firmware mapping review, Client-1 simulated/static proof, Client-2 live read-only Wi-Fi proof, dummy-output proof, copied screenshot proof, live browser proof, runtime public API, firmware ABI, bridge ABI, serial ABI, Gate F service-code map, `mesh_discovery.v1`, or Win31 transport change is accepted. | Continue with Gate M3 design-only mapping review or Client-1 static/simulated browser proof; any live proof requires a separate future Tier 3 gate. |
| Multi-agentic continuous enforcement | implemented-host-tooling-only | repo-local script, hook tests, source ledger, task, and handoff | `SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29` | `scripts/agent_process_decision.py` evaluates required roles, weighted approval, P1/P2 vetoes, Tier 3 prerequisites, automatable evidence, and irreducible physical-fact requests. Hook tests cover semantic Stop/SubagentStop behavior and `bypassPermissions` non-denial. | Runtime hook trust remains advisory; no live hardware, serial/XCTU, radio, firmware, relay/load/mains, or strict system policy authority is opened. | Use the helper for future Tier 2/Tier 3 continuation packets and keep hard safety gates closed until same-session evidence exists. |
| BLE/Android client-node branch | design-only | source-backed design | `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`, `SRC-ESP-IDF-BLE-API`, `SRC-ESP-IDF-BLE-SMP`, `SRC-ANDROID-BLE-OVERVIEW`, `SRC-ANDROID-BLE-GATT-CONNECT`, `SRC-ANDROID-BLUETOOTH-PERMISSIONS` | BLE GATT/Android model is documented only. | No UUIDs, Android package, permissions proof, bonding/SMP proof, coexistence proof, or live GATT proof. | Separate BLE live gate. |
| Web Serial, Web Bluetooth, and raw serial client work | blocked | source-backed future references | `SRC-MDN-WEB-SERIAL-2026-05-24`, `SRC-MDN-WEB-BLUETOOTH-2026-05-24`, `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24` | Browser APIs are documented as future experiments only. | No live browser serial writes, BLE pairing, or replacement of accepted Win31 path. | Keep closed behind separate browser/device gates. |
| Cross-project Wi-Fi browser client UI and dummy output | design-only | source-backed plan | `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24`, `SRC-ESP-IDF-WIFI`, `SRC-ESP-IDF-HTTP-SERVER`, `SRC-GITHUB-PAGES-WHAT-IS` | Plan chooses Wi-Fi web first for phone and laptop and dummy-output-only first live control. | No selected board, current identity, Wi-Fi mode, browser proof, auth policy, dummy fixture, or no-relay/load/mains observation. | Stage 1 simulated UI, then selected-board read-only proof, then dummy-output gate. |
| Firmware flash/erase/monitor/serial-write expansion | blocked | live-gate policy plus esptool sources | `SRC-ESPTOOL-BASIC`, `SRC-ESPTOOL-ADVANCED-VERIFY`, `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS`, `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23` | Past accepted flashes are limited to their proof packets. Current expansion is closed. | Fresh identity, backups, manifests, hashes, recovery, write confirmation, verify, and cleanup are required for any new flash. | Do not run prepare/flash/erase/monitor unless a new live gate explicitly opens it. |
| GitHub Pages public site and public docs | implemented-validated | local build/audit/smoke proof | `SRC-GITHUB-PAGES-WHAT-IS`, `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`, `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`, `SRC-GITHUB-PAGES-LIMITS`, `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21` | Public-safe generated Pages artifact, manifest audit, smoke checks, and prior browser validation exist. | Does not prove live hardware, relay switching, MicroSD mount, TFT wiring, firmware flashing, XBee writes, load, or mains work. | Continue with build/audit/smoke before publication changes. |
| Four-relay board, relay, power, load, and mains lane | blocked | design/source-backed gaps | `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-1910-305` | Photo/source records exist only for visible components and candidate hazard context. | Exact board, shield schematic, regulator, relay module, trigger polarity, isolation, current, rail budget, load type, enclosure, grounding, and qualified review. | Low-voltage inspection and bench records before any relay or load work; qualified review before mains. |
| XBee lane | bridge-flashed-rf-proof-accepted | source-backed study, host XCTU install proof, selected-port programming evidence, bidirectional benign RF proof, corrected ESP32 bridge failure evidence, permanent bridge firmware, COM6-only flash evidence, and bridge RF proof | `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`, `SRC-WAVESHARE-XBEE-USB-ADAPTER`, `SRC-DIGI-XCTU-LOCAL-DISCOVERY-2026-05-29`, `SRC-DIGI-XBEE-900HP-BD-2026-05-29`, `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`, `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`, `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`, `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`, `SRC-LOCAL-XBEE-TWO-DEVICE-READONLY-STUDY-2026-05-29`, `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`, `SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`, `SRC-LOCAL-XBEE-ESP32-UART-WIRING-PLAN-2026-05-29`, `SRC-LOCAL-ESP32-CONNECTED-XBEE-COM15-LIVE-TEST-2026-05-29`, `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`, `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30` | User-selected `COM15` and `COM6` were programmed to `AP=2`, `AO=0`, `EE=1`, and earlier exchanged benign `link_probe` API payloads in both directions. Corrected evidence later proved `COM6` is the ESP32 and `COM15` is the peer XBee; `COM6` did not expose XBee API frames before bridge firmware. The permanent bridge now maps UART0 host `115200` to UART2 XBee `9600` on GPIO17/GPIO16 with no app logging in the copy loop; it was flashed to `COM6` only, then passed redacted COM6 local-AT readback, COM15 peer readback, and corrected bidirectional benign `link_probe` RF proof. | Deployment range, throughput, relay command acceptance, source address allowlisting integration, antenna/regulatory deployment review, measured rail-current margin for broader hardware expansion, load/mains readiness, and future XBee setting-write authority remain open. | Keep bridge firmware installed for raw COM6-to-XBee API access; reopen only with a separate gate for range/throughput, relay command payloads, future radio setting writes, or load/mains work. |
| Four-relay LCD I2C test | accepted-live-visual | firmware/docs/audit source record plus COM6-only backup/write/verify and user visual proof | `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`, `SRC-ESP-IDF-I2C`, `SRC-NXP-PCF8574-74A`, `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30` | Firmware adds a low-priority display-status task on I2C0 GPIO21/GPIO22 beside the COM6 bridge, probes PCF8574/PCF8574A candidate address ranges, exits without blocking the bridge if zero or multiple candidates are detected, was written/verified to COM6 after 2MB and 4MB rollback backups, and user visual proof passed for page cycling, detected-address line display, and clean four-row rendering. | Exact LCD module/backpack identity, voltage/pullups, exact detected address value, contrast, backlight current, and rail-current margin remain open. | Keep monitor, XBee/RF, relay/load/mains, encoder, and future flash actions closed unless a separate gate opens them. |
| Four-relay rotary encoder LCD menu input | PF0530H-live-ready-for-user-testing | input-only firmware/docs/audit preparation, prior COM6-only rollback/write/verify, raw diagnostic GPIO13 backup/write/verify records, KY-040 selected-module source, GPIO13-only pullup refactor, COM6 KY-040 write/verify evidence, COM6 PF0530A pin-finder write/verify evidence, COM6 PF0530B row-0 write/verify evidence plus user no-change report, COM6 PF0530C contact-tracer write/verify evidence, COM6 PF0530D DevKitC 13/14/32 write/verify evidence, PF0530E serial pintrace implementation plus r4/r5 monitor evidence, PF0530F menu-proof source, PF0530F COM6 flash/verify plus blocked read-only monitor evidence, PF0530G COM6 LCD init diagnostic proof, and PF0530H BBS LCD menu source plus PF0530H COM6 live flash/verify/monitor evidence | `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`, `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`, `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`, `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`, `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-ROTARY-ENCODER-MENU-PLAN-2026-05-30`, `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`, `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`, `SRC-ESP32-DEVKITC`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-PCNT`, `SRC-ESPRESSIF-KNOB-1-0-2`, `SRC-ESPRESSIF-BUTTON-4-1-6`, `SRC-BOURNS-PEC11R` | PF0530H write-flash and separate verify-flash passed on COM6; read-only monitor captured LCD init OK, BBS ready, render, and heartbeat proof with no crash/fault or closed-surface markers. | Physical LCD visual confirmation, renewed menu acceptance, LCD page changes, encoder direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, and button-window A/B suppression evidence remain pending under a separate gate. | Keep XBee/RF, relay/load/mains, hardware acceptance, final pin reassignment, and unapproved future flash/monitor gates closed. |
| Remote LCD XBee solar client hardware-device stream | private-submodule-scaffolded-design-only | parent coordination plus private docs-only submodules | `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`, `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`, `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26` | Seven private `rlxsc-*` hardware submodules exist and the lane is now recorded as separate from ESP-NOW BBS, Win31/DOS-C, Gate F runtime, Gate G export, Gate H proof, mesh, BLE, network, relay, TFT, MicroSD, load, and mains work. | Exact ESP32 board, LCD/backpack, encoder, cell, BMS, charger/power path, panel, XBee carrier, antenna, fuse/protection, enclosure, power budget, pin map, framework ADR, and read-only bench proof remain open. | Start source-backed identity intake inside the private submodules, prioritizing cell, BMS/protection, charger/power path, panel, fuse/protection, enclosure, and current-limit evidence before board or interface bench action. |
| Hardware rapid prototyping and CAD | planned-doc-status-program | Tier 2 plan/source ledger/task/handoff plus official equipment/material/CAD/safety sources | `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`, `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`, `SRC-CREALITY-K1-SUPPORT-2026-05-28`, `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`, `SRC-CREALITY-CR30-2026-05-28`, `SRC-CREALITY-CR-SCAN-LIZARD-2026-05-28`, `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`, `SRC-OPENSCAD-DOCS-2026-05-28`, `SRC-CADQUERY-DOCS-2026-05-28`, `SRC-FREECAD-FEATURES-2026-05-28`, `SRC-KICAD9-PCBNEW-3D-EXPORT-2026-05-28`, `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`, `SRC-BAMBULAB-PA6-CF-2026-05-28` | The program maps printer/scanner defaults, CAD workflow, material gates, lane-specific prototype needs, and a nontechnical build-guide template. The first four-relay kit adds one public guide, one internal workbook, and one provisional OpenSCAD source only. K1, Kobra 2 Max, CR-30, and CR-Scan Lizard roles are planning defaults only. | No local printer/scanner condition, hardened-nozzle proof, ventilation record, filament SDS, drying record, calibration coupon, scan-to-caliper proof, slicer packet, live print, live scan, or fit acceptance is recorded. No hardware gate is closed. | Complete the four-relay fixture workbook and per-lane measurement packets before any guide becomes repeatable procedure. |
| Four-relay low-voltage fixture kit | provisional-doc-cad-package | public guide, internal workbook, source ledger/task/handoff, and one OpenSCAD source | `SRC-LOCAL-FOUR-RELAY-LOW-VOLTAGE-FIXTURE-KIT-2026-05-28`, `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`, `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`, `SRC-OPENSCAD-DOCS-2026-05-28` | Public-safe guide, internal evidence workbook, Pages allowlist limited to the public guide, public source-index redaction for workbook/CAD paths, and a provisional plate model with cable-tie slots, label zones, measurement grid, and no board-specific mounting holes. | Printer/scanner identity, K1 hardened-nozzle proof, filament SDS/dry state, ventilation, calibration coupon, board/relay/XBee/MicroSD/TFT/expander dimensions, fit proof, live print, live scan, and hardware acceptance remain open. | Fill the workbook and rerun review before printing or treating the plate as fit evidence. |
| TFT, MicroSD, expander, storage, and instrument support lanes | design-only | source-backed candidates | `SRC-LCDWIKI-R61509V-MRB2802`, `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`, `SRC-ESP-IDF-SDMMC`, `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SD-PULLUP`, `SRC-SD-ASSOCIATION-FORMATTER`, `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-FLUKE-87V`, `SRC-KEYSIGHT-E36200`, `SRC-SALEAE-LOGIC-8` | Candidate references exist for planning only. | Exact modules, wiring, voltage, boot-pin conflicts, bus pullups, address pins, card policy, and bench instrument inventory. | Create source-backed profiles and bench records before wiring or firmware dependencies. |
| Agricultural telemetry, pivot, soil, and GPS planning | design-only | external candidate sources | `SRC-LINDSAY-FIELDNET-PIVOT-MONITOR-2026-05-25`, `SRC-METER-TEROS12-2026-05-25`, `SRC-SENTEK-DRILLDROP-2026-05-25`, `SRC-IRROMETER-SOIL-SENSORS-2026-05-25`, `SRC-GEOTAB-ASSET-TRACKING-2026-05-25` | Candidate telemetry classes are source-backed. | No selected local hardware, wiring, controller protocol, calibration, units, power, voltage, isolation, connector, GPS integration, or live-proof plan. | Source-backed hardware profile and protocol ADR before implementation. |

## Closed Gates

Keep firmware runtime implementation, firmware persistence, Win31 export
controls, bridge export request types, live SoftAP proof, Windows Wi-Fi
mutation, physical output proof, BLE pairing, live mesh, PCAP, live LCD I2C
proof, encoder live proof, relay/XBee, TFT, MicroSD, load, mains,
battery/solar charging, live printing, live scanning,
additional CAD source implementation beyond the approved four-relay fixture
source, generated CAD/print artifacts, slicer projects, G-code, raw scanner
captures, erase, monitor, cleanup acceptance, and serial-write expansion closed
unless a later source-backed gate explicitly opens the exact surface.
