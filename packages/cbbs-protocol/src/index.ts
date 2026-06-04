export const CBBS_CLIENT_SCHEMA = "cbbs_client_fixture.v1" as const;
export const HOST_COMMAND_BRIDGE_SCHEMA = "cbbs_host_command_bridge.v1" as const;
export const MAX_UI_INTENT_BYTES = 512;
export const MAX_HOST_COMMAND_BRIDGE_BYTES = 512;
export const LOCAL_ONLY_REASON = "fixture-only-ui-intent" as const;

export const APP_ROLES = ["client", "sysop", "monitor", "devconfig"] as const;
export const VIEW_IDS = [
  "home",
  "messages",
  "downloads",
  "peers",
  "network",
  "diagnostics",
  "safety",
  "config",
  "evidence"
] as const;
export const INTENT_IDS = [
  "navigate",
  "refresh",
  "filter",
  "select_row",
  "open_detail",
  "compose_draft",
  "queue_file_request",
  "ack_local",
  "view_proof"
] as const;

export const CLOSED_SURFACE_IDS = [
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
] as const;

export const ALLOWED_UI_INTENT_KEYS = [
  "schema",
  "intent",
  "role",
  "view",
  "targetView",
  "rowId",
  "proofId",
  "filter",
  "draftText",
  "localOnlyReason"
] as const;

export const HOST_COMMAND_APP_IDS = ["hardware-tools"] as const;
export const HOST_COMMAND_ACTION_IDS = [
  "mesh.statusSnapshot",
  "mesh.serviceList",
  "radio.inventorySummary",
  "radio.queryPreview",
  "radio.profileCompare",
  "radio.changePreview",
  "firmware.artifactReview",
  "firmware.installPreview",
  "device.readinessCheck"
] as const;
export const HOST_COMMAND_ACTION_CLASSES = ["read", "change", "install"] as const;
export const HOST_COMMAND_REDACTION_PROFILES = ["primary", "advanced"] as const;
export const DOSC_WIN31_REQUEST_NAMES = [
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
] as const;
export const DOSC_WIN31_REQUEST_NAMES_AUDIT_ONLY = true as const;
export const HOST_COMMAND_RESULT_STATUSES = [
  "unavailable",
  "rejected",
  "planned",
  "validated",
  "running",
  "complete",
  "failed",
  "cancelled"
] as const;
export const HOST_COMMAND_UNAVAILABLE_REASON = "adapter_unavailable" as const;
export const ALLOWED_HOST_COMMAND_REQUEST_KEYS = [
  "schema",
  "requestId",
  "appId",
  "actorRole",
  "actionId",
  "actionClass",
  "targetRef",
  "params",
  "dryRun",
  "gateRef",
  "timeoutMs",
  "redactionProfile",
  "idempotencyKey"
] as const;
export const ALLOWED_HOST_COMMAND_RESULT_KEYS = [
  "schema",
  "requestId",
  "accepted",
  "executed",
  "available",
  "status",
  "reason",
  "startedAt",
  "endedAt",
  "exitCode",
  "transcriptRef",
  "artifactRefs",
  "redactionSummary",
  "noSecretScan",
  "boundsProof",
  "recoveryRef"
] as const;

const SECRET_KEY_PATTERNS = [
  /secret/i,
  /token/i,
  /\bpmk\b/i,
  /\blmk\b/i,
  /credential/i,
  /password/i,
  /signing/i,
  /private[_-]?key/i,
  /device[_-]?id/i,
  /android[_-]?id/i,
  /mac/i,
  /com[_-]?port/i,
  /pnp/i,
  /location/i,
  /message[_-]?body/i,
  /file[_-]?content/i
] as const;
const NON_SECRET_PROOF_KEYS = new Set(["noSecretScan"]);

const FORBIDDEN_METADATA_KEY_PATTERNS = [
  /^url$/i,
  /^uri$/i,
  /^href$/i,
  /endpoint/i,
  /path/i,
  /^file$/i,
  /file[_-]?name/i,
  /file[_-]?path/i,
  /^content$/i,
  /\bbody\b/i,
  /payload/i,
  /host/i,
  /port/i,
  /address/i,
  /transport/i,
  /network/i,
  /socket/i,
  /capability/i,
  /permission/i
] as const;

