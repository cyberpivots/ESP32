import type { ReactNode } from "react";
import { fireEvent, render, screen } from "@testing-library/react-native";
import { AppRegistry } from "react-native";
import { validateUiIntent, type UiIntentRecord } from "@cbbs/protocol";
import { CbbsSysopWindowsApp, WINDOWS_SYSOP_APP_COMPONENT_NAME } from "../src";

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
    View: createHost("View")
  };
});

describe("CBBS Sysop Windows app", () => {
  test("registers and renders the Sysop product surface", () => {
    expect(WINDOWS_SYSOP_APP_COMPONENT_NAME).toBe("CbbsSysopWindows");
    expect(AppRegistry.getAppKeys()).toContain("CbbsSysopWindows");

    render(<CbbsSysopWindowsApp />);
    expect(screen.getByText("CBBS Sysop")).toBeTruthy();
    expect(screen.getByTestId("windows-sysop-shell")).toBeTruthy();
  });

  test("drives Sysop page and action as local-only UI intents", () => {
    const intents: UiIntentRecord[] = [];
    render(<CbbsSysopWindowsApp onIntent={(intent) => intents.push(intent)} />);

    fireEvent.press(screen.getByTestId("windows-sysop-page-messages"));
    fireEvent.press(screen.getByTestId("windows-sysop-action-sysop.pullMessages"));

    expect(intents.map((intent) => intent.intent)).toEqual(["navigate", "open_detail"]);
    for (const intent of intents) {
      expect(validateUiIntent(intent)).toEqual({ ok: true, errors: [] });
      expect(JSON.stringify(intent)).not.toMatch(/HostCommandBridge|serial|xbee|rf|flash|relay|COM\d+|child_process|exec|spawn/i);
    }
    expect(screen.getByTestId("windows-sysop-transcript")).toBeTruthy();
  });
});
