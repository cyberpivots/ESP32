import { useReducer } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { cbbsReducer, createInitialState } from "@cbbs/state";
import { cbbsFixtureSnapshot } from "@cbbs/fixtures";
import { OperatorShell } from "@cbbs/ui";
import type { UiIntentRecord } from "@cbbs/protocol";

const initialState = createInitialState("sysop", "home");

export default function ClientIndex() {
  const [state, dispatch] = useReducer(cbbsReducer, initialState);

  const onIntent = (intent: UiIntentRecord) => {
    dispatch(intent);
  };

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <OperatorShell
        snapshot={cbbsFixtureSnapshot}
        state={state}
        onIntent={onIntent}
      />
    </SafeAreaView>
  );
}