const FORBIDDEN_INTENT_PATTERNS = [
  /serial/i,
  /\brf\b/i,
  /xbee/i,
  /ble/i,
  /bluetooth/i,
  /web[_-]?serial/i,
  /web[_-]?bluetooth/i,
  /softap/i,
  /local[_-]?network/i,
  /flash/i,
  /erase/i,
  /monitor/i,
  /relay/i,
  /\bmains\b/i,
  /\bload\b/i,
  /router/i,
  /config[_-]?write/i,
  /\beas\b/i,
  /app[_-]?center/i,
  /deploy/i,
  /\brelease\b/i
] as const;

const FORBIDDEN_HOST_COMMAND_KEY_PATTERNS = [
  /^command$/i,
  /command[_-]?preview/i,
  /^argv$/i,
  /^args$/i,
  /shell/i,
  /^script$/i,
  /^script[_-]/i,
  /^host$/i,
  /^port$/i,
  /com[_-]?port/i,
  /^url$/i,
  /^uri$/i,
  /^href$/i,
  /^path$/i,
  /file[_-]?path/i,
  /serial/i,
  /xbee/i,
  /\brf\b/i,
  /flash/i,
  /erase/i,
  /monitor/i,
  /relay/i,
  /deploy/i,
  /release/i
] as const;

const FORBIDDEN_HOST_COMMAND_VALUE_PATTERNS = [
  /\bCOM\d+\b/i,
  /child_process/i,
  /\bexec\b/i,
  /\bspawn\b/i,
  /powershell/i,
  /serial(?:[-_\s]?|P)ort/i,
  /navigator\.serial/i,
  /esptool/i,
  /idf\.py/i,
  /react-native\s+run-windows/i,
  /\bXCTU\b/i,
  /xbee/i,
  /\brf\b/i,
  /serial/i,
  /flash/i,
  /erase/i,
  /monitor/i,
  /relay/i,
  /\bmains\b/i,
  /\bload\b/i,
  /deploy/i,
  /release/i
] as const;

export type AppRole = (typeof APP_ROLES)[number];
export type ViewId = (typeof VIEW_IDS)[number];
export type IntentId = (typeof INTENT_IDS)[number];
export type ClosedSurfaceId = (typeof CLOSED_SURFACE_IDS)[number];
export type AllowedUiIntentKey = (typeof ALLOWED_UI_INTENT_KEYS)[number];
export type HostCommandAppId = (typeof HOST_COMMAND_APP_IDS)[number];
export type HostCommandActionId = (typeof HOST_COMMAND_ACTION_IDS)[number];
export type HostCommandActionClass = (typeof HOST_COMMAND_ACTION_CLASSES)[number];
export type HostCommandRedactionProfile = (typeof HOST_COMMAND_REDACTION_PROFILES)[number];
export type DoscWin31RequestName = (typeof DOSC_WIN31_REQUEST_NAMES)[number];
export type HostCommandResultStatus = (typeof HOST_COMMAND_RESULT_STATUSES)[number];
export type AllowedHostCommandRequestKey = (typeof ALLOWED_HOST_COMMAND_REQUEST_KEYS)[number];
export type AllowedHostCommandResultKey = (typeof ALLOWED_HOST_COMMAND_RESULT_KEYS)[number];

export interface UiIntentRecord {
  schema: typeof CBBS_CLIENT_SCHEMA;
  intent: IntentId;
  role: AppRole;
  view: ViewId;
  targetView?: ViewId;
  rowId?: string;
  proofId?: string;
  filter?: string;
  draftText?: string;
  localOnlyReason: typeof LOCAL_ONLY_REASON;
}

export interface ValidationResult {
  ok: boolean;
  errors: string[];
}

export type HostCommandParamValue = string | number | boolean;

