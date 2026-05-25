# Custom Wireless Protocol Gate H Live Attempt - 2026-05-25

## Summary

Gate H had fresh same-session user authorization, but the live acceptance run
stopped at read-only preflight. The accepted path was not launched because Pi
identity and peer enumeration were not in the required state.

## Verified Facts

- First preflight command:
  `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --out research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124841Z.json --summary`.
- Second preflight command:
  `python3 scripts/live_bench_preflight.py --pi-host 172.16.0.2 --out research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124920Z.json --summary`.
- Both preflights reported `ok:false` and `readiness:blocked_pi_identity`.
- Both preflights observed Windows CP210x peer inventory as `COM6`, `COM7`,
  and `COM9`, while the gate profile requires exactly `COM4`, `COM5`, and
  `COM6`.
- The gate script rejected `--windows-ports COM6 COM7 COM9` with:
  `this gate currently requires exactly COM4 COM5 COM6 in that order`.
- Default-profile `COM6` read-only identity passed with MAC
  `78:e3:6d:0a:90:14` and 4 MB flash. `COM4` and `COM5` were missing.
- `ssh-keyscan -T 3` returned no host keys for both accepted Pi addresses:
  `172.16.0.2` and `192.168.137.93`.
- `ping -c 1 -W 1` to both accepted Pi addresses had 100% packet loss.
- `nc -vz -w 2` to TCP 22 on both accepted Pi addresses timed out.
- `ip route` showed `192.168.137.0/24` on `eth0`, but the forwarded Pi address
  did not answer.
- No bridge, DOSBox-X, Win31/OPCON, flash, erase, monitor, serial-write
  expansion, PCAP, router/admin, BLE, mesh, relay, XBee, TFT, MicroSD, load,
  or mains action was started.

## Assumptions

- The intended Gate H path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- `COM7` and `COM9` are unaccepted by this gate until a reviewed gate-profile
  update or restored peer enumeration passes fresh identity checks.

## Unknowns

- Pi power, cabling, current IP, SSH daemon, and host-key state.
- Coordinator identity and stale listener/process state on the Pi.
- Current physical USB-only/no-load boundary.
- Whether `COM7` and `COM9` map to the previous peer boards.

## Result

Gate H remains blocked. Resume only after Pi reachability and expected peer
enumeration are restored or the gate profile is explicitly updated with source
evidence, then rerun read-only preflight to `ok:true` before any live transcript
capture.
