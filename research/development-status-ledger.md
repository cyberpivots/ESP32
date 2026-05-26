# Development Status Ledger

Source index: [../knowledge-base/source-index.md](../knowledge-base/source-index.md)

Date: 2026-05-26

This is the canonical planning-status ledger for the ESP32 workspace, with
paired DOS-C evidence included only where ESP32 acceptance depends on DOS-C
bridge, operator, firmware, or live-proof truth.

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
  `ADR-0006`, but it does not accept runtime firmware behavior or live proof
  work.
- The 2026-05-25 LAN DHCP/current-remap pass ended with a read-only preflight
  `ok:true` for the current Pi/coordinator/peer identities, but it did not run
  bridge, Win31/OPCON, BBS, flash, erase, monitor, or radio proof.

## Assumptions

- Historical task logs and handoffs remain immutable historical records.
  Current truth is recorded here and in the 2026-05-26 source ledger.
- If a lane has simulator tests plus draft documents but no accepted live proof,
  it remains `implemented-simulator-only` or `design-only` as classified below.
- If a lane is explicitly closed by a live-gate boundary, it remains closed
  even when a related source or simulator exists.

## Unknowns

- No firmware runtime implementation or live proof is accepted for the custom
  wireless protocol service jobs or export behavior.
- No Win31/OPCON analytics export control and no live bridge export request type
  are accepted.
- No current same-session physical USB-only/no-load/no-relay/no-XBee/no-TFT/
  no-MicroSD state was captured by this documentation review.
