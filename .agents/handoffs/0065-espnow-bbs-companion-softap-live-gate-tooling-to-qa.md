# Handoff 0065: ESP-NOW BBS Companion SoftAP Live-Gate Tooling To QA

## Status

Implemented and host-validated. This handoff is for Tier 2 tooling validation
only and does not claim live proof.

## Verified Facts

- The accepted serial-nullmodem BBS path remains unchanged.
- Companion Gate 1 must keep dummy output disabled and prove only API behavior.
- Companion Gate 2 requires separate GPIO, no-load fixture, observation, and
  recovery evidence.

## QA Next Steps

1. Re-run ESP32 live-gate unit tests before any live gate continuation.
2. Re-run DOS-C companion generator and bridge tests before any live gate
   continuation.
3. Confirm no passphrase appears in prepare manifests or completion evidence.
4. Confirm `complete` requires `--companion-proof` only for manifests with
   companion HTTP enabled.
5. Confirm the PowerShell proof script records API state, all-off, disabled
   dummy-output rejection, wired-control probe, and temporary Wi-Fi profile
   cleanup without claiming physical output.

## Validation Recorded

- PASS: `python3 tests/live_bench/test_espnow_bbs_live_gate.py` (15 tests)
- PASS: `python3 -m py_compile scripts/espnow_bbs_live_gate.py`
- PASS: `python3 scripts/scaffold_audit_agent_process.py`
- PASS: `python3 scripts/verify_scaffold.py`
- PASS: `git diff --check`
- PASS: paired DOS-C generator test, bridge suite, scaffold verification, and
  no-flash companion-enabled coordinator plus peer01 ESP-IDF build.
- SKIPPED: PowerShell parse because `pwsh` is not installed in this environment.
- Not run: live `prepare`, `flash`, Windows Wi-Fi proof, bridge proof,
  vision gate, completion gate, or cleanup proof.

## Stop Gates

Do not open live flash, SoftAP proof, Windows Wi-Fi mutation, physical serial
writes, dummy GPIO/output, relay, XBee, TFT, MicroSD, load, mains, erase,
monitor, PCAP, router-admin, release gating, or cleanup acceptance from this
handoff.
