#include "four_relay_core.h"

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

static int failures = 0;

static void check(bool condition, const char *message)
{
    if (!condition) {
        fprintf(stderr, "FAIL: %s\n", message);
        ++failures;
    }
}

static fr_command_context_t valid_context(uint32_t sequence)
{
    fr_command_context_t context;
    context.admin_authenticated = true;
    context.source_allowed = true;
    context.xbee_link_verified = true;
    context.sequence = sequence;
    return context;
}

static void test_safe_defaults(void)
{
    fr_relay_state_t state;
    fr_config_snapshot_t config;
    fr_storage_status_t storage;

    fr_relay_state_init(&state);
    fr_config_store_default(&config);
    fr_storage_status_default(&storage);

    check(!state.hardware_gate_closed, "relay hardware gate defaults open");
    check(!state.safety_lock_open, "safety lock defaults closed");
    check(!state.relay_config_valid, "relay config defaults invalid");
    for (size_t index = 0; index < FR_RELAY_CHANNELS; ++index) {
        check(!state.desired_on[index], "relay desired state defaults off");
    }
    check(fr_config_validate_for_relay(&config) == FR_REJECT_RELAY_CONFIG_MISSING,
          "default config rejects relay use");
    check(fr_storage_require_logs(&storage) == FR_REJECT_STORAGE_UNAVAILABLE,
          "default storage rejects log writes");
}

static void test_relay_gates(void)
{
    fr_relay_state_t state;
    fr_relay_state_init(&state);

    fr_command_context_t context = valid_context(1);
    check(fr_relay_request_set(0, 0, true, &context) == FR_REJECT_PAYLOAD_INVALID,
          "null relay state rejects invalid payload");
    check(fr_relay_request_set(&state, 0, true, 0) == FR_REJECT_PAYLOAD_INVALID,
          "null relay context rejects invalid payload");

    state.safety_lock_open = true;
    state.relay_config_valid = true;

    check(fr_relay_request_set(&state, 0, true, &context) == FR_REJECT_HARDWARE_GATE_OPEN,
          "relay change rejects while hardware gate is open");
    check(strcmp(fr_status_name(FR_REJECT_HARDWARE_GATE_OPEN), "hardware_gate_open") == 0,
          "hardware_gate_open reject reason is stable");
    check(!state.desired_on[0], "rejected relay change does not alter desired state");

    state.hardware_gate_closed = true;
    state.safety_lock_open = false;
    check(fr_relay_request_set_public(&state, 1, true, &context) == FR_REJECT_SAFETY_LOCKED,
          "relay change rejects while safety lock is closed");
    state.safety_lock_open = true;
    state.relay_config_valid = false;
    check(fr_relay_request_set_public(&state, 1, true, &context) == FR_REJECT_RELAY_CONFIG_MISSING,
          "relay change rejects missing relay config");
    state.relay_config_valid = true;
    context.admin_authenticated = false;
    check(fr_relay_request_set_public(&state, 1, true, &context) == FR_REJECT_ADMIN_REQUIRED,
          "relay change rejects missing admin");
    context.admin_authenticated = true;
    context.source_allowed = false;
    check(fr_relay_request_set_public(&state, 1, true, &context) == FR_REJECT_SOURCE_NOT_ALLOWED,
          "relay change rejects blocked source");
    context.source_allowed = true;
    context.xbee_link_verified = false;
    check(fr_relay_request_set_public(&state, 1, true, &context) == FR_REJECT_XBEE_LINK_UNVERIFIED,
          "relay change rejects unverified XBee link");
    context.xbee_link_verified = true;

    check(fr_relay_request_set_public(&state, 1, true, &context) == FR_OK,
          "public relay channel 1 maps to internal index zero");
    check(state.desired_on[0], "accepted relay change updates desired state");
    context.sequence = 2;
    check(fr_relay_request_set_public(&state, 4, true, &context) == FR_OK,
          "public relay channel 4 maps to internal index three");
    check(state.desired_on[3], "accepted public channel four updates final internal state");
    check(fr_relay_request_set_public(&state, 0, true, &context) == FR_REJECT_RELAY_CHANNEL_INVALID,
          "public relay channel zero rejects");
    check(fr_relay_request_set_public(&state, 5, true, &context) == FR_REJECT_RELAY_CHANNEL_INVALID,
          "public relay channel five rejects");
    check(fr_relay_request_set(&state, 4, true, &context) == FR_REJECT_RELAY_CHANNEL_INVALID,
          "invalid internal relay index rejects");

    context.sequence = 2;
    check(fr_relay_request_set_public(&state, 2, true, &context) == FR_REJECT_SEQUENCE_REPLAY,
          "sequence replay rejects");

    state.hardware_gate_closed = false;
    check(fr_relay_all_off(&state, &context) == FR_OK, "authenticated all-off updates desired state");
    check(!state.desired_on[0], "all-off clears internal channel zero");
    check(!state.desired_on[3], "all-off clears internal channel three");

    context.admin_authenticated = false;
    state.desired_on[0] = true;
    check(fr_relay_all_off(&state, &context) == FR_REJECT_ADMIN_REQUIRED,
          "all-off rejects missing admin");
    check(state.desired_on[0], "rejected all-off preserves desired state");
}

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

