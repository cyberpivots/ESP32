# Handoff 0107: LCD Pixel Preview Catalog To QA

Date: 2026-06-02

From: LCD Menu Developer

To: QA, LCD UX, Evidence Records

## Summary

Task 0146 adds host-only `bbs_lcd_pixel_preview.v1` metadata, five candidate
ART catalog panels, ART focus parity with PF0530W firmware, and shorter HOME
first-viewport labels. The browser mirror remains inert and PF0530W firmware
identity remains unchanged.

Validation passed for LCD generator freshness, focused LCD tests, LCD
discovery, firmware boundary regressions, firmware audit, source/docs/records/
agent-process audits, scaffold-audit unittest discovery, no-flash ESP-IDF
build to `/tmp/esp32-pf0530w-lcd-pixel-preview-build`, `git diff --check`,
`scripts/scaffold_audit_skills.py`, and `scripts/verify_scaffold.py`.

## Continue With

- Review the LCD pixel preview and catalog tests and no-flash build evidence.
- Confirm generated LCD menu artifacts remain fresh from XML.
- Keep physical LCD ART readability and ART navigation telemetry as unresolved
  gaps until a separate Tier 3 live/visual proof is authorized.

## Boundaries

No flash, erase, monitor, serial command writes, XBee/RF, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, SoftAP/browser firmware
runtime, persistent config, MicroSD/TFT, wiring, DMM/current/load/mains work,
release, commit, push, PR, or deploy is authorized by this handoff.

## Evidence

- Task record:
  [../TASK_LOG/0146-espnow-bbs-lcd-pixel-preview-catalog.md](../TASK_LOG/0146-espnow-bbs-lcd-pixel-preview-catalog.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-espnow-bbs-lcd-pixel-preview-catalog.md](../../knowledge-base/source-ledger/2026-06-02-espnow-bbs-lcd-pixel-preview-catalog.md)
- Source ID:
  `SRC-LOCAL-ESPNOW-BBS-LCD-PIXEL-PREVIEW-CATALOG-2026-06-02`
