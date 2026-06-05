# Handoff 0130 - XBee Tier A No-Serial Identity Evidence To QA/Communications/Hardware

Continuation record for Task 0182
`xbee-tier-a-no-serial-identity-evidence`.

## Continue with

- Treat Task 0182 as status accepted for the record-only/no-serial evidence
  boundary, not as Tier A completion.
- Use
  `SRC-LOCAL-XBEE-TIER-A-NO-SERIAL-IDENTITY-EVIDENCE-2026-06-05`
  for the accepted no-serial status packet.
- Before Tier A can complete, capture the second one-at-a-time adapter
  disconnect/reconnect delta plus same-session physical adapter markings,
  antenna state, isolation notes, voltage/header/carrier facts, recovery path,
  and cleanup evidence.
- Keep historical Task 0091/0092/0096 evidence scoped to selected-port
  programming, benign RF proof, and COM6 bridge retest only. Do not use those
  records to infer current physical adapter identity.

## Stop Gates

- No Tier B AT read-query, XCTU selected-port local discovery, XBee Studio
  operation, serial open, broad COM scan, API transmit, RF/range/throughput,
  setting write, `WR`, `AC`, `KY`, firmware update/recovery, ESP32 carrier
  wiring, relay/load/mains, flash, erase, monitor, release, publication, commit,
  push, PR, deploy, `/etc/codex/requirements.toml`, or `admin-strict` mutation
  is authorized by Task 0182.
- Do not publish raw COM/PnP mappings, `SH`/`SL`, AES keys, address plans,
  passive bytes, full setting snapshots, or private local evidence.

## Validation to preserve

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py inventory --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py identity-delta --before <before.json> --after <after.json> --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py xctu-discovery-plan --ports COM15 COM6 --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 182
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
git diff --check
```
