# ESP32 Development Workspace

This repository is the primary workspace for ESP32-based device development,
hardware integration research, firmware architecture, communication interfaces,
and multi-agent engineering operations.

The workspace starts framework-neutral. No firmware framework is selected until
an ADR explicitly chooses one. ADR-0002 accepts ESP-IDF stable v6.0.1 for the
`four-relay-xbee-wifi` project only.

## Current scaffold

- `AGENTS.md` is the root operating contract for all agents and contributors.
- `.agents/` contains governance, roles, task records, handoffs, and ADRs.
- `docs/` contains architecture, prompt, risk, and process documentation.
- `knowledge-base/` stores verified findings, source ledgers, and registries.
- `hardware-profiles/` stores source-backed device profiles and known gaps.
- `firmware/` is prepared for future implementation but contains no framework.
- `comm-protocols/` is prepared for wireless, wired, and custom protocol work.

## Active project packages

- `docs/projects/four-relay-xbee-wifi/` contains the first photographed
  ESP-WROOM-32 development board plus ESP32 I/O expansion shield, four-channel
  Songle relay module candidate, XBee-PRO 900HP, Waveshare XBee USB Adapter,
  local Wi-Fi UI design package, public build guide, and staged DIY
  bench-readiness documentation.

## Required workflow

1. Read `AGENTS.md`.
2. Check `.agents/GOVERNANCE.md` and `.agents/OWNERSHIP.md`.
3. If adding factual hardware, protocol, or toolchain information, update
   `knowledge-base/source-index.md` first.
4. Keep unknowns explicit. Do not convert assumptions into facts.
5. Run `python3 scripts/verify_scaffold.py` before handoff.
