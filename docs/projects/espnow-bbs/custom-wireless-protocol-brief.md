# Custom Wireless Protocol Brief

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## 1. Verified Facts

- [repo-verified] The accepted BBS integration path is
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
  Source IDs: `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`,
  `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`.
- [repo-verified] The bridge/operator protocol uses compact ASCII JSON lines
  with a 512-byte line budget on the Win31/Pi boundary. Source IDs:
  `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`,
  `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`.
- [repo-verified] The current radio envelope is packetized and bounded around a
  250-byte ESP-NOW payload budget, 32-byte protocol header, 190-byte body
  budget, and 16-fragment maximum. Source ID:
  `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`.
- [live-verified] The 2026-05-23 corrected live record reports four full-flash
  backups, manifest review, coordinator plus `peer01`/`peer02`/`peer03`
  flash/verify evidence, three `espnow-enc` peers over `serial-nullmodem`,
  moving RX/TX/ACK counters, Win31 runtime evidence, and cleanup. Source ID:
  `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`.
- [repo-verified] The current LAN/current-remap source record reports a
  post-cleanup read-only preflight `ok:true` for Pi `192.168.200.153`,
  coordinator `/dev/ttyUSB0`, and peers `COM6`/`COM10`/`COM12`; it does not
  prove a fresh BBS runtime run. Source ID:
  `SRC-LOCAL-ESPNOW-LAN-DHCP-CURRENT-REMAP-2026-05-25`.
- [live-verified] The 2026-05-25 structured Gate H rerun captured
  `bridge-transcript.jsonl`, passed the DOS-C vision gate, passed the ESP32
  completion gate, and cleaned up stale runtime state. Source ID:
  `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`.
- [official-source-verified] ESP-NOW is a connectionless Wi-Fi protocol that
  carries application data in vendor-specific action frames. Source ID:
  `SRC-ESP-IDF-ESPNOW`.
- [official-source-verified] ESP-NOW v1.0 packet body length is 250 bytes and
  ESP-NOW v2.0 packet body length is 1470 bytes, with compatibility limits for
  v1.0 receivers. Source ID: `SRC-ESP-IDF-ESPNOW`.
- [official-source-verified] ESP-NOW PMK/LMK encryption applies to paired
  unicast use, and encrypted multicast vendor-specific action frames are not
  supported. Source ID: `SRC-ESP-IDF-ESPNOW`.
- [official-source-verified] ESP-NOW send callback success is MAC-layer status,
  not application delivery proof, so app ACK, timeout, retransmit, sequence,
  and duplicate handling are required for reliable application delivery. Source
  ID: `SRC-ESP-IDF-ESPNOW`.
- [official-source-verified] Vendor sources establish candidate agricultural
  telemetry classes for remote center-pivot monitoring, soil moisture and soil
  water tension probes, SDI-12 or Modbus probe integration, and GPS asset
  tracking. Source IDs: `SRC-LINDSAY-FIELDNET-PIVOT-MONITOR-2026-05-25`,
  `SRC-METER-TEROS12-2026-05-25`,
  `SRC-SENTEK-DRILLDROP-2026-05-25`,
  `SRC-IRROMETER-SOIL-SENSORS-2026-05-25`,
  `SRC-GEOTAB-ASSET-TRACKING-2026-05-25`.

## 2. Unknowns / Required Evidence

- [unknown] No accepted project payload schema exists for direct wireless BBS
  messages, file chunks, interval telemetry, agricultural telemetry, GPS pivot
  positioning, GPS asset tracking, or client analytics. Required evidence:
  accepted ADR or protocol document plus simulator tests.
- [unknown] No local hardware profile exists for any center-pivot controller,
  soil moisture probe, SDI-12/Modbus adapter, GPS receiver, or asset tracker.
  Required evidence: source-backed hardware profile with power, voltage,
  boot-pin, isolation, connector, and protocol notes.
