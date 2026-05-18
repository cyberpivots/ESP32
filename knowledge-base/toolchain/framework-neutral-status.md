# Framework-Neutral Status

## Current decision

ADR-0001 keeps the workspace framework-neutral by default.

ADR-0002 accepts ESP-IDF stable v6.0.1 only for the
`four-relay-xbee-wifi` project design and future firmware implementation.

## Prohibited until ADR acceptance

- `CMakeLists.txt`
- `sdkconfig`
- `sdkconfig.*`
- `platformio.ini`
- `idf_component.yml`
- `arduino-cli.yaml`
- framework-specific firmware source

## Allowed

- Architecture docs
- Interface contracts
- Source-backed hardware profiles
- Verification scripts
- Research ledgers
- Project-specific ADRs and design notes that do not add framework-dependent
  firmware source
