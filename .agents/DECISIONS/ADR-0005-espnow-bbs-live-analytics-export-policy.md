# ADR-0005: ESP-NOW BBS Live Analytics Export Policy

Status: Proposed

Date: 2026-05-25

## Context

Gate G currently provides simulator-only analytics for the custom wireless
protocol lane. Those analytics are not exposed through the DOS-C bridge, live
OPCON workflow, firmware ABI, or any operator export command.

Live export would move evidence out of the local simulator fixture boundary, so
it needs an explicit policy decision before any bridge request, file export, UI
action, or automated cleanup is implemented.

## Decision

Keep live analytics export disabled until this ADR, or a replacement ADR, is
accepted with all of the following fields filled in:

- Retention period for raw records, derived reports, and export files.
- Privacy and redaction rules for operator, client, message, file, telemetry,
  node, and device identifiers.
- Export format and schema version.
- Storage location, filename convention, permissions, and backup boundary.
- Operator access rules, including who may generate, read, copy, and delete an
  export.
- Cleanup expectations for stale exports, temporary files, audit logs, and
  copied proof packets.

Until acceptance, Gate G is only a prepare-live-export planning gate. Simulator
analytics may continue to run in local tests, but live bridge/export surfaces
must remain absent.

## Rationale

The simulator report already proves the report shape can be generated from
fixture data. It does not prove privacy, retention, authorization, or live
storage behavior. Requiring the policy decision first prevents a live export
surface from becoming accepted by accident.

## Consequences

- No `analytics_export`, `report_export`, or equivalent live bridge request is
  authorized by Gate G.
- No Win31/OPCON export control is authorized by Gate G.
- No firmware ABI or ESP32 runtime export behavior is authorized by Gate G.
- Any future implementation must reference the accepted ADR status and include
  tests that reject live export when the policy gate is not accepted.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-G-ANALYTICS-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`