- [unknown] No live proof exists for chunked BBS message delivery, live file
  transfer, agricultural telemetry, GPS packet delivery, or reporting analytics
  over ESP-NOW. Required evidence: simulator proof first, then a separately
  authorized live-gate run.
- [unknown] No current same-session live identity, bridge runtime state, or
  Win31/OPCON UI state was captured for this brief. Required evidence:
  `scripts/live_bench_preflight.py` output plus bridge transcript and Win31
  proof in the same session as any live acceptance claim.
- [unknown] No security provisioning, key rotation, or custody-retention policy
  is accepted beyond the current BBS spool and Gate G export policy. Gate G
  local-admin redacted JSON export is accepted by `ADR-0005`, but Win31 export
  controls, firmware export ABI, and live bridge export request types remain
  unresolved. Required evidence: source-backed ADR and test plan.

## 3. Streaming vs Packetized Decision Matrix

| Operation class | Decision | Evidence boundary |
| --- | --- | --- |
| Interactive BBS UI | [inference] Keep streaming line I/O on the accepted COM1/nullmodem/Pi bridge path. | [repo-verified] The accepted path and 512-byte line budget are already documented by `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`. |
| Direct messaging | [inference] Model wireless delivery as packetized radio jobs with Pi-owned durable custody. | [official-source-verified] ESP-NOW is bounded action-frame transport, not transparent serial, per `SRC-ESP-IDF-ESPNOW`. |
| File transfer | [inference] Model files as cataloged chunks with checksums, resume state, and custody ACKs. | [repo-verified] The existing envelope and bridge spool sources already separate bounded radio payloads from stream UI. |
| Interval telemetry | [inference] Model telemetry as compact reports with class, cadence, priority, and link-status metadata. | [official-source-verified] Ag sensor and asset-tracking classes are source-backed, but local schemas are not accepted. |
| Node/client status | [inference] Keep node health/status as packetized radio telemetry summarized through the bridge UI. | [repo-verified] Existing status fields and peer counters already support operations visibility. |
| Analytics/reporting | [inference] Generate reports from Pi bridge/spool records before firmware-resident analytics. | [repo-verified] `ADR-0005` accepts only local-admin redacted JSON export from the DOS-C/Pi bridge spool for v1. |
| Mesh/BLE/PCAP/router/admin/relay | [assumption] Keep out of scope for this protocol brief. | [repo-verified] Live-gate docs keep those lanes closed unless a later explicit gate opens them. |

## 4. Proposed Protocol Model

- [assumption] Public interface additions are documentation-first service
  classes: `direct_message`, `file_chunk`, `telemetry_report`, `node_status`,
  `custody_ack`, and `control_intent`.
- [inference] Layer 0 is the bridge stream boundary: newline ASCII JSON,
  maximum 512 bytes, operator requests/responses, and no transparent ESP-NOW
  stream.
- [inference] Layer 1 is the bounded radio envelope: version, frame type,
  flags, source ID, destination ID, message ID, sequence number, fragment
  index/count, TTL, ACK target/status, body, and integrity field.
- [inference] Layer 2 is the service semantic layer: message custody, file
  chunking, telemetry batching, node status, and non-executing control intents.
- [assumption] v1 uses ESP-NOW v1-compatible 250-byte budgeting until every
  participating device and test fixture explicitly accepts a larger format.
- [inference] Reliability requires application ACKs, retry windows, duplicate
  suppression, TTL expiry, final custody status, and bridge-visible failure
  reasons.
- [inference] Security defaults to encrypted unicast with peer allowlists when
  live keys are provisioned; broadcast/discovery payloads must not contain
  secrets.
- [unknown] Authentication beyond PMK/LMK, key rotation, replay windows, and
  analytics privacy are not accepted design facts yet.

## 5. Direct Messaging Model

- [inference] The Pi bridge owns durable message IDs, user inbox/outbox state,
  search, pull, post, ACK, and delivery status.
- [inference] Wireless direct messages use one or more bounded radio frames
  addressed by peer ID or route ID; delivery state is reported back to the Pi
  bridge.
