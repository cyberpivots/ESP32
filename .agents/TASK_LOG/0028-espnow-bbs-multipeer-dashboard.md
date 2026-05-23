# Task Log 0028 - ESP-NOW BBS Multi-Peer Dashboard

## Task

- ID: 0028-espnow-bbs-multipeer-dashboard
- Owner role: Firmware, Communications, QA
- Status: source implementation pending live proof
- Created: 2026-05-23
- Updated: 2026-05-23

## Goal

Track the source-level DOS-C implementation for the next RETRO-CBBS-NOW
multi-peer dashboard slice while preserving the accepted one-peer live proof
boundaries.

## Scope

Included:

- Win31 OPCON original retro splash and Message Board search/pull/post/ack UI.
- Bounded OPCON peer/message row parsing.
- Pi bridge `peer_list` upsert behavior and compact row limits.
- Coordinator serial `peer_list` source path.
- Three encrypted coordinator peer slots and ignored timestamped live config
  generation for `peer01` through `peer03`.
- Program Manager DDE helper source for a persistent dashboard item.
- ESP32 documentation and source ledger updates.

Excluded:

- Live flashing, erase, monitor, relay, XBee, TFT, MicroSD, load, mains, PCAP,
  router admin, or Windows COM proxy work.

## Sources

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESPTOOL-BASIC`
- `SRC-LOCAL-ESPNOW-ENCRYPTED-PEER-2026-05-22`
- `SRC-LOCAL-ESPNOW-MULTIPEER-DASHBOARD-2026-05-23`

## Validation

- Local DOS-C validation is recorded in the implementing DOS-C task.
- No live COM4/COM5/COM6 identity, flash, or three-peer radio acceptance is
  claimed by this ESP32 record.

## Handoff

Continue through
`.agents/handoffs/0018-espnow-bbs-multipeer-to-firmware-hardware-qa.md` before
any live bench action.
