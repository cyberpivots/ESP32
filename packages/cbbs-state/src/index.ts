import {
  assertValidUiIntent,
  type AppRole,
  type UiIntentRecord,
  type ViewId
} from "@cbbs/protocol";

export interface CbbsClientState {
  role: AppRole;
  activeView: ViewId;
  filter: string;
  selectedRowId?: string;
  detailId?: string;
  localDraftText: string;
  queuedLocalRequests: string[];
  localAckCount: number;
  viewedProofId?: string;
  lastIntent?: UiIntentRecord["intent"];
  lastValidation: "ok" | "rejected";
  rejectionReason?: string;
}

export function createInitialState(role: AppRole, activeView: ViewId): CbbsClientState {
  return {
    role,
    activeView,
    filter: "",
    localDraftText: "",
    queuedLocalRequests: [],
    localAckCount: 0,
    lastValidation: "ok"
  };
}

export function cbbsReducer(state: CbbsClientState, intent: UiIntentRecord): CbbsClientState {
  try {
    assertValidUiIntent(intent);
  } catch (error) {
    return {
      ...state,
      lastValidation: "rejected",
      rejectionReason: error instanceof Error ? error.message : "invalid intent"
    };
  }

  switch (intent.intent) {
    case "navigate":
      return {
        ...state,
        activeView: intent.targetView ?? intent.view,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "refresh":
      return {
        ...state,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "filter":
      return {
        ...state,
        filter: intent.filter ?? "",
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "select_row":
      return {
        ...state,
        selectedRowId: intent.rowId,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "open_detail":
      return {
        ...state,
        detailId: intent.rowId,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "compose_draft":
      return {
        ...state,
        localDraftText: intent.draftText ?? "",
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "queue_file_request":
      return {
        ...state,
        queuedLocalRequests: intent.rowId
          ? [...state.queuedLocalRequests, intent.rowId]
          : state.queuedLocalRequests,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "ack_local":
      return {
        ...state,
        localAckCount: state.localAckCount + 1,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    case "view_proof":
      return {
        ...state,
        viewedProofId: intent.proofId,
        lastIntent: intent.intent,
        lastValidation: "ok"
      };
    default:
      return state;
  }
}