- [assumption] Delivery states are `queued`, `sent`, `delivered`, `acked`,
  `failed`, and `expired` until an ADR renames or extends them.
- [assumption] OPCON/Win31 continues to use compact bridge responses rather
  than direct radio framing.
- [unknown] User identity, message retention, search indexing, and private
  message authorization require a separate BBS data-policy record.

## 6. File Transfer Model

- [inference] Files use a Pi-owned catalog with `file_id`, display name, size,
  chunk count, checksum/hash, per-chunk status, and final verification state.
- [inference] Radio transfer uses bounded `file_chunk` frames and compact ACK
  bitmaps or missing-range requests.
- [assumption] File chunks must fit the current body budget after all headers
  and integrity fields are reserved.
- [assumption] Resume starts from the receiver's missing chunk map, not from a
  stream offset.
- [unknown] File size limits, compression, storage retention, malware scanning,
  and operator approval policy are not accepted.

## 7. Interval Telemetry Model

- [inference] Common telemetry fields are node ID, report class, sequence,
  cadence, priority, sensor profile ID, values, units, power status, link
  status, RSSI, and error flags.
- [inference] Center-pivot telemetry candidate fields include pivot state,
  alert state, tower/alignment fault summary, and selected-equipment sensor
  values after hardware-source verification.
- [official-source-verified] Lindsay FieldNET/Pivot Watch sources support
  remote pivot monitoring, real-time alerts, and compatibility claims for
  monitored pivot systems. Source ID:
  `SRC-LINDSAY-FIELDNET-PIVOT-MONITOR-2026-05-25`.
- [official-source-verified] METER TEROS 12 supports soil moisture,
  temperature, EC, and SDI-12 communication options. Source ID:
  `SRC-METER-TEROS12-2026-05-25`.
- [official-source-verified] Sentek Drill and Drop supports moisture,
  temperature, optional salinity, RS232, RS485, SDI-12, and Modbus telemetry
  integration options. Source ID: `SRC-SENTEK-DRILLDROP-2026-05-25`.
- [official-source-verified] IRROMETER sources support soil water tension
  sensor classes and electronic or SDI-12 adapter integration. Source ID:
  `SRC-IRROMETER-SOIL-SENSORS-2026-05-25`.
- [official-source-verified] Geotab sources support GPS asset tracking for
  vehicles, trailers, containers, heavy equipment, and utilization reporting.
  Source ID: `SRC-GEOTAB-ASSET-TRACKING-2026-05-25`.
- [hypothesis] GPS pivot positioning, pump status, weather station packets,
  pressure/flow telemetry, tank level, enclosure tamper, battery/solar
  telemetry, and service truck or equipment location are candidate
  interval-data classes until selected
  hardware and source-backed profiles exist.

## 8. BBS Integration Plan

- [inference] Preserve the accepted serial-nullmodem path as the only live BBS
  integration boundary for this design.
- [inference] Keep the Pi bridge as the translation boundary between stream UI,
  durable BBS spool, and packet radio jobs.
- [inference] Keep physical coordinator serial behavior read-mostly for
  `hello`, `state`, `diag`, and `peer_list` until a separate gate authorizes
  state-changing serial commands.
- [inference] Expose direct-message, file, telemetry, and node-status summaries
  through compact bridge responses that fit the Win31 line budget.
- [assumption] Client/user reporting and analytics are generated from bridge
  records first, not from ESP32 firmware state.
- [repo-verified] Gate G simulator analytics remain fixture coverage for
  counters, custody rollups, file rollups, telemetry rollups, and fixture-only
  client/user summary fields.
- [repo-verified] `ADR-0005` is accepted as the Gate G live analytics export
  policy. It allows only local-admin redacted JSON export using
  `gate-g.analytics.v1` and `adr-0005-redacted-local-operator-v1`, with 7-day
  stale-export cleanup.
- [repo-verified] Gate G live export is open only as the DOS-C/Pi local-admin
  export from a file-backed bridge spool into ignored proof/runtime roots. It
  remains closed to Win31/OPCON controls, firmware ABI/runtime export behavior,
  and bridge request types.

