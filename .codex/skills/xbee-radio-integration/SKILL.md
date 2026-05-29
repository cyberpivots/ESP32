---
name: xbee-radio-integration
description: Use for Digi XBee, XCTU, XBee Studio, XBee-PRO 900HP/S3B, XBP9B-DPUT-001, radio profile, or repo-local XBee CLI study work in the ESP32 workspace.
---

# XBee Radio Integration

1. Re-read `AGENTS.md`, `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`,
   `.agents/ROLES.md`, `docs/index.md`, and `knowledge-base/source-index.md`
   before edits.
2. Keep verified facts, assumptions, unknowns, and stop gates separate.
3. Use `docs/projects/four-relay-xbee-wifi/xbee-radio-programming-study.md`
   for the current study boundary, and
   `docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md` for the
   existing Tier A/Tier B bench proof.
4. Treat `scripts/xbee_radio_study.py inventory`, `profile-diff`, and
   `write-plan` as host/offline Tier 2 tooling. Treat any command that opens a
   real serial port or communicates with a radio as live bench work requiring
   an explicit gate.
5. Do not write settings, send `WR` or `AC`, generate API transmit frames,
   update/recover firmware, range test, connect ESP32 DIN/DOUT, or touch relay,
   load, or mains paths unless a later Tier 3 packet names that authority.
6. Redact radio serial identifiers, `SH`/`SL`, raw passive bytes, AES keys,
   address plans, full setting snapshots, private COM mappings, and local bench
   records unless the task is explicitly local-only evidence handling.
7. Cite source-index IDs for XBee identity, XCTU/XBee Studio behavior,
   command/API facts, and local proof claims. Mark anything else as an
   unresolved gap.
