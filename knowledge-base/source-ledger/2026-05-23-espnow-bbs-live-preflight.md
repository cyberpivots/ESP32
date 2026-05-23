# ESP-NOW BBS Live Preflight Ledger - 2026-05-23

Source index: [../source-index.md](../source-index.md)

## Scope

Read-only live implementation preflight for the ESP-NOW BBS three-peer bench
after the network live-gate design work. No flashing, erase, monitor
automation, ESP-NOW traffic generation, router mutation, relay, XBee, TFT,
MicroSD, load, or mains action was performed.

## Evidence

- Ignored preflight record:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T192610Z.json`.
- Ignored forwarded-path preflight record:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-forwarded-20260523T1938Z.json`.
- Ignored forwarded-path preflight after Pi esptool install:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-forwarded-after-esptool-20260523T1940Z.json`.
- Ignored forwarded-path preflight after Pi `--no-stub` support:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-forwarded-nostub-20260523T1945Z.json`.
- Read-only reachability checks:
  `ping -c 2 -W 2 172.16.0.2`, `ssh-keyscan -T 5 172.16.0.2`,
  `ip route get 172.16.0.2`, Windows `Test-NetConnection` to TCP 22,
  `ssh-keyscan -T 5 192.168.137.93`, SSH read-only Pi identity commands
  through `192.168.137.93`, and Windows `Test-NetConnection` to
  `192.168.137.93:22`.
- Pi tooling commands: `apt-cache policy esptool`, `sudo apt-get install -y
  esptool`, `esptool version`, and `esptool --no-stub` read-only coordinator
  identity probes.

## Verified Facts

- Windows inventory contained exactly `COM4`, `COM5`, and `COM6` as CP210x
  USB-UART peers with VID:PID `10C4:EA60`.
- Read-only esptool identity passed for all three Windows peers:
  `COM4` MAC `94:b9:7e:da:17:d0`, `COM5` MAC `78:e3:6d:0a:90:14`, and
  `COM6` MAC `94:b9:7e:da:9a:50`.
- Each Windows peer reported ESP32-D0WDQ6 profile evidence and 4 MB flash.
- Direct Pi `172.16.0.2` did not return SSH host keys during the first
  preflight, and ping/TCP 22 checks also failed from the current host routing
  state.
- The current WSL route to direct `172.16.0.2` was via `192.168.1.1` on
  `eth1`, not a verified accepted Pi LAN path.
- The accepted SSH-forwarded address `192.168.137.93` reached the Pi. The Pi
  host-key fingerprints, hostname, model, serial, root filesystem,
  `eth0=172.16.0.2/24`, stale listener absence, stale process absence, and
  `/dev/ttyUSB0` presence gates passed through that path.
- Coordinator `/dev/ttyUSB0` identity did not pass because the Pi returned
  `esptool not found` for `chip_id`, `read_mac`, and `flash_id`.
- Debian Trixie offered `esptool` `4.7.0+dfsg-0.1`; it was installed on the
  verified Pi with non-interactive sudo.
- Pi `esptool` default stub mode failed because
  `stub_flasher_32.json` was missing from the Debian package path used by the
  tool.
- Pi `esptool --no-stub` read-only identity commands passed for coordinator
  `/dev/ttyUSB0`, MAC `78:e3:6d:10:4d:6c`, ESP32-D0WDQ6, and 4 MB flash.
- The latest preflight through `192.168.137.93` reports
  `readiness=ready_for_prepare`.

## Assumptions

- `COM4`, `COM5`, and `COM6` remain candidates only until the full preflight
  passes and the physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD
  state is confirmed in the same session as any write.
- The accepted Pi identity remains the `dospi@172.16.0.2` gate until a later
  source-backed decision changes it.

## Unknowns

- No backup, build hash, flash, Win31 dashboard, or live radio acceptance proof
  exists for the three-peer slice.
- Physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state is not
  proven by the script and still requires same-session operator confirmation
  before backup or flash work.

## Stop Gate

Live implementation may proceed only to the backup/manifest `prepare` step
after same-session physical USB-only/no-load confirmation. Flash remains closed
until a reviewed prepare manifest records backups, build hashes, recovery
commands, and explicit write confirmation.
