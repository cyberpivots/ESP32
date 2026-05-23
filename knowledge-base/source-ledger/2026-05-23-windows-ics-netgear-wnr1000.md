# Windows ICS Netgear WNR1000 Bench Feed Ledger

Accessed: 2026-05-23

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-MICROSOFT-INETSHARINGCONFIG-ENABLESHARING`
- `SRC-MICROSOFT-SHARINGCONNECTIONTYPE`
- `SRC-MICROSOFT-ICS-FULL-SUBNET`
- `SRC-NETGEAR-WNR1000V2-USER-MANUAL`
- `SRC-LOCAL-WINDOWS-ICS-WNR1000-2026-05-23`

## Verified Facts

- Windows PowerShell ran elevated for the ICS change.
- Pre-change `Wi-Fi` was the upstream internet path with IPv4
  `192.168.1.2/24` and default gateway `192.168.1.1`.
- Pre-change `Ethernet 3` was the ASIX USB Ethernet adapter and had only APIPA
  IPv4 addressing.
- Pre-change HNetCfg state showed Internet Connection Sharing disabled on all
  listed Windows adapters.
- Pre-change `Get-NetNat` returned no manual NAT object.
- HNetCfg `EnableSharing(0)` was applied to `Wi-Fi`, and
  `EnableSharing(1)` was applied to `Ethernet 3`.
- Post-change HNetCfg state showed `Wi-Fi` sharing enabled as public type `0`
  and `Ethernet 3` sharing enabled as private type `1`.
- Post-change `Ethernet 3` had IPv4 `192.168.137.1/24`.
- Post-change `SharedAccess` was running.
- Post-change upstream internet from the Windows host still worked through
  `Wi-Fi`.
- Post-change `Get-NetNat` still returned no manual NAT object.
- A bounded ARP sweep of the ICS private subnet found one WAN-side candidate at
  `192.168.137.93`.
- A Windows probe resolved the WAN-side candidate to a WNR1000v2 host name.
  This is candidate identity evidence only, not a verified hardware revision.
- ICMP and HTTP/HTTPS/8080 probes to the WAN-side candidate did not pass.
- The prior Pi address `192.168.200.104` and gateway candidate
  `192.168.200.1` timed out from the Windows host.
- SSH to `dospi@192.168.200.104` timed out from WSL.
- A fresh WSL-side check at `2026-05-23T05:52:27-06:00` verified the active
  shell was Windows host WSL (`Predator`) with `eth0` on `192.168.137.1/24` and
  default route through upstream `192.168.1.1`; it was not the Pi local console.
- In that fresh WSL-side check, ping to `192.168.200.104`,
  `192.168.200.1`, and `192.168.137.93` each had 100% packet loss,
  `ssh-keyscan -T 5 192.168.200.104` returned no host keys, SSH to
  `dospi@192.168.200.104` timed out, and HTTP HEAD to `192.168.137.93` timed
  out.
- LAN-side router admin was authorized and completed after temporarily moving
  the Windows Ethernet cable to a Netgear LAN port.
- A temporary Windows `Ethernet 3` LAN-side address `172.16.0.250/24` was added
  alongside the existing ICS address `192.168.137.1/24` to reach router admin.
- The router admin page answered at `172.16.0.1` with auth realm
  `NETGEAR WNR1000v2-VC`.
- Router LAN was verified as `172.16.0.1/24`.
- Router DHCP was verified enabled with pool `172.16.0.2` to `172.16.0.254`.
- Router Status showed WAN DHCP client mode; while the PC was connected to a
  LAN port for admin, Internet Port IP was `0.0.0.0`.
- Pi `172.16.0.2` was visible with its hardware MAC retained only in ignored
  raw evidence, and TCP `22` was reachable from Windows source
  `172.16.0.250`.
- Address reservation was configured for `172.16.0.2`,
  redacted Pi hardware MAC, `DOS-PI4-POE`.
- Port forwarding was configured as `DOSPI_SSH TCP 22 22 172.16.0.2`.
- The observed custom-service form did not expose separate external/internal
  port fields, so WAN `2222` to LAN `22` translation was not configured.
- After the cable was moved back to the Netgear Internet/WAN port, the
  temporary Windows LAN-side address `172.16.0.250/24` was removed; `Ethernet
  3` and WSL `eth0` then showed only `192.168.137.1/24` on the ICS link.
- The router WAN candidate remained at `192.168.137.93`; Windows TCP testing
  from source `192.168.137.1` passed for port `22` and failed for ports `80`
  and `443`.
- SSH to `dospi@192.168.137.93` reached the Pi and presented the previously
  recorded Pi host-key fingerprints.
- The first SSH-forwarded Pi acceptance run reached the Netgear LAN gateway,
  Windows ICS address, `1.1.1.1`, and DNS, but default HTTPS timed out while
  `curl -4` succeeded.
- The Pi `dos-c-wired` profile had static public IPv6 DNS configured without an
  IPv6 gateway. IPv6 was disabled for that wired bench profile and IPv6 DNS was
  cleared, leaving IPv4 DHCP and IPv4 DNS in place.
- The exact acceptance command block was rerun from the Pi at
  `2026-05-23T08:52:17-06:00` and exited `0`: `eth0` was `172.16.0.2/24`,
  default route was via `172.16.0.1`, `/etc/resolv.conf` listed `1.1.1.1` and
  `8.8.8.8`, gateway/ICS/`1.1.1.1` pings had zero packet loss,
  `getent hosts example.com` resolved, and
  `curl -I --max-time 15 https://example.com` returned `HTTP/2 200`.

## Assumptions

- The observed WNR1000v2 identity remains candidate identity evidence until a
  physical label or Router Status page verifies exact hardware revision.

## Unknowns

- Exact WNR1000 hardware revision from physical label.
- Router Status WAN IP and DNS after the cable is moved back to the Netgear
  Internet/WAN port.
- Whether ICS survives a Windows reboot in this bench configuration.

## Validation Output

- Windows ICS host: PASS.
- WAN-side client candidate: PASS for SSH forwarding at `192.168.137.93:22`.
- Router Status: PASS for LAN-side admin view while the PC is connected to a
  Netgear LAN port; not captured from the WAN-fed final state.
- Pi downstream proof: ACCEPTED from the SSH-forwarded Pi shell.
- SSH router configuration: PASS for address reservation and forwarding table;
  PASS for WAN-side connection proof.
- Acceptance: PASS for downstream Pi internet over the Netgear LAN through
  Windows ICS.

## Rollback Steps

Preferred HNetCfg rollback from elevated PowerShell:

```powershell
$m = New-Object -ComObject HNetCfg.HNetShare
@($m.EnumEveryConnection) | ForEach-Object {
    $p = $m.NetConnectionProps.Invoke($_)
    if ($p.Name -in @("Wi-Fi", "Ethernet 3")) {
        $c = $m.INetSharingConfigurationForINetConnection.Invoke($_)
        if ($c.SharingEnabled) {
            $c.DisableSharing()
        }
    }
}
```

Manual rollback: open `ncpa.cpl`, open `Wi-Fi` properties, use the Sharing tab,
and clear Internet Connection Sharing for `Ethernet 3`.

## Stop Gate

Do not change ESP32 firmware, flash devices, touch relay/XBee/TFT/MicroSD/load
or mains wiring, select a new framework, create a manual WinNAT object, or
change the Netgear LAN subnet without separate authorization and LAN-side admin
access.
