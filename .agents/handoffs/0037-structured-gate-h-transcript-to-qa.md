# Handoff 0037 - Structured Gate H Transcript To QA

Task:
[../TASK_LOG/0048-structured-gate-h-transcript.md](../TASK_LOG/0048-structured-gate-h-transcript.md)

## Status

Future Gate H proof packets should use the structured bridge JSONL transcript
as the machine-audit input. The earlier 2026-05-25 Gate H evidence remains
accepted with its manual-review visual caveat because it used the older summary
shape.

## Verified Facts

- Start the DOS-C bridge with
  `--audit-transcript <proof-dir>/bridge-transcript.jsonl`.
- Feed `<proof-dir>/bridge-transcript.jsonl` to both:
  - DOS-C `scripts/win31_dashboard_vision_gate.py --bridge-transcript`
  - ESP32 `scripts/espnow_bbs_live_gate.py complete --bridge-transcript`
- Keep `bridge.log` for human-readable request summaries only.
- Capture two OPCON telemetry refresh cycles: one before BBS/download/OTAP
  actions and one after them.
- Screenshots remain secondary corroboration; transcript and cleanup proof
  remain authoritative.

## Closed Gates

Keep PCAP, router/admin mutation, BLE, ESP-WIFI-MESH live action, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, and serial-write expansion closed
unless a later explicit gate opens them.
