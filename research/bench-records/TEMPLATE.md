# Bench Record Template

Use this template for physical evidence records. Keep measurements and photos in
local records until a curated public-safe summary is reviewed.

## Record metadata

- Record ID:
- Date:
- Operator:
- Workspace:
- Device/project:
- Bench location:
- Scope:
- Excluded work:

## Source coverage

- Source IDs reviewed:
- Local records reviewed:
- New source-index entries required:

## Verified facts

- Fact:
- Evidence:
- Measurement or source ID:

## Assumptions

- Assumption:
- Why it is still only an assumption:
- Closure path:

## Unknowns

- Unknown:
- Risk if unresolved:
- Next measurement/source needed:

## Board and shield power

- Exact ESP32 board markings:
- Expansion shield markings:
- USB-UART marking:
- Regulator marking:
- Jumper position:
- Selected power input:
- Supply voltage measured:
- 3.3 V rail measured:
- 5 V rail measured:
- Current-limit setting:
- Brownout or reset observed:
- Reverse/overcurrent protection evidence:
- Boot-pin or strapping risk:
- Stop condition triggered:

## Relay module

- Exact module markings:
- Relay component markings:
- Input voltage measured:
- Trigger polarity measured:
- Input current measured per channel:
- `JD-VCC`/`VCC` jumper state:
- Isolation evidence:
- Contact/load terminals disconnected:
- Low-voltage dummy-load fixture used:
- GPIO or expander path under test:
- Result:
- Stop condition triggered:

## MicroSD reader

- Exact reader markings:
- Power path measured:
- Pull-ups present or unresolved:
- Card-detect/write-protect behavior:
- Candidate SPI pins:
- Shield continuity result:
- Card capacity/class:
- FAT preparation method:
- Low-space behavior tested:
- Log rotation behavior tested:
- Web fallback behavior tested:
- Result:

## XBee adapter or carrier

- Exact adapter/carrier markings:
- Serial port:
- UART voltage measured:
- DIN/DOUT routing:
- PC dock only or ESP32 carrier candidate:
- Tier A passive discovery result:
- Tier B read-query result:
- AT reads attempted:
- Setting writes attempted:
- Redaction applied:
- Result:

## TFT module

- Exact module markings:
- Controller identity evidence:
- Interface width/pinout:
- Supply voltage:
- Backlight current/path:
- Touch interface:
- Driver path:
- Shared pin-budget conflicts:
- Boot/flash/UART0 risks:
- Result:

## Mux

- Exact breakout markings:
- Select/enable wiring:
- ADC1 input path:
- Voltage protection:
- Source impedance:
- Input-only scan proof:
- Relay-output claims excluded:
- Result:

## Expander

- Exact expander board:
- Address pins:
- Pull-ups:
- Inactive defaults:
- Output latch behavior:
- Readback behavior:
- Driver-stage boundary:
- Relay-current compatibility unresolved:
- Result:

## Instruments and fixtures

- DMM:
- Current-limited bench supply:
- Logic analyzer or LED proof fixture:
- USB serial tools:
- Labeled harnesses:
- Low-voltage dummy loads:
- Calibration/identity notes:

## Qualified review gate

- Load/mains work requested:
- Qualified reviewer:
- Enclosure evidence:
- Overcurrent protection evidence:
- Grounding/bonding evidence:
- Strain relief evidence:
- GFCI/de-energization evidence:
- Separation/label/disconnect evidence:
- Decision: blocked until qualified review remains complete.

## Outcome

- Pass/fail:
- Files updated:
- New known gaps:
- Next owner:
