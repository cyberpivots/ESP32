# Handoff 0020: ESP-NOW BBS Network Live-Gate QA

Task: [../TASK_LOG/0030-espnow-bbs-network-live-gate-design.md](../TASK_LOG/0030-espnow-bbs-network-live-gate-design.md)

## Continue With

- Review ADR-0004 while keeping status `Proposed` until a migration is
  explicitly accepted.
- Verify the paired DOS-C Win31 dashboard shows the Network view over the
  existing COM1/nullmodem bridge in a simulator or live read-only run.
- Keep all network mutation controls disabled or intent-only.

## Required Evidence Before Live Acceptance

- Fresh board/Pi identity, USB serial mapping, power/voltage/boot-pin/isolation
  review, backups, build hashes, and recovery commands.
- ESP-WIFI-MESH router policy, mesh ID, route-table, parent, root, layer, and
  healing proof.
- Wi-Fi/BLE coexistence proof under representative traffic.
- Android BLE permissions, bonding/SMP status, advertising content review, and
  GATT service/characteristic inventory.
- Cleanup proof for bridge, DOSBox-X, modals, and listeners after the run.

## Closed Gates

No live flash, router admin change, BLE pairing, Android build, serial write,
packet-driver/PCAP path, relay, XBee, TFT, MicroSD, load, or mains action is
authorized by this handoff.
