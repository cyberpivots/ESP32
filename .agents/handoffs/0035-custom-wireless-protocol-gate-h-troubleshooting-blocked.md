# Handoff 0035 - Custom Wireless Protocol Gate H Troubleshooting Blocked

Task:
[../TASK_LOG/0046-custom-wireless-protocol-gate-h-troubleshooting.md](../TASK_LOG/0046-custom-wireless-protocol-gate-h-troubleshooting.md)

## Status

Gate H still cannot run the accepted bridge path because the Pi/router network
path is not reachable. The prior peer-COM blocker has been reduced to an
explicit remap mode gated by accepted peer MACs.

## Verified Facts

- Current peer map:
  - `peer01` MAC `94:b9:7e:da:17:d0` on `COM9`
  - `peer02` MAC `78:e3:6d:0a:90:14` on `COM6`
  - `peer03` MAC `94:b9:7e:da:9a:50` on `COM7`
- Use `--allow-peer-port-remap --windows-ports COM9 COM6 COM7` for the current
  bench state.
- Remap preflight records:
  - `research/bench-records/live-bench/espnow-bbs-gate-h-remap-preflight-20260525T131123Z.json`
  - `research/bench-records/live-bench/espnow-bbs-gate-h-remap-direct-preflight-20260525T131208Z.json`
- Both records stopped at `readiness:blocked_pi_identity`.
- `192.168.137.93` does not currently ARP or answer SSH after stale-neighbor
  cleanup.
- Temporary direct `172.16.0.250/24` probing from Windows did not reach
  `172.16.0.1` or `172.16.0.2:22`, and the temporary address was removed.
- No bridge, DOSBox-X, Win31/OPCON, flash, erase, monitor, serial-write
  expansion, PCAP, router/admin mutation, or hardware expansion action was run.

## Resume Conditions

1. Restore or verify Pi/router physical-network state.
2. Rerun read-only preflight with the current remap command and require
   `ok:true`.
3. Then run only the accepted serial-nullmodem bridge transcript,
   Win31/OPCON corroboration, and cleanup proof.

## Closed Gates

Keep PCAP, router/admin mutation, BLE, ESP-WIFI-MESH live action, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, and serial-write expansion closed.
