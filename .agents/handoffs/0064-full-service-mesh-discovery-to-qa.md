# Handoff 0064: Full-Service Mesh Discovery To QA

## Status

ESP32 accepts `ADR-0009` as a host-only `mesh_discovery.v1` simulator and
design contract. It does not accept live mesh, BLE pairing, Android app
behavior, firmware runtime migration, router/admin mutation, serial writes, or
hardware action.

## Verified Facts

- The accepted BBS path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- `ADR-0004` remains only the proposed ESP-WIFI-MESH self-healing transport
  branch for live migration.
- `ADR-0009` adds host-only discovery records, events, compact summaries,
  service/capability catalog, BLE/Android metadata, and secret-field rejection.
- Gate F radio packet service codes and golden vectors remain unchanged.
- `discovery_snapshot`, `discovery_events`, `service_catalog`, and
  `capability_report` are simulator bridge summaries only.

## Assumptions

- Gate M2 should add DOS-C companion fixture support and a read-only Win31
  Network/Services summary before firmware mapping starts.
- Firmware mapping waits for Gate M3 owner review.

## Unknowns

- No live mesh route-table, parent, root, healing, coexistence, flash, or
  cleanup proof exists.
- No BLE UUIDs, Android package, permission proof, bonding/SMP proof,
  coexistence proof, or live GATT proof exists.
- No accepted firmware mapping from ESP-WIFI-MESH APIs/events into
  `mesh_discovery.v1` exists.

## QA Next Steps

1. Re-run the ESP32 custom wireless protocol host tests.
2. Re-run `python3 scripts/verify_scaffold.py` and `git diff --check`.
3. Confirm targeted `rg` checks find `mesh_discovery.v1`, `ADR-0009`, and
   `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27` in the expected
   durable records.
4. For Gate M2, add DOS-C companion bridge/operator fixture support without
   changing live bridge authority.

## Stop Gates

Do not open ESP32 flashing, physical serial writes, PCAP, BLE pairing,
ESP-WIFI-MESH live action, router-admin, relay/XBee, SD-card, TFT, MicroSD,
load, mains, erase, monitor, bridge/operator runtime mutation, firmware
runtime packet queues, persistence, scheduler migration, or live proof from
this handoff.
