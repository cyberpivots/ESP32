# Handoff 0062 - Win31 CBBS Input, Rename, Icon, And UI To QA

Date: 2026-05-27

## Current State

- DOS-C implements the `CBBS` user-facing rename, original Win31-compatible
  icon, DDE-only Program Manager item repair, CBBS package/launcher names, and
  plain primary UI tasks.
- Local validation passed in DOS-C and ESP32.
- Live input acceptance is fail-closed because the same-session preflight found
  stale runtime and no physical movement/click matrix was captured.

## QA Focus

1. Re-run a fresh read-only preflight before any new live proof.
2. If the user wants live acceptance, decide whether to clean the stale
   bridge/DOSBox-X runtime left by the prior proof, then capture cleanup proof.
3. Run physical input A/B checks before changing tracked Pi DOSBox-X mouse
   settings.
4. For Program Manager acceptance, capture `COMMUNICATIONS` showing item
   `CBBS`, CBBS launched from that icon, transcript proof when serial behavior
   is claimed, and cleanup or explicit left-running proof.

## Do Not Claim

- Do not claim wireless pointer root cause.
- Do not claim permanent pointer fix.
- Do not claim live CBBS Program Manager/icon acceptance from this local pass.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP,
packet-driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT,
MicroSD, load, mains, erase, monitor, serial-write expansion, Gate G export,
tracked Pi DOSBox-X mouse config mutation, and unsafe controls remain closed.
