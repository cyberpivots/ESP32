#include "four_relay_core.h"
#include "test_support.h"

#include <string.h>

static void test_storage_gates(void)
{
    fr_storage_status_t storage;
    fr_storage_status_default(&storage);

    check(fr_storage_require_logs(0) == FR_REJECT_PAYLOAD_INVALID,
          "null storage status rejects invalid payload");
    check(fr_storage_require_logs(&storage) == FR_REJECT_STORAGE_UNAVAILABLE,
          "storage log gate rejects default unavailable storage");

    storage.hardware_gate_closed = true;
    storage.mounted = true;
    storage.writable = true;
    storage.logs_available = false;
    check(fr_storage_require_logs(&storage) == FR_REJECT_LOG_APPEND_FAILED,
          "storage log gate rejects append failure path");

    storage.logs_available = true;
    check(fr_storage_require_logs(&storage) == FR_OK,
          "storage log gate accepts writable log path");
}

static void test_storage_api_responses(void)
{
    fr_assets_manifest_t manifest;
    fr_logs_recent_response_t logs;

    fr_api_assets_manifest_default(&manifest);
    check(strcmp(manifest.name, "four-relay-admin-hmi") == 0,
          "GET /api/assets/manifest response exposes manifest name");
    check(strcmp(manifest.version, "2026-05-18-admin-hmi") == 0,
          "GET /api/assets/manifest response exposes version");
    check(manifest.file_count == FR_API_ASSET_FILE_COUNT,
          "GET /api/assets/manifest response exposes file list");
    check(strcmp(manifest.files[0], "index.html") == 0,
          "GET /api/assets/manifest response includes index file");

    fr_api_logs_recent_empty(50u, "all", &logs);
    check(logs.limit == 50u, "GET /api/logs/recent response preserves limit");
    check(strcmp(logs.type, "all") == 0,
          "GET /api/logs/recent response preserves type");
    check(logs.item_count == 0u, "GET /api/logs/recent response defaults empty");
    check(!logs.truncated, "GET /api/logs/recent response defaults untruncated");

    fr_api_logs_recent_empty(10u, 0, &logs);
    check(strcmp(logs.type, "all") == 0,
          "GET /api/logs/recent null type defaults to all");
}

int main(void)
{
    test_storage_gates();
    test_storage_api_responses();
    return finish_tests("test_storage_contracts");
}
