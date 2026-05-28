# ESP-NOW BBS UI-0/M2-B Host-Only Slice

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This packet starts the BBS UI System Operation Improvement Program with two
host-only slices:

- UI-0: ranked operator-facing improvements for Win31/CBBS clarity.
- M2-B: Network/Services UX proof for existing host-only discovery summaries.

The accepted live path remains unchanged:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

This slice does not change runtime public APIs, firmware ABI, bridge ABI,
coordinator serial ABI, `mesh_discovery.v1`, Gate F service codes, or Win31
transport.

## Verified Facts

- `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28` records UI-0 and
  M2-B as the lowest-risk next BBS UI slices.
- `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-GATE-M2A-DOSC-2026-05-27`
  records existing DOS-C companion support for `discovery_snapshot`,
  `discovery_events`, `service_catalog`, and `capability_report`.
- DOS-C commit `7f0b5df` records the paired UI-0/M2-B host-only operator
  wording and source-test slice. DOS-C commit `7819b93` refreshes the paired
  BBS records after a later unrelated offgrid submodule pointer update allowed
  the broad DOS-C scaffold check to pass.
- DOS-C `m2a.discovery.v1` is companion output derived from the ESP32 host
  `mesh_discovery.v1` contract. This slice does not change
  `mesh_discovery.v1`.
- Existing M2-A tests keep discovery responses ASCII, schema-versioned,
  no-secret-field, bounded to 512-byte bridge lines, and out of coordinator
  serial ABI files.
- The DOS-C UI source now states that Network/Services summaries are
  host-only/read-only, the 512-byte bridge line remains the limit, and routes,
  BLE, admin, serial, and link changes require separate gates.

## Assumptions

- UI-0 can use existing tracked UI backlogs and source records to rank
  operator-facing improvements without requiring a fresh screenshot packet.
- M2-B proof can be host-only because it validates existing DOS-C bridge and
  operator behavior, not live ESP-WIFI-MESH, BLE, or firmware mapping.

## Unknowns

- No fresh copied Win31 screenshot/OCR/CV packet was captured by this slice.
- No Client-1 static/simulated browser proof or Client-2 selected-board live
  Wi-Fi proof exists.
- No firmware mapping review from ESP-WIFI-MESH APIs/events into
  `mesh_discovery.v1` is accepted.
- No live mesh, BLE, Android app, router/admin, PCAP, flash, serial-write,
  relay, XBee, TFT, MicroSD, load, mains, dummy-output, release, or cleanup
  evidence was captured.

## UI-0 Ranked Packet

| Rank | Improvement | Source basis | Acceptance for this slice |
| ---: | --- | --- | --- |
| 1 | Make Network/Services explicitly host-only and read-only. | M2-A DOS-C support plus BBS UI program. | Done in DOS-C commit `7f0b5df`; source-tested wording exists. |
| 2 | Keep disabled or advanced controls paired with the owner gate that can open them. | Win31 interface backlog and live-gate boundaries. | Carried into Network/Services wording; broader controls remain future UI work. |
| 3 | Preserve transcript-first proof language. | Gate H structured acceptance and legibility backlog. | This packet states screenshots/OCR/CV remain corroboration only. |
| 4 | Keep schema and bridge-line constraints visible to operators. | M2-A 512-byte/schema proof. | Done for Network/Services; future views can reuse the pattern. |
| 5 | Continue reducing footer/log density from copied evidence. | Win31 legibility backlog. | Deferred until a later copied-evidence UI pass. |

## M2-B Proof Packet

| Boundary | Evidence | Result |
| --- | --- | --- |
| Read-only request set | Existing M2-A request names only: `discovery_snapshot`, `discovery_events`, `service_catalog`, `capability_report`. | No new request names accepted. |
| Bridge line budget | DOS-C bridge tests assert encoded discovery responses are `<= 512` bytes before newline. | Host-only pass in DOS-C validation. |
| Secret/body exclusion | DOS-C bridge tests assert no secret fields and no raw private message body in discovery responses. | Host-only pass in DOS-C validation. |
| Schema distinction | UI wording distinguishes DOS-C `m2a.discovery.v1` companion output from ESP32 `mesh_discovery.v1`. | Host-only pass in DOS-C source test. |
| Coordinator serial ABI | DOS-C source guard asserts the request names are absent from `coordinator_protocol.py` and firmware serial protocol headers. | Host-only pass in DOS-C validation. |
| Operator wording | DOS-C source test asserts host-only/read-only/512-byte/no-link-change wording. | Host-only pass in DOS-C validation. |

## Validation Plan

- ESP32 scaffold and agent-process checks.
- ESP32 custom wireless protocol tests.
- ESP32 Win31 legibility analyzer tests.
- GitHub Pages build, manifest audit, and smoke checks because
  `knowledge-base/source-index.md` is public-bundle input.
- Changed-file source-ID, link, and closed-surface scans.
- DOS-C paired validation recorded in DOS-C commit `7f0b5df`.
- `git diff --check`.

## Stop Gates

Runtime public API changes, firmware ABI changes, bridge ABI changes,
coordinator serial ABI changes, Gate F service-code changes,
`mesh_discovery.v1` schema changes, Win31 transport changes, live browser
proof, firmware runtime migration, live mesh, BLE pairing, Android app
behavior, PCAP, router/admin mutation, flash, erase, monitor, serial-write
expansion, physical serial writes, relay, XBee, TFT, MicroSD, load, mains,
dummy-output control, release gating, and cleanup acceptance remain closed.
