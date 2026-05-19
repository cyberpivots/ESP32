# TPIC6B595 Relay Driver Reference Profile

## Status

Reference-only relay driver candidate. It is not selected for the current relay
module until relay trigger polarity, input current, voltage compatibility, and
isolation behavior are verified.

## Verified Facts

- TI identifies TPIC6B595 as an 8-bit shift register with 150 mA per channel.
  Source ID: `SRC-TI-TPIC6B595`.
- TI documents an 8-bit serial-in, parallel-out shift register feeding an
  8-bit storage register and open-drain DMOS outputs with relay and solenoid
  application context. Source ID: `SRC-TI-TPIC6B595`.

## Assumptions

- TPIC6B595 is useful as a reference for low-side relay-driver architecture when
  an exact load path matches its electrical model.
- It is not automatically compatible with relay-module logic inputs,
  opto-isolated boards, active-low modules, or modules requiring a different
  current source/sink behavior.

## Required Verification Checklist

| Item | Required evidence before selection |
| --- | --- |
| Relay input model | Exact-module source or measurement for trigger polarity, current, and voltage. |
| Isolation behavior | Proof that the driver does not defeat the module isolation boundary. |
| Supply compatibility | Driver supply, logic levels, output voltage/current, and common-ground needs. |
| Boot behavior | Output-enable, clear, and storage-register defaults keep relay inputs inactive. |

## Unknowns

- Whether the exact relay module wants low-side sinking, high-side sourcing,
  dry-contact simulation, optocoupler current drive, or another interface.
- Whether a GPIO expander alone is enough for relay-module inputs or a separate
  driver device is required.
