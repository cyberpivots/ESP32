# Custom Wireless Protocol Gate H Troubleshooting Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Scope

Authorized Gate H troubleshooting after the live attempt stopped at read-only
preflight. This iteration fixed the peer-COM remap gate and isolated the
remaining blocker to Pi/router physical-network reachability.

No bridge, DOSBox-X, Win31/OPCON, flash, erase, monitor, serial-write
expansion, PCAP, router/admin mutation, BLE, mesh, relay, XBee, TFT, MicroSD,
load, or mains action was run.

## Evidence

- Preflight remap implementation:
  `scripts/live_bench_preflight.py`.
- Preflight remap tests:
  `tests/live_bench/test_multipeer_preflight.py`.
- Ignored remap preflight through forwarded address:
  `research/bench-records/live-bench/espnow-bbs-gate-h-remap-preflight-20260525T131123Z.json`.
- Ignored remap preflight through direct address:
  `research/bench-records/live-bench/espnow-bbs-gate-h-remap-direct-preflight-20260525T131208Z.json`.
- Tracked bench record:
  `research/bench-records/live-bench/2026-05-25-custom-wireless-protocol-gate-h-troubleshooting.md`.
- Task record:
  `.agents/TASK_LOG/0046-custom-wireless-protocol-gate-h-troubleshooting.md`.
- Handoff:
  `.agents/handoffs/0035-custom-wireless-protocol-gate-h-troubleshooting-blocked.md`.

## Verified Facts

- The current CP210x COM set is `COM6`, `COM7`, and `COM9`.
- Read-only esptool identity matched accepted peer role MACs:
  `peer01` `94:b9:7e:da:17:d0` on `COM9`,
  `peer02` `78:e3:6d:0a:90:14` on `COM6`, and
  `peer03` `94:b9:7e:da:9a:50` on `COM7`.
- The default preflight still requires `COM4`, `COM5`, and `COM6`. The new
  `--allow-peer-port-remap` option permits a different three-port map only
  when the accepted peer role MAC set matches.
- Windows HNetCfg still reports `Wi-Fi` public sharing type `0`, `Ethernet 3`
  private sharing type `1`, and running `SharedAccess`.
- After stale ARP cleanup, `192.168.137.93` did not reappear as a reachable
  neighbor and TCP 22 was not reachable.
- Temporary direct-LAN probing with Windows `172.16.0.250/24` did not reach
  router `172.16.0.1` or Pi `172.16.0.2:22`; the temporary address was
  removed.
- No SSH listener was found on bounded scans of `192.168.137.2-254` or
  `192.168.1.2-254`.

## Assumptions

- The remaining blocker is outside the source tree and requires restored
  Pi/router physical-network state before the accepted path can run.

## Unknowns

- Pi power, cabling, SSH daemon state, and current coordinator attachment.
- Router power, WAN/LAN cabling, and forwarding persistence.

## Stop Gate

Do not start bridge/DOSBox-X live proof until read-only preflight passes with
`ok:true`.
