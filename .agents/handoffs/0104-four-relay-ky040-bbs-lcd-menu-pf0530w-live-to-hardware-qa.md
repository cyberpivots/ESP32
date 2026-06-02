# Handoff 0104: PF0530W Live Flash To Hardware QA

Date: 2026-06-02

From: Firmware live-gate owner

To: Hardware QA, LCD UX, Evidence Records

## Summary

PF0530W was written and separately verify-flashed on COM6 after a fresh 4 MB
rollback backup. The read-only monitor captured PF0530W LCD/input readiness,
15 pages, 7 glyph banks, PCNT readiness, and repeated HOME renders with no
unsafe markers.

## Continue With

- Use the physical encoder to navigate from HOME to `LCD art badge panel` and
  open the `ART` page.
- Record whether the 4x20 custom-character art panel is visible, readable, and
  cohesive on the physical LCD.
- If transcript characterization is needed, run read-only monitoring only;
  keep serial command writes closed.

## Boundaries

No erase, reflash, serial command writes, XBee/RF, ESP-NOW runtime expansion,
relay GPIO writes, relay-expander writes, MicroSD/TFT, wiring mutation,
DMM/current/load/mains work, persistent config, external services, commit, or
push is authorized by this handoff.

## Evidence

- Live source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md](../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md)
- Live task:
  [../TASK_LOG/0143-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md](../TASK_LOG/0143-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md)
- Source/build task:
  [../TASK_LOG/0142-four-relay-ky040-bbs-lcd-menu-pf0530w-visual-art.md](../TASK_LOG/0142-four-relay-ky040-bbs-lcd-menu-pf0530w-visual-art.md)
