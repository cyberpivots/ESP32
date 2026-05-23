# Handoff 0017 - Windows ICS Netgear To QA

## From

Communications, QA

## To

QA, local bench operator

## Status

Downstream Pi proof accepted; optional Router Status and reboot-persistence
follow-up remain

## Context

Windows Internet Connection Sharing is enabled from `Wi-Fi` to `Ethernet 3`.
The Windows host side is verified: `Ethernet 3` is `192.168.137.1/24`, HNetCfg
marks `Wi-Fi` as public sharing and `Ethernet 3` as private sharing, and no
manual `Get-NetNat` object was created.

A WAN-side candidate appeared on the ICS subnet at `192.168.137.93`, and one
probe resolved it as a WNR1000v2 host name. This is not enough to verify exact
hardware revision; use the router label or the Router Status page for that.

A fresh WSL-side check on `2026-05-23T05:52:27-06:00` confirmed the active
agent shell is the Windows host WSL environment (`Predator`) with `eth0` on
`192.168.137.1/24` and default route through upstream `192.168.1.1`; it is not
the Pi local console. From that host-side context, ping to `192.168.200.104`,
`192.168.200.1`, and `192.168.137.93` had 100% packet loss, `ssh-keyscan`
returned no Pi host keys, SSH to `dospi@192.168.200.104` timed out, and HTTP to
`192.168.137.93` timed out. This does not satisfy downstream acceptance.

On `2026-05-23`, LAN-side admin was authorized and completed while the Windows
PC was temporarily connected to a Netgear LAN port. A temporary Windows
LAN-side address `172.16.0.250/24` was added on `Ethernet 3` to reach the
router at `172.16.0.1`. Router Status and live pages verified LAN
`172.16.0.1/24`, DHCP pool `172.16.0.2` to `172.16.0.254`, WAN DHCP client
mode, and Internet Port IP `0.0.0.0` because the WAN cable was disconnected
during LAN-side admin. The Pi was visible at `172.16.0.2`; TCP `22` was
reachable from the LAN-side Windows address.

Configured router state:

- Address reservation: `172.16.0.2` -> redacted Pi hardware MAC,
  `DOS-PI4-POE`.
- Port forwarding: `DOSPI_SSH TCP 22 22 172.16.0.2`.
- DMZ was not enabled, remote router administration was not enabled, and no
  UPnP or broad firewall changes were made.
- The observed WNR1000 form does not expose separate external/internal port
  fields, so WAN TCP `22` is the configured SSH forward. Do not claim WAN
  `2222` -> LAN `22` translation from current evidence.

After the cable was moved back to the Netgear Internet/WAN port, the temporary
Windows LAN-side address `172.16.0.250/24` was removed. `Ethernet 3` and WSL
`eth0` then only carried `192.168.137.1/24` on the ICS side. The router remained
visible on the ICS subnet at `192.168.137.93`; TCP `22` passed from Windows
source `192.168.137.1`, while TCP `80` and `443` remained closed from the WAN
side.

The exact downstream acceptance block was run from the Pi through the WAN-side
SSH forward at `2026-05-23T08:52:17-06:00` after correcting the Pi wired
profile DNS state. The Pi reported `eth0` at `172.16.0.2/24`, default route via
`172.16.0.1`, resolver entries `1.1.1.1` and `8.8.8.8`, successful three-packet
pings to `172.16.0.1`, `192.168.137.1`, and `1.1.1.1`, DNS resolution for
`example.com`, and `HTTP/2 200` from
`curl -I --max-time 15 https://example.com`. The command exited `0`.

## Continue With

- Optional: Recheck Router Status from a LAN-side browser or SSH tunnel and
  record a redacted summary of Internet/WAN IP, DHCP mode, DNS, LAN IP, and LAN
  DHCP state. Do not enable remote router administration just for this.
- Optional: Verify whether ICS survives a Windows reboot if persistence matters
  for the bench.

## Blockers

- None for downstream Pi internet acceptance.
- Router Status is still not reachable from the WAN-side candidate address.
- Windows ICS reboot persistence remains unverified because no Windows reboot
  test was performed.

## Evidence

- Source ledger:
  `knowledge-base/source-ledger/2026-05-23-windows-ics-netgear-wnr1000.md`.
- Public-safe bench record:
  `research/bench-records/live-bench/2026-05-23-windows-ics-netgear-wnr1000.md`.
- Raw local Windows evidence, ignored by Git:
  `research/bench-records/live-bench/windows-ics-20260523/local-*.txt`.
- Fresh host-side blocker evidence, ignored by Git:
  `research/bench-records/live-bench/windows-ics-20260523/local-fresh-pi-console-blocker-20260523T115227Z.txt`.
- Router admin/configuration evidence, ignored by Git:
  `research/bench-records/live-bench/windows-ics-20260523/local-router-pages-20260523T1438Z/`.
- SSH-forwarded Pi downstream proof, ignored by Git:
  `research/bench-records/live-bench/windows-ics-20260523/local-pi-downstream-proof-20260523T144904Z.txt`
  and
  `research/bench-records/live-bench/windows-ics-20260523/local-pi-downstream-proof-after-ipv4-dns-20260523T145209Z.txt`.

## Closed Gates

Do not infer authorization for ESP32 firmware, flashing, relay, XBee, TFT,
MicroSD, load wiring, mains wiring, framework changes, manual WinNAT, or
Netgear LAN readdressing from this handoff.
