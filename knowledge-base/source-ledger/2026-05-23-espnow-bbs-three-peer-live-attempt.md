# ESP-NOW BBS Three-Peer Live Attempt Source Ledger

Source ID: `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`

## Evidence

- Ignored preflight JSON:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T200026Z.json`
- Tracked bench summary:
  `research/bench-records/live-bench/2026-05-23-espnow-bbs-three-peer-live-attempt.md`
- Ignored partial live directories from failed prepare attempts:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200125Z/`,
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200209Z/`, and
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200237Z/`

## Supported Facts

- The fresh preflight passed with three Windows CP210x peer devices and a
  distinct Pi-attached coordinator.
- The live gate needed two prepare-path fixes before reaching backup:
  live-config generation must happen before `known_hosts` makes the live
  directory non-empty, and Pi-side coordinator backup must use `read_flash`
  spelling with Debian `esptool` 4.7.0.
- The 2026-05-23 three-peer live attempt stopped at coordinator full-flash
  backup because Pi-side `read_flash` failed around 50% with a CRC/checksum
  error.
- No valid coordinator backup, peer backup, build manifest, flash evidence,
  bridge transcript, Win31 screenshot, or three-peer radio acceptance was
  produced by this attempt.

## Boundary

This ledger does not prove live three-peer ESP-NOW behavior, dashboard
acceptance, chunked delivery, provisioning UX, firmware inventory, or any
physical wiring beyond the USB-only boundary stated in the user-provided plan.
