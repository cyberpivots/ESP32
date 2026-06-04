// Generated RNW Win31 parity model; do not edit.

export const CBBS_RNW_WIN31_PARITY_SCHEMA = "cbbs_rnw_win31_parity.v1" as const;
export const win31ParityContract = {
  "schema": "cbbs_rnw_win31_parity.v1",
  "visiblePlatform": "OG Communication Retro3.1",
  "moduleName": "CBBS",
  "internalEvidenceRef": "OPCON.EXE",
  "sourceXml": "cbbs_rnw_win31_parity.v1.xml",
  "doscSourceRoot": "/mnt/h/dos-c",
  "sourceRefs": [
    {
      "ref_id": "branding",
      "path": "knowledge-base/og-communication-retro31-branding-2026-05-28.md",
      "markers": [
        "Versioned platform references use `OG Communication Retro3.1`.",
        "BBS module: CBBS",
        "OPCON.EXE"
      ]
    },
    {
      "ref_id": "operator-readme",
      "path": "software/win31-operator/README.md",
      "markers": [
        "Two-row view selector with plain primary tasks",
        "Devices, and Help.",
        "Peers, Link, Updates, Setup, Diagnostics, and Locks are",
        "Operator Protocol"
      ]
    },
    {
      "ref_id": "operator-menu",
      "path": "software/win31-operator/src/operator.rc",
      "markers": [
        "POPUP \"&Session\"",
        "POPUP \"&Views\"",
        "POPUP \"&Messages\"",
        "POPUP \"&Files\"",
        "POPUP \"&Devices\"",
        "POPUP \"&Style\"",
        "POPUP \"&Help\""
      ]
    },
    {
      "ref_id": "operator-source",
      "path": "software/win31-operator/src/operator.c",
      "markers": [
        "#define APP_TITLE \"OG Communication\"",
        "add_owner_button(hwnd, \"STATUS\"",
        "add_owner_button(hwnd, \"LOCKS\"",
        "Link wait",
        "Queue 0"
      ]
    },
    {
      "ref_id": "operator-protocol-h",
      "path": "software/win31-operator/include/operator_protocol.h",
      "markers": [
        "OPCON_REQ_HELLO",
        "OPCON_REQ_OTAP_INTENT"
      ]
    },
    {
      "ref_id": "operator-protocol-c",
      "path": "software/win31-operator/src/operator_protocol.c",
      "markers": [
        "{\\\"type\\\":\\\"maint_intent\\\",\\\"action\\\":",
        "{\\\"type\\\":\\\"otap_intent\\\",\\\"action\\\":"
      ]
    }
  ],
  "status": {
    "label": "Link wait",
    "counters": [
      "In 0",
      "Out 0 Err 0",
      "Queue 0"
    ]
  },
  "menus": [
    {
      "id": "session",
      "label": "Session"
    },
    {
      "id": "views",
      "label": "Views"
    },
    {
      "id": "messages",
      "label": "Messages"
    },
    {
      "id": "files",
      "label": "Files"
    },
    {
      "id": "devices",
      "label": "Devices"
    },
    {
      "id": "style",
      "label": "Style"
    },
    {
      "id": "help",
      "label": "Help"
    }
  ],
  "pages": [
    {
      "id": "status",
      "label": "Status",
      "viewId": "home",
      "summary": "Readiness, link wait, counters, and queue depth."
    },
    {
      "id": "messages",
      "label": "Messages",
      "viewId": "messages",
      "summary": "Message pull, post, search, and acknowledge views."
    },
    {
      "id": "files",
      "label": "Files",
      "viewId": "downloads",
      "summary": "Catalog, queue, and transfer-intent views."
    },
    {
      "id": "devices",
      "label": "Devices",
      "viewId": "diagnostics",
      "summary": "Status and intent views for gated device work."
    },
    {
      "id": "help",
      "label": "Help",
      "viewId": "evidence",
      "summary": "First-run help and operator orientation."
    },
    {
      "id": "peers",
      "label": "Peers",
      "viewId": "peers",
      "summary": "Known station summaries."
    },
    {
      "id": "link",
      "label": "Link",
      "viewId": "network",
      "summary": "Advanced link readiness and discovery summaries."
    },
    {
      "id": "updates",
      "label": "Updates",
      "viewId": "config",
      "summary": "Status, readiness, and update intent."
    },
    {
      "id": "setup",
      "label": "Setup",
      "viewId": "config",
      "summary": "Layout and style setup."
    },
    {
      "id": "diagnostics",
      "label": "Diagnostics",
      "viewId": "diagnostics",
      "summary": "Backend, sequence, and inventory summaries."
    },
    {
      "id": "locks",
      "label": "Locks",
      "viewId": "safety",
      "summary": "Closed gate and external authority explanations."
    }
  ],
  "actions": [
    {
      "id": "sysop.connect",
      "label": "Connect",
      "menuId": "session",
      "pageId": "status",
      "viewId": "home",
      "intent": "refresh",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Review link wait state and readiness counters.",
      "requestName": "hello"
    },
    {
      "id": "sysop.refreshStatus",
      "label": "Refresh Status",
      "menuId": "session",
      "pageId": "status",
      "viewId": "home",
      "intent": "refresh",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Update readiness, counters, queues, and summaries.",
      "requestName": "state_get"
    },
    {
      "id": "sysop.pullMessages",
      "label": "Pull Messages",
      "menuId": "messages",
      "pageId": "messages",
      "viewId": "messages",
      "intent": "open_detail",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Review queued message pull results.",
      "requestName": "msg_pull"
    },
    {
      "id": "sysop.postMessage",
      "label": "Post Message",
      "menuId": "messages",
      "pageId": "messages",
      "viewId": "messages",
      "intent": "compose_draft",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Stage a bounded message note.",
      "requestName": "msg_post"
    },
    {
      "id": "sysop.searchBoard",
      "label": "Search Board",
      "menuId": "messages",
      "pageId": "messages",
      "viewId": "messages",
      "intent": "filter",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Review bounded message search results.",
      "requestName": "msg_search"
    },
    {
      "id": "sysop.ackMessage",
      "label": "Acknowledge Message",
      "menuId": "messages",
      "pageId": "messages",
      "viewId": "messages",
      "intent": "ack_local",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Mark a message note as locally acknowledged.",
      "requestName": "msg_ack"
    },
    {
      "id": "sysop.refreshCatalog",
      "label": "Refresh Catalog",
      "menuId": "files",
      "pageId": "files",
      "viewId": "downloads",
      "intent": "refresh",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Review catalog and queue depth.",
      "requestName": "download_list"
    },
    {
      "id": "sysop.queueSelectedFile",
      "label": "Queue Selected File",
      "menuId": "files",
      "pageId": "files",
      "viewId": "downloads",
      "intent": "queue_file_request",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Stage a store-and-forward transfer intent.",
      "requestName": "download_queue"
    },
    {
      "id": "sysop.updateGateStatus",
      "label": "Update Gate Status",
      "menuId": "devices",
      "pageId": "updates",
      "viewId": "config",
      "intent": "view_proof",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Review update status, readiness, and rollback notes.",
      "requestName": "otap_status"
    },
    {
      "id": "sysop.recordUpdateIntent",
      "label": "Record Update Intent",
      "menuId": "devices",
      "pageId": "updates",
      "viewId": "config",
      "intent": "view_proof",
      "executionMode": "localOnly",
      "state": "ready",
      "summary": "Record review intent while external gates stay closed.",
      "requestName": "otap_intent"
    }
  ],
  "requestNames": [
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
  ],
  "roleCoverage": {
    "sysop": [
      {
        "pageId": "status",
        "disposition": "represented",
        "reason": "Win31 primary category."
      },
      {
        "pageId": "messages",
        "disposition": "represented",
        "reason": "Win31 primary category."
      },
      {
        "pageId": "files",
        "disposition": "represented",
        "reason": "Win31 primary category."
      },
      {
        "pageId": "devices",
        "disposition": "represented",
        "reason": "Win31 primary category."
      },
      {
        "pageId": "help",
        "disposition": "represented",
        "reason": "Win31 primary category."
      },
      {
        "pageId": "peers",
        "disposition": "represented",
        "reason": "Win31 secondary category."
      },
      {
        "pageId": "link",
        "disposition": "represented",
        "reason": "Win31 secondary category."
      },
      {
        "pageId": "updates",
        "disposition": "represented",
        "reason": "Win31 secondary category."
      },
      {
        "pageId": "setup",
        "disposition": "represented",
        "reason": "Win31 secondary category."
      },
      {
        "pageId": "diagnostics",
        "disposition": "represented",
        "reason": "Win31 secondary category."
      },
      {
        "pageId": "locks",
        "disposition": "represented",
        "reason": "Win31 secondary category."
      }
    ],
    "client": [
      {
        "pageId": "status",
        "disposition": "represented",
        "reason": "Client shows readiness and queue summaries."
      },
      {
        "pageId": "messages",
        "disposition": "represented",
        "reason": "Client keeps message drafting and reading."
      },
      {
        "pageId": "files",
        "disposition": "represented",
        "reason": "Client keeps file request staging."
      },
      {
        "pageId": "devices",
        "disposition": "notRenderedRoleBoundary",
        "reason": "Device intent views stay sysop-oriented in DOS-C source."
      },
      {
        "pageId": "help",
        "disposition": "represented",
        "reason": "Help remains user-facing."
      },
      {
        "pageId": "peers",
        "disposition": "represented",
        "reason": "Known station summaries remain useful to callers."
      },
      {
        "pageId": "link",
        "disposition": "evidenceOnly",
        "reason": "Advanced link details are not part of the primary user path."
      },
      {
        "pageId": "updates",
        "disposition": "notRenderedRoleBoundary",
        "reason": "Update intent stays sysop-oriented in DOS-C source."
      },
      {
        "pageId": "setup",
        "disposition": "evidenceOnly",
        "reason": "Layout and style setup is represented as evidence notes."
      },
      {
        "pageId": "diagnostics",
        "disposition": "notRenderedRoleBoundary",
        "reason": "Diagnostics retain operator backend detail."
      },
      {
        "pageId": "locks",
        "disposition": "evidenceOnly",
        "reason": "Closed gate explanations remain evidence-only for callers."
      }
    ]
  },
  "hardwareAdjacency": [
    {
      "pageId": "bench",
      "adjacentTo": "devices",
      "reason": "Target readiness supports device views."
    },
    {
      "pageId": "radio",
      "adjacentTo": "devices",
      "reason": "Radio planning supports device views."
    },
    {
      "pageId": "mesh",
      "adjacentTo": "link",
      "reason": "Mesh summaries support link views."
    },
    {
      "pageId": "firmware",
      "adjacentTo": "updates",
      "reason": "Firmware review supports update views."
    },
    {
      "pageId": "fabrication",
      "adjacentTo": "setup",
      "reason": "Fixture notes support setup views."
    },
    {
      "pageId": "safety",
      "adjacentTo": "locks",
      "reason": "Safety gates support lock views."
    },
    {
      "pageId": "activity",
      "adjacentTo": "diagnostics",
      "reason": "Evidence packets support diagnostic review."
    }
  ]
} as const;
