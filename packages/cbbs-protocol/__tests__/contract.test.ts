import {
  APP_ROLES,
  CBBS_CLIENT_SCHEMA,
  CLOSED_SURFACE_IDS,
  INTENT_IDS,
  LOCAL_ONLY_REASON,
  VIEW_IDS,
  localIntent,
  validateUiIntent
} from "../src";

describe("CBBS client protocol contract", () => {
  test("pins stable roles, views, and intents", () => {
    expect(APP_ROLES).toEqual(["client", "sysop", "monitor", "devconfig"]);
    expect(VIEW_IDS).toEqual([
      "home",
      "messages",
      "downloads",
      "peers",
      "network",
      "diagnostics",
      "safety",
      "config",
      "evidence"
    ]);
    expect(INTENT_IDS).toEqual([
      "navigate",
      "refresh",
      "filter",
      "select_row",
      "open_detail",
      "compose_draft",
      "queue_file_request",
      "ack_local",
      "view_proof"
    ]);
  });

  test("accepts local fixture-only intents", () => {
    const intent = localIntent("navigate", "sysop", "home", { targetView: "messages" });
    expect(validateUiIntent(intent)).toEqual({ ok: true, errors: [] });
    expect(intent.localOnlyReason).toBe(LOCAL_ONLY_REASON);
  });

  test("rejects unsupported intent names", () => {
    const result = validateUiIntent({
      schema: CBBS_CLIENT_SCHEMA,
      intent: "serial_write",
      role: "sysop",
      view: "diagnostics",
      localOnlyReason: LOCAL_ONLY_REASON
    });
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("intent is not in the whitelist");
  });

  test("requires the exact local-only marker", () => {
    const missing = validateUiIntent({
      schema: CBBS_CLIENT_SCHEMA,
      intent: "refresh",
      role: "client",
      view: "home"
    });
    expect(missing.ok).toBe(false);
    expect(missing.errors.join(" ")).toContain("localOnlyReason must be fixture-only-ui-intent");

    const wrong = validateUiIntent({
      ...localIntent("refresh", "client", "home"),
      localOnlyReason: "demo"
    });
    expect(wrong.ok).toBe(false);
    expect(wrong.errors.join(" ")).toContain("localOnlyReason must be fixture-only-ui-intent");
  });

  test("rejects unknown and metadata-like keys", () => {
    const unknown = validateUiIntent({
      ...localIntent("refresh", "client", "home"),
      extra: "not allowed"
    });
    expect(unknown.ok).toBe(false);
    expect(unknown.errors.join(" ")).toContain("unknown intent key extra");

    for (const key of ["url", "endpoint", "path", "fileName", "content", "body", "host", "port"]) {
      const result = validateUiIntent({
        ...localIntent("refresh", "client", "home"),
        [key]: "blocked"
      });
      expect(result.ok).toBe(false);
      expect(result.errors.join(" ")).toContain(`unknown intent key ${key}`);
      expect(result.errors.join(" ")).toContain(`forbidden metadata field ${key}`);
    }
  });

  test("rejects non-string optional fields", () => {
    const result = validateUiIntent({
      ...localIntent("select_row", "client", "messages"),
      rowId: 123
    });
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("rowId must be a string");
  });

  test("rejects secret-like fields recursively", () => {
    const result = validateUiIntent({
      ...localIntent("refresh", "monitor", "network"),
      nested: { token: "redacted" }
    });
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("secret-like field nested.token");
  });

  test("rejects oversized intent payloads", () => {
    const result = validateUiIntent({
      ...localIntent("compose_draft", "client", "messages"),
      draftText: "x".repeat(700)
    });
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("exceeds 512 bytes");
  });

  test("rejects live-action values even in whitelisted local intents", () => {
    const result = validateUiIntent({
      ...localIntent("open_detail", "sysop", "safety"),
      rowId: "relay-test"
    });
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("forbidden live-action value rowId");
  });

  test("pins closed surface ids for fixture/UI parity", () => {
    expect(CLOSED_SURFACE_IDS).toEqual([
      "bridge_abi",
      "serial_abi",
      "firmware_abi",
      "gate_f_service_code",
      "serial_write",
      "rf_xbee_write",
      "ble_pairing",
      "web_bluetooth",
      "web_serial",
      "softap_probe",
      "local_network_discovery",
      "flash_erase_monitor",
      "relay_or_load",
      "persistent_config_write",
      "native_prebuild",
      "native_windows_project",
      "external_service_build"
    ]);
  });
});