static void test_http_contracts(void)
{
    fr_http_route_t route = fr_http_classify_route("GET", "/api/state");
    check(route.endpoint == FR_HTTP_ENDPOINT_STATE, "state route classified");
    check(!route.state_changing, "state route is read-only");

    route = fr_http_classify_route("POST", "/api/relay/2");
    check(route.endpoint == FR_HTTP_ENDPOINT_RELAY, "relay route classified");
    check(route.state_changing, "relay route is state changing");
    check(route.relay_channel == 2, "relay route captures public channel");

    route = fr_http_classify_route("POST", "/api/relay/1");
    check(route.endpoint == FR_HTTP_ENDPOINT_RELAY, "public relay channel one route accepts");
    check(route.relay_channel == 1, "relay route captures public channel one");

    route = fr_http_classify_route("POST", "/api/relay/4");
    check(route.endpoint == FR_HTTP_ENDPOINT_RELAY, "public relay channel four route accepts");
    check(route.relay_channel == 4, "relay route captures public channel four");

    route = fr_http_classify_route("GET", "/api/storage/status");
    check(route.endpoint == FR_HTTP_ENDPOINT_STORAGE_STATUS, "storage route classified");

    route = fr_http_classify_route("POST", "/api/relay/0");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "public relay channel zero route rejects");

    route = fr_http_classify_route("POST", "/api/relay/9");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "invalid relay route rejects");

    route = fr_http_classify_route("POST", "/api/relay/5");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "public relay channel five route rejects");

    route = fr_http_classify_route("GET", "/api/relay/1");
    check(route.endpoint == FR_HTTP_ENDPOINT_UNKNOWN, "relay route requires POST");
}

static void test_xbee_frames(void)
{
    const uint8_t frame_data[] = {
        0x90, 0x00, 0x13, 0xa2, 0x00, 0x41, 0x7e, 0x7d, 0x11, 0x13, 0x01
    };
    uint8_t wire[64];
    size_t wire_len = 0;
    fr_xbee_frame_t decoded;

    check(fr_xbee_encode_api2(frame_data, sizeof(frame_data), wire, sizeof(wire), &wire_len) == FR_OK,
          "XBee API2 encode succeeds in memory");
    check(wire_len > sizeof(frame_data), "XBee API2 encoder escapes reserved bytes");
    check(fr_xbee_decode_api2(wire, wire_len, &decoded) == FR_OK,
          "XBee API2 decode succeeds in memory");
    check(decoded.data_len == sizeof(frame_data), "XBee decoded length matches");
    check(memcmp(decoded.data, frame_data, sizeof(frame_data)) == 0,
          "XBee decoded frame matches input");

    wire[wire_len - 1u] ^= 0x01u;
    check(fr_xbee_decode_api2(wire, wire_len, &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee bad checksum rejects");

    const uint8_t status_frame[] = {0x8b, 0x01, 0xff, 0xfe, 0x00, 0x00, 0x00};
    check(fr_xbee_encode_api2(status_frame, sizeof(status_frame), wire, sizeof(wire), &wire_len) == FR_OK,
          "XBee transmit status frame encodes");
    check(fr_xbee_decode_api2(wire, wire_len, &decoded) == FR_OK,
          "XBee transmit status frame decodes");
    check(decoded.data_len == sizeof(status_frame), "XBee status frame decoded length matches");
    check(decoded.data[0] == 0x8b, "XBee status frame type preserved");

    const uint8_t bad_length[] = {0x7e, 0x00, 0x02, 0x90, 0x6f};
    check(fr_xbee_decode_api2(bad_length, sizeof(bad_length), &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee bad length rejects");

    const uint8_t truncated_escape[] = {0x7e, 0x00, 0x01, 0x7d};
    check(fr_xbee_decode_api2(truncated_escape, sizeof(truncated_escape), &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee truncated escape rejects");

    const uint8_t too_short[] = {0x7e, 0x00, 0x01};
    check(fr_xbee_decode_api2(too_short, sizeof(too_short), &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee short frame rejects");
}

int main(void)
{
    test_safe_defaults();
    test_relay_gates();
    test_storage_gates();
    test_http_contracts();
    test_xbee_frames();

    if (failures != 0) {
        fprintf(stderr, "%d host test failure(s)\n", failures);
        return 1;
    }

    printf("PASS: four_relay_safe_core host tests succeeded\n");
    return 0;
}
