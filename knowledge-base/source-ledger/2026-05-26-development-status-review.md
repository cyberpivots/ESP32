# Development Status Review Source Ledger - 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-DEVELOPMENT-STATUS-REVIEW-2026-05-26`

## Scope

Source-backed review of current ESP32 planning/development lanes and paired
DOS-C bridge/operator/live-proof truth. This task does not change runtime APIs,
firmware behavior, scripts, or tests.

## Verified Facts

- ESP32 required governance files, docs index, and source index were re-read
  before edits.
- `/mnt/h/ESP32` had existing uncommitted live-gate/tooling changes and
  untracked 0052/0041 LAN-DHCP records before this review started.
- `/mnt/h/dos-c` was clean before this review started.
- The accepted BBS path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25` is the
  strongest current Gate H live proof because it includes
  `bridge-transcript.jsonl`, pre/post telemetry refreshes, DOS-C vision `pass`,
  ESP32 completion `pass`, and cleanup proof.
- `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25` opens only
  local-admin redacted JSON export under accepted `ADR-0005`.
- `SRC-LOCAL-ESPNOW-LAN-DHCP-CURRENT-REMAP-2026-05-25` records a current
  read-only LAN/current-remap preflight but no BBS runtime proof.

## External Source Refresh

The active external primary sources referenced by current gaps and plans were
live-refreshed on 2026-05-26. The source-index `Accessed` dates were updated
only for sources verified on 2026-05-26.

Verified groups:

- GitHub Pages: what Pages is, publishing source, custom workflows, and limits.
- Espressif: ESP-IDF, ESP-NOW, esptool, Wi-Fi, HTTP server, GPIO, UART, NVS,
  FATFS, SDSPI, SDMMC, SD pull-ups, brownout, build-system flash args,
  ESP-WIFI-MESH, RF coexistence, BLE API, BLE SMP, ESP32 datasheets, DevKitC,
  hardware design checklist, examples, EIM docs, and EIM release.
- Android BLE and MDN Web Serial/Web Bluetooth.
- Raspberry Pi configuration and DOSBox serial configuration.
- Digi XBee, Waveshare adapter, XBee command/reference pages, and XCTU.
- Relay, TFT, expander, MicroSD/storage, bench-instrument, and safety sources:
  Songle mirror, LCDWiki, nopnop2002 README, TI, Littelfuse, SD Association,
  Fluke, Keysight, Saleae, CDC/NIOSH, OSHA, and NEMA.
- Microsoft ICS and NETGEAR WNR1000 references used by LAN/router evidence.
- Agricultural telemetry candidate sources: Lindsay, METER TEROS 12, Sentek,
  IRROMETER, and Geotab.

Refresh notes:

- The old Espressif stable Wi-Fi provisioning URL
  `api-reference/provisioning/wifi_provisioning.html` returned 404. The
  source-index row now points to the current stable Provisioning API index.
- Raspberry Pi, NEMA 250, METER, TaiwanIOT, and Keysight had curl or redirect
  behavior that was not enough by itself; browser fetches reached the pages.
- No vendor PDFs or bulky source artifacts were copied into the repository.

## Assumptions

- Source-index access-date updates are evidence that the source was reachable
  on 2026-05-26, not proof of local hardware identity or safe wiring.
- Local evidence source IDs remain dated to the run that produced them unless a
  new local proof was captured.

## Unknowns

- No new physical bench proof was captured by this documentation review.
- No source refresh can resolve local unknowns such as exact board revision,
  relay trigger polarity, USB-only physical state, or live BLE/mesh/PCAP proof.

## Validation

- ESP32 validation passed:
  `python3 scripts/verify_scaffold.py`,
  `python3 scripts/build_github_pages.py`,
  `python3 scripts/audit_public_manifest.py build/github-pages/public-file-manifest.json`,
  `python3 scripts/smoke_github_pages.py build/github-pages`, and
  `git diff --check`.
- DOS-C validation passed:
  `bash scripts/verify_scaffold.sh`,
  `python3 tests/espnow_bbs_bridge/test_bridge_protocol.py`,
  `bash tests/win31_operator/run_host_tests.sh`, and `git diff --check`.
- Evidence checks passed: every new ledger `SRC-*` ID exists in
  `knowledge-base/source-index.md`, every new review artifact linked from
  `docs/index.md` exists, and no tracked ESP32 or DOS-C ignored proof artifact
  path was found.
- Public docs audit initially flagged a raw private backup hash copied into the
  public source-index bundle; the source-index summary now keeps that hash in
  local-only bench evidence instead of publishing the raw value.

## Result

The current status is captured in
[../../research/development-status-ledger.md](../../research/development-status-ledger.md).
The prior blocked Gate H records are historical and superseded by later
accepted evidence; blocked filenames should not be rewritten.
