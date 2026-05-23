# Handoff 0021: ESP-NOW BBS Live Implementation Prepare Gate

Task: [../TASK_LOG/0031-espnow-bbs-live-implementation-preflight.md](../TASK_LOG/0031-espnow-bbs-live-implementation-preflight.md)

## Continue With

- Use the accepted SSH-forwarded Pi access path `dospi@192.168.137.93` unless
  direct `172.16.0.2` routing is deliberately restored and verified.
- Rerun:
  `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --summary --out research/bench-records/live-bench/<fresh-name>.json`.
- Continue only if the summary reports `readiness: ready_for_prepare` and the
  full ignored JSON reports `ok: true`.
- Confirm physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state in
  the same session before running `espnow_bbs_live_gate.py prepare`.

## Current Passing Surface

- `COM4`, `COM5`, and `COM6` are present as CP210x VID:PID `10C4:EA60` peers.
- Read-only esptool identity passed on all three Windows peer ports.
- Observed peer MACs:
  `COM4=94:b9:7e:da:17:d0`,
  `COM5=78:e3:6d:0a:90:14`,
  `COM6=94:b9:7e:da:9a:50`.
- SSH to `dospi@192.168.137.93` reached the expected Pi identity and showed
  `eth0=172.16.0.2/24`.
- Pi `/dev/ttyUSB0` is present.
- Pi-side `esptool` `4.7.0` is installed.
- Pi-side coordinator identity passes when `esptool --no-stub` is used:
  `78:e3:6d:10:4d:6c`, ESP32-D0WDQ6, 4 MB flash.

## Current Stop Gate

- Backup/manifest `prepare` is blocked until same-session physical
  USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state is confirmed.
- Flash remains blocked until `prepare` records backups, build hashes, and
  recovery commands and the manifest is reviewed.
- Direct `172.16.0.2` is not currently reachable from the Windows/WSL host
  route and should not be used for the gate unless direct routing is restored
  intentionally.

## Closed Gates

No `read-flash` backup, build generation, flash, monitor automation, ESP-NOW
radio acceptance, router mutation, relay, XBee, TFT, MicroSD, load, mains,
PCAP, packet-driver work, BLE pairing, Android build, or ESP-WIFI-MESH radio
work is authorized from this handoff.
