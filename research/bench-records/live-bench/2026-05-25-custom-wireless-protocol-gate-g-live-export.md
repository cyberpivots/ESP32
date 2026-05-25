# Custom Wireless Protocol Gate G Live Export - 2026-05-25

## Summary

Gate G live export was generated as a local-admin redacted JSON report from the
existing structured Gate H live proof spool after `ADR-0005` acceptance. No new
Gate H rerun, prepare, flash, erase, monitor, serial-write expansion, PCAP,
BLE, mesh, relay/XBee, TFT, MicroSD, load, mains, or router/admin action was
run.

## Verified Facts

- Read-only preflight with default peer ports stopped because current Windows
  peer inventory was `COM9`/`COM6`/`COM7`, not `COM4`/`COM5`/`COM6`.
- Read-only preflight with explicit accepted remap `COM9`/`COM6`/`COM7`
  reported `ok:true`.
- Coordinator identity: `/dev/ttyUSB0`, MAC `78:e3:6d:10:4d:6c`, ESP32-D0WDQ6,
  4 MB flash.
- Peer remap identity:
  `peer01=COM9/94:b9:7e:da:17:d0`,
  `peer02=COM6/78:e3:6d:0a:90:14`,
  `peer03=COM7/94:b9:7e:da:9a:50`.
- Gate G export source spool:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/spool.sqlite3`.
- DOS-C export artifact:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/analytics-report.v1.json`.
- ESP32 ignored proof copy:
  `research/bench-records/live-bench/gate-h-structured-live-20260525T155900Z/analytics-report.v1.json`.
- Export verification reported schema `gate-g.analytics.v1`, status
  `live_export`, privacy policy `adr-0005-redacted-local-operator-v1`,
  retention `7_days`, one direct message, one file request, four node-status
  rows, no Win31 control, and no firmware request.
- String audit did not find the known message body, `sysop`, `client-01`, or
  default file names in the JSON report.
- Cleanup proof removed one stale `analytics-report-stale.json` file and kept
  the current `analytics-report.v1.json`.

## Assumptions

- Reusing the structured Gate H proof spool is sufficient for Gate G export
  proof because the export reads local bridge evidence and does not require a
  new live radio run.

## Unknowns

- Firmware export ABI remains unresolved.
- Win31/OPCON export UI remains unresolved.
- A live bridge request type for analytics export remains unresolved.

## Validation

- `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.105 --windows-ports COM9 COM6 COM7 --allow-peer-port-remap --summary`: `ok:true`.
- `python3 software/espnow-bbs-bridge/espnow_bbs_bridge.py --spool <proof>/spool.sqlite3 --analytics-policy adr-0005-redacted-local-operator-v1 --export-analytics-json <proof>/analytics-report.v1.json`: wrote export.
- `python3 software/espnow-bbs-bridge/espnow_bbs_bridge.py --cleanup-analytics-exports <proof> --cleanup-analytics-older-than-days 7`: removed one stale export.

## Result

Gate G live export passed as a local-admin redacted proof artifact. The export
surface remains closed to Win31 controls, firmware ABI, and bridge request
types.
