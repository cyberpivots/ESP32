# Mains Readiness Gate

## Verified facts

- The current project has no source-backed load type, load voltage/current,
  enclosure, overcurrent protection, grounding/bonding plan, strain relief
  design, or qualified electrical review. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- NIOSH electrical safety material identifies qualified-person boundaries and
  recommends de-energizing circuits, lockout, voltage testing, insulated tools,
  and PPE for electrical injury prevention. Source ID:
  `SRC-NIOSH-ELECTRICAL-SAFETY`.
- OSHA de-energized-work material warns that a system is not properly
  de-energized until hazardous-energy controls and grounding requirements are
  satisfied. Source ID: `SRC-OSHA-DEENERGIZED-WORK`.
- OSHA GFCI and grounding references provide safety context for ground-fault
  protection, equipment grounding, continuity/terminal checks, and protective
  devices. Source IDs: `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`.
- NEMA maintains enclosure standards and enclosure type references for
  electrical equipment; this project has not selected an enclosure type. Source
  ID: `SRC-NEMA-ENCLOSURES`.

## Assumptions

- The intended user-facing prototype can be proven with relay contacts
  disconnected or with a reviewed low-voltage dummy load.
- Any mains switching path requires a separate design package and qualified
  review before wiring.

## Unknowns

- Whether the final load is mains AC, DC, inductive, capacitive, resistive, or
  outside the relay module's safe scope.
- Required enclosure type, ingress/environment constraints, physical mounting,
  spacing, strain relief, fuse or breaker selection, conductor sizing, ground
  continuity, and local code requirements.
- Whether relay contacts are appropriate for the final load or whether a
  contactor, SSR, snubber, MOV, fuse, or other protective design is required.

## Hard-block checklist

Mains switching remains blocked until every item below has review evidence:

| Gate | Required evidence | Status |
| --- | --- | --- |
| Qualified review | Named qualified person or licensed reviewer, review date, and acceptance notes. | Blocked |
| Load definition | Load type, voltage, current, inrush, duty cycle, and fault assumptions. | Blocked |
| Enclosure | Source-backed enclosure type, material, mounting, guarding of live parts, and environmental rating. | Blocked |
| Overcurrent protection | Fuse/breaker/protective-device design matched to load, conductors, and enclosure. | Blocked |
| Grounding/bonding | Equipment grounding or isolation decision with continuity/test plan. | Blocked |
| Strain relief | Cord/cable entry, pullout protection, abrasion protection, and serviceability plan. | Blocked |
| GFCI/de-energization | GFCI or equivalent protection context, lockout/de-energization process, and voltage-verification method. | Blocked |
| Separation | Physical separation between low-voltage control wiring and hazardous voltage wiring. | Blocked |
| Labels and disconnect | Durable labeling and accessible disconnect concept. | Blocked |
| Test record | Inspection and test artifacts before first energization. | Blocked |

## Prohibited content in this workspace phase

- No step-by-step mains wiring instructions.
- No relay terminal mapping for line, neutral, or load.
- No suggested fuse size, wire gauge, enclosure type, or grounding topology
  without qualified review and source/code evidence.
- No live-load tests.

## Allowed next work

- Keep relay contacts disconnected.
- Use only reviewed low-voltage dummy loads for relay-contact proof.
- Collect source links and qualified-review requirements for a future design
  package.
