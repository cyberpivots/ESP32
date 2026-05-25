# Task Log 0046 - Custom Wireless Protocol Gate H Troubleshooting

## Task

- ID: 0046-custom-wireless-protocol-gate-h-troubleshooting
- Owner role: Communications, QA, Hardware
- Status: blocked on Pi/router physical-network reachability
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Continue Gate H troubleshooting after the authorized live attempt stopped at
read-only preflight. Resolve actionable software blockers and identify the
remaining blocker before the accepted path can run:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- The current Windows CP210x ports are `COM6`, `COM7`, and `COM9`.
- Read-only esptool identity shows the same accepted peer MAC set from the
  2026-05-23 proof, but on new COM labels:
  - `COM9` = `peer01`, MAC `94:b9:7e:da:17:d0`
  - `COM6` = `peer02`, MAC `78:e3:6d:0a:90:14`
  - `COM7` = `peer03`, MAC `94:b9:7e:da:9a:50`
- `scripts/live_bench_preflight.py` now has an explicit
  `--allow-peer-port-remap` mode. The default remains strict
  `COM4`/`COM5`/`COM6`; remap mode accepts a different three-port map only
  when read-only identity matches the accepted peer role MACs.
- Remap preflight through `192.168.137.93` wrote ignored record
  `research/bench-records/live-bench/espnow-bbs-gate-h-remap-preflight-20260525T131123Z.json`.
- Remap preflight through `172.16.0.2` wrote ignored record
  `research/bench-records/live-bench/espnow-bbs-gate-h-remap-direct-preflight-20260525T131208Z.json`.
- Both remap preflights verified the peer remap and then stopped with
  `readiness:blocked_pi_identity` because no Pi SSH host keys or coordinator
  identity could be collected.
- Windows HNetCfg still reports Internet Connection Sharing enabled with
  `Wi-Fi` as public sharing type `0` and `Ethernet 3` as private sharing type
  `1`; `SharedAccess` is running.
- After deleting the stale Windows ARP entry for `192.168.137.93`, ping did
  not re-learn the neighbor and Windows reported no ARP entry.
- WSL `ip neigh` showed `192.168.137.93` as `INCOMPLETE` after the same check.
- A bounded TCP 22 scan of `192.168.137.2-254` found no SSH listener.
- A bounded TCP 22 scan of current `192.168.1.0/24` ARP candidates and then
  `192.168.1.2-254` found no SSH listener.
- A temporary Windows `172.16.0.250/24` address on `Ethernet 3` did not reach
  `172.16.0.1` by ping or `172.16.0.2:22`, and the temporary address was
  removed.
- No local stale listener was found on `31331`, `31332`, or `8080`.
- No bridge, DOSBox-X, Win31/OPCON, flash, erase, monitor, serial-write
  expansion, PCAP, router/admin mutation, BLE, mesh, relay, XBee, TFT,
  MicroSD, load, or mains action was run.

## Assumptions

- The current COM remap is acceptable only because the accepted peer MAC set
  was freshly verified in read-only mode.
- The remaining blocker is physical/network state outside the repo: Pi power,
  router power, Ethernet cabling, router WAN/LAN attachment, or Pi SSH state.

## Unknowns

- Whether the Netgear router is powered and attached to `Ethernet 3`.
- Whether the Pi is powered, attached to the router LAN, and running SSH.
- Whether the coordinator is still attached to the Pi as `/dev/ttyUSB0`.
- Whether the prior router SSH forwarding rule still exists; router/admin was
  not opened during this iteration.

## Required Evidence To Unblock

- Re-establish a reachable Pi path at either accepted address:
  `192.168.137.93` forwarded SSH or direct `172.16.0.2`.
- Rerun:
  `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --windows-ports COM9 COM6 COM7 --allow-peer-port-remap --summary --out research/bench-records/live-bench/<fresh>.json`
  or the direct `172.16.0.2` equivalent, and require `ok:true`.
- Only after preflight passes, collect bridge transcript evidence on the
  accepted serial-nullmodem path, Win31/OPCON corroboration, and cleanup proof.

## Handoff

Continue with
[../handoffs/0035-custom-wireless-protocol-gate-h-troubleshooting-blocked.md](../handoffs/0035-custom-wireless-protocol-gate-h-troubleshooting-blocked.md).
