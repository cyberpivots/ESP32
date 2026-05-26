# Handoff 0041 - ESP-NOW BBS LAN DHCP Role Recovery Cleanup Resolved

Task:
[../TASK_LOG/0052-espnow-bbs-lan-dhcp-role-recovery.md](../TASK_LOG/0052-espnow-bbs-lan-dhcp-role-recovery.md)

## Summary

The bench network is in LAN DHCP mode instead of Windows ICS mode, and the
current peer role map is verified as `peer01=COM6`, `peer02=COM10`,
`peer03=COM12`. Pi `/dev/ttyUSB0` is coordinator MAC `78:e3:6d:10:4d:6c`, so
do not run recovery flashing.

## Cleanup Outcome

Fresh SSH keyscan/known-hosts verification on 2026-05-26 UTC matched the
expected Pi fingerprints. The only pre-cleanup related Pi process was:

`1346 dosbox-x -conf /home/dospi/dos-c/devices/pi4-poe/win31.conf -nomenu -fullscreen`

A normal `SIGTERM` removed that exact PID. No `SIGKILL` was used. Post-cleanup
checks found no related DOSBox-X, DOSBox, bridge, modal, or
`31331`/`31332`/`8080` listener state.

## Current Gate State

Post-cleanup read-only preflight passed:

```bash
python3 scripts/live_bench_preflight.py \
  --pi-host 192.168.200.153 \
  --allow-discovered-pi-host \
  --current-peer-remap \
  --summary \
  --out research/bench-records/live-bench/espnow-bbs-lan-dhcp-current-remap-preflight-YYYYMMDDTHHMMSSZ.json
```

Evidence:
`research/bench-records/live-bench/espnow-bbs-lan-dhcp-current-remap-preflight-20260526T032217Z.json`
returned `ok:true` with no failures and summary readiness `ready_for_prepare`.

If work continues, proceed only with a newly requested read-only proof or a
separately authorized gated action. The current coordinator role does not
require flashing.

## Closed Lanes

Keep prepare, flash, erase, monitor, serial-write expansion, PCAP,
router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load, and mains
closed.
