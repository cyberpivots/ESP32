# Custom Wireless Protocol Gate H Troubleshooting - 2026-05-25

## Summary

Gate H remains blocked, but the peer-COM blocker is resolved in the preflight
tool. The current hard blocker is Pi/router physical-network reachability.

## Verified Facts

- Current peer identity:
  - `peer01` MAC `94:b9:7e:da:17:d0` on `COM9`
  - `peer02` MAC `78:e3:6d:0a:90:14` on `COM6`
  - `peer03` MAC `94:b9:7e:da:9a:50` on `COM7`
- `scripts/live_bench_preflight.py` now supports explicit
  `--allow-peer-port-remap` mode and rejects remaps unless the accepted peer
  role MAC set matches.
- Forwarded remap preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-remap-preflight-20260525T131123Z.json`.
- Direct remap preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-remap-direct-preflight-20260525T131208Z.json`.
- Both remap preflights verified peer identity and stopped at
  `readiness:blocked_pi_identity`.
- HNetCfg ICS state still reports `Wi-Fi` public and `Ethernet 3` private.
- Clearing stale ARP for `192.168.137.93` left no reachable ARP entry.
- `192.168.137.2-254` TCP 22 scan found no SSH listener.
- `192.168.1.2-254` TCP 22 scan found no SSH listener.
- Temporary Windows `172.16.0.250/24` direct-LAN probing did not reach
  `172.16.0.1` or `172.16.0.2:22`, and the address was removed.
- No local stale listener was found on `31331`, `31332`, or `8080`.
- No bridge, DOSBox-X, Win31/OPCON, flash, erase, monitor, serial-write
  expansion, PCAP, router/admin mutation, BLE, mesh, relay, XBee, TFT,
  MicroSD, load, or mains action was run.

## Assumptions

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- The current unreachable Pi state is a physical/network issue until new
  evidence shows otherwise.

## Unknowns

- Pi/router power and cabling state.
- Pi SSH state.
- Coordinator attachment on Pi `/dev/ttyUSB0`.
- Router forwarding persistence.

## Resume Command

After the Pi/router path is restored, rerun:

```bash
python3 scripts/live_bench_preflight.py \
  --pi-host 192.168.137.93 \
  --windows-ports COM9 COM6 COM7 \
  --allow-peer-port-remap \
  --summary \
  --out research/bench-records/live-bench/espnow-bbs-gate-h-remap-preflight-YYYYMMDDTHHMMSSZ.json
```

If direct LAN access is intentionally restored, use `--pi-host 172.16.0.2`
with the same peer remap flags.
