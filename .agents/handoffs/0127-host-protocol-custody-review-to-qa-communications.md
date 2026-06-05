# Handoff 0127 - Host Protocol Custody Review To QA/Communications

Continuation record for Task 0179 `host-protocol-custody-review`.

## Continue with

- Preserve the host-only simulator policy that semantic `custody_ack` packets
  require JSON body fields matching packet header fields before a custody
  record is updated.
- Treat byte-level Gate F golden vectors as codec fixtures unless a later gate
  explicitly changes their role.
- If firmware runtime work opens later, decide whether the firmware should
  adopt the same semantic ACK checks under a separate implementation gate.
- If XBee custody/backhaul work opens later, keep the XBee hub-spoke simulator
  and ESP-NOW custody semantics distinct until a source-backed bridge/backhaul
  contract exists.

## Stop gates

- No live hardware, serial open/write, AT read/write, `WR`, `AC`, `KY`,
  XCTU/XBee Studio launch, API transmit to hardware, RF/range/throughput,
  HostCommandBridge dispatch, firmware runtime migration, flash, erase,
  monitor, BLE, live mesh, PCAP, relay/load/mains, release, commit, push, PR,
  deploy, `/etc/codex/requirements.toml`, or `admin-strict` mutation without a
  fresh gate.

## Validation to preserve

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.custom_wireless_protocol.test_espnow_bbs_custom_protocol
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 179
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
git diff --check
```