export interface HostCommandBridgeRequest {
  schema: typeof HOST_COMMAND_BRIDGE_SCHEMA;
  requestId: string;
  appId: HostCommandAppId;
  actorRole: Extract<AppRole, "sysop">;
  actionId: HostCommandActionId;
  actionClass: HostCommandActionClass;
  targetRef: string;
  params?: Record<string, HostCommandParamValue>;
  dryRun: true;
  gateRef?: string;
  timeoutMs: number;
  redactionProfile: HostCommandRedactionProfile;
  idempotencyKey: string;
}

export interface HostCommandBoundsProof {
  maxBytes: typeof MAX_HOST_COMMAND_BRIDGE_BYTES;
  actualBytes: number;
}

export interface HostCommandBridgeResult {
  schema: typeof HOST_COMMAND_BRIDGE_SCHEMA;
  requestId: string;
  accepted: boolean;
  executed: boolean;
  available: boolean;
  status: HostCommandResultStatus;
  reason: string;
  startedAt: string;
  endedAt: string;
  exitCode?: number;
  transcriptRef: string;
  artifactRefs: string[];
  redactionSummary: string;
  noSecretScan: boolean;
  boundsProof: HostCommandBoundsProof;
  recoveryRef?: string;
}

export function isAppRole(value: unknown): value is AppRole {
  return typeof value === "string" && APP_ROLES.includes(value as AppRole);
}

export function isViewId(value: unknown): value is ViewId {
  return typeof value === "string" && VIEW_IDS.includes(value as ViewId);
}

export function isIntentId(value: unknown): value is IntentId {
  return typeof value === "string" && INTENT_IDS.includes(value as IntentId);
}

export function isHostCommandAppId(value: unknown): value is HostCommandAppId {
  return typeof value === "string" && HOST_COMMAND_APP_IDS.includes(value as HostCommandAppId);
}

export function isHostCommandActionId(value: unknown): value is HostCommandActionId {
  return typeof value === "string" && HOST_COMMAND_ACTION_IDS.includes(value as HostCommandActionId);
}

export function isHostCommandActionClass(value: unknown): value is HostCommandActionClass {
  return typeof value === "string" && HOST_COMMAND_ACTION_CLASSES.includes(value as HostCommandActionClass);
}

export function isHostCommandRedactionProfile(value: unknown): value is HostCommandRedactionProfile {
  return (
    typeof value === "string" &&
    HOST_COMMAND_REDACTION_PROFILES.includes(value as HostCommandRedactionProfile)
  );
}

export function isDoscWin31RequestName(value: unknown): value is DoscWin31RequestName {
  return typeof value === "string" && DOSC_WIN31_REQUEST_NAMES.includes(value as DoscWin31RequestName);
}

export function isHostCommandResultStatus(value: unknown): value is HostCommandResultStatus {
  return typeof value === "string" && HOST_COMMAND_RESULT_STATUSES.includes(value as HostCommandResultStatus);
}

export function validateUiIntent(value: unknown): ValidationResult {
  const errors: string[] = [];

  if (!isRecord(value)) {
    return { ok: false, errors: ["intent must be an object"] };
  }

  if (value.schema !== CBBS_CLIENT_SCHEMA) {
    errors.push("schema must be cbbs_client_fixture.v1");
  }
  errors.push(...findUnknownIntentKeys(value));
  if (!isIntentId(value.intent)) {
    errors.push("intent is not in the whitelist");
  }
  if (!isAppRole(value.role)) {
    errors.push("role is not in the whitelist");
  }
  if (!isViewId(value.view)) {
    errors.push("view is not in the whitelist");
  }
  if ("targetView" in value && !isViewId(value.targetView)) {
    errors.push("targetView is not in the whitelist");
  }
  if (value.localOnlyReason !== LOCAL_ONLY_REASON) {
    errors.push("localOnlyReason must be fixture-only-ui-intent");
  }
  errors.push(...findInvalidOptionalStringFields(value));

  const payloadBytes = new TextEncoder().encode(JSON.stringify(value)).length;
  if (payloadBytes > MAX_UI_INTENT_BYTES) {
    errors.push(`intent payload exceeds ${MAX_UI_INTENT_BYTES} bytes`);
  }

  errors.push(...findSecretFields(value));
  errors.push(...findForbiddenMetadataFields(value));
  errors.push(...findForbiddenLiveActionFields(value));

  return { ok: errors.length === 0, errors };
}

