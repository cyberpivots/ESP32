# Windows ICS To Netgear WNR1000 Bench Record - 2026-05-23

## Record Metadata

- Record ID: 2026-05-23-windows-ics-netgear-wnr1000
- Date: 2026-05-23
- Operator: Codex
- Workspace: `/mnt/h/ESP32`
- Device/project: Windows 11 Wi-Fi feed to Netgear WNR1000 via ICS
- Scope: Windows ICS host configuration, WAN-side discovery, LAN-side Netgear
  admin configuration, WAN-side SSH forwarding, and downstream Pi internet
  proof
- Excluded work: ESP32 firmware, flashing, relay, XBee, TFT, MicroSD, load
  wiring, mains wiring, framework selection, manual WinNAT, and unauthenticated
  Netgear LAN reconfiguration

## Source Coverage

- Source IDs reviewed:
  `SRC-MICROSOFT-INETSHARINGCONFIG-ENABLESHARING`,
  `SRC-MICROSOFT-SHARINGCONNECTIONTYPE`,
  `SRC-MICROSOFT-ICS-FULL-SUBNET`,
  `SRC-NETGEAR-WNR1000V2-USER-MANUAL`,
  `SRC-LOCAL-WINDOWS-ICS-WNR1000-2026-05-23`
- Local records reviewed:
  `research/bench-records/live-bench/windows-ics-20260523/local-*.txt`
- Fresh blocker record:
  `research/bench-records/live-bench/windows-ics-20260523/local-fresh-pi-console-blocker-20260523T115227Z.txt`
- Router admin/configuration records:
  `research/bench-records/live-bench/windows-ics-20260523/local-router-pages-20260523T1438Z/`
- SSH-forwarded Pi downstream records:
  `research/bench-records/live-bench/windows-ics-20260523/local-pi-downstream-proof-20260523T144904Z.txt`,
  `research/bench-records/live-bench/windows-ics-20260523/local-pi-downstream-proof-after-ipv4-dns-20260523T145209Z.txt`
- New source-index entries required: complete for this record

## Verified Facts

- `Wi-Fi` remained the Windows upstream internet connection.
- `Ethernet 3` is the ASIX USB Ethernet adapter used as the ICS private
  interface.
- HNetCfg Internet Connection Sharing is enabled with `Wi-Fi` public and
  `Ethernet 3` private.
- `Ethernet 3` is `192.168.137.1/24` after ICS.
- No manual `Get-NetNat` object was introduced.
- A WAN-side candidate appeared at `192.168.137.93`; one Windows probe resolved
  it to a WNR1000v2 host name.
- On `2026-05-23T05:52:27-06:00`, the active shell was verified as Windows host
  WSL (`Predator`), not the Pi. It had `eth0` on `192.168.137.1/24` and default
  route through upstream `192.168.1.1`.
- From the WSL host context, `192.168.200.104`, `192.168.200.1`, and
  `192.168.137.93` each had 100% packet loss for a one-packet ICMP check.
- From the WSL host context, `ssh-keyscan -T 5 192.168.200.104` returned no
  host keys, SSH to `dospi@192.168.200.104` timed out, and HTTP HEAD to
  `192.168.137.93` timed out.
- The Windows PC was temporarily connected to a Netgear LAN port for authorized
  router admin. A temporary `Ethernet 3` address `172.16.0.250/24` was added
  alongside the ICS address `192.168.137.1/24`.
- Router admin answered at `172.16.0.1` with realm `NETGEAR WNR1000v2-VC`.
- Router LAN is `172.16.0.1/24`.
- Router DHCP is enabled with pool `172.16.0.2` to `172.16.0.254`.
- Router Status showed WAN DHCP client mode; during LAN-side admin, Internet
  Port IP was `0.0.0.0` because the Windows cable was not connected to the
  router Internet/WAN port.
- Pi `172.16.0.2` was visible in the router attached-device/reservation page;
  the Pi hardware MAC is retained only in ignored raw evidence.
- Address reservation was configured for `172.16.0.2`,
  redacted Pi hardware MAC, `DOS-PI4-POE`.
