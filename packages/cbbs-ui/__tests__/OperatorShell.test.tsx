import { fireEvent, render, screen } from "@testing-library/react-native";
import { cbbsFixtureSnapshot } from "@cbbs/fixtures";
import { APP_ROLES, CLOSED_SURFACE_IDS, INTENT_IDS, LOCAL_ONLY_REASON, VIEW_IDS, type UiIntentRecord } from "@cbbs/protocol";
import { createInitialState } from "@cbbs/state";
import { OperatorShell } from "../src";

describe("OperatorShell", () => {
  test("renders fixture-only closed authority labels", () => {
    render(
      <OperatorShell
        snapshot={cbbsFixtureSnapshot}
        state={createInitialState("sysop", "home")}
        onIntent={() => undefined}
      />
    );

    expect(screen.getByText("CBBS")).toBeTruthy();
    expect(screen.getByText("Serial writes")).toBeTruthy();
    expect(screen.getByText(/Transcript-first fixture evidence/)).toBeTruthy();
  });

  test("renders every role and view without opening live surfaces", () => {
    for (const role of APP_ROLES) {
      for (const view of VIEW_IDS) {
        const rendered = render(
          <OperatorShell
            snapshot={cbbsFixtureSnapshot}
            state={createInitialState(role, view)}
            onIntent={() => undefined}
          />
        );

        expect(screen.getByText(`Fixture-only ${roleLabel(role)} console`)).toBeTruthy();
        expect(screen.getAllByText(view.toUpperCase()).length).toBeGreaterThan(0);
        rendered.unmount();
      }
    }
  });

  test("emits local-only intents for every enabled control", () => {
    const intents: UiIntentRecord[] = [];
    render(
      <OperatorShell
        snapshot={cbbsFixtureSnapshot}
        state={createInitialState("sysop", "home")}
        onIntent={(intent) => intents.push(intent)}
      />
    );

    fireEvent.press(screen.getByTestId("cbbs-view-tab-downloads"));
    fireEvent.press(screen.getByTestId("cbbs-row-row-home-local"));
    for (const intent of INTENT_IDS.filter((id) => id !== "navigate" && id !== "select_row")) {
      fireEvent.press(screen.getByTestId(`cbbs-action-${intent}`));
    }

    expect(new Set(intents.map((intent) => intent.intent))).toEqual(new Set(INTENT_IDS));
    for (const intent of intents) {
      expect(intent.localOnlyReason).toBe(LOCAL_ONLY_REASON);
    }
  });

  test("renders every closed surface as disabled", () => {
    render(
      <OperatorShell
        snapshot={cbbsFixtureSnapshot}
        state={createInitialState("sysop", "safety")}
        onIntent={() => undefined}
      />
    );

    for (const surface of CLOSED_SURFACE_IDS) {
      const control = screen.getByTestId(`cbbs-closed-surface-${surface}`);
      expect(control.props.accessibilityState).toMatchObject({ disabled: true });
    }
  });

  test("shows transcript-first proof id and fixture-only evidence summary", () => {
    render(
      <OperatorShell
        snapshot={cbbsFixtureSnapshot}
        state={createInitialState("client", "evidence")}
        onIntent={() => undefined}
      />
    );

    expect(screen.getByText(/proof-local-transcript-note/)).toBeTruthy();
    expect(screen.getByText(/no live browser, native device, Windows runner, or CBBS hardware proof/)).toBeTruthy();
  });
});

function roleLabel(role: (typeof APP_ROLES)[number]): string {
  const labels = {
    client: "Client",
    sysop: "Sysop",
    monitor: "Monitor",
    devconfig: "Dev Config"
  };
  return labels[role];
}