export function assertValidUiIntent(value: unknown): asserts value is UiIntentRecord {
  const result = validateUiIntent(value);
  if (!result.ok) {
    throw new Error(result.errors.join("; "));
  }
}

export function validateHostCommandBridgeRequest(value: unknown): ValidationResult {
  const errors: string[] = [];

  if (!isRecord(value)) {
    return { ok: false, errors: ["host command request must be an object"] };
  }

  if (value.schema !== HOST_COMMAND_BRIDGE_SCHEMA) {
    errors.push("schema must be cbbs_host_command_bridge.v1");
  }
  errors.push(...findUnknownHostCommandKeys(value, ALLOWED_HOST_COMMAND_REQUEST_KEYS, "request"));
  if (!isAlias(value.requestId)) {
    errors.push("requestId must be a bounded alias");
  }
  if (!isHostCommandAppId(value.appId)) {
    errors.push("appId is not in the host command allowlist");
  }
  if (value.actorRole !== "sysop") {
    errors.push("actorRole must be sysop");
  }
  if (!isHostCommandActionId(value.actionId)) {
    errors.push("actionId is not in the host command allowlist");
  }
  if (!isHostCommandActionClass(value.actionClass)) {
    errors.push("actionClass is not in the host command allowlist");
  }
  if (!isAlias(value.targetRef)) {
    errors.push("targetRef must be a bounded alias");
  }
  if (value.dryRun !== true) {
    errors.push("dryRun must be true for the non-executing bridge contract");
  }
  if ("gateRef" in value && !isAlias(value.gateRef)) {
    errors.push("gateRef must be a bounded alias when present");
  }
  if (!isIntegerInRange(value.timeoutMs, 250, 120000)) {
    errors.push("timeoutMs must be between 250 and 120000");
  }
  if (!isHostCommandRedactionProfile(value.redactionProfile)) {
    errors.push("redactionProfile is not in the allowlist");
  }
  if (!isAlias(value.idempotencyKey)) {
    errors.push("idempotencyKey must be a bounded alias");
  }
  errors.push(...validateHostCommandParams(value.params));
  errors.push(...findSecretFields(value));
  errors.push(...findForbiddenHostCommandFields(value));

  const payloadBytes = encodedBytes(value);
  if (payloadBytes > MAX_HOST_COMMAND_BRIDGE_BYTES) {
    errors.push(`host command request exceeds ${MAX_HOST_COMMAND_BRIDGE_BYTES} bytes`);
  }

  return { ok: errors.length === 0, errors };
}

