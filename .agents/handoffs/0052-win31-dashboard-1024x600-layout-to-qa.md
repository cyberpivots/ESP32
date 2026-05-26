# Handoff 0052 - Win31 Dashboard 1024x600 Layout To QA

## Context

The DOS-C Win31 operator source has been refactored for the actual 1024x600
proof screen. The requested client is now 1000x500 so the top-left Win3.1 window
can use the available width while leaving room for frame and menu chrome.

## Verified Facts

- Source changed only under `/mnt/h/dos-c/software/win31-operator/` plus task
  records and local ledgers.
- Existing request handlers, resource IDs, bridge request types, serial
  transport, PCAP transport, and ESP32 firmware behavior were preserved.
- The two-row navigation vocabulary remains stable:
  `HOME`, `BBS BOARD`, `DOWNLOADS`, `NETWORK`, `PEERS`, `DEVICES`, `OTAP`,
  `SETTINGS`, `WIZARD`, `DIAGNOSTICS`, and `SAFETY`.
- Relay, Flash, Serial, and PCAP controls remain disabled and externally owned.
- DOS-C host tests, Open Watcom build, DOS-C vision-gate tests, ESP32 advisory
  analyzer tests, and scaffold checks passed after the source change.
- The latest copied structured Gate H packet still passes the DOS-C vision gate.
- ESP32 advisory analysis on that copied packet still maps `7/10` target views
  because it predates this layout and lacks Settings, Wizard, and Devices
  screenshots.
- No fresh copied screenshot packet exists yet for the 1000x500 layout.

## Next QA Step

Capture or copy a fresh revised UI packet without driving unsafe lanes. The
packet should include Home, BBS Board, Downloads, Network, Peers, Devices, OTAP,
Settings, Wizard, Diagnostics, and Safety views; `bridge-transcript.jsonl`;
cleanup proof; and a DOS-C `vision-gate.json`.

## Acceptance Checks

- DOS-C `scripts/win31_dashboard_vision_gate.py` reports `status: pass`.
- ESP32 advisory analyzer maps `10/10` target views.
- No `console_fit_risk` or `log_region_overflow`.
- Bottom margin is measured on the fresh 1024x600 packet and stays above the
  required quiet-zone threshold.
- Navigation-label gaps disappear or are reduced with source-backed evidence.
- OCR/CV remains advisory; bridge transcript behavior remains authoritative.

## Stop Gates

Do not open PCAP, packet-driver, BLE, mesh, router-admin, relay/XBee, TFT,
MicroSD, load, mains, ESP32 flash/erase/monitor, physical serial writes, or
firmware runtime migration as part of this visual QA handoff.
