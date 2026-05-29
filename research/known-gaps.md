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
- Complete XCTU/XBee Studio host evidence before relying on GUI behavior:
  official support URL, installer SHA-256 if downloaded, install path,
  first-run version, and update prompt state.
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
| XBee read-only bench proof | Tier A passive record and optional Tier B `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, `NP` read record with `--confirm-sends-read-commands`. |
| XBee radio programming study | Offline `inventory`, `profile-diff`, and blocked `write-plan` evidence may be used for planning; XCTU host install proof is recorded. Live serial reads, writes, API transmit frames, firmware operations, range tests, and radio setting changes remain separate gates. |
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
