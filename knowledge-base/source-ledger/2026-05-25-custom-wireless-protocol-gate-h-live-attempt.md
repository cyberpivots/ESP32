# Custom Wireless Protocol Gate H Live Attempt Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Scope

Live Gate H acceptance attempt for the custom wireless protocol sequence after
fresh same-session user authorization. The intended accepted path was:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

The gate stopped during read-only preflight. No live bridge, DOSBox-X,
Win31/OPCON, flash, erase, monitor, serial-write expansion, PCAP,
router/admin, BLE, mesh, relay, XBee, TFT, MicroSD, load, or mains action was
started.

## Evidence

- Ignored preflight record for `dospi@192.168.137.93`:
  `research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124841Z.json`.
- Ignored preflight record for `dospi@172.16.0.2`:
  `research/bench-records/live-bench/espnow-bbs-gate-h-preflight-20260525T124920Z.json`.
- Read-only diagnostics:
  `ssh-keyscan -T 3 172.16.0.2`,
  `ssh-keyscan -T 3 192.168.137.93`,
  `ping -c 1 -W 1 172.16.0.2`,
  `ping -c 1 -W 1 192.168.137.93`,
  `nc -vz -w 2 172.16.0.2 22`,
  `nc -vz -w 2 192.168.137.93 22`, and `ip route`.
- Tracked bench summary:
  `research/bench-records/live-bench/2026-05-25-custom-wireless-protocol-gate-h-live-attempt.md`.
- Task record:
  `.agents/TASK_LOG/0045-custom-wireless-protocol-gate-h-live-attempt.md`.
- Handoff:
  `.agents/handoffs/0034-custom-wireless-protocol-gate-h-live-attempt-blocked.md`.

## Verified Facts

- Both preflight records reported `ok:false` and
  `readiness:blocked_pi_identity`.
- Windows CP210x inventory exposed `COM6`, `COM7`, and `COM9`, while the gate
  profile requires exactly `COM4`, `COM5`, and `COM6`.
- The gate script rejected a different port order with:
  `this gate currently requires exactly COM4 COM5 COM6 in that order`.
- Default-profile `COM6` read-only identity passed as an ESP32 with MAC
  `78:e3:6d:0a:90:14` and 4 MB flash. Default-profile `COM4` and `COM5` were
  absent and did not produce valid peer identities.
- `ssh-keyscan` returned no host keys for `172.16.0.2` or `192.168.137.93`.
- Ping to both accepted Pi addresses reported 100% packet loss, and TCP 22
  probes to both addresses timed out.
- Current routing showed `192.168.137.0/24` on `eth0`, but no Pi response was
  observed at `192.168.137.93`.

## Assumptions

- The accepted serial-nullmodem path remains the only Gate H path until a later
  source-backed decision changes it.
- The current `COM7` and `COM9` devices are not accepted as peer replacements
  by this attempt because the gate profile and fresh identity evidence do not
  accept that map.

## Unknowns

- Pi power, cabling, IP assignment, SSH daemon state, and host-key state.
- Current coordinator identity on `/dev/ttyUSB0`.
- Whether `COM7` and `COM9` are the earlier physical peer boards or a different
  hardware mix.
- Physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state.

## Stop Gate

Do not proceed to bridge transcript, Win31/OPCON corroboration, or cleanup
acceptance until the read-only preflight passes with `ok:true`.
