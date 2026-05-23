# Handoff 0018 - ESP-NOW BBS Multi-Peer Live Proof

## From

Agent operations, Firmware, Communications, QA

## To

Firmware, Hardware, QA

## Context

DOS-C source now implements the next multi-peer dashboard slice, but live
three-peer acceptance is not proven.

## Continue With

- Fresh Pi identity and stale-listener cleanup proof.
- Fresh Windows serial inventory for exactly COM4, COM5, and COM6 CP210x peer
  devices.
- Read-only esptool identity for each peer before any write.
- Private read-flash backups and hashes for all boards to be written.
- Ignored live config generation under `secrets/espnow-bbs/live-<timestamp>/`.
- Clean coordinator and peer builds using the generated overrides.
- Flash only after identity, backup, build hash, and recovery gates pass.
- Win3.1 OPCON proof showing splash, Program Manager item, Message Board,
  three peers, `espnow-enc`, moving counters, zero serial errors, and disabled
  unsafe controls.
- Cleanup proof showing no DOSBox-X, modal, bridge process, or
  `31331`/`31332`/`8080` listener unless the user explicitly wants it left
  running.

## Stop Gates

- Do not infer COM4/COM5/COM6 identity from older evidence.
- Do not flash if any expected device is missing, duplicated, or reports an
  unexpected chip/MAC/flash profile.
- Do not open relay, XBee, TFT, MicroSD, load, mains, PCAP, router-admin, or
  packet-driver lanes from this handoff.
