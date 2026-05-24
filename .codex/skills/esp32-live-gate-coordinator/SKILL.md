---
name: esp32-live-gate-coordinator
description: Use when coordinating ESP32 ESP-NOW BBS live-gate work, completion audits, or source-backed handoffs between the ESP32 and DOS-C repositories.
---

# ESP32 Live Gate Coordinator

1. Re-read `AGENTS.md`, `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`, `.agents/ROLES.md`, `docs/index.md`, and `knowledge-base/source-index.md` before edits.
2. Keep verified facts, assumptions, unknowns, and stop gates separate in every durable record.
3. Treat `scripts/live_bench_preflight.py` as the read-only gate, `scripts/espnow_bbs_live_gate.py prepare` as the backup/manifest gate, `flash` as the write gate, and `complete` as the post-run evidence gate.
4. Require same-session physical confirmation before any prepare/flash action. Without it, stay in read-only audit or documentation mode.
5. Keep transcript proof authoritative for BBS behavior. Treat Win31 screenshots and DOS-C vision-gate JSON as UI corroboration.
6. Keep closed lanes closed: relay, XBee, TFT, MicroSD, load, mains, erase, monitor, PCAP, packet-driver, BLE, ESP-WIFI-MESH, router admin, or serial-write expansion.

For exact artifact expectations, read `references/live-completion-evidence.md`.