- Port forwarding was configured as `DOSPI_SSH TCP 22 22 172.16.0.2`.
- The WNR1000 custom-service page exposed one port range and did not expose
  separate external/internal port fields; no WAN `2222` to LAN `22` port
  translation was configured.
- From Windows `Ethernet 3` source `172.16.0.250`, TCP checks passed to
  router `172.16.0.1:80` and Pi `172.16.0.2:22`.
- After the Windows cable was moved back to the Netgear Internet/WAN port, the
  temporary Windows LAN-side address `172.16.0.250/24` was removed. `Ethernet
  3` and WSL `eth0` then carried only `192.168.137.1/24` for the ICS link.
- Windows neighbor state still showed the router WAN candidate at
  `192.168.137.93`.
- From Windows source `192.168.137.1`, TCP `22` to `192.168.137.93` passed;
  TCP `80` and `443` failed, so WAN-side router administration remained closed.
- SSH to `dospi@192.168.137.93` presented the previously recorded Pi host-key
  fingerprints and reached hostname `dos-pi4-poe`.
- The first SSH-forwarded Pi acceptance run showed `eth0` at `172.16.0.2/24`,
  default route via `172.16.0.1`, gateway/ICS/`1.1.1.1` ping success, and DNS
  resolution, but default `curl -I --max-time 15 https://example.com` timed
  out. `curl -4` to the same URL returned `HTTP/2 200`.
- The active Pi `dos-c-wired` profile had static public IPv6 DNS servers
  configured while the Pi had no IPv6 gateway. The profile was changed to
  disable IPv6 on the wired bench link and clear IPv6 DNS, leaving IPv4 DHCP
  and IPv4 DNS `1.1.1.1` and `8.8.8.8`.
- The unchanged acceptance block was rerun from the Pi at
  `2026-05-23T08:52:17-06:00` and exited `0`: `eth0` was `172.16.0.2/24`,
  default route was `172.16.0.1`, `/etc/resolv.conf` listed `1.1.1.1` and
  `8.8.8.8`, pings to `172.16.0.1`, `192.168.137.1`, and `1.1.1.1` each had
  zero packet loss, `getent hosts example.com` resolved, and
  `curl -I --max-time 15 https://example.com` returned `HTTP/2 200`.

## Assumptions

- The exact WNR1000 hardware revision remains the candidate `WNR1000v2` until
  verified by physical label or Router Status evidence.

## Unknowns

- Exact router hardware revision from label or Router Status.
- Router Status WAN IP, DHCP mode, DNS, LAN IP, and LAN DHCP state after final
  cabling.
- ICS persistence after a Windows reboot.

## Network Result

- Windows ICS host configuration: PASS.
- WNR1000 WAN-side discovery: PASS for the ICS-side WAN candidate and TCP `22`
  forwarding; Router Status remains closed from the WAN side.
- Netgear Router Status proof: PASS for LAN-side admin view while the PC was
  connected to a Netgear LAN port; not captured from the WAN-fed final state.
- Pi downstream internet proof: ACCEPTED from the SSH-forwarded Pi shell.
- LAN-side Router Status/admin proof: PASS for router LAN `172.16.0.1/24`,
  DHCP enabled, Pi reservation, and SSH forwarding table configuration.
- WAN-side SSH forwarding proof: PASS.

## Outcome

- Pass/fail: pass for downstream internet acceptance. Windows ICS setup,
  LAN-side router configuration, WAN-side SSH forwarding, and Pi DNS/HTTPS
  proof passed. Router Status in the final WAN-fed state and Windows reboot
  persistence remain unverified.
- Files updated:
  `.agents/TASK_LOG/0027-windows-ics-netgear-wnr1000.md`,
  `.agents/handoffs/0017-windows-ics-netgear-to-qa.md`,
  `knowledge-base/source-ledger/2026-05-23-windows-ics-netgear-wnr1000.md`,
  `knowledge-base/source-index.md`, and `docs/index.md`.
- Next owner: QA or local bench operator only if optional Router Status or
  Windows reboot-persistence proof is required.
- Reboot persistence remains unverified; no Windows reboot test was performed.
