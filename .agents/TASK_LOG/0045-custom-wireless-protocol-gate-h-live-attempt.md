# Task Log 0045 - Custom Wireless Protocol Gate H Live Attempt

## Task

- ID: 0045-custom-wireless-protocol-gate-h-live-attempt
- Owner role: Communications, QA, Firmware, Hardware
- Status: blocked at read-only preflight
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Perform Gate H live acceptance after same-session user authorization, while
preserving the accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- Same-session user authorization for live Gate H was present on 2026-05-25.
- Gates E-G remained simulator/documentation/build-only and did not require a
  prepare or flash step before Gate H.
- Fresh read-only preflight against `dospi@192.168.137.93` wrote ignored
  record
  `research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124841Z.json`
  and reported `ok:false`, `readiness:blocked_pi_identity`.
- Fresh read-only preflight against `dospi@172.16.0.2` wrote ignored record
  `research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124920Z.json`
  and reported `ok:false`, `readiness:blocked_pi_identity`.
- Both preflights found the current CP210x Windows peer set as `COM6`,
  `COM7`, and `COM9`; the gate profile requires exactly `COM4`, `COM5`, and
  `COM6`.
- The gate script rejected an attempted port-profile override with:
  `this gate currently requires exactly COM4 COM5 COM6 in that order`.
- Read-only identity succeeded only for default-profile `COM6`, MAC
  `78:e3:6d:0a:90:14`, ESP32 profile, 4 MB flash. `COM4` and `COM5` were not
  present and did not produce valid peer identities.
- `ssh-keyscan -T 3` returned no host keys for both `172.16.0.2` and
  `192.168.137.93`.
- `ping -c 1 -W 1` to both accepted Pi addresses had 100% packet loss, and
  `nc -vz -w 2` to TCP 22 on both addresses timed out.
- Current WSL routing includes `192.168.137.0/24` on `eth0`, but the Pi did
  not answer on `192.168.137.93`.
- No bridge, DOSBox-X, Win31/OPCON run, monitor, erase, flash, serial-write
  expansion, router/admin, PCAP, BLE, mesh, relay, XBee, TFT, MicroSD, load,
  or mains action was started.

## Assumptions

- The accepted Gate H path remains the serial-nullmodem path named above until
  a later source-backed decision changes it.
- `COM7` and `COM9` are unaccepted peer candidates until a source-backed gate
  profile change or restored `COM4`/`COM5`/`COM6` bench mapping passes fresh
  identity checks.

## Unknowns

- Whether the Pi is powered, attached to the expected network segment, running
  SSH, or still using the previously accepted host keys.
- Current coordinator identity on `/dev/ttyUSB0`; it could not be checked
  because the Pi was unreachable.
- Whether `COM7` and `COM9` are the former `peer01`/`peer03` devices or a
  different hardware mix.
- Physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state for the
  current bench.

## Required Evidence To Unblock

- Restore Pi reachability and host-key verification on an accepted address.
- Restore the expected `COM4`/`COM5`/`COM6` peer mapping, or land a separate
  reviewed gate-profile change that accepts the current port map with source
  evidence.
- Rerun the fresh read-only preflight and obtain `ok:true`.
- Only after preflight passes, collect bridge transcript evidence on the
  accepted serial-nullmodem path, Win31/OPCON corroboration, and cleanup proof
  showing no DOSBox-X, modal, bridge process, or stale listener state remains.

## Handoff

Continue with
[../handoffs/0034-custom-wireless-protocol-gate-h-live-attempt-blocked.md](../handoffs/0034-custom-wireless-protocol-gate-h-live-attempt-blocked.md).
