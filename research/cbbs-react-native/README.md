# CBBS React Native Research Notes

## Verified Facts

- The accepted lane is client/operator app work, not firmware work.
- Expo SDK 56 is the selected Android/iOS/browser lane for fixture work.
- RNW remains a separate Windows lane because its support line is versioned
  separately from Expo and React Native Web.
- Windows W0/W1 is host-only: source records, TypeScript source models,
  protocol/UI tests, audits, and CI validation only.
- Windows W2 is package-only: RNW/RN dependencies are scoped to
  `apps/cbbs-windows` and do not prove native build/run behavior.
- App Center is not selected for build, test, distribution, hosted CodePush, or
  analytics in this scaffold.

## Assumptions

- Host-only browser export and package tests are the next useful evidence.
- Device/simulator runs should be planned only after permission records and
  native-build gates.

## Unknowns

- Native distribution and signing model.
- Live local-network, BLE, serial, or Web Serial/Web Bluetooth transport.
- Windows runner/toolchain evidence, native project generation, package
  identity, capability manifest, signing, and runtime proof.

## Next Gates

1. Keep Phase 1 scaffold validation green.
2. Add browser export proof under a host-only gate.
3. Plan Android/iOS permissions before any simulator/device work.
4. Keep Windows W3/W4 native generation/build proof behind separate gates.
5. Open a separate Tier 3 gate for any live connectivity.
