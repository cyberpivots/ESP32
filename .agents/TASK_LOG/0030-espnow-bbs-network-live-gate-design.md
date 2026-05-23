# Task 0030: ESP-NOW BBS Network Live-Gate Design

Status: implemented as design and simulator metadata slice

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Add a source-backed live-gate design for improving the Windows 3.1 dashboard
network lane while preserving the accepted path:

`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`

## Scope

Included:

- Proposed ADR for ESP-WIFI-MESH as the future self-healing branch.
- Source-backed design packet for ESP-NOW limits, ESP-WIFI-MESH self-healing,
  BLE GATT Android integration, and RF coexistence risk.
- Compact optional bridge fields for simulator-first Win31 dashboard proof.
- Paired DOS-C bridge/operator updates for a read-only Network view and
  simulator metadata.

Excluded:

- Live flashing, ESP-WIFI-MESH radio run, BLE pairing, Android app build,
  router changes, PCAP, packet-driver work, serial writes, relay, XBee, TFT,
  MicroSD, load, or mains work.

## Validation

- Source index and docs/index updated.
- `python3 scripts/verify_scaffold.py` passed in `/mnt/h/ESP32`.
- `bash tests/espnow_bbs_bridge/run_tests.sh` passed in `/mnt/h/dos-c`.
- `bash tests/win31_operator/run_host_tests.sh` passed in `/mnt/h/dos-c`.
- `software/win31-operator/build-watcom.sh` rebuilt `OPCON.EXE` in
  `/mnt/h/dos-c`.
- `git diff --check` passed in both `/mnt/h/ESP32` and `/mnt/h/dos-c`.
- Live acceptance remains blocked by the later live-gate evidence packet.

## Handoff

Use [../handoffs/0020-espnow-bbs-network-live-gate-to-qa.md](../handoffs/0020-espnow-bbs-network-live-gate-to-qa.md).
