# Handoff 0023 - Win31 Dashboard ML Live Gate To QA

Task: [../TASK_LOG/0033-win31-dashboard-ml-live-gate.md](../TASK_LOG/0033-win31-dashboard-ml-live-gate.md)

## Continue With

- Capture or copy the next live OPCON evidence packet into ignored local
  evidence paths.
- Run the DOS-C vision gate on copied screenshots, authoritative bridge
  transcript, and cleanup proof.
- Run `scripts/espnow_bbs_live_gate.py complete` with the matching manifest,
  flash evidence, transcript, cleanup proof, and DOS-C vision-gate JSON.
- Review `needs_manual_review` output manually before claiming acceptance.

## Required Evidence Before Live Acceptance

- Fresh same-session identity, power/USB-only state, backups, build hashes,
  manifest, recovery commands, write/verify evidence, bridge transcript,
  screenshot hashes, and cleanup proof.
- OPCON splash/dashboard, Peers, Message Board, Downloads, Network, OTAP,
  Diagnostics/Safety, disabled unsafe controls, Program Manager item when
  present, three `espnow-enc` peers, zero serial errors, moving RX/TX/ACK
  counters, `download_list`, `download_status`, `otap_status`, and
  non-executing `otap_intent`.
- Final proof that DOSBox-X, warning/quit modals, bridge process, and listeners
  on `31331`, `31332`, and `8080` are closed.

## Closed Gates

Do not open PCAP, packet-driver, router admin, BLE, ESP-WIFI-MESH live action,
relay, XBee, TFT, MicroSD, load, mains, erase, monitor, or serial write
expansion from this handoff.
