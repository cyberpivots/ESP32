#ifndef FOUR_RELAY_CORE_H
#define FOUR_RELAY_CORE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define FR_RELAY_CHANNELS 4u
#define FR_RELAY_PUBLIC_MIN_CHANNEL 1u
#define FR_RELAY_PUBLIC_MAX_CHANNEL FR_RELAY_CHANNELS
#define FR_XBEE_MAX_FRAME_DATA 128u
#define FR_XBEE_AT_VALUE_MAX 64u
#define FR_API_ASSET_FILE_COUNT 4u

typedef enum {
    FR_OK = 0,
    FR_REJECT_ADMIN_REQUIRED,
    FR_REJECT_SAFETY_LOCKED,
    FR_REJECT_RELAY_CONFIG_MISSING,
    FR_REJECT_RELAY_CHANNEL_INVALID,
    FR_REJECT_PAYLOAD_INVALID,
    FR_REJECT_SEQUENCE_REPLAY,
    FR_REJECT_SOURCE_NOT_ALLOWED,
    FR_REJECT_XBEE_LINK_UNVERIFIED,
    FR_REJECT_HARDWARE_GATE_OPEN,
    FR_REJECT_STORAGE_UNAVAILABLE,
    FR_REJECT_LOG_APPEND_FAILED
} fr_status_t;

typedef struct {
    bool admin_authenticated;
    bool source_allowed;
    bool xbee_link_verified;
    uint32_t sequence;
} fr_command_context_t;

typedef struct {
    bool desired_on[FR_RELAY_CHANNELS];
    bool hardware_gate_closed;
    bool safety_lock_open;
    bool relay_config_valid;
    uint32_t last_sequence;
} fr_relay_state_t;

typedef struct {
    bool provisioned;
    bool relay_config_valid;
    bool xbee_allowlist_present;
    bool storage_config_valid;
} fr_config_snapshot_t;

typedef struct {
    bool hardware_gate_closed;
    bool mounted;
    bool writable;
    bool assets_available;
    bool logs_available;
    uint32_t free_kib;
} fr_storage_status_t;

typedef enum {
    FR_HTTP_METHOD_GET = 0,
    FR_HTTP_METHOD_POST,
    FR_HTTP_METHOD_UNSUPPORTED
} fr_http_method_t;

typedef enum {
    FR_HTTP_ENDPOINT_STATE = 0,
    FR_HTTP_ENDPOINT_RELAY,
    FR_HTTP_ENDPOINT_ALL_OFF,
    FR_HTTP_ENDPOINT_SAFETY_LOCK,
    FR_HTTP_ENDPOINT_STORAGE_STATUS,
    FR_HTTP_ENDPOINT_ASSETS_MANIFEST,
    FR_HTTP_ENDPOINT_LOGS_RECENT,
    FR_HTTP_ENDPOINT_UNKNOWN
} fr_http_endpoint_t;

typedef struct {
    fr_http_method_t method;
    fr_http_endpoint_t endpoint;
    bool state_changing;
    int relay_channel;
} fr_http_route_t;

typedef struct {
    uint8_t data[FR_XBEE_MAX_FRAME_DATA];
    size_t data_len;
} fr_xbee_frame_t;

typedef struct {
    bool has_state;
    bool state;
    bool has_sequence;
    uint32_t sequence;
} fr_relay_command_payload_t;

typedef struct {
    bool has_sequence;
    uint32_t sequence;
} fr_sequence_payload_t;

typedef struct {
    bool has_locked;
    bool locked;
    bool has_sequence;
    uint32_t sequence;
} fr_safety_lock_payload_t;

typedef struct {
    size_t channel;
    bool state;
    bool enabled;
} fr_relay_snapshot_t;

typedef struct {
    bool safety_locked;
    bool admin_provisioned;
    bool hardware_gate_closed;
    fr_relay_snapshot_t relays[FR_RELAY_CHANNELS];
    fr_storage_status_t storage;
    const char *last_result;
} fr_state_snapshot_t;

typedef struct {
    const char *name;
    const char *version;
    const char *asset_root;
    const char *files[FR_API_ASSET_FILE_COUNT];
    size_t file_count;
} fr_assets_manifest_t;

typedef struct {
    size_t limit;
    const char *type;
    size_t item_count;
    bool truncated;
} fr_logs_recent_response_t;

typedef struct {
    uint8_t frame_id;
    char command[3];
    uint8_t command_status;
    uint8_t value[FR_XBEE_AT_VALUE_MAX];
    size_t value_len;
} fr_xbee_at_response_t;

typedef struct {
    uint8_t source64[8];
    uint16_t source16;
    uint8_t receive_options;
    uint8_t payload[FR_XBEE_MAX_FRAME_DATA];
    size_t payload_len;
} fr_xbee_receive_packet_t;

const char *fr_status_name(fr_status_t status);

void fr_relay_state_init(fr_relay_state_t *state);
fr_status_t fr_relay_public_channel_to_index(
    size_t public_channel,
    size_t *index
);
fr_status_t fr_relay_request_set(
    fr_relay_state_t *state,
    size_t channel,
    bool on,
    const fr_command_context_t *context
);
fr_status_t fr_relay_request_set_public(
    fr_relay_state_t *state,
    size_t public_channel,
    bool on,
    const fr_command_context_t *context
);
fr_status_t fr_relay_all_off(
    fr_relay_state_t *state,
    const fr_command_context_t *context
);

fr_status_t fr_safety_supervisor_accepts_change(
    const fr_relay_state_t *state,
    const fr_command_context_t *context
);

void fr_config_store_default(fr_config_snapshot_t *config);
fr_status_t fr_config_validate_for_relay(const fr_config_snapshot_t *config);

void fr_storage_status_default(fr_storage_status_t *status);
fr_status_t fr_storage_require_logs(const fr_storage_status_t *status);

fr_http_route_t fr_http_classify_route(const char *method, const char *path);

fr_status_t fr_api_validate_relay_payload(
    const fr_relay_command_payload_t *payload
);
fr_status_t fr_api_validate_all_off_payload(
    const fr_sequence_payload_t *payload
);
fr_status_t fr_api_validate_safety_lock_payload(
    const fr_safety_lock_payload_t *payload
);
void fr_api_build_state_snapshot(
    const fr_relay_state_t *state,
    const fr_storage_status_t *storage,
    fr_state_snapshot_t *snapshot
);
void fr_api_assets_manifest_default(fr_assets_manifest_t *manifest);
void fr_api_logs_recent_empty(
    size_t limit,
    const char *type,
    fr_logs_recent_response_t *response
);

fr_status_t fr_xbee_encode_api2(
    const uint8_t *frame_data,
    size_t frame_len,
    uint8_t *wire,
    size_t wire_capacity,
    size_t *wire_len
);
fr_status_t fr_xbee_decode_api2(
    const uint8_t *wire,
    size_t wire_len,
    fr_xbee_frame_t *frame
);
fr_status_t fr_xbee_parse_at_response(
    const fr_xbee_frame_t *frame,
    fr_xbee_at_response_t *response
);
fr_status_t fr_xbee_parse_receive_packet(
    const fr_xbee_frame_t *frame,
    fr_xbee_receive_packet_t *packet
);

#endif
