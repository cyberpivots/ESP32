import {
  APP_ROLES,
  CBBS_CLIENT_SCHEMA,
  CLOSED_SURFACE_IDS,
  DOSC_WIN31_REQUEST_NAMES,
  DOSC_WIN31_REQUEST_NAMES_AUDIT_ONLY,
  HOST_COMMAND_ACTION_IDS,
  HOST_COMMAND_BRIDGE_SCHEMA,
  HOST_COMMAND_RESULT_STATUSES,
  HOST_COMMAND_UNAVAILABLE_REASON,
  INTENT_IDS,
  LOCAL_ONLY_REASON,
  MAX_HOST_COMMAND_BRIDGE_BYTES,
  VIEW_IDS,
  createUnavailableHostCommandResult,
  isDoscWin31RequestName,
  localIntent,
  validateHostCommandBridgeRequest,
  validateHostCommandBridgeResult,
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

  test("rejects secret-like fields for every value type", () => {
    for (const [key, value] of [
      ["token", 1],
      ["secret", true],
      ["pmk", 0],
      ["deviceId", false],
      ["privateKey", { redacted: true }],
      ["lmk", ["redacted"]],
      ["macAddress", null]
    ] as const) {
      const result = validateHostCommandBridgeRequest({
        ...validHostCommandRequest(),
        params: { [key]: value }
      });
      expect(result.ok).toBe(false);
      expect(result.errors.join(" ")).toContain(`secret-like field params.${key}`);
    }

    const result = validateHostCommandBridgeResult({
      ...createUnavailableHostCommandResult({ requestId: "request-secret-field" }, "2026-06-03T00:00:00.000Z"),
      deviceId: 7
    });
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("secret-like field deviceId");
  });

  test("rejects secret-like values in neutral HostCommandBridge fields", () => {
    for (const [label, override] of [
      ["target", { targetRef: "pmk" }],
      ["param", { params: { profile: "pairing-token" } }],
      ["result", { artifactRefs: ["private-key"] }]
    ] as const) {
      const result =
        label === "result"
          ? validateHostCommandBridgeResult(
              withExactBoundsProof({
                ...createUnavailableHostCommandResult({ requestId: "request-neutral-value" }, "2026-06-03T00:00:00.000Z"),
                ...override,
                boundsProof: {
                  ...createUnavailableHostCommandResult({ requestId: "request-neutral-value" }, "2026-06-03T00:00:00.000Z").boundsProof,
                  actualBytes: 0
                }
              })
            )
          : validateHostCommandBridgeRequest({
              ...validHostCommandRequest(),
              ...override
            });
      expect(result.ok).toBe(false);
      expect(result.errors.join(" ")).toMatch(/secret-like value/);
    }
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

  test("pins inert HostCommandBridge action ids separately from UI intents", () => {
    expect(HOST_COMMAND_ACTION_IDS).toEqual([
      "mesh.statusSnapshot",
      "mesh.serviceList",
      "radio.inventorySummary",
      "radio.queryPreview",
      "radio.profileCompare",
      "radio.changePreview",
      "firmware.artifactReview",
      "firmware.installPreview",
      "device.readinessCheck"
    ]);
    expect(HOST_COMMAND_ACTION_IDS.some((id) => INTENT_IDS.includes(id as (typeof INTENT_IDS)[number]))).toBe(false);
    expect(JSON.stringify(HOST_COMMAND_ACTION_IDS)).not.toMatch(/serial|xbee|rf|flash|erase|monitor|relay|write|apply|deploy|release|COM\d+/i);
  });

  test("exports DOS-C Win31 request names for audit only", () => {
    expect(DOSC_WIN31_REQUEST_NAMES_AUDIT_ONLY).toBe(true);
    expect(DOSC_WIN31_REQUEST_NAMES).toEqual([
      "hello",
      "state_get",
      "peer_list",
      "msg_pull",
      "msg_search",
      "msg_post",
      "msg_ack",
      "diag_get",
      "fw_inventory",
      "coordinator_state",
      "maint_intent",
      "download_list",
      "download_queue",
      "download_status",
      "discovery_snapshot",
      "discovery_events",
      "service_catalog",
      "capability_report",
      "otap_status",
      "otap_intent"
    ]);
    expect(isDoscWin31RequestName("state_get")).toBe(true);
    expect(isDoscWin31RequestName("raw_live_command")).toBe(false);
    expect(DOSC_WIN31_REQUEST_NAMES.some((id) => INTENT_IDS.includes(id as (typeof INTENT_IDS)[number]))).toBe(false);
    expect(DOSC_WIN31_REQUEST_NAMES.some((id) => HOST_COMMAND_ACTION_IDS.includes(id as (typeof HOST_COMMAND_ACTION_IDS)[number]))).toBe(false);
  });

  test("accepts bounded non-executing HostCommandBridge requests", () => {
    const request = validHostCommandRequest();

    expect(validateHostCommandBridgeRequest(request)).toEqual({ ok: true, errors: [] });
    expect(validateUiIntent(request).ok).toBe(false);
  });

  test("rejects DOS-C request type frames as UI intents and host commands", () => {
    const rawIntent = validateUiIntent({
      ...localIntent("refresh", "sysop", "home"),
      type: "state_get"
    });
    expect(rawIntent.ok).toBe(false);
    expect(rawIntent.errors.join(" ")).toContain("unknown intent key type");

    const rawHostCommand = validateHostCommandBridgeRequest({
      schema: HOST_COMMAND_BRIDGE_SCHEMA,
      requestId: "request-type-frame",
      appId: "hardware-tools",
      actorRole: "sysop",
      actionId: "radio.queryPreview",
      actionClass: "read",
      targetRef: "primary-radio",
      dryRun: true,
      timeoutMs: 1000,
      redactionProfile: "primary",
      idempotencyKey: "request-type-frame",
      type: "state_get"
    });
    expect(rawHostCommand.ok).toBe(false);
    expect(rawHostCommand.errors.join(" ")).toContain("unknown host command request key type");
  });

  test("rejects host-command requests with execution and identifier fields", () => {
    const result = validateHostCommandBridgeRequest({
      schema: HOST_COMMAND_BRIDGE_SCHEMA,
      requestId: "request-002",
      appId: "hardware-tools",
      actorRole: "sysop",
      actionId: "radio.queryPreview",
      actionClass: "read",
      targetRef: "COM6",
      params: { command: "powershell esptool flash" },
      dryRun: false,
      timeoutMs: 1000,
      redactionProfile: "primary",
      idempotencyKey: "query-preview-002",
      host: "localhost"
    });

    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("dryRun must be true");
    expect(result.errors.join(" ")).toContain("unknown host command request key host");
    expect(result.errors.join(" ")).toMatch(/forbidden host-command/);
  });

  test("rejects raw host-command action names and live-operation aliases", () => {
    const rawAction = validateHostCommandBridgeRequest({
      schema: HOST_COMMAND_BRIDGE_SCHEMA,
      requestId: "request-raw",
      appId: "hardware-tools",
      actorRole: "sysop",
      actionId: "firmware.flashCom6",
      actionClass: "install",
      targetRef: "primary-target",
      dryRun: true,
      timeoutMs: 1000,
      redactionProfile: "primary",
      idempotencyKey: "request-raw"
    });
    expect(rawAction.ok).toBe(false);
    expect(rawAction.errors.join(" ")).toContain("actionId is not in the host command allowlist");

    const rawValues = validateHostCommandBridgeRequest({
      schema: HOST_COMMAND_BRIDGE_SCHEMA,
      requestId: "request-live",
      appId: "hardware-tools",
      actorRole: "sysop",
      actionId: "radio.queryPreview",
      actionClass: "read",
      targetRef: "primary-xbee",
      params: { preview: "serial flash release" },
      dryRun: true,
      timeoutMs: 1000,
      redactionProfile: "primary",
      idempotencyKey: "request-live"
    });
    expect(rawValues.ok).toBe(false);
    expect(rawValues.errors.join(" ")).toMatch(/forbidden host-command/);
  });

  test("returns unavailable HostCommandBridge results without execution", () => {
    const result = createUnavailableHostCommandResult({ requestId: "request-003" }, "2026-06-03T00:00:00.000Z");

    expect(result).toMatchObject({
      schema: HOST_COMMAND_BRIDGE_SCHEMA,
      requestId: "request-003",
      accepted: false,
      executed: false,
      available: false,
      status: "unavailable",
      reason: HOST_COMMAND_UNAVAILABLE_REASON,
      artifactRefs: [],
      noSecretScan: true
    });
    expect(result.boundsProof.actualBytes).toBeLessThanOrEqual(512);
    expect(result.boundsProof.actualBytes).toBe(encodedBytes(result));
    expect(validateHostCommandBridgeResult(result)).toEqual({ ok: true, errors: [] });
    expect(validateUiIntent(result).ok).toBe(false);
  });

  test("rejects HostCommandBridge results with stale byte proofs", () => {
    const result = createUnavailableHostCommandResult({ requestId: "request-005" }, "2026-06-03T00:00:00.000Z");
    for (const actualBytes of [result.boundsProof.actualBytes - 1, result.boundsProof.actualBytes + 1]) {
      const stale = {
        ...result,
        boundsProof: {
          ...result.boundsProof,
          actualBytes
        }
      };
      const validation = validateHostCommandBridgeResult(stale);
      expect(validation.ok).toBe(false);
      expect(validation.errors.join(" ")).toContain("boundsProof.actualBytes must match encoded result bytes");
    }
  });

  test("rejects unavailable HostCommandBridge results without positive secret-scan proof", () => {
    const unavailable = createUnavailableHostCommandResult({ requestId: "request-secret-scan" }, "2026-06-03T00:00:00.000Z");
    const missingProof = withExactBoundsProof({
      ...unavailable,
      noSecretScan: false,
      boundsProof: {
        ...unavailable.boundsProof,
        actualBytes: 0
      }
    });

    const result = validateHostCommandBridgeResult(missingProof);
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("noSecretScan must remain true");
  });

  test("rejects all non-unavailable HostCommandBridge result statuses", () => {
    const unavailable = createUnavailableHostCommandResult({ requestId: "request-status-proof" }, "2026-06-03T00:00:00.000Z");

    for (const status of HOST_COMMAND_RESULT_STATUSES.filter((candidate) => candidate !== "unavailable")) {
      const result = validateHostCommandBridgeResult(
        withExactBoundsProof({
          ...unavailable,
          status,
          boundsProof: {
            ...unavailable.boundsProof,
            actualBytes: 0
          }
        })
      );
      expect(result.ok).toBe(false);
      expect(result.errors.join(" ")).toContain("status must remain unavailable");
    }
  });

  test("enforces exact 512-byte HostCommandBridge request and result bounds", () => {
    const exactRequest = sizedHostCommandRequest(MAX_HOST_COMMAND_BRIDGE_BYTES);
    expect(encodedBytes(exactRequest)).toBe(MAX_HOST_COMMAND_BRIDGE_BYTES);
    expect(validateHostCommandBridgeRequest(exactRequest)).toEqual({ ok: true, errors: [] });

    const oversizedRequest = sizedHostCommandRequest(MAX_HOST_COMMAND_BRIDGE_BYTES + 1);
    expect(encodedBytes(oversizedRequest)).toBe(MAX_HOST_COMMAND_BRIDGE_BYTES + 1);
    expect(validateHostCommandBridgeRequest(oversizedRequest).errors.join(" ")).toContain("exceeds 512 bytes");

    const exactResult = sizedUnavailableResult(MAX_HOST_COMMAND_BRIDGE_BYTES);
    expect(exactResult.boundsProof.actualBytes).toBe(MAX_HOST_COMMAND_BRIDGE_BYTES);
    expect(encodedBytes(exactResult)).toBe(MAX_HOST_COMMAND_BRIDGE_BYTES);
    expect(validateHostCommandBridgeResult(exactResult)).toEqual({ ok: true, errors: [] });

    const oversizedResult = sizedUnavailableResult(MAX_HOST_COMMAND_BRIDGE_BYTES + 1);
    expect(oversizedResult.boundsProof.actualBytes).toBe(MAX_HOST_COMMAND_BRIDGE_BYTES + 1);
    expect(validateHostCommandBridgeResult(oversizedResult).errors.join(" ")).toContain("host command result exceeds 512 bytes");
  });

  test("rejects HostCommandBridge results that claim execution or availability", () => {
    const unavailable = createUnavailableHostCommandResult({ requestId: "request-004" }, "2026-06-03T00:00:00.000Z");
    const executed = {
      ...unavailable,
      accepted: true,
      executed: true,
      available: true,
      status: "complete",
      reason: "done"
    };
    const result = validateHostCommandBridgeResult(executed);
    expect(result.ok).toBe(false);
    expect(result.errors.join(" ")).toContain("accepted must remain false");
    expect(result.errors.join(" ")).toContain("executed must remain false");
    expect(result.errors.join(" ")).toContain("available must remain false");
    expect(result.errors.join(" ")).toContain("status must remain unavailable");
    expect(result.errors.join(" ")).toContain("reason must remain adapter_unavailable");
  });
});

function validHostCommandRequest() {
  return {
    schema: HOST_COMMAND_BRIDGE_SCHEMA,
    requestId: "request-001",
    appId: "hardware-tools",
    actorRole: "sysop",
    actionId: "radio.queryPreview",
    actionClass: "read",
    targetRef: "primary-radio",
    params: { profile: "saved" },
    dryRun: true,
    gateRef: "future-review",
    timeoutMs: 1000,
    redactionProfile: "primary",
    idempotencyKey: "query-preview-001"
  } as const;
}

function sizedHostCommandRequest(targetBytes: number) {
  const base = validHostCommandRequest();
  for (let entryCount = 0; entryCount <= 20; entryCount++) {
    for (let valueLength = 0; valueLength <= 64; valueLength++) {
      const params = Object.fromEntries(
        Array.from({ length: entryCount }, (_value, index) => [
          `p${String(index).padStart(2, "0")}`,
          "x".repeat(valueLength)
        ])
      );
      const request = {
        ...base,
        params
      };
      if (encodedBytes(request) === targetBytes) {
        return request;
      }
    }
  }
  throw new Error(`Unable to create request with ${targetBytes} encoded bytes`);
}

function sizedUnavailableResult(targetBytes: number) {
  const base = createUnavailableHostCommandResult({ requestId: "request-sized" }, "2026-06-03T00:00:00.000Z");
  for (let redactionLength = 1; redactionLength <= 96; redactionLength++) {
    for (let artifactCount = 0; artifactCount <= 8; artifactCount++) {
      for (let firstArtifactLength = 2; firstArtifactLength <= 64; firstArtifactLength++) {
        const artifactRefs = Array.from({ length: artifactCount }, (_value, index) =>
          index === 0 ? "a".repeat(firstArtifactLength) : `b${String(index).padStart(2, "0")}`
        );
        const result = withExactBoundsProof({
          ...base,
          artifactRefs,
          redactionSummary: "x".repeat(redactionLength),
          boundsProof: {
            ...base.boundsProof,
            actualBytes: 0
          }
        });
        if (encodedBytes(result) === targetBytes) {
          return result;
        }
      }
    }
  }
  throw new Error(`Unable to create result with ${targetBytes} encoded bytes`);
}

function withExactBoundsProof<T extends { boundsProof: { actualBytes: number } }>(result: T): T {
  let next = result;
  for (let index = 0; index < 8; index++) {
    const actualBytes = encodedBytes(next);
    if (next.boundsProof.actualBytes === actualBytes) {
      return next;
    }
    next = {
      ...next,
      boundsProof: {
        ...next.boundsProof,
        actualBytes
      }
    };
  }
  return next;
}

function encodedBytes(value: unknown): number {
  return new TextEncoder().encode(JSON.stringify(value)).length;
}