- No current live proof opens BLE, ESP-WIFI-MESH, PCAP, relay, XBee, TFT,
  MicroSD, load, mains, erase, monitor, or serial-write expansion.

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
| Gate F firmware ABI design contract | accepted-design-contract | ADR/source ledger plus host tests | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`, `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26` | Accepted `ADR-0006` mirrors simulator packet budgets, service codes, custody codes, packet header layout, and non-executing `control_intent` semantics as a design contract only. | Firmware runtime queues, memory budgets, timeouts, retries, persistence, scheduler, migration, recovery, and live proof are not accepted. | Keep the next step host-only unless a separate owner gate opens firmware runtime work. |
| Gate G simulator analytics | superseded | simulator tests | `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-G-ANALYTICS-2026-05-25`, `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25` | Simulator analytics remain useful for test coverage, but policy fields are superseded by accepted ADR-0005 and live export implementation. | Simulator reports are not live export authority. | Treat as fixture coverage only. |
| Gate G local-admin redacted JSON export | accepted-live | policy plus local-admin live proof | `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`, `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25` | Accepted `ADR-0005`, file-backed spool export, redacted `analytics-report.v1.json`, approved ignored roots, existing-destination refusal, raw identifier/body omission, and stale cleanup proof. | No Win31 export UI, firmware export ABI, or live bridge export request type. | Keep export CLI local-admin only until separate owner gates open additional surfaces. |
| Win31 dashboard CV/OCR gate | implemented-validated | corroboration tooling and fixture tests | `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`, `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24` | DOS-C vision gate can corroborate required views and passed the structured Gate H packet. | Screenshots remain secondary to transcript and cleanup evidence. | Use OCR/CV only after transcript proof is present. |
| DOS-C bridge/operator default path | accepted-live | paired live proof and source implementation | `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`, `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`, `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` | COM1/nullmodem/Pi bridge path is accepted for BBS status, message, download, and non-executing OTAP intent proof. | Runtime export controls and firmware ABI runtime behavior remain closed. | Continue DOS-C work through companion KB records and host tests before ESP32 claims depend on it. |
| DOSBox-X PCAP/packet-driver path | blocked | historical diagnostic only | `SRC-DOSBOX-SERIAL-CONFIG`, `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20` | No accepted PCAP proof. Serial-nullmodem is the accepted path. | Pi identity, wired `eth0`, capability setup/restore, redacted packet capture, and rollback proof. | Reopen only by explicit PCAP live-gate request. |
| ESP-WIFI-MESH self-healing branch | design-only | source-backed design | `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`, `SRC-ESP-IDF-WIFI-MESH`, `SRC-ESP-IDF-RF-COEXIST` | Optional metadata and Network view are simulator/source-level only. | No mesh route-table, parent, root, healing, coexistence, flash, or cleanup proof. | Accepted ADR plus fresh identity, backups, build hashes, mesh config, route/healing proof, rollback. |
| BLE/Android client-node branch | design-only | source-backed design | `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`, `SRC-ESP-IDF-BLE-API`, `SRC-ESP-IDF-BLE-SMP`, `SRC-ANDROID-BLE-OVERVIEW`, `SRC-ANDROID-BLE-GATT-CONNECT`, `SRC-ANDROID-BLUETOOTH-PERMISSIONS` | BLE GATT/Android model is documented only. | No UUIDs, Android package, permissions proof, bonding/SMP proof, coexistence proof, or live GATT proof. | Separate BLE live gate. |
| Web Serial, Web Bluetooth, and raw serial client work | blocked | source-backed future references | `SRC-MDN-WEB-SERIAL-2026-05-24`, `SRC-MDN-WEB-BLUETOOTH-2026-05-24`, `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24` | Browser APIs are documented as future experiments only. | No live browser serial writes, BLE pairing, or replacement of accepted Win31 path. | Keep closed behind separate browser/device gates. |
| Cross-project Wi-Fi browser client UI and dummy output | design-only | source-backed plan | `SRC-LOCAL-CLIENT-UI-LIVE-GATE-2026-05-24`, `SRC-ESP-IDF-WIFI`, `SRC-ESP-IDF-HTTP-SERVER`, `SRC-GITHUB-PAGES-WHAT-IS` | Plan chooses Wi-Fi web first for phone and laptop and dummy-output-only first live control. | No selected board, current identity, Wi-Fi mode, browser proof, auth policy, dummy fixture, or no-relay/load/mains observation. | Stage 1 simulated UI, then selected-board read-only proof, then dummy-output gate. |
| Firmware flash/erase/monitor/serial-write expansion | blocked | live-gate policy plus esptool sources | `SRC-ESPTOOL-BASIC`, `SRC-ESPTOOL-ADVANCED-VERIFY`, `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS`, `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23` | Past accepted flashes are limited to their proof packets. Current expansion is closed. | Fresh identity, backups, manifests, hashes, recovery, write confirmation, verify, and cleanup are required for any new flash. | Do not run prepare/flash/erase/monitor unless a new live gate explicitly opens it. |
| GitHub Pages public site and public docs | implemented-validated | local build/audit/smoke proof | `SRC-GITHUB-PAGES-WHAT-IS`, `SRC-GITHUB-PAGES-PUBLISHING-SOURCE`, `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`, `SRC-GITHUB-PAGES-LIMITS`, `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21` | Public-safe generated Pages artifact, manifest audit, smoke checks, and prior browser validation exist. | Does not prove live hardware, relay switching, MicroSD mount, TFT wiring, firmware flashing, XBee writes, load, or mains work. | Continue with build/audit/smoke before publication changes. |
| Four-relay board, relay, power, load, and mains lane | blocked | design/source-backed gaps | `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-1910-305` | Photo/source records exist only for visible components and candidate hazard context. | Exact board, shield schematic, regulator, relay module, trigger polarity, isolation, current, rail budget, load type, enclosure, grounding, and qualified review. | Low-voltage inspection and bench records before any relay or load work; qualified review before mains. |
| XBee lane | blocked | source-backed hardware gap | `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`, `SRC-WAVESHARE-XBEE-USB-ADAPTER`, `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18` | Candidate XBee and adapter sources exist; old local probe found no accepted serial path. | Adapter serial path, UART voltage, DIN/DOUT routing, settings backup, legal/antenna constraints, and read-only Tier A/Tier B evidence. | Run read-only XBee bench proof only after current adapter identity is verified. |
| TFT, MicroSD, expander, storage, and instrument support lanes | design-only | source-backed candidates | `SRC-LCDWIKI-R61509V-MRB2802`, `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`, `SRC-ESP-IDF-SDMMC`, `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SD-PULLUP`, `SRC-SD-ASSOCIATION-FORMATTER`, `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-FLUKE-87V`, `SRC-KEYSIGHT-E36200`, `SRC-SALEAE-LOGIC-8` | Candidate references exist for planning only. | Exact modules, wiring, voltage, boot-pin conflicts, bus pullups, address pins, card policy, and bench instrument inventory. | Create source-backed profiles and bench records before wiring or firmware dependencies. |
| Agricultural telemetry, pivot, soil, and GPS planning | design-only | external candidate sources | `SRC-LINDSAY-FIELDNET-PIVOT-MONITOR-2026-05-25`, `SRC-METER-TEROS12-2026-05-25`, `SRC-SENTEK-DRILLDROP-2026-05-25`, `SRC-IRROMETER-SOIL-SENSORS-2026-05-25`, `SRC-GEOTAB-ASSET-TRACKING-2026-05-25` | Candidate telemetry classes are source-backed. | No selected local hardware, wiring, controller protocol, calibration, units, power, voltage, isolation, connector, GPS integration, or live-proof plan. | Source-backed hardware profile and protocol ADR before implementation. |

## Closed Gates

Keep firmware ABI runtime implementation, Win31 export controls, bridge export
request types, BLE, mesh, PCAP, relay/XBee, TFT, MicroSD, load, mains, erase,
monitor, and serial-write expansion closed unless a later source-backed gate
explicitly opens the exact surface.