export function validateHostCommandBridgeResult(value: unknown): ValidationResult {
  const errors: string[] = [];

  if (!isRecord(value)) {
    return { ok: false, errors: ["host command result must be an object"] };
  }

  if (value.schema !== HOST_COMMAND_BRIDGE_SCHEMA) {
    errors.push("schema must be cbbs_host_command_bridge.v1");
  }
  errors.push(...findUnknownHostCommandKeys(value, ALLOWED_HOST_COMMAND_RESULT_KEYS, "result"));
  if (!isAlias(value.requestId)) {
    errors.push("requestId must be a bounded alias");
  }
  for (const field of ["accepted", "executed", "available", "noSecretScan"] as const) {
    if (typeof value[field] !== "boolean") {
      errors.push(`${field} must be boolean`);
    }
  }
  if (!isHostCommandResultStatus(value.status)) {
    errors.push("status is not in the result status allowlist");
  }
  if (value.accepted !== false) {
    errors.push("accepted must remain false while the bridge is unavailable");
  }
  if (value.executed !== false) {
    errors.push("executed must remain false while the bridge is unavailable");
  }
  if (value.available !== false) {
    errors.push("available must remain false while the bridge is unavailable");
  }
  if (value.status !== "unavailable") {
    errors.push("status must remain unavailable while the bridge is unavailable");
  }
  if (value.reason !== HOST_COMMAND_UNAVAILABLE_REASON) {
    errors.push("reason must remain adapter_unavailable while the bridge is unavailable");
  }
  for (const field of ["reason", "startedAt", "endedAt", "transcriptRef", "redactionSummary"] as const) {
    if (typeof value[field] !== "string" || value[field].length < 1 || value[field].length > 96) {
      errors.push(`${field} must be a bounded string`);
    }
  }
  if ("exitCode" in value && !isIntegerInRange(value.exitCode, -1, 255)) {
    errors.push("exitCode must be between -1 and 255 when present");
  }
  if (!Array.isArray(value.artifactRefs) || value.artifactRefs.some((entry) => !isAlias(entry))) {
    errors.push("artifactRefs must be bounded aliases");
  }
  const payloadBytes = encodedBytes(value);
  if (!isRecord(value.boundsProof)) {
    errors.push("boundsProof must be an object");
  } else {
    if (value.boundsProof.maxBytes !== MAX_HOST_COMMAND_BRIDGE_BYTES) {
      errors.push("boundsProof.maxBytes must match bridge byte limit");
    }
    if (!isIntegerInRange(value.boundsProof.actualBytes, 1, MAX_HOST_COMMAND_BRIDGE_BYTES)) {
      errors.push("boundsProof.actualBytes must be within byte limit");
    } else if (value.boundsProof.actualBytes !== payloadBytes) {
      errors.push("boundsProof.actualBytes must match encoded result bytes");
    }
  }
  if ("recoveryRef" in value && !isAlias(value.recoveryRef)) {
    errors.push("recoveryRef must be a bounded alias when present");
  }
  errors.push(...findSecretFields(value));
  errors.push(...findForbiddenHostCommandFields(value));

  if (payloadBytes > MAX_HOST_COMMAND_BRIDGE_BYTES) {
    errors.push(`host command result exceeds ${MAX_HOST_COMMAND_BRIDGE_BYTES} bytes`);
  }

  return { ok: errors.length === 0, errors };
}

export function createUnavailableHostCommandResult(
  request: Pick<HostCommandBridgeRequest, "requestId">,
  now = "1970-01-01T00:00:00.000Z"
): HostCommandBridgeResult {
  const base = {
    schema: HOST_COMMAND_BRIDGE_SCHEMA,
    requestId: request.requestId,
    accepted: false,
    executed: false,
    available: false,
    status: "unavailable",
    reason: HOST_COMMAND_UNAVAILABLE_REASON,
    startedAt: now,
    endedAt: now,
    transcriptRef: "activity-log",
    artifactRefs: [],
    redactionSummary: "identifiers-hidden",
    noSecretScan: true,
    boundsProof: {
      maxBytes: MAX_HOST_COMMAND_BRIDGE_BYTES,
      actualBytes: 0
    }
  } satisfies HostCommandBridgeResult;

  return withExactBoundsProof(base);
}

export function findSecretFields(value: unknown): string[] {
  const paths: string[] = [];
  visit(value, [], (path) => {
    const key = path[path.length - 1] ?? "";
    if (
      path.length > 0 &&
      !NON_SECRET_PROOF_KEYS.has(key) &&
      SECRET_KEY_PATTERNS.some((pattern) => pattern.test(key))
    ) {
      paths.push(`secret-like field ${path.join(".")}`);
    }
  });
  return paths;
}

export function findUnknownIntentKeys(value: Record<string, unknown>): string[] {
  const allowed = new Set<string>(ALLOWED_UI_INTENT_KEYS);
  return Object.keys(value)
    .filter((key) => !allowed.has(key))
    .map((key) => `unknown intent key ${key}`);
}

export function findInvalidOptionalStringFields(value: Record<string, unknown>): string[] {
  const stringFields = ["rowId", "proofId", "filter", "draftText", "localOnlyReason"] as const;
  const errors: string[] = [];
  for (const field of stringFields) {
    if (field in value && typeof value[field] !== "string") {
      errors.push(`${field} must be a string`);
    }
  }
  return errors;
}

