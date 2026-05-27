# Handoff 0058 - Win31 OPCON Dual Visual Style To QA

Task:
[../TASK_LOG/0069-win31-opcon-dual-style.md](../TASK_LOG/0069-win31-opcon-dual-style.md)

## Status

Implemented in DOS-C and locally validated. Fresh live visual proof is
deferred.

## Verified Facts

- Default OPCON style is Windows 3.1; ANSI Terminal remains selectable.
- The accepted serial-nullmodem path remains unchanged.
- Rebuilt ignored DOS-C `OPCON.EXE` SHA-256:
  `ac5d898cf4275548b80e61caddfa3681358f99c90506cdbd600930a14c557620`.
- Rebuilt ignored DOS-C `OPCONPC.EXE` SHA-256:
  `f6c8ae9f227914db53a2c3f91bd861cdbfae5cd9506aebac437e324bffcf5d85`.
- Validation passed in both DOS-C and ESP32 advisory tests.

## QA Next Steps

After fresh bench/session confirmation, capture a copied 1024x600 packet for
all ten Windows 3.1 default views, then switch to ANSI Terminal and capture
Home, Settings, and Safety. When a full acceptance packet is intended, include
`bridge-transcript.jsonl`, cleanup proof, DOS-C vision-gate output, and ESP32
completion output.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP, packet
driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load,
mains, erase, monitor, serial-write expansion, Gate G export, and forced
tracking of ignored runtime artifacts remain closed.
