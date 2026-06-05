import type { ReactNode } from "react";
import { fireEvent, render, screen } from "@testing-library/react-native";
import { AppRegistry } from "react-native";
import { validateUiIntent, type UiIntentRecord } from "@cbbs/protocol";
import {
  CbbsHardwareToolsWindowsApp,
  WINDOWS_HARDWARE_TOOLS_APP_COMPONENT_NAME
} from "../src";

type MockNativeProps = {
  children?: ReactNode;
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
    View: createHost("View"),
    useWindowDimensions: () => ({ width: 1280, height: 720, scale: 1, fontScale: 1 })
  };
});

describe("CBBS Hardware Tools Windows app", () => {
  test("registers and renders the Hardware Tools product surface", () => {
    expect(WINDOWS_HARDWARE_TOOLS_APP_COMPONENT_NAME).toBe("CbbsHardwareToolsWindows");
    expect(AppRegistry.getAppKeys()).toContain("CbbsHardwareToolsWindows");

    render(<CbbsHardwareToolsWindowsApp />);
    expect(screen.getByText("CBBS Hardware Tools")).toBeTruthy();
    expect(screen.getByTestId("windows-hardware-tools-shell")).toBeTruthy();
    expect(screen.queryByText(/COM6|COM15/)).toBeNull();
  });

  test("drives Hardware Tools page and artifact action without dispatch", () => {
    const intents: UiIntentRecord[] = [];
    render(<CbbsHardwareToolsWindowsApp onIntent={(intent) => intents.push(intent)} />);

    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-action-hardware.radioInventory"));

    expect(intents.map((intent) => intent.intent)).toEqual(["navigate", "view_proof"]);
    for (const intent of intents) {
      expect(validateUiIntent(intent)).toEqual({ ok: true, errors: [] });
      expect(JSON.stringify(intent)).not.toMatch(/HostCommandBridge|serial|xbee|rf|flash|relay|COM\d+|child_process|exec|spawn/i);
    }
    expect(screen.getByText("reason: adapter_unavailable")).toBeTruthy();
    expect(screen.getByText("executed: false")).toBeTruthy();
    expect(screen.getByText("available: false")).toBeTruthy();
  });
});
