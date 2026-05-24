# Handoff 0024 - Win31 Viewfinder Downloads OTAP Gate To QA

Task:
[../TASK_LOG/0034-win31-viewfinder-downloads-otap-gate-alignment.md](../TASK_LOG/0034-win31-viewfinder-downloads-otap-gate-alignment.md)

## Continue With

- Use the paired DOS-C task
  `/mnt/h/dos-c/.agents/tasks/0014-win31-viewfinder-downloads-otap.md`.
- Capture or copy the next live OPCON evidence packet after launching the
  updated Win31 dashboard.
- Run the DOS-C vision gate, then run
  `scripts/espnow_bbs_live_gate.py complete` with matching manifest,
  flash evidence, bridge transcript, cleanup proof, and vision-gate JSON.

## Required Evidence Before Acceptance

- Fresh same-session device identity, power/USB-only state, backups, build
  hashes, manifest, recovery commands, write/verify evidence, bridge
  transcript, screenshot hashes, and cleanup proof.
- Visible OPCON Home, Peers, Message Board, Downloads, Network, OTAP,
  Diagnostics/Safety, disabled unsafe controls, and Program Manager item when
  present.
- Transcript proof for BBS requests plus `download_list`, `download_status`,
  `otap_status`, and `otap_intent` returning `executed:false`.

## Closed Gates

Do not treat the Win31 OTAP screen as live flashing authority. Keep PCAP,
packet-driver, router admin, BLE, ESP-WIFI-MESH live action, relay, XBee, TFT,
MicroSD, load, mains, erase, monitor, and serial write expansion closed unless
a later explicit gate opens them.
