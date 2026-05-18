# Handoff 0005 - Admin HMI MicroSD Assets and Logs

## From

Architect, QA

## To

Hardware, Firmware, QA

## Summary

The `four-relay-xbee-wifi` project now has a copyable static admin HMI and a
source-backed MicroSD storage contract:

- `docs/projects/four-relay-xbee-wifi/ui/index.html`
- `docs/projects/four-relay-xbee-wifi/ui/styles.css`
- `docs/projects/four-relay-xbee-wifi/ui/app.js`
- `docs/projects/four-relay-xbee-wifi/ui/manifest.json`
- `docs/projects/four-relay-xbee-wifi/web-interface.md`
- `hardware-profiles/storage/spi-microsd-reader/README.md`
- `knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md`

The UI keeps relay state-changing controls disabled unless admin, hardware
gate, safety lock, and per-relay enable conditions are satisfied. Storage and
log panels render from mock data locally and from read-only API contracts in
future firmware.

## Required next checks

- Hardware must identify the exact SPI MicroSD reader module, revision, voltage
  path, regulator/level-shifter behavior, pull-ups, and CD/WP pins.
- Hardware must prove shield continuity for the preferred investigation pins:
  `GPIO18`, `GPIO19`, `GPIO23`, and `GPIO32`.
- Hardware must verify one selected 3.3 V power source, no dual-power conflict,
  card current budget, and boot/flashing behavior with the reader present.
- Firmware must keep `/api/state` usable when storage-specific endpoints fail
  and must not auto-retry state-changing commands from UI failures.
- Firmware must keep admin credentials, relay polarity, safety configuration,
  and XBee allowlists in NVS unless a future accepted ADR changes the storage
  boundary.
- QA must continue rejecting framework files and image/bulky assets outside
  approved locations during scaffold-phase work.

## Blockers

- MicroSD reader identity, schematic, voltage path, and pull-ups are unresolved.
- SPI wiring remains blocked until power, pull-up, continuity, and boot-pin
  review pass.
- Card capacity, host FAT preparation, low-space behavior, log rotation, and
  embedded fallback page content are unresolved.
- No live ESP32 flashing, MicroSD wiring, relay switching, XBee writes, or
  mains/load wiring is approved by this handoff.

## Evidence

- Source IDs are recorded in `knowledge-base/source-index.md`.
- Storage and API contract is recorded in
  `docs/projects/four-relay-xbee-wifi/web-interface.md`.
- MicroSD blocker closure requirements are recorded in
  `hardware-profiles/storage/spi-microsd-reader/README.md` and
  `knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md`.
- Validation results are recorded in
  `.agents/TASK_LOG/0005-admin-hmi-microsd-assets-logs.md`.
