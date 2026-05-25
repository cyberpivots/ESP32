# Custom Wireless Protocol Gate G Analytics Source Ledger

Date: 2026-05-25

## Verified Facts

- [repo-verified] Gate G adds simulator-only analytics generation through
  `ProtocolSimulator.analytics_report()`.
- [repo-verified] The analytics report includes retained counters for direct
  messages, files, telemetry reports, node status reports, custody ACKs,
  control intents, and blocked state-changing requests.
- [repo-verified] The report includes custody rollups by status, file rollups
  by queued/completed/failed counts and bytes, and telemetry rollups by report
  class plus distinct node count.
- [repo-verified] The client/user summary is derived from simulator fixture
  labels only and does not claim an accepted identity or privacy policy.
- [repo-verified] Export boundary fields are explicit:
  `simulator_only: true`, `privacy_policy: unreviewed`, and
  `retention: unresolved`.
- [repo-verified] Gate G does not add an analytics bridge request or wire
  analytics into a live bridge/export surface.
- [repo-verified] `ADR-0005` is proposed as the future live export policy gate.

## Supersession

- Later on 2026-05-25, `ADR-0005` was accepted and simulator analytics policy
  fields were updated by
  `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`.
  It is not accepted.

## Assumptions

- [assumption] Analytics review should remain separate from bridge ABI and
  firmware ABI acceptance.
- [assumption] The Pi bridge remains the future durability boundary unless a
  later accepted ADR changes that architecture.

## Unknowns

- [unknown] No accepted analytics storage format, dashboard report shape,
  retention policy, export policy, authorization policy, privacy policy,
  storage location, operator access policy, or cleanup expectation exists after
  Gate G.
- [unknown] No live bridge transcript, Win31/OPCON visual proof, firmware proof,
  serial proof, or live analytics export proof was produced by Gate G.

## Validation

- `python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `python3 tools/simulators/custom_wireless_protocol/espnow_bbs_custom_protocol.py --analytics-demo`

## Stop Gates

Gate G does not authorize live bridge/export surfaces, flashing, erase,
monitor, serial writes, radio setting changes, PCAP, router/admin work, BLE,
ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load, or mains work.
