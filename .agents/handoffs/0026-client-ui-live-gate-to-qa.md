# Handoff 0026 - Client UI Live-Gate To QA

Task:
[../TASK_LOG/0036-client-ui-live-gate.md](../TASK_LOG/0036-client-ui-live-gate.md)

## Continue With

- Start with Stage 1 static or simulated UI only.
- Prove phone and laptop viewport readability, safety state, reject reasons,
  safety-lock, all-off, and dummy-output controls without live hardware
  mutation.
- Keep BLE and Serial/UART client surfaces design-only unless a later task
  opens separate live gates.

## Required Evidence Before Stage 2

- Selected ESP32 target with same-session board identity and USB/serial mapping.
- Power source, rail voltage, boot-pin, isolation, attached-peripheral, and
  recovery review.
- Selected Wi-Fi mode, SSID/authentication policy, addressing/provisioning
  record, and cleanup plan.
- Phone and laptop browser proof plan with screenshots and no hidden mutation.

## Required Evidence Before Stage 3

- Exact GPIO and dummy fixture selection.
- Proof that no relay module, relay contact, load, or mains path is attached.
- Firmware/build hashes and recovery commands if firmware changes.
- Command transcript showing monotonic sequence, source transport, accepted or
  rejected status, visible result, and explicit reject reason.
- Observed dummy-output result, all-off result, safety-lock rejection result,
  and cleanup evidence.

## Closed Gates

No relay coil energizing, relay contacts, loads, mains, firmware flash, firmware
erase, monitor expansion, hidden firmware mutation, serial writes outside the
accepted command path, PCAP, router-admin work, BLE pairing, Web Bluetooth live
proof, Android app live proof, or replacement of the accepted
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`
path is authorized by this handoff.
