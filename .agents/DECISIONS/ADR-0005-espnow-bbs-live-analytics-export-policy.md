# ADR-0005: ESP-NOW BBS Live Analytics Export Policy

Status: Accepted

Date: 2026-05-25

## Context

Gate G originally provided simulator-only analytics for the custom wireless
protocol lane. Those analytics were not exposed through the DOS-C bridge, live
OPCON workflow, firmware ABI, or any operator export command because no
retention, privacy, storage, access, or cleanup policy had been accepted.

The user accepted a conservative v1 policy for Gate G live export on
2026-05-25. Gate G may now add a local-admin redacted JSON export from the
DOS-C/Pi bridge spool, while Win31/OPCON controls, firmware export behavior,
and bridge request types remain closed.

## Decision

Accept Gate G live analytics export only under this policy:

- Retention: raw bridge spool records remain governed by existing ignored
  runtime/proof-packet handling; derived analytics export files are local proof
  artifacts with a 7-day stale-export cleanup expectation.
- Privacy/redaction: derived exports omit message bodies, file names, event
  details, and raw operator, client, message, file, telemetry, node, and device
  identifiers. Identifiers included in derived records use salted SHA-256 hashes
  with a per-export salt that is not written into the export.
- Format: derived exports use JSON schema version `gate-g.analytics.v1` and
  policy selector `adr-0005-redacted-local-operator-v1`.
- Storage: default proof storage is an ignored local proof packet under the
  DOS-C/Pi runtime or integration artifact roots, copied into the ignored ESP32
  live-bench record only when proving the gate.
- Permissions: export files are operator-local artifacts and should be written
  with owner-only permissions where the host filesystem supports them.
- Access: local operator/admin CLI only. No Win31/OPCON export button, no live
  bridge request such as `analytics_export`, and no ESP32 firmware ABI/runtime
  export behavior is authorized.
- Cleanup: stale `analytics-report*.json` files in approved ignored export
  roots should be removed after 7 days. Cleanup proof may be recorded in the
  bench packet; cleanup does not delete `bridge-transcript.jsonl`, screenshots,
  or human-readable logs.

## Rationale

The accepted policy opens the minimum useful Gate G live export surface while
keeping sensitive content and device/client identifiers out of derived proof
reports. Keeping export as a local admin CLI action avoids introducing a Win31
operator workflow, firmware ABI, or bridge request before those interfaces are
reviewed separately.

## Consequences

- A DOS-C/Pi local-admin command may generate `analytics-report.v1.json` from a
  file-backed bridge spool when the accepted policy selector is supplied.
- Simulator analytics may reference the accepted policy, but remain
  simulator-only and do not prove live export by themselves.
- Raw SQLite snapshots remain separate local-admin evidence and are not the
  Gate G derived analytics export.
- Win31/OPCON export controls, firmware export ABI, bridge export request
  types, serial-write expansion, flash, erase, monitor, PCAP, BLE, mesh,
  relay/XBee, TFT, MicroSD, load, mains, and router/admin mutation remain out of
  scope.

## Sources

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-G-ANALYTICS-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-POLICY-2026-05-25`
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`
