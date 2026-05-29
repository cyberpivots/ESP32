# Handoff 0077 - XBee Read-Only Live-Radio Gate To QA

## Current State

The continued XBee/XCTU study is implemented as host-only tooling and records.
The Tier 3 live-radio gate failed closed before any serial port was opened.

New CLI behavior:

- `inventory --json --out <path>` writes only under
  `research/bench-records/xbee-readonly/`.
- `identity-delta --before FILE --after FILE --json` compares inventory files
  offline and redacts raw PnP/hardware IDs.
- `xctu-discovery-plan --ports COMx COMy --json` emits a locked manual
  checklist only; it does not launch XCTU or discover devices.
- `readonly` remains the only study command that can delegate to serial
  read-query traffic, and it still requires `--confirm-sends-read-commands`.
- There is still no `apply` command.

## Files To Review

- `scripts/xbee_radio_study.py`
- `tests/scaffold_audits/test_xbee_radio_study.py`
- `docs/projects/four-relay-xbee-wifi/xbee-radio-programming-study.md`
- `docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md`
- `knowledge-base/source-ledger/2026-05-29-xbee-read-only-live-radio-gate.md`
- `knowledge-base/source-index.md`
- `research/development-plan.md`
- `research/development-status-ledger.md`
- `research/triage-status.md`
- `research/known-gaps.md`
- `submodules/hardware/rlxsc-xbee-pro-s3b/`

## Local Evidence

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-20260529T043721Z/
```

The WSL and Windows inventory records show `serialOpenAttempted: false`. The
delta records are host/environment evidence only and are not physical
disconnect/reconnect adapter mapping proof.

## QA Focus

- Confirm `inventory`, `identity-delta`, `profile-diff`, `write-plan`, and
  `xctu-discovery-plan` do not open serial ports or write serial data.
- Confirm `xctu-discovery-plan` does not launch XCTU and keeps all-port
  discovery, broad parameter scans, network/remote discovery, writes, firmware,
  recovery, range, and throughput actions blocked.
- Confirm public records do not publish raw PnP IDs, raw passive bytes, SH/SL,
  AES keys, full setting snapshots, or private COM mappings.
- Confirm `readonly` remains fixed to `VR`, `HV`, `SH`, `SL`, `AP`, `AO`,
  `BD`, and `NP` and still requires confirmation.
- Confirm no `apply` command or radio write path exists.

## Still Blocked

Live adapter identity, one-at-a-time disconnect/reconnect mapping, Tier B radio
readback, XCTU Discover/Add, setting writes, `WR`, `AC`, API transmit frames,
firmware recovery/update, range/throughput tests, ESP32 carrier wiring,
relay/load/mains work, and public raw identifiers/private COM mappings remain
blocked until a future explicit Tier 3 gate has same-session physical evidence,
recovery path, cleanup criteria, and reviewer quorum.
