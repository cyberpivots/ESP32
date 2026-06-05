# XBee Hub-Spoke Host-Only Plan

## Verified facts

- The repo radio part is tracked as Digi `XBP9B-DPUT-001`, XBee-PRO 900HP S3B
  Point2Multipoint, 900 MHz, 250 mW, U.FL, 10 kbps. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- Digi documents `AP=2` escaped API mode and `AO=0` standard Receive Packet
  `0x90`. Source IDs: `SRC-DIGI-XBEE-900HP-AP`,
  `SRC-DIGI-XBEE-900HP-AO`.
- Digi's 900HP/XSC API references map Transmit Request `0x10` to Extended
  Transmit Status `0x8B` for nonzero frame IDs. Source ID:
  `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`.
- Digi `TO` documentation records the 10k product default as `0x40` and says
  DigiMesh bits are not available on the 10k build. Source ID:
  `SRC-DIGI-XBEE-900HP-TO-2026-06-05`.
- The host-only simulator is implemented under
  `tools/simulators/xbee_hub_spoke/` and exposed through
  `scripts/xbee_radio_study.py hub-spoke-plan`. Source ID:
  `SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`.

## Assumptions

- Hub-spoke means one local hub/operator side and at least 10 redacted spoke
  aliases using point-to-multipoint planning for the current 10k part.
- Payloads stay compact JSON-like planning records unless future parser tests
  prove the `NP` budget requires another encoding.
- Hardware Tools may display saved hub-spoke planning evidence, but it does not
  dispatch live bridge, serial, RF, or relay actions.

## Unknowns

- Current radio settings, exact local port identity, key state, address plan,
  antenna/regulatory posture, carrier wiring, voltage evidence, and live payload
  limit are not proven by this plan.
- Remote LCD solar-client power budget, battery/charger facts, and telemetry
  schema remain unresolved.
- Any use of another 900HP variant, DigiMesh, repeater deployment, range test,
  throughput test, or live field topology requires a later sourced gate.

## Host-only use-case matrix

The simulator records these use cases as synthetic planning scenarios:

1. BBS custody acknowledgement backhaul.
2. Remote node heartbeat/status rollup.
3. Direct low-bandwidth BBS message exchange.
4. Packetized bulletin or small-file queue metadata.
5. Remote LCD field-console status feed.
6. Service catalog and capability report sideband.
7. Commissioning/link-probe and profile-readback evidence lane.
8. Remote telemetry snapshots from field spokes.
9. Hardware Tools saved-evidence analysis.
10. Non-executing control-intent audit trail.
11. Hub-spoke lock/safety-state broadcast.
12. Remote solar-client health beacon.

## Stop gates

This plan does not authorize serial-port opens, AT reads, AT writes, `WR`, `AC`,
`KY`, XCTU or XBee Studio launch, API transmit to a radio, RF/range/throughput
tests, firmware update/recovery, ESP32 DIN/DOUT wiring, bridge expansion,
relay/load/mains work, publication of raw identifiers, release, commit, push,
or PR creation.

Future Tier 3 work must name exact devices and ports, same-session authority,
physical isolation, voltage and antenna evidence, local-only key handling,
readback backup, rollback, redaction, cleanup proof, and a no-P1/P2 reviewer
quorum.

## Validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
```
