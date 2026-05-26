# 20x4 I2C LCD Profile

## Status

Planning stub for the `remote-lcd-xbee-solar-client` lane. Exact LCD module and
I2C backpack are unresolved.

## Verified facts

- NXP documents PCF8574/74A as an 8-bit I2C-bus I/O expander with interrupt,
  quasi-bidirectional ports, hardware address inputs, and power-up inputs. This
  is candidate/reference coverage only and does not verify the exact LCD
  backpack. Source ID: `SRC-NXP-PCF8574-74A`.
- This workspace has not verified the exact 20x4 LCD module, LCD controller,
  backpack IC, I2C address, pullup voltage, logic voltage, backlight current, or
  pinout. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.

## Assumptions

- The display is intended for local status, not direct safety control.
- The LCD may use an I2C GPIO-expander backpack, but the expander family is not
  selected.

## Unknowns

- Exact display vendor, model, revision, controller, and backpack IC.
- Logic voltage, pullup voltage, I2C address, backlight current, and contrast
  adjustment method.
- Whether the module has onboard level shifting or 5 V-only pullups.
- Mechanical size, connector orientation, and enclosure fit.

## Risks

- 5 V pullups can overdrive ESP32 pins if no level shifting exists.
- LCD backlight current can exceed an assumed low-power budget.
- I2C address conflicts may appear if a fuel gauge or charger status device is
  later added.
- Pullups or control pins can interact with boot-sensitive ESP32 pins if assigned
  without a board-specific pin review.

## Required next evidence

- Exact module source or vendor datasheet.
- Physical inspection photos of controller/backpack markings.
- Measured or source-backed logic voltage, pullup voltage, and backlight current.
- I2C address record and bus-sharing review.
- ESP32 pin review after the exact board is selected.
