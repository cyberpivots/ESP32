# Handoff 0126 - XBee Hub-Spoke Host Plan To QA/Communications

Continuation record for Task 0176 `xbee-hub-spoke-host-plan`.

## Continue with

- Review `tools/simulators/xbee_hub_spoke/` and
  `scripts/xbee_radio_study.py hub-spoke-plan` as host-only planning surfaces.
- Keep `0x8B` as the 900HP transmit-status fixture for `0x10` requests.
- Expand semantic protocol tests only if they remain synthetic and do not open
  serial ports, launch Digi tools, transmit RF, mutate firmware, or touch
  relay/load/mains.

## Stop gates

- No serial open, AT read/write, `WR`, `AC`, `KY`, XCTU/XBee Studio launch, API
  transmit to hardware, RF/range/throughput, firmware update/recovery, bridge
  dispatch, ESP32 carrier wiring, relay/load/mains, release, commit, push, PR,
  or deploy without a fresh gate.
- Do not publish raw radio identifiers, keys, address plans, private COM
  mappings, passive bytes, or full setting snapshots.

## Validation to preserve

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 176
git diff --check
```
