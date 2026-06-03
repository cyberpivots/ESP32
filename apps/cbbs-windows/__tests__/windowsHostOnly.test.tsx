import { fireEvent, render, screen } from "@testing-library/react-native";
import { CLOSED_SURFACE_IDS, LOCAL_ONLY_REASON, validateUiIntent, type UiIntentRecord } from "@cbbs/protocol";
import {
  WindowsClientSysopShell,
  WindowsDependencyProof,
  createWindowsLocalIntent,
  windowsClientSysopPlan,
  windowsDependencyLane,
  windowsRoleProfiles,
  windowsSpikeStatus
} from "../src";

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

  test("models one role-aware client/sysop app with shared protocol constants", () => {
    expect(windowsClientSysopPlan.appShape).toBe("single-role-aware-windows-app");
    expect(windowsClientSysopPlan.localOnlyReason).toBe(LOCAL_ONLY_REASON);
    expect(windowsClientSysopPlan.modes.map((mode) => mode.role)).toEqual(["client", "sysop"]);
    expect(windowsClientSysopPlan.protocolClosedSurfaces).toEqual(CLOSED_SURFACE_IDS);
    expect(windowsClientSysopPlan.closedGates).toContain("native_windows_project");
    expect(windowsClientSysopPlan.closedGates).toContain("live_transport");
    expect(windowsClientSysopPlan.closedGates).toContain("signing_release");
  });

  test("renders Client and Sysop local shells without native runtime claims", () => {
    for (const profile of windowsRoleProfiles) {
      const rendered = render(<WindowsClientSysopShell activeRole={profile.role} />);

      expect(screen.getByText(`Fixture-only ${profile.label} Windows console`)).toBeTruthy();
      expect(screen.getByText("Package-only RNW lane; no Windows native runtime proof.")).toBeTruthy();
      expect(screen.getByText(`Local-only marker: ${LOCAL_ONLY_REASON}`)).toBeTruthy();
      for (const view of profile.views) {
        expect(screen.getByTestId(`windows-view-${profile.role}-${view}`)).toBeTruthy();
      }

      rendered.unmount();
    }
  });

  test("emits valid local-only intents from view and action controls", () => {
    const intents: UiIntentRecord[] = [];
    render(
      <WindowsClientSysopShell
        activeRole="client"
        activeView="messages"
        onIntent={(intent) => intents.push(intent)}
      />
    );

    fireEvent.press(screen.getByTestId("windows-view-client-downloads"));
    fireEvent.press(screen.getByTestId("windows-action-client-compose_draft"));
    fireEvent.press(screen.getByTestId("windows-action-client-queue_file_request"));
    fireEvent.press(screen.getByTestId("windows-action-client-view_proof"));

    expect(intents.map((intent) => intent.intent)).toEqual([
      "navigate",
      "compose_draft",
      "queue_file_request",
      "view_proof"
    ]);
    for (const intent of intents) {
      expect(validateUiIntent(intent)).toEqual({ ok: true, errors: [] });
      expect(intent.localOnlyReason).toBe(LOCAL_ONLY_REASON);
    }
  });

  test("renders every closed surface as disabled", () => {
    render(<WindowsClientSysopShell activeRole="sysop" activeView="safety" />);

    for (const surface of CLOSED_SURFACE_IDS) {
      const control = screen.getByTestId(`windows-closed-surface-${surface}`);
      expect(control.props.accessibilityState).toMatchObject({ disabled: true });
    }
  });

  test("keeps transcript-first evidence visible", () => {
    render(<WindowsClientSysopShell activeRole="client" activeView="evidence" />);

    expect(screen.getByText("Transcript-first Windows fixture evidence")).toBeTruthy();
    expect(screen.getByText("proof-local-transcript-note")).toBeTruthy();
    expect(screen.getByText(/No native device, Windows runner, transport, or CBBS hardware proof/)).toBeTruthy();
  });

  test("exports local intent helper and proof component without native runtime claims", () => {
    expect(validateUiIntent(createWindowsLocalIntent("refresh", "sysop", "home"))).toEqual({
      ok: true,
      errors: []
    });
    expect(typeof WindowsDependencyProof).toBe("function");
  });
});
