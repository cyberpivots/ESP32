export const CBBS_CLIENT_SCHEMA = "cbbs_client_fixture.v1" as const;
export const MAX_UI_INTENT_BYTES = 512;
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

export type AppRole = (typeof APP_ROLES)[number];
export type ViewId = (typeof VIEW_IDS)[number];
export type IntentId = (typeof INTENT_IDS)[number];
export type ClosedSurfaceId = (typeof CLOSED_SURFACE_IDS)[number];
export type AllowedUiIntentKey = (typeof ALLOWED_UI_INTENT_KEYS)[number];

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

export function isAppRole(value: unknown): value is AppRole {
  return typeof value === "string" && APP_ROLES.includes(value as AppRole);
}

export function isViewId(value: unknown): value is ViewId {
  return typeof value === "string" && VIEW_IDS.includes(value as ViewId);
}

export function isIntentId(value: unknown): value is IntentId {
  return typeof value === "string" && INTENT_IDS.includes(value as IntentId);
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

export function findSecretFields(value: unknown): string[] {
  const paths: string[] = [];
  visit(value, [], (path, current) => {
    if (typeof current !== "string") {
      return;
    }
    if (SECRET_KEY_PATTERNS.some((pattern) => pattern.test(path[path.length - 1] ?? ""))) {
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
