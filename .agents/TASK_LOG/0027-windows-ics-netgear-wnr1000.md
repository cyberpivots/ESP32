# Task 0027 - Windows ICS Netgear WNR1000 Bench Feed

## Task

- ID: 0027-windows-ics-netgear-wnr1000
- Owner role: Communications, QA
- Status: Accepted downstream Pi internet proof; Router Status WAN summary and
  Windows reboot persistence remain unverified
- Created: 2026-05-23
- Updated: 2026-05-23

## Goal

Share the Windows 11 `Wi-Fi` internet connection through `Ethernet 3` to the
Netgear WNR1000 Internet/WAN port using Windows Internet Connection Sharing
instead of manual WinNAT, then verify downstream internet from the Pi on the
Netgear LAN.

## Scope

Included:

- Pre-change Windows network evidence capture.
- HNetCfg Internet Connection Sharing configuration.
- Post-change Windows ICS proof for `Wi-Fi` public sharing and `Ethernet 3`
  private sharing.
- WAN-side candidate discovery on the ICS private subnet.
- Reachability checks for the prior Pi address and Netgear LAN gateway
  candidates.
- Fresh 2026-05-23 WSL host-side check for Pi/local-console accessibility.
- LAN-side router admin configuration for the bench Pi reservation and SSH
  forwarding rule.
- WAN-side cable-reconnected SSH forwarding proof and downstream Pi internet
  acceptance block.
- Durable source ledger, public-safe bench record, and continuation handoff.

Excluded:

- Manual `New-NetNat` or WinNAT configuration.
- Netgear LAN readdressing without LAN-side admin access.
- DMZ, remote router administration, UPnP changes, or broad inbound exposure.
- ESP32 firmware, flashing, relay, XBee, TFT, MicroSD, load wiring, mains
  wiring, and framework choices.

## Sources

- `SRC-MICROSOFT-INETSHARINGCONFIG-ENABLESHARING`
- `SRC-MICROSOFT-SHARINGCONNECTIONTYPE`
- `SRC-MICROSOFT-ICS-FULL-SUBNET`
- `SRC-NETGEAR-WNR1000V2-USER-MANUAL`
- `SRC-LOCAL-WINDOWS-ICS-WNR1000-2026-05-23`

## Decisions

- Use Windows ICS through HNetCfg rather than creating a manual NAT object.
- Configure `Wi-Fi` as the public/shared connection and `Ethernet 3` as the
  private/home connection.
- Treat the observed WNR1000v2 name as a candidate identity only. Exact router
  hardware revision still requires label evidence or a Router Status page.
- Do not add routes or bypass the router firewall to reach the Netgear LAN from
  the Windows host; the requested acceptance proof is a Pi local-console proof.
- Use the Netgear LAN-side admin path only while the Windows PC is temporarily
  connected to a Netgear LAN port. Keep the final feed path as Windows
  `Ethernet 3` to the Netgear Internet/WAN port.

## Validation

- Pre-change Windows state: PASS. `Wi-Fi` had internet via `192.168.1.1`,
  `Ethernet 3` was the ASIX adapter on APIPA, HNetCfg showed ICS disabled on
  all listed adapters, and `Get-NetNat` returned no NAT object.
- HNetCfg action: PASS. `Wi-Fi` was enabled as sharing type `0` and
  `Ethernet 3` as sharing type `1`.
- Post-change Windows state: PASS. `Ethernet 3` became `192.168.137.1/24`,
  HNetCfg showed `Wi-Fi` public and `Ethernet 3` private, `SharedAccess` was
  running, upstream internet remained reachable, and no `Get-NetNat` object was
  introduced.
- Router WAN-side candidate: PASS for forwarding reachability. After the cable
  was moved back to the Netgear Internet/WAN port, the temporary Windows
  LAN-side address `172.16.0.250/24` was removed from `Ethernet 3`; Windows and
  WSL then showed `Ethernet 3`/`eth0` only on `192.168.137.1/24`. The router
  remained visible as WAN-side neighbor `192.168.137.93`; Windows
  `Test-NetConnection` passed for TCP `22` from source `192.168.137.1` and
  failed for TCP `80` and `443`, matching the intended SSH-only exposure.
- Pi downstream acceptance: ACCEPTED. SSH through `192.168.137.93:22` reached
  the Pi and presented the previously recorded Pi host-key fingerprints. The
  exact acceptance command block was run from that Pi shell after a DNS fix at
  `2026-05-23T08:52:17-06:00` and exited `0`. The Pi reported hostname
  `dos-pi4-poe`, `eth0` at `172.16.0.2/24`, default route via `172.16.0.1`,
  resolver entries `1.1.1.1` and `8.8.8.8`, `NETGEAR_LAN_GATEWAY=172.16.0.1`,
  successful three-packet pings to `172.16.0.1`, `192.168.137.1`, and
  `1.1.1.1`, DNS resolution for `example.com`, and `HTTP/2 200` from
  `curl -I --max-time 15 https://example.com`.
- Pi DNS correction: PASS. The first SSH-forwarded run reached the gateway,
  Windows ICS, `1.1.1.1`, and DNS, but default HTTPS timed out while
  `curl -4` succeeded. The active `dos-c-wired` NetworkManager profile had
  public IPv6 DNS configured but no IPv6 gateway. The profile was changed to
  disable IPv6 on the wired bench link and clear IPv6 DNS, leaving IPv4 DHCP
  and IPv4 DNS intact; the unchanged acceptance block then passed.
- LAN-side admin access: PASS. With the Windows PC temporarily connected to a
  Netgear LAN port, `Ethernet 3` retained ICS address `192.168.137.1/24` and a
  temporary LAN-side address `172.16.0.250/24` was added for admin access. The
  router answered at `172.16.0.1` with auth realm `NETGEAR WNR1000v2-VC`.
- Netgear LAN/DHCP configuration: PASS. Router LAN is `172.16.0.1/24`; DHCP is
  enabled with pool `172.16.0.2` to `172.16.0.254`.
- Pi reservation: PASS. Address reservation now maps Pi `172.16.0.2` to the
  redacted Pi hardware MAC with name `DOS-PI4-POE`.
- Inbound SSH rule: PASS for router table configuration. Port forwarding now
  has `DOSPI_SSH TCP 22 22 172.16.0.2`. The observed WNR1000 custom-service
  form supports one service port range and does not expose separate external
  and internal port fields, so this rule forwards WAN TCP `22` to Pi TCP `22`
  rather than translating WAN `2222` to LAN `22`.
- LAN-side reachability: PASS. From Windows `Ethernet 3` source
  `172.16.0.250`, TCP to router `172.16.0.1:80` and Pi `172.16.0.2:22` passed.
- WAN-side final proof: PASS for downstream acceptance. During LAN-side admin,
  the Netgear WAN was disconnected and Router Status showed Internet Port IP
  `0.0.0.0` while DHCP client mode remained configured. After final cabling,
  SSH forwarding and Pi internet acceptance passed through WAN-side
  `192.168.137.93`. Router Status was not reachable from the WAN side and
  remote router administration was not enabled.
- Reboot persistence: UNVERIFIED. No Windows reboot was performed after enabling
  ICS.

## Handoff

Continue through
`.agents/handoffs/0017-windows-ics-netgear-to-qa.md` only for optional Router
Status capture or reboot persistence testing. Windows ICS, the Netgear LAN
configuration, WAN-side SSH forwarding, and Pi downstream internet proof are
accepted. Keep reboot persistence unverified unless a Windows reboot test is
actually performed.