## 9. Test and Acceptance Plan

- [inference] Simulator tests come first: line-size enforcement, ASCII/JSON
  compatibility, radio envelope encode/decode, fragmentation/reassembly,
  ACK/retry/dedupe, TTL expiry, direct-message custody, file resume, telemetry
  batching, and reporting fixtures.
- [inference] Live proof stays separate from simulator proof: fresh same-session
  read-only preflight, identity match, backups, manifest review, explicit
  write authorization if firmware changes exist, bridge transcript, Win31/OPCON
  visual corroboration, and cleanup proof.
- [assumption] Live acceptance requires transcript evidence for direct message,
  file transfer, interval telemetry, node status, error handling, zero serial
  errors, and expected moving counters.
- [repo-verified] Gate H live acceptance is recorded separately in
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-H-LIVE-ACCEPTANCE-2026-05-25`
  for the accepted serial-nullmodem path after fresh preflight and cleanup
  proof. The later structured Gate H live acceptance is recorded in
  `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` and should be
  treated as the stronger current proof because it uses
  `bridge-transcript.jsonl`.

## 10. Risks / Non-Goals

- [risk] Treating ESP-NOW as transparent serial can hide packet loss,
  duplication, ordering, payload-size, and custody failures.
- [risk] Treating MAC-layer send success as delivery can overclaim BBS message,
  file, or telemetry acceptance.
- [risk] Agricultural sensor integration can create unverified power, voltage,
  isolation, protocol, connector, or environmental assumptions unless hardware
  profiles are sourced first.
- [risk] Analytics/reporting can expose operational or client data unless
  retention, redaction, export, storage, operator access, and cleanup policy is
  accepted.
- [non-goal] This brief does not authorize flashing, serial writes, relay
  control, XBee work, router/admin action, PCAP, BLE pairing, ESP-WIFI-MESH
  live action, erased flash, monitor automation, or framework migration.

## 11. Source Ledger

- [repo-verified] Local source ledger for this brief:
  `knowledge-base/source-ledger/2026-05-25-custom-wireless-protocol-brief.md`.
- [repo-verified] Existing local protocol/live evidence source IDs:
  `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`,
  `SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`,
  `SRC-LOCAL-ESPNOW-LIVE-PREFLIGHT-2026-05-23`,
  `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`.
- [official-source-verified] ESP-NOW source ID: `SRC-ESP-IDF-ESPNOW`.
- [official-source-verified] Agricultural and GPS source IDs:
  `SRC-LINDSAY-FIELDNET-PIVOT-MONITOR-2026-05-25`,
  `SRC-METER-TEROS12-2026-05-25`,
  `SRC-SENTEK-DRILLDROP-2026-05-25`,
  `SRC-IRROMETER-SOIL-SENSORS-2026-05-25`,
  `SRC-GEOTAB-ASSET-TRACKING-2026-05-25`.

## 12. Next-Step Implementation Plan With Explicit Gates

- [repo-verified] Gate B simulator protocol proof, Gate C bridge-adapter proof,
  Gate D DOS-C fixture pairing, Gate E draft bridge ABI, Gate F accepted
  firmware ABI design contract, Gate G simulator analytics, Gate G
  local-admin redacted export, Gate H structured transcript, and Gate H
  structured live acceptance are all recorded in source-index IDs.
- [accepted-design-contract] Gate F firmware ABI now has accepted `ADR-0006`,
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-FIRMWARE-ABI-2026-05-26`,
  and `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
  but remains unresolved for runtime packet/job queues, persistence, scheduler,
  migration, recovery, and live proof.
- [blocked-until-evidence] Ag telemetry payloads, GPS pivot positioning, GPS
  asset tracking, analytics surfaces beyond ADR-0005 local-admin export,
  selected sensors, power/voltage/isolation notes, and retention policies
  remain unresolved until source-backed profiles and ADRs exist.
