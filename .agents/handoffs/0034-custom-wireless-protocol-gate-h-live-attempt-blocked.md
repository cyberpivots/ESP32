# Handoff 0034 - Custom Wireless Protocol Gate H Live Attempt Blocked

Task:
[../TASK_LOG/0045-custom-wireless-protocol-gate-h-live-attempt.md](../TASK_LOG/0045-custom-wireless-protocol-gate-h-live-attempt.md)

## Status

Gate H had fresh user authorization on 2026-05-25 but is blocked before live
bridge/DOSBox-X execution because the read-only preflight failed.

## Verified Facts

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Preflight records:
  - `research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124841Z.json`
  - `research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124920Z.json`
- Both records reported `ok:false` and `readiness:blocked_pi_identity`.
- The current CP210x peer inventory is `COM6`, `COM7`, and `COM9`; the gate
  profile requires `COM4`, `COM5`, and `COM6`.
- `ssh-keyscan`, `ping`, and TCP 22 probes did not reach `172.16.0.2` or
  `192.168.137.93`.
- No live bridge, DOSBox-X, Win31/OPCON, flash, erase, monitor, or serial-write
  action was run.

## Resume Conditions

1. Restore Pi SSH reachability and host-key verification on an accepted address.
2. Restore expected peer enumeration or make a reviewed source change to the
   gate profile before using a different COM map.
3. Rerun `scripts/live_bench_preflight.py` and require `ok:true`.
4. Then run only the accepted serial-nullmodem transcript, Win31/OPCON
   corroboration, and cleanup proof steps.

## Closed Gates

Keep PCAP, router/admin, BLE, ESP-WIFI-MESH live action, relay, XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, and bridge
mutation outside the accepted read-only transcript path closed.
