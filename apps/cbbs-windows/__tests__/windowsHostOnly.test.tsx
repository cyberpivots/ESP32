import type { ReactNode } from "react";
import { fireEvent, render, screen } from "@testing-library/react-native";
import { AppRegistry } from "react-native";
import { validateUiIntent, type UiIntentRecord } from "@cbbs/protocol";
import {
  CBBS_PRODUCT_WINDOWS_APP_IDS,
  WINDOWS_APP_COMPONENT_NAME,
  WindowsProductMigrationShell,
  legacyWindowsMigrationStatus,
  windowsProductAppProfiles
} from "../src";

type MockNativeProps = {
  children?: ReactNode;
  disabled?: boolean;
  onChangeText?: (text: string) => void;
  onPress?: () => void;
  value?: string;
  [key: string]: unknown;
};

jest.mock("react-native", () => {
  const React = jest.requireActual<typeof import("react")>("react");
  const registry: Record<string, unknown> = {};
  const createHost = (name: string) => {
    const Host = React.forwardRef<unknown, MockNativeProps>(({ children, ...props }, ref) =>
      React.createElement(name, { ...props, ref }, children)
    );
    Host.displayName = name;
    return Host;
  };

  return {
    AppRegistry: {
      getAppKeys: () => Object.keys(registry),
      registerComponent: (name: string, componentProvider: unknown) => {
        registry[name] = componentProvider;
        return name;
      }
    },
    Pressable: createHost("Pressable"),
    ScrollView: createHost("ScrollView"),
    StyleSheet: {
      create: <T extends Record<string, unknown>>(styles: T) => styles,
      flatten: (style: unknown): Record<string, unknown> => {
        if (Array.isArray(style)) {
          return Object.assign({}, ...style.map((entry) => (entry == null ? {} : entry)));
        }
        return typeof style === "object" && style !== null ? (style as Record<string, unknown>) : {};
      }
    },
    Text: createHost("Text"),
    TextInput: createHost("TextInput"),
    View: createHost("View")
  };
});

describe("CBBS Windows product migration shell", () => {
  test("registers the legacy component as a Sysop parity compatibility entry", () => {
    expect(WINDOWS_APP_COMPONENT_NAME).toBe("CbbsWindows");
    expect(AppRegistry.getAppKeys()).toContain("CbbsWindows");
    expect(legacyWindowsMigrationStatus).toMatchObject({
      defaultProductApp: "sysop",
      packageIdentityAccepted: false,
      capabilityUseAccepted: false,
      signingConfigured: false,
      releaseConfigured: false,
      liveExecutionAvailable: false
    });
    expect(legacyWindowsMigrationStatus.productApps).toEqual(CBBS_PRODUCT_WINDOWS_APP_IDS);
  });

  test("renders Sysop parity without the old developer cockpit wording", () => {
    render(<WindowsProductMigrationShell />);

    expect(screen.getByText("OG Communication Retro3.1")).toBeTruthy();
    expect(screen.getByText("CBBS Sysop")).toBeTruthy();
    expect(screen.getByTestId("windows-sysop-shell")).toBeTruthy();
    expect(screen.getByTestId("windows-sysop-page-status")).toBeTruthy();
    expect(screen.getByTestId("windows-sysop-page-locks")).toBeTruthy();
    expect(screen.queryByText(/RNW|fixture-only|local-only|source evidence|developer|Dev Config|schema|ADR|task log|Advanced Details|Confirmation text/i)).toBeNull();
  });

  test("exports the three product profiles", () => {
    expect(windowsProductAppProfiles.map((app) => app.id)).toEqual(["client", "sysop", "hardware-tools"]);
    expect(windowsProductAppProfiles.map((app) => app.title)).toEqual([
      "OG Communication Retro3.1",
      "OG Communication Retro3.1",
      "OG Communication Retro3.1"
    ]);
    expect(windowsProductAppProfiles.map((app) => app.subtitle)).toEqual([
      "CBBS Client",
      "CBBS Sysop",
      "CBBS Hardware Tools"
    ]);
  });

  test("Hardware Tools preview actions emit only local UI intents", () => {
    const intents: UiIntentRecord[] = [];
    render(<WindowsProductMigrationShell appId="hardware-tools" onIntent={(intent) => intents.push(intent)} />);

    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-action-hardware.radioInventory"));

    expect(intents).toHaveLength(2);
    for (const intent of intents) {
      expect(validateUiIntent(intent)).toEqual({ ok: true, errors: [] });
      expect(JSON.stringify(intent)).not.toMatch(/HostCommandBridge|serial|xbee|rf|flash|relay|COM\d+|child_process|exec|spawn/i);
    }
  });
});
