# Cross-Project Client UI Live-Gate

Source index: [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)

## Scope

This document defines a source-backed live-gate plan for improving ESP32
hardware/software dashboard UX across current project lanes. It is a design
artifact only.

It does not add firmware, framework files, web UI code, BLE code, Android code,
serial client code, flash commands, erase commands, router administration, PCAP
work, relay wiring, load wiring, or mains work.

The accepted ESP-NOW BBS dashboard path remains:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

The client UI plan must be additive to that path, not a replacement. Source
IDs: `SRC-LOCAL-DOSC-ESPNOW-BBS-BRIDGE-2026-05-20`,
`SRC-LOCAL-ESPNOW-NETWORK-LIVE-GATE-2026-05-23`,
`SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`.

## Verified Facts

- ESP-IDF HTTP Server supports running a lightweight web server on ESP32,
  URI handlers, and REST-style API/web-serving examples. Source IDs:
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`.
- ESP-IDF Wi-Fi documentation includes station mode, SoftAP mode, and
  concurrent station/AP mode. Source ID: `SRC-ESP-IDF-WIFI`.
- ESP-IDF Wi-Fi provisioning manager examples cover configuring ESP32 as a
  Wi-Fi station with supplied credentials, with Bluetooth LE as the default
  provisioning transport in the referenced example. Source ID:
  `SRC-ESP-IDF-WIFI-PROVISIONING-2026-05-24`.
- ESP-IDF Bluetooth LE documentation exposes GAP, GATT define, GATT server,
  and GATT client API surfaces. Source ID: `SRC-ESP-IDF-BLE-API`.
- Android BLE documentation describes Android central-role BLE support and
  separates central/peripheral roles from GATT client/server roles; the phone
  can scan as central and act as GATT client while the peripheral fulfills GATT
  requests as server. Source ID: `SRC-ANDROID-BLE-OVERVIEW`.
- MDN documents Web Serial as limited-availability, secure-context API access
  for websites to read from and write to serial devices, including USB or
  Bluetooth devices that emulate serial ports. Source ID:
  `SRC-MDN-WEB-SERIAL-2026-05-24`.
- MDN documents Web Bluetooth as limited-availability and experimental,
  secure-context API access for connecting to BLE peripherals, with explicit
  permission and Permissions-Policy considerations. Source ID:
  `SRC-MDN-WEB-BLUETOOTH-2026-05-24`.
- ESP-IDF GPIO documentation covers GPIO, strapping, flash/PSRAM pin, UART0,
  and input-only caveats that must be reviewed before selecting any dummy
  output pin. Source ID: `SRC-ESP-IDF-GPIO`.
- Saleae Logic 8 is only a candidate logic-analyzer class source in this
  workspace, not a required purchase or selected fixture. Source ID:
  `SRC-SALEAE-LOGIC-8`.

## Assumptions

- First user-facing proof target is Wi-Fi browser access from phone and laptop.
- The first Wi-Fi proof may use ESP32 SoftAP or local LAN, but the exact mode,
  SSID, authentication, addressing, and provisioning flow are not accepted yet.
- BLE and Serial/UART clients are staged fallback or parity paths, not first
  live-proof paths.
- Future implementation will route every client transport through one shared
  safety supervisor instead of letting any transport own hardware authority.
- First state-changing proof is dummy-output only after a separate live gate
  selects the board, GPIO, fixture, observation method, and rollback path.

## Unknowns

- Exact target board, USB-UART path, firmware build, and current board identity
  for the first client UI proof.
- Exact power source, rail voltage, boot-pin exposure, attached peripherals,
  isolation boundary, and recovery method for the selected target.
- Exact Wi-Fi mode, SSID, credential handling, SoftAP/LAN addressing, browser
  support matrix, and phone/laptop viewport acceptance packet.
- Exact dummy-output GPIO, LED or logic-analyzer fixture, inactive state, boot
  behavior, and observation record.
- BLE service UUIDs, characteristic UUIDs, properties, permissions, bonding or
  pairing policy, Android API level, target SDK, and app-layer security.
- Serial/UART visual-client shape, framing, permission model, read-only versus
  write-capable commands, and recovery interaction.
- Wi-Fi plus BLE coexistence behavior on the selected board and firmware.
- Authentication, anti-replay, per-client sequence storage, and audit-log
  retention policy for browser/API clients.

## Client Interface Method Matrix

| Method | First use | Authority model | Gate status |
| --- | --- | --- | --- |
| Wi-Fi browser | ESP32 HTTP server with REST state/control endpoints, reached from phone and laptop browser by SoftAP or local LAN. | Browser actions submit requests; one shared safety supervisor accepts or rejects them. | First priority. Stage 1 simulated, Stage 2 read-only live, Stage 3 dummy-output only. |
| BLE GATT | Android phone as BLE central/GATT client; ESP32 as peripheral/GATT server. | BLE characteristics mirror the same state/control authority and must not bypass the supervisor. | Design-only until a separate BLE live proof accepts UUIDs, permissions, security, pairing, and coexistence evidence. |
| Serial/UART | Diagnostics and recovery-compatible visual clients, including future browser Web Serial experiments where supported. | Serial clients use the same command model, source-transport logging, monotonic sequence, and rejection surface. | Design-only. Must preserve the accepted Win31 serial-nullmodem proof path and avoid hidden serial writes. |

## First Control Authority

The first live control gate is dummy-output only. All live controls must be
visible, reversible, logged, and rejected by default until the stage-specific
gate opens.

Allowed in Stage 1 simulated proof:

- Refresh state.
- View status and safety state.
- Display reject reasons.
- Render safety-lock, all-off, and dummy-output controls without live hardware
  mutation.

Allowed in Stage 2 read-only live proof:

- Refresh and status view only.
- Browser proof from phone and laptop.
- Read-only board/network state capture.

Allowed in Stage 3 dummy-output proof:

- Safety-lock.
- All-off.
- One explicitly selected dummy output on an LED or logic-analyzer fixture.
- Dummy-output command rejection while safety-lock is active.

Blocked until a later accepted gate:

- Relay module energizing, relay contacts, loads, and mains.
- Firmware flash, erase, monitor expansion, and hidden firmware mutation.
- Serial writes outside the accepted command path.
- PCAP, router-admin work, or replacement of the Win31 serial-nullmodem path.
- BLE pairing, Web Bluetooth live proof, or Android app live proof.
- Any control that cannot show a visible result or reject reason to the
  operator.

## Minimum API Contract

Every client transport must submit to the same state/control authority. The
transport is evidence, not authority.

| Endpoint | Method | Minimum contract |
| --- | --- | --- |
| `/api/state` | `GET` | Returns dashboard state, safety gate, source transport, active client transport, dummy-output status, last command result, last reject reason, and current state version. |
| `/api/safety-lock` | `POST` | Requires monotonic `sequence`, requested lock state, and logged source transport. Rejects stale sequence or unauthorized source. |
| `/api/all-off` | `POST` | Requires monotonic `sequence`, logs source transport, routes through safety supervisor, and returns visible result or reject reason. |
| `/api/dummy-output/{channel}` | `POST` | Requires monotonic `sequence`, selected channel, requested state, current dummy-fixture gate, logged source transport, and safety-supervisor approval. |

All command responses must include:

- Accepted/rejected status.
- Client-provided `sequence`.
- Current safety gate.
- Source transport recorded by the server.
- Visible result or explicit reject reason.
- Updated state version or unchanged state version on reject.

## Live-Gate Proof Ladder

### Stage 0: Source-Backed Design Only

- No code.
- No flashing.
- No wiring.
- No live browser/device claim.
- Source records, known gaps, task log, and QA handoff only.

### Stage 1: Static Or Simulated UI Proof

- Phone and laptop viewport proof with readable status, safety state, reject
  reasons, and disabled or simulated dummy-output controls.
- No live ESP32 required.
- Browser smoke checks required for any generated UI artifact.

### Stage 2: Wi-Fi Web Read-Only Live Proof

- Select one ESP32 target.
- Capture same-session board identity, USB/serial identity, power source,
  voltage/rail evidence, boot-pin/isolation review, attached-peripheral review,
  recovery path, and cleanup evidence.
- Serve or proxy read-only state to phone and laptop browser.
- Do not submit state-changing commands.

### Stage 3: Dummy-Output Control Proof

- Select exact GPIO and fixture before firmware or wiring changes.
- Verify no relay module, load, or mains path is attached.
- Capture firmware/build hashes if firmware changes.
- Prove safety-lock rejection, all-off result, dummy-output result, and cleanup.
- Observe output only through a selected LED or logic-analyzer fixture.

### Stage 4: BLE And Serial/UART Parity Plans

- Keep BLE and Serial/UART design-only until separate live gates define UUIDs,
  Android permissions, UART framing, pairing/security, coexistence, rollback,
  and acceptance evidence.

## Required Same-Session Evidence For Future Live Work

- Board identity and USB/serial mapping.
- Power source, rail voltage, boot-pin, and isolation review.
- Selected Wi-Fi mode and network/provisioning record.
- Firmware image hashes and recovery commands if firmware changes.
- Selected dummy fixture and proof that relay/load/mains paths are absent.
- Browser screenshots for phone and laptop.
- Command transcript with monotonic sequences, source transports, results, and
  reject reasons.
- Observed dummy-output result, all-off result, safety-lock rejection result,
  and cleanup evidence.

## Validation Plan

- Run `python3 scripts/verify_scaffold.py`.
- Run `git diff --check`.
- Validate any later JSON examples with `python3 -m json.tool` or repo-local
  JSON checks.
- For any later simulated UI artifact, run browser smoke checks on phone and
  laptop viewport sizes.
