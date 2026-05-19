#include "four_relay_core.h"
#include "test_support.h"

#include <string.h>

static void test_http_routes(void)
{
    fr_http_route_t route = fr_http_classify_route("GET", "/api/state");
    check(route.endpoint == FR_HTTP_ENDPOINT_STATE, "GET /api/state route classified");
    check(!route.state_changing, "GET /api/state route is read-only");

    route = fr_http_classify_route("POST", "/api/relay/1");
    check(route.endpoint == FR_HTTP_ENDPOINT_RELAY, "public relay channel one route accepts");
    check(route.relay_channel == 1, "relay route captures public channel one");

    route = fr_http_classify_route("POST", "/api/relay/4");
    check(route.endpoint == FR_HTTP_ENDPOINT_RELAY, "public relay channel four route accepts");
    check(route.relay_channel == 4, "relay route captures public channel four");

    route = fr_http_classify_route("POST", "/api/all-off");
    check(route.endpoint == FR_HTTP_ENDPOINT_ALL_OFF, "POST /api/all-off route classified");
    check(route.state_changing, "POST /api/all-off route is state changing");

    route = fr_http_classify_route("GET", "/api/storage/status");
    check(route.endpoint == FR_HTTP_ENDPOINT_STORAGE_STATUS, "GET /api/storage/status route classified");

    route = fr_http_classify_route("GET", "/api/assets/manifest");
    check(route.endpoint == FR_HTTP_ENDPOINT_ASSETS_MANIFEST, "GET /api/assets/manifest route classified");

    route = fr_http_classify_route("GET", "/api/logs/recent");
    check(route.endpoint == FR_HTTP_ENDPOINT_LOGS_RECENT, "GET /api/logs/recent route classified");

    route = fr_http_classify_route("POST", "/api/relay/0");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "public relay channel zero route rejects");

    route = fr_http_classify_route("POST", "/api/relay/5");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "public relay channel five route rejects");

    route = fr_http_classify_route("GET", "/api/relay/1");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "relay route requires POST");
}

static void test_command_payloads(void)
{
    fr_relay_command_payload_t relay_payload;
    relay_payload.has_state = true;
    relay_payload.state = true;
    relay_payload.has_sequence = true;
    relay_payload.sequence = 1;
    check(fr_api_validate_relay_payload(&relay_payload) == FR_OK,
          "POST /api/relay/{1..4} payload contract accepts state and sequence");

    relay_payload.has_state = false;
    check(fr_api_validate_relay_payload(&relay_payload) == FR_REJECT_PAYLOAD_INVALID,
          "POST /api/relay/{1..4} payload contract rejects missing state");
    relay_payload.has_state = true;
    relay_payload.sequence = 0;
    check(fr_api_validate_relay_payload(&relay_payload) == FR_REJECT_SEQUENCE_REPLAY,
          "POST /api/relay/{1..4} payload contract rejects zero sequence");

    fr_sequence_payload_t all_off_payload;
    all_off_payload.has_sequence = true;
    all_off_payload.sequence = 2;
    check(fr_api_validate_all_off_payload(&all_off_payload) == FR_OK,
          "POST /api/all-off payload contract accepts sequence");

    fr_safety_lock_payload_t lock_payload;
    lock_payload.has_locked = true;
    lock_payload.locked = true;
    lock_payload.has_sequence = true;
    lock_payload.sequence = 3;
    check(fr_api_validate_safety_lock_payload(&lock_payload) == FR_OK,
          "POST /api/safety-lock payload contract accepts locked and sequence");
}

static void test_state_snapshot_response(void)
{
    fr_relay_state_t state;
    fr_storage_status_t storage;
    fr_state_snapshot_t snapshot;

    fr_relay_state_init(&state);
    fr_storage_status_default(&storage);
    state.hardware_gate_closed = true;
    state.safety_lock_open = true;
    state.relay_config_valid = true;
    state.desired_on[3] = true;
    storage.mounted = true;
    storage.hardware_gate_closed = true;
    storage.assets_available = true;

    fr_api_build_state_snapshot(&state, &storage, &snapshot);
    check(!snapshot.safety_locked, "GET /api/state response reflects open safety lock");
    check(snapshot.hardware_gate_closed, "GET /api/state response reflects hardware gate");
    check(snapshot.relays[3].channel == 4u, "GET /api/state response uses public channel numbers");
    check(snapshot.relays[3].state, "GET /api/state response includes relay state");
    check(snapshot.relays[3].enabled, "GET /api/state response includes relay enabled state");
    check(snapshot.storage.mounted, "GET /api/state response snapshot includes storage");
    check(strcmp(snapshot.last_result, "safe_default") == 0,
          "GET /api/state response includes last command result");

    fr_api_build_state_snapshot(0, 0, &snapshot);
    check(snapshot.safety_locked, "GET /api/state null state falls back to locked");
    check(!snapshot.storage.mounted, "GET /api/state null storage falls back to unavailable");
}

int main(void)
{
    test_http_routes();
    test_command_payloads();
    test_state_snapshot_response();
    return finish_tests("test_http_api_contracts");
}
