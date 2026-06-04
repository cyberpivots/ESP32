// Generated RNW product menu model; do not edit.

export const CBBS_RNW_MENU_SCHEMA = "cbbs_rnw_menu.v1" as const;
export const hardwareToolsMenu = {
  "schema": "cbbs_rnw_menu.v1",
  "appId": "hardware-tools",
  "menuId": "hardware-tools-main",
  "label": "CBBS Hardware Tools",
  "sourceXml": "cbbs_rnw_menu.v1.xml",
  "pages": [
    {
      "id": "bench",
      "label": "Bench",
      "targetPage": "bench",
      "capabilityGroup": "bench",
      "executionMode": "bridgePreviewUnavailable",
      "state": "needsDevice",
      "viewId": "diagnostics",
      "summary": "Target aliases and readiness notes stay visible before any equipment contact.",
      "evidenceRef": "bench-readiness",
      "sections": [
        {
          "id": "bench-targets",
          "label": "Targets",
          "pageId": "bench",
          "targetPage": "bench",
          "capabilityGroup": "bench",
          "executionMode": "bridgePreviewUnavailable",
          "state": "needsDevice",
          "summary": "Target aliases and readiness notes stay visible before any equipment contact.",
          "evidenceRef": "bench-readiness",
          "items": [
            {
              "id": "bench-target-readiness",
              "actionId": "hardware.benchTargetReview",
              "label": "Target Readiness",
              "pageId": "bench",
              "targetPage": "bench",
              "capabilityGroup": "bench",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "diagnostics",
              "intent": "view_proof",
              "summary": "Review target aliases, required evidence, and closed work gates.",
              "bridgeActionId": "device.readinessCheck",
              "evidenceRef": "bench-readiness"
            }
          ]
        }
      ]
    },
    {
      "id": "radio",
      "label": "Radio",
      "targetPage": "radio",
      "capabilityGroup": "radio",
      "executionMode": "artifactReview",
      "state": "ready",
      "viewId": "network",
      "summary": "Radio review uses hidden identifiers and saved profile classes.",
      "evidenceRef": "radio-study",
      "sections": [
        {
          "id": "radio-review",
          "label": "Planning",
          "pageId": "radio",
          "targetPage": "radio",
          "capabilityGroup": "radio",
          "executionMode": "artifactReview",
          "state": "ready",
          "summary": "Radio review uses hidden identifiers and saved profile classes.",
          "evidenceRef": "radio-study",
          "items": [
            {
              "id": "radio-inventory",
              "actionId": "hardware.radioInventory",
              "label": "Radio Inventory",
              "pageId": "radio",
              "targetPage": "radio",
              "capabilityGroup": "radio",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "diagnostics",
              "intent": "view_proof",
              "summary": "Review radio family, tool presence, and profile class records with identifiers hidden.",
              "bridgeActionId": "radio.inventorySummary",
              "evidenceRef": "radio-study"
            },
            {
              "id": "radio-read-status-plan",
              "actionId": "hardware.radioReadStatusPlan",
              "label": "Read Status Plan",
              "pageId": "radio",
              "targetPage": "radio",
              "capabilityGroup": "radio",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "network",
              "intent": "view_proof",
              "summary": "Review the status-read checklist without contacting equipment.",
              "bridgeActionId": "radio.queryPreview",
              "evidenceRef": "radio-study"
            },
            {
              "id": "radio-profile-compare",
              "actionId": "hardware.radioProfileCompare",
              "label": "Profile Compare",
              "pageId": "radio",
              "targetPage": "radio",
              "capabilityGroup": "radio",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "config",
              "intent": "view_proof",
              "summary": "Compare saved profile classes while private values stay hidden.",
              "bridgeActionId": "radio.profileCompare",
              "evidenceRef": "radio-study"
            },
            {
              "id": "radio-change-plan",
              "actionId": "hardware.radioChangePlan",
              "label": "Change Plan",
              "pageId": "radio",
              "targetPage": "radio",
              "capabilityGroup": "radio",
              "executionMode": "tier3Closed",
              "state": "needsSafetyCheck",
              "viewId": "safety",
              "intent": "view_proof",
              "summary": "Requires target review, recovery steps, and fresh authority.",
              "bridgeActionId": "radio.changePreview",
              "evidenceRef": "radio-study"
            }
          ]
        }
      ]
    },
    {
      "id": "mesh",
      "label": "Mesh",
      "targetPage": "mesh",
      "capabilityGroup": "mesh",
      "executionMode": "artifactReview",
      "state": "ready",
      "viewId": "peers",
      "summary": "Mesh summaries come from recorded service views.",
      "evidenceRef": "mesh-records",
      "sections": [
        {
          "id": "mesh-previews",
          "label": "Previews",
          "pageId": "mesh",
          "targetPage": "mesh",
          "capabilityGroup": "mesh",
          "executionMode": "artifactReview",
          "state": "ready",
          "summary": "Mesh summaries come from recorded service views.",
          "evidenceRef": "mesh-records",
          "items": [
            {
              "id": "mesh-summary",
              "actionId": "hardware.meshSummary",
              "label": "Mesh Summary",
              "pageId": "mesh",
              "targetPage": "mesh",
              "capabilityGroup": "mesh",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "network",
              "intent": "view_proof",
              "summary": "Review mesh health from recorded summaries.",
              "bridgeActionId": "mesh.statusSnapshot",
              "evidenceRef": "mesh-records"
            },
            {
              "id": "mesh-service-summary",
              "actionId": "hardware.meshServices",
              "label": "Service Summary",
              "pageId": "mesh",
              "targetPage": "mesh",
              "capabilityGroup": "mesh",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "peers",
              "intent": "view_proof",
              "summary": "Review station service availability from recorded summaries.",
              "bridgeActionId": "mesh.serviceList",
              "evidenceRef": "mesh-records"
            }
          ]
        }
      ]
    },
    {
      "id": "firmware",
      "label": "Firmware",
      "targetPage": "firmware",
      "capabilityGroup": "firmware",
      "executionMode": "artifactReview",
      "state": "ready",
      "viewId": "config",
      "summary": "Firmware records show image identity and update readiness.",
      "evidenceRef": "firmware-records",
      "sections": [
        {
          "id": "firmware-review",
          "label": "Review",
          "pageId": "firmware",
          "targetPage": "firmware",
          "capabilityGroup": "firmware",
          "executionMode": "artifactReview",
          "state": "ready",
          "summary": "Firmware records show image identity and update readiness.",
          "evidenceRef": "firmware-records",
          "items": [
            {
              "id": "firmware-build-review",
              "actionId": "hardware.firmwareBuildReview",
              "label": "Build Review",
              "pageId": "firmware",
              "targetPage": "firmware",
              "capabilityGroup": "firmware",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "config",
              "intent": "view_proof",
              "summary": "Review image identity, compatibility notes, and acceptance status.",
              "bridgeActionId": "firmware.artifactReview",
              "evidenceRef": "firmware-records"
            },
            {
              "id": "firmware-device-update-plan",
              "actionId": "hardware.deviceUpdatePlan",
              "label": "Device Update Plan",
              "pageId": "firmware",
              "targetPage": "firmware",
              "capabilityGroup": "firmware",
              "executionMode": "tier3Closed",
              "state": "needsConfirmation",
              "viewId": "safety",
              "intent": "view_proof",
              "summary": "Requires selected target, recovery steps, and fresh authority.",
              "bridgeActionId": "firmware.installPreview",
              "evidenceRef": "firmware-records"
            }
          ]
        }
      ]
    },
    {
      "id": "fabrication",
      "label": "Fabrication",
      "targetPage": "fabrication",
      "capabilityGroup": "fabrication",
      "executionMode": "artifactReview",
      "state": "ready",
      "viewId": "config",
      "summary": "Fixture assets stay provisional until measurement records are complete.",
      "evidenceRef": "fixture-plate",
      "sections": [
        {
          "id": "fabrication-assets",
          "label": "Assets",
          "pageId": "fabrication",
          "targetPage": "fabrication",
          "capabilityGroup": "fabrication",
          "executionMode": "artifactReview",
          "state": "ready",
          "summary": "Fixture assets stay provisional until measurement records are complete.",
          "evidenceRef": "fixture-plate",
          "items": [
            {
              "id": "fabrication-print-asset",
              "actionId": "hardware.fabricationPrintAsset",
              "label": "Print Asset",
              "pageId": "fabrication",
              "targetPage": "fabrication",
              "capabilityGroup": "fabrication",
              "executionMode": "artifactReview",
              "state": "ready",
              "viewId": "config",
              "intent": "view_proof",
              "summary": "Review provisional plate parameters, label zones, and measurement grid notes.",
              "evidenceRef": "fixture-plate"
            },
            {
              "id": "fabrication-enclosure-checklist",
              "actionId": "hardware.enclosureChecklist",
              "label": "Enclosure Checklist",
              "pageId": "fabrication",
              "targetPage": "fabrication",
              "capabilityGroup": "fabrication",
              "executionMode": "localOnly",
              "state": "ready",
              "viewId": "safety",
              "intent": "view_proof",
              "summary": "Review clearance, ventilation, material, and fit evidence gaps.",
              "evidenceRef": "fixture-plate"
            }
          ]
        }
      ]
    },
    {
      "id": "safety",
      "label": "Safety",
      "targetPage": "safety",
      "capabilityGroup": "safety",
      "executionMode": "localOnly",
      "state": "needsSafetyCheck",
      "viewId": "safety",
      "summary": "Safety gates separate ready reviews from closed work.",
      "evidenceRef": "safety-gates",
      "sections": [
        {
          "id": "safety-gates",
          "label": "Gates",
          "pageId": "safety",
          "targetPage": "safety",
          "capabilityGroup": "safety",
          "executionMode": "localOnly",
          "state": "needsSafetyCheck",
          "summary": "Safety gates separate ready reviews from closed work.",
          "evidenceRef": "safety-gates",
          "items": [
            {
              "id": "safety-gate-dashboard",
              "actionId": "hardware.safetyGates",
              "label": "Safety Gates",
              "pageId": "safety",
              "targetPage": "safety",
              "capabilityGroup": "safety",
              "executionMode": "localOnly",
              "state": "ready",
              "viewId": "safety",
              "intent": "view_proof",
              "summary": "Review target, recovery, isolation, and authority status.",
              "evidenceRef": "safety-gates"
            },
            {
              "id": "safety-recovery-checklist",
              "actionId": "hardware.recoveryChecklist",
              "label": "Recovery Checklist",
              "pageId": "safety",
              "targetPage": "safety",
              "capabilityGroup": "safety",
              "executionMode": "localOnly",
              "state": "ready",
              "viewId": "safety",
              "intent": "view_proof",
              "summary": "Review rollback notes, cleanup status, and unresolved gaps.",
              "evidenceRef": "safety-gates"
            }
          ]
        }
      ]
    },
    {
      "id": "activity",
      "label": "Activity",
      "targetPage": "activity",
      "capabilityGroup": "activity",
      "executionMode": "localOnly",
      "state": "complete",
      "viewId": "evidence",
      "summary": "Evidence packet and transcript rows show what was reviewed.",
      "evidenceRef": "activity-records",
      "sections": [
        {
          "id": "activity-evidence",
          "label": "Evidence",
          "pageId": "activity",
          "targetPage": "activity",
          "capabilityGroup": "activity",
          "executionMode": "localOnly",
          "state": "complete",
          "summary": "Evidence packet and transcript rows show what was reviewed.",
          "evidenceRef": "activity-records",
          "items": [
            {
              "id": "activity-evidence-packet",
              "actionId": "hardware.evidencePacket",
              "label": "Evidence Packet",
              "pageId": "activity",
              "targetPage": "activity",
              "capabilityGroup": "activity",
              "executionMode": "localOnly",
              "state": "ready",
              "viewId": "evidence",
              "intent": "view_proof",
              "summary": "Review the bounded evidence packet and current transcript rows.",
              "evidenceRef": "activity-records"
            }
          ]
        }
      ]
    }
  ]
} as const;
