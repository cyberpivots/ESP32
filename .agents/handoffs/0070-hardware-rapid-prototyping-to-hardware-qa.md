# Handoff 0070: Hardware Rapid Prototyping To Hardware QA

Date: 2026-05-28

Task:
[../TASK_LOG/0081-hardware-rapid-prototyping.md](../TASK_LOG/0081-hardware-rapid-prototyping.md)

## Current State

- A new cross-project hardware rapid-prototyping plan lives at
  [../../docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md](../../docs/projects/hardware-rapid-prototyping/3d-printed-prototype-development.md).
- The lane is Tier 2 documentation/status/source-record work only.
- The plan records printer defaults for K1, Kobra 2 Max, CR-30, and CR-Scan
  Lizard, plus material, CAD, scanner, guide-template, and stop-gate rules.
- The accepted BBS serial-nullmodem path is preserved and the
  `remote-lcd-xbee-solar-client` stream remains separate from BBS/network
  runtime work.

## QA Focus

1. Confirm future build guides keep verified facts, assumptions, unknowns,
   risks, and required evidence separate.
2. Confirm K1 hardened-nozzle status remains user-stated until same-session
   physical evidence proves the upgrade.
3. Confirm ABS, ASA, PA/nylon, PA-CF, PET-CF, and other engineering-material
   guides require SDS, ventilation, drying, nozzle, enclosure, and thermal
   evidence before becoming build instructions.
4. Confirm CR-Scan Lizard output is treated as reference geometry until
   caliper or known-dimension verification is recorded.
5. Confirm CR-30 work remains limited to batch/long rails/cable guides after
   belt adhesion and slicer calibration proof.
6. Confirm no new firmware, framework, serial, radio, bridge, mesh, Win31,
   relay/load/mains, battery/solar, or live bench authority is inferred from
   this documentation lane.

## Validation Recorded

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: changed-file source-ID scan over 14 Markdown files.
- PASS: changed-file Markdown link check over 14 Markdown files.
- PASS: `git diff --check`

## Stop Gates

Do not use this program to authorize live bench action, wiring, flashing,
monitor/serial write, radio write, BLE/live mesh, relay/load/mains work,
battery or solar charging, firmware runtime change, framework selection,
public runtime API change, firmware ABI change, bridge ABI change,
`mesh_discovery.v1` schema change, Gate F service map change, Win31 transport
change, CAD source implementation, bulky vendor artifact, slicer project,
G-code, or raw scanner capture.
