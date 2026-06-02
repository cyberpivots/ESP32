# Handoff 0109: PF0530W ART Carousel To QA

Date: 2026-06-02

From: LCD Menu Developer

To: QA, LCD UX, Firmware, Evidence Records

## Summary

Task 0148 turns the Task 0146 five-panel ART catalog into a source/build
carousel for the host simulator and PF0530W firmware renderer. Rotary movement
on the ART page now cycles `bbs_badge`, `mesh_radar`, `packet_flow`,
`signal_skyline`, and `link_heat` while preserving the menu item focus. The
firmware renderer reloads the same `art_panel` glyph-bank slot with the
selected panel's CGRAM rows and reports `art=%u` in `BBS_LCD_RENDER`.

The focused host/firmware-boundary tests and no-flash ESP-IDF v6.0.1 build to
`/tmp/esp32-pf0530w-art-carousel-build` passed. This handoff does not claim
physical LCD readability or live-flashed carousel behavior.

## Continue With

- Review host ART carousel behavior, firmware ART cache invalidation, and
  scaffold audit marker updates.
- Confirm final validation in the Task 0148 source ledger.
- Keep physical ART readability and any fresh flash as separate Tier 3 gates.

## Boundaries

No flash, erase, monitor, serial command writes, XBee/RF, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, SoftAP/browser firmware
runtime, persistent config, MicroSD/TFT, wiring, DMM/current/load/mains work,
release, commit, push, PR, or deploy is authorized by this handoff.

## Evidence

- Task record:
  [../TASK_LOG/0148-four-relay-ky040-bbs-lcd-menu-pf0530w-art-carousel.md](../TASK_LOG/0148-four-relay-ky040-bbs-lcd-menu-pf0530w-art-carousel.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-art-carousel.md](../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-art-carousel.md)
- Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-ART-CAROUSEL-2026-06-02`
