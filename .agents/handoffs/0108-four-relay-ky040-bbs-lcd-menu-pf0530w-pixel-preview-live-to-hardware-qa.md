# Handoff 0108: PF0530W Pixel Preview Live Flash To Hardware QA

Date: 2026-06-02

From: Firmware live-gate coordinator

To: Hardware QA, LCD UX, Evidence Records

## Summary

Task 0146's generated LCD pixel-preview/catalog menu artifact was built,
written, and separately verify-flashed on COM6 under the PF0530W firmware
identity. The read-only monitor captured app version `9aae6c6`, LCD init on
`0x27`, BBS LCD/input readiness, 15 pages, 65 items, 7 glyph banks, PCNT
readiness, repeated HOME renders with the shortened Task 0146 labels, and
zero crash markers. A fresh full 4 MB rollback backup was captured before the
write.

## Continue With

- Use the physical encoder to navigate from HOME to the ART page.
- Record whether the generated ART panels are visible, readable, cohesive, and
  stable on the physical 20x4 LCD.
- If transcript characterization is needed, run read-only monitoring only and
  keep serial command writes closed.

## Boundaries

No erase, reflash, serial command writes, XBee/RF, ESP-NOW runtime expansion,
relay GPIO writes, relay-expander writes, MicroSD/TFT, wiring mutation,
DMM/current/load/mains work, persistent config, external services, release,
commit, push, PR, or deploy is authorized by this handoff.

## Evidence

- Live source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-pixel-preview-live.md](../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-pixel-preview-live.md)
- Live task:
  [../TASK_LOG/0147-four-relay-ky040-bbs-lcd-menu-pf0530w-pixel-preview-live.md](../TASK_LOG/0147-four-relay-ky040-bbs-lcd-menu-pf0530w-pixel-preview-live.md)
- Source/catalog task:
  [../TASK_LOG/0146-espnow-bbs-lcd-pixel-preview-catalog.md](../TASK_LOG/0146-espnow-bbs-lcd-pixel-preview-catalog.md)
- Prior PF0530W live task:
  [../TASK_LOG/0143-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md](../TASK_LOG/0143-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md)
