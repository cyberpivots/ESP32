import { localIntent } from "@cbbs/protocol";
import { cbbsReducer, createInitialState } from "../src";

describe("CBBS state reducer", () => {
  test("keeps navigation local", () => {
    const initial = createInitialState("sysop", "home");
    const state = cbbsReducer(
      initial,
      localIntent("navigate", "sysop", "home", { targetView: "diagnostics" })
    );
    expect(state.activeView).toBe("diagnostics");
    expect(state.lastValidation).toBe("ok");
  });

  test("treats queue_file_request as a local placeholder", () => {
    const initial = createInitialState("client", "downloads");
    const state = cbbsReducer(
      initial,
      localIntent("queue_file_request", "client", "downloads", { rowId: "row-download-request" })
    );
    expect(state.queuedLocalRequests).toEqual(["row-download-request"]);
  });

  test("rejects unsafe action wording before state changes", () => {
    const initial = createInitialState("sysop", "safety");
    const state = cbbsReducer(
      initial,
      localIntent("open_detail", "sysop", "safety", { rowId: "flash-command" })
    );
    expect(state.lastValidation).toBe("rejected");
    expect(state.detailId).toBeUndefined();
  });
});
