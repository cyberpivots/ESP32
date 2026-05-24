# Handoff 0024 - Win31 Viewfinder Downloads OTAP Gate To QA

Task:
[../TASK_LOG/0034-win31-viewfinder-downloads-otap-gate-alignment.md](../TASK_LOG/0034-win31-viewfinder-downloads-otap-gate-alignment.md)

## Continue With

- Use the paired DOS-C task
  `/mnt/h/dos-c/.agents/tasks/0014-win31-viewfinder-downloads-otap.md`.
- The 2026-05-24 live OPCON evidence packet passed both the DOS-C vision gate
  and ESP32 completion gate:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-viewfinder-full-completion/full-completion-20260524T135020Z/`.
- Continue future work from the compact maximized Win31 viewfinder layout and
  the neutral cleanup-line parser behavior.

## Required Evidence Before Acceptance

- Fresh same-session device identity, power/USB-only state, backups, build
  hashes, manifest, recovery commands, write/verify evidence, bridge
  transcript, screenshot hashes, and cleanup proof.
- Visible OPCON Home, Peers, Message Board, Downloads, Network, OTAP,
  Diagnostics/Safety, disabled unsafe controls, and Program Manager item when
  present.
- Transcript proof for BBS requests plus `download_list`, `download_status`,
  `otap_status`, and `otap_intent` returning `executed:false`.

## Accepted Evidence

- `completion.json` status: `pass`
- `vision-gate.json` status: `pass`
- Bridge transcript: three `espnow-enc` peers, zero serial errors, moving
  RX/TX/ACK counters, BBS post/search/ack, Downloads queue/status, and gated
  OTAP intent.
- Cleanup: DOSBox-X, warning modal, bridge/proxy processes, and listeners
  `31331`, `31332`, `31333`, and `8080` clear.

## Closed Gates

Do not treat the Win31 OTAP screen as live flashing authority. Keep PCAP,
packet-driver, router admin, BLE, ESP-WIFI-MESH live action, relay, XBee, TFT,
MicroSD, load, mains, erase, monitor, and serial write expansion closed unless
a later explicit gate opens them.