export function findForbiddenMetadataFields(value: unknown): string[] {
  const paths: string[] = [];
  visit(value, [], (path) => {
    const key = path[path.length - 1] ?? "";
    if (FORBIDDEN_METADATA_KEY_PATTERNS.some((pattern) => pattern.test(key))) {
      paths.push(`forbidden metadata field ${path.join(".")}`);
    }
  });
  return paths;
}

export function findForbiddenLiveActionFields(value: unknown): string[] {
  const paths: string[] = [];
  visit(value, [], (path, current) => {
    const key = path[path.length - 1] ?? "";
    if (typeof current === "string" && FORBIDDEN_INTENT_PATTERNS.some((pattern) => pattern.test(current))) {
      paths.push(`forbidden live-action value ${path.join(".")}`);
    }
    if (FORBIDDEN_INTENT_PATTERNS.some((pattern) => pattern.test(key))) {
      paths.push(`forbidden live-action field ${path.join(".")}`);
    }
  });
  return paths;
}

export function findForbiddenHostCommandFields(value: unknown): string[] {
  const paths: string[] = [];
  visit(value, [], (path, current) => {
    const key = path[path.length - 1] ?? "";
    if (FORBIDDEN_HOST_COMMAND_KEY_PATTERNS.some((pattern) => pattern.test(key))) {
      paths.push(`forbidden host-command field ${path.join(".")}`);
    }
    if (
      typeof current === "string" &&
      FORBIDDEN_HOST_COMMAND_VALUE_PATTERNS.some((pattern) => pattern.test(current))
    ) {
      paths.push(`forbidden host-command value ${path.join(".")}`);
    }
  });
  return paths;
}

export function localIntent(
  intent: IntentId,
  role: AppRole,
  view: ViewId,
  extra: Omit<Partial<UiIntentRecord>, "schema" | "intent" | "role" | "view" | "localOnlyReason"> = {}
): UiIntentRecord {
  return {
    schema: CBBS_CLIENT_SCHEMA,
    intent,
    role,
    view,
    ...extra,
    localOnlyReason: LOCAL_ONLY_REASON
  };
}

function findUnknownHostCommandKeys(
  value: Record<string, unknown>,
  allowedKeys: readonly string[],
  label: string
): string[] {
  const allowed = new Set<string>(allowedKeys);
  return Object.keys(value)
    .filter((key) => !allowed.has(key))
    .map((key) => `unknown host command ${label} key ${key}`);
}

function validateHostCommandParams(value: unknown): string[] {
  if (value === undefined) {
    return [];
  }
  if (!isRecord(value)) {
    return ["params must be an object when present"];
  }
  const errors: string[] = [];
  for (const [key, entry] of Object.entries(value)) {
    if (!isAlias(key)) {
      errors.push(`params key ${key} must be a bounded alias`);
    }
    if (!["string", "number", "boolean"].includes(typeof entry)) {
      errors.push(`params.${key} must be a string, number, or boolean`);
    }
    if (typeof entry === "string" && entry.length > 64) {
      errors.push(`params.${key} must be 64 characters or less`);
    }
  }
  return errors;
}

function isAlias(value: unknown): value is string {
  return typeof value === "string" && /^[a-z][a-z0-9-]{1,63}$/i.test(value);
}

function isIntegerInRange(value: unknown, min: number, max: number): value is number {
  return typeof value === "number" && Number.isInteger(value) && value >= min && value <= max;
}

function encodedBytes(value: unknown): number {
  return new TextEncoder().encode(JSON.stringify(value)).length;
}

function withExactBoundsProof(result: HostCommandBridgeResult): HostCommandBridgeResult {
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

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function visit(
  value: unknown,
  path: string[],
  callback: (path: string[], value: unknown) => void
): void {
  callback(path, value);
  if (Array.isArray(value)) {
    value.forEach((entry, index) => visit(entry, [...path, String(index)], callback));
    return;
  }
  if (!isRecord(value)) {
    return;
  }
  for (const [key, entry] of Object.entries(value)) {
    visit(entry, [...path, key], callback);
  }
}
