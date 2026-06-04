import type { ReactNode } from "react";
import { fireEvent, render, screen } from "@testing-library/react-native";
import { validateUiIntent, type UiIntentRecord } from "@cbbs/protocol";
import { CBBS_PRODUCT_WINDOWS_APP_IDS } from "@cbbs/product";
import { ProductWindowsShell } from "../src";

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
  const createHost = (name: string) => {
    const Host = React.forwardRef<unknown, MockNativeProps>(({ children, ...props }, ref) =>
      React.createElement(name, { ...props, ref }, children as ReactNode)
    );
    Host.displayName = name;
    return Host;
  };

  return {
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

describe("ProductWindowsShell", () => {
  test("renders all three product apps without developer-facing labels", () => {
    for (const appId of CBBS_PRODUCT_WINDOWS_APP_IDS) {
      const rendered = render(<ProductWindowsShell appId={appId} />);

      expect(screen.getByTestId(`windows-${appId}-shell`)).toBeTruthy();
      expect(screen.getByTestId(`windows-${appId}-banner`)).toBeTruthy();
      expect(screen.getByTestId(`windows-${appId}-menubar`)).toBeTruthy();
      expect(screen.getByTestId(`windows-${appId}-nav`)).toBeTruthy();
      expect(screen.getByTestId(`windows-${appId}-workspace`)).toBeTruthy();
      expect(screen.getByTestId(`windows-${appId}-side-panel`)).toBeTruthy();
      expect(screen.getByTestId(`windows-${appId}-transcript`)).toBeTruthy();
      expect(screen.getByText("OG Communication Retro3.1")).toBeTruthy();
      expect(screen.getByText(/Link wait \| In 0 \| Out 0 Err 0 \| Queue 0/)).toBeTruthy();

      const textContent = visibleText(rendered.toJSON());
      expect(textContent).not.toMatch(
        /RNW|fixture-only|local-only|source evidence|source-backed|developer|Dev Config|schema|ADR|task log|package|Advanced Details|Confirmation text|COM6|COM15|serial|XBee|\bRF\b|flash|relay|mains|PMK|LMK|private key/i
      );

      rendered.unmount();
    }
  });

  test("keeps the shell layout responsive without rigid wide rows", () => {
    render(<ProductWindowsShell appId="hardware-tools" />);

    expect(styleOf("windows-hardware-tools-body")).toMatchObject({
      flexDirection: "row",
      flexWrap: "wrap"
    });
    expect(styleOf("windows-hardware-tools-menubar")).toMatchObject({
      flexDirection: "row",
      flexWrap: "wrap"
    });
    expect(styleOf("windows-hardware-tools-workspace")).toMatchObject({
      flex: 1,
      flexBasis: 320,
      flexShrink: 1,
      minWidth: 280
    });
    expect(styleOf("windows-hardware-tools-side-panel")).toMatchObject({
      flexBasis: 260,
      flexGrow: 1,
      flexShrink: 1,
      maxWidth: 340,
      minWidth: 260
    });
  });

  test("opens and closes dropdown menus", () => {
    render(<ProductWindowsShell appId="hardware-tools" />);

    fireEvent.press(screen.getByTestId("windows-hardware-tools-menu-views"));
    expect(screen.getByTestId("windows-hardware-tools-menu-views").props.accessibilityState).toMatchObject({
      expanded: true
    });
    expect(screen.getByTestId("windows-hardware-tools-dropdown-views-radio")).toBeTruthy();

    fireEvent.press(screen.getByTestId("windows-hardware-tools-menu-views"));
    expect(screen.getByTestId("windows-hardware-tools-menu-views").props.accessibilityState).toMatchObject({
      expanded: false
    });
    expect(screen.queryByTestId("windows-hardware-tools-dropdown-views-radio")).toBeNull();
  });

  test("renders Sysop in exact Win31 category order", () => {
    render(<ProductWindowsShell appId="sysop" />);

    expect(screen.getByText("CBBS Sysop")).toBeTruthy();
    const pageIds = [
      "status",
      "messages",
      "files",
      "devices",
      "help",
      "peers",
      "link",
      "updates",
      "setup",
      "diagnostics",
      "locks"
    ];
    for (const pageId of pageIds) {
      expect(screen.getByTestId(`windows-sysop-page-${pageId}`)).toBeTruthy();
    }
    fireEvent.press(screen.getByTestId("windows-sysop-menu-messages"));
    expect(screen.getByTestId("windows-sysop-dropdown-messages-sysop.pullMessages")).toBeTruthy();
    expect(screen.getByTestId("windows-sysop-dropdown-messages-sysop.ackMessage")).toBeTruthy();
  });

  test("marks active page with selected accessibility state", () => {
    render(<ProductWindowsShell appId="hardware-tools" />);

    expect(screen.getByTestId("windows-hardware-tools-page-bench").props.accessibilityState).toMatchObject({
      selected: true
    });
    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    expect(screen.getByTestId("windows-hardware-tools-page-radio").props.accessibilityState).toMatchObject({
      selected: true
    });
  });

  test("renders only page-scoped Hardware Tools actions", () => {
    render(<ProductWindowsShell appId="hardware-tools" />);

    expect(screen.getByTestId("windows-hardware-tools-action-hardware.benchTargetReview")).toBeTruthy();
    expect(screen.queryByTestId("windows-hardware-tools-action-hardware.radioInventory")).toBeNull();

    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    expect(screen.getByTestId("windows-hardware-tools-action-hardware.radioInventory")).toBeTruthy();
    expect(screen.getByTestId("windows-hardware-tools-action-hardware.radioReadStatusPlan")).toBeTruthy();
    expect(screen.queryByTestId("windows-hardware-tools-action-hardware.benchTargetReview")).toBeNull();
  });

  test("emits local UI intents and renders unavailable transcript results for artifact reviews", () => {
    const intents: UiIntentRecord[] = [];
    render(<ProductWindowsShell appId="hardware-tools" onIntent={(intent) => intents.push(intent)} />);

    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-action-hardware.radioInventory"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-action-hardware.radioReadStatusPlan"));

    expect(intents).toHaveLength(3);
    for (const intent of intents) {
      expect(validateUiIntent(intent)).toEqual({ ok: true, errors: [] });
      expect(JSON.stringify(intent)).not.toMatch(/xbee|flash|serial|rf|relay|COM\d+|child_process|exec|spawn/i);
    }
    expect(intents[1]?.intent).toBe("view_proof");
    expect(screen.getAllByText("reason: adapter_unavailable").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("executed: false").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("available: false").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("noSecretScan: true").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("transcriptRef: activity-log").length).toBeGreaterThanOrEqual(2);
  });

  test("keeps dangerous controls and gate phrase inert", () => {
    const intents: UiIntentRecord[] = [];
    render(<ProductWindowsShell appId="hardware-tools" onIntent={(intent) => intents.push(intent)} />);

    fireEvent.changeText(screen.getByTestId("windows-hardware-tools-gate-phrase"), "READY");
    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-action-hardware.radioChangePlan"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-firmware"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-action-hardware.deviceUpdatePlan"));

    expect(intents).toHaveLength(2);
    expect(screen.getByTestId("windows-hardware-tools-action-hardware.deviceUpdatePlan").props.accessibilityState).toMatchObject({
      disabled: true
    });
    expect(screen.getByText("Gate phrase records notes but does not unlock closed work.")).toBeTruthy();
  });

  test("dropdown tools are scoped to the selected page", () => {
    render(<ProductWindowsShell appId="hardware-tools" />);

    fireEvent.press(screen.getByTestId("windows-hardware-tools-page-radio"));
    fireEvent.press(screen.getByTestId("windows-hardware-tools-menu-devices"));
    expect(screen.getByTestId("windows-hardware-tools-dropdown-devices-hardware.radioInventory")).toBeTruthy();
    expect(screen.queryByTestId("windows-hardware-tools-dropdown-devices-hardware.meshSummary")).toBeNull();
  });
});

function visibleText(node: unknown): string {
  if (node == null) {
    return "";
  }
  if (typeof node === "string" || typeof node === "number") {
    return String(node);
  }
  if (Array.isArray(node)) {
    return node.map((entry) => visibleText(entry)).join("\n");
  }
  if (typeof node === "object" && "children" in node) {
    const children = (node as { children?: unknown }).children;
    return visibleText(children);
  }
  return "";
}

function styleOf(testId: string): Record<string, unknown> {
  const style = screen.getByTestId(testId).props.style;
  if (Array.isArray(style)) {
    return Object.assign({}, ...style.map((entry) => (entry == null ? {} : entry)));
  }
  return typeof style === "object" && style !== null ? (style as Record<string, unknown>) : {};
}
