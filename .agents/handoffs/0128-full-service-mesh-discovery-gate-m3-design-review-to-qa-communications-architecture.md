# Handoff 0128 - Full-Service Mesh Discovery Gate M3 Design Review To QA/Communications/Architecture

Continuation record for Task 0180
`full-service-mesh-discovery-gate-m3-design-review`.

## Continue with

- Treat [../../docs/architecture/espnow-bbs-mesh-m3-firmware-mapping.md](../../docs/architecture/espnow-bbs-mesh-m3-firmware-mapping.md)
  as the M3 design review, not an implementation plan with runtime authority.
- Preserve `mesh_discovery.v1`, Gate F service codes, bridge ABI, coordinator
  serial ABI, and Win31 transport until a separate source-backed gate opens
  those surfaces.
- For any future M4 build-only adapter proof, add fixtures for mapping events,
  512-byte bridge bounds, secret rejection, live-action rejection,
  queue/custody isolation, and schema/ABI invariance.
- Keep M5 live mesh proof separate and Tier 3 only.

## Stop Gates

- No firmware runtime implementation, firmware persistence, coordinator/peer
  migration, framework changes, build proof, live ESP-WIFI-MESH, BLE pairing,
  Android app behavior, router/admin mutation, PCAP, flash, erase, monitor,
  serial writes, RF/XBee writes, relay/load/mains work, release, publication,
  commit, push, PR, deploy, `/etc/codex/requirements.toml`, or `admin-strict`
  mutation without a fresh gate.

## Validation to preserve

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 180
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
git diff --check
```
