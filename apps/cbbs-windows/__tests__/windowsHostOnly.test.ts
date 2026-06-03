import { CLOSED_SURFACE_IDS } from "@cbbs/protocol";
import { WindowsDependencyProof, windowsClientSysopPlan, windowsDependencyLane, windowsSpikeStatus } from "../src";

describe("CBBS Windows host-only spike", () => {
  test("keeps native Windows generation closed while selecting package-only RNW deps", () => {
    expect(windowsSpikeStatus).toEqual({
      status: "package-only-rnw-dependency-lane",
      nativeProjectGenerated: false,
      nativeDependencySelected: true,
      requiredGate: "windows-runner-toolchain-review"
    });
    expect(windowsDependencyLane).toEqual({
      react: "19.2.3",
      reactNative: "0.83.9",
      reactNativeWindows: "0.83.0",
      reactNativeWindowsPackage: "react-native-windows",
      packageOnly: true,
      nativeProjectGenerated: false
    });
  });

  test("models one role-aware client/sysop app with local-only actions", () => {
    expect(windowsClientSysopPlan.appShape).toBe("single-role-aware-windows-app");
    expect(windowsClientSysopPlan.localOnlyReason).toBe("fixture-only-ui-intent");
    expect(windowsClientSysopPlan.modes.map((mode) => mode.role)).toEqual(["client", "sysop"]);
    expect(windowsClientSysopPlan.closedGates).toContain("native_windows_project");
    expect(windowsClientSysopPlan.closedGates).toContain("live_transport");
    expect(windowsClientSysopPlan.closedGates).toContain("signing_release");
  });

  test("keeps Windows protocol closed surfaces in parity", () => {
    expect(windowsClientSysopPlan.protocolClosedSurfaces).toEqual(CLOSED_SURFACE_IDS);
  });

  test("exposes a React Native primitive proof component without native runtime claims", () => {
    expect(typeof WindowsDependencyProof).toBe("function");
  });
});
