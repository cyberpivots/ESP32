# Research Triage Status

| Area | Status | Next action |
| --- | --- | --- |
| Canonical development status | Current | Use [development status ledger](development-status-ledger.md) for current lane status and superseded blocker links. |
| ESP-NOW BBS live proof | Accepted-live | Treat `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` as the current authoritative structured proof packet. |
| ESP-NOW BBS LAN/current remap | Implemented-validated | Use `SRC-LOCAL-ESPNOW-LAN-DHCP-CURRENT-REMAP-2026-05-25` only as read-only preflight/cleanup evidence; rerun proof gates before new live acceptance. |
| Gate G analytics export | Accepted-live, limited | Keep open only for local-admin redacted JSON export under accepted `ADR-0005`; Win31 controls, firmware ABI runtime behavior, and bridge request types remain closed. |
| Custom wireless Gate B/C/D | Implemented-simulator-only | Continue simulator and DOS-C fixture work without claiming live radio or runtime bridge acceptance. |
| Custom wireless Gate E/F ABI | Gate F accepted-design-contract | Gate E is draft bridge ABI; Gate F `ADR-0006` is accepted as a design contract only with host packet golden vectors; runtime implementation and live proof remain closed. |
| Firmware framework | Open outside accepted project ADRs | Keep workspace framework-neutral except accepted project ADRs; write ADR comparison before any new framework decision. |
| XBee `XBP9B-DPUT-001 RevF` | Blocked | Verify Waveshare adapter serial path, voltage, DIN/DOUT routing, settings backup, and operating constraints before reads or writes. |
| Relay boards/load/mains | Blocked | Identify exact module and complete low-voltage evidence before relay action; require qualified review before mains/load work. |
| Photographed ESP32 board/shield | Partial | Identify dev-board vendor/revision, shield schematic, jumper position, power path, and GPIO continuity. |
| TFT/MicroSD/expander/storage | Design-only | Create exact module/card/bus/pin records before wiring, driver selection, or firmware dependencies. |
| BLE, Web Bluetooth, Web Serial, PCAP, mesh | Closed | Keep behind separate live gates with current identity, rollback, source-backed config, proof packet, and cleanup evidence. |
| Agricultural telemetry profiles | Design-only | Select source-backed hardware profiles before schemas, wiring, or live telemetry proof. |
| Heltec WiFi LoRa 32(V2) | Partial | Confirm physical revision and pin map. |
| Prompt/model routing | Seeded | Convert governance docs into tooling when needed. |
