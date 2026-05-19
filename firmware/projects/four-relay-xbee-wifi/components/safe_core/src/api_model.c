#include "four_relay_core.h"

static bool has_valid_sequence(bool has_sequence, uint32_t sequence)
{
    return has_sequence && sequence != 0u;
}

fr_status_t fr_api_validate_relay_payload(
    const fr_relay_command_payload_t *payload
)
{
    if (payload == 0 || !payload->has_state) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!has_valid_sequence(payload->has_sequence, payload->sequence)) {
        return FR_REJECT_SEQUENCE_REPLAY;
    }
    return FR_OK;
}

fr_status_t fr_api_validate_all_off_payload(
    const fr_sequence_payload_t *payload
)
{
    if (payload == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!has_valid_sequence(payload->has_sequence, payload->sequence)) {
        return FR_REJECT_SEQUENCE_REPLAY;
    }
    return FR_OK;
}

fr_status_t fr_api_validate_safety_lock_payload(
    const fr_safety_lock_payload_t *payload
)
{
    if (payload == 0 || !payload->has_locked) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!has_valid_sequence(payload->has_sequence, payload->sequence)) {
        return FR_REJECT_SEQUENCE_REPLAY;
    }
    return FR_OK;
}

void fr_api_build_state_snapshot(
    const fr_relay_state_t *state,
    const fr_storage_status_t *storage,
    fr_state_snapshot_t *snapshot
)
{
    if (snapshot == 0) {
        return;
    }

    fr_relay_state_t default_state;
    fr_storage_status_t default_storage;
    if (state == 0) {
        fr_relay_state_init(&default_state);
        state = &default_state;
    }
    if (storage == 0) {
        fr_storage_status_default(&default_storage);
        storage = &default_storage;
    }

    snapshot->safety_locked = !state->safety_lock_open;
    snapshot->admin_provisioned = false;
    snapshot->hardware_gate_closed = state->hardware_gate_closed;
    snapshot->storage = *storage;
    snapshot->last_result = "safe_default";

    bool relays_enabled =
        state->hardware_gate_closed &&
        state->safety_lock_open &&
        state->relay_config_valid;
    for (size_t index = 0; index < FR_RELAY_CHANNELS; ++index) {
        snapshot->relays[index].channel = index + 1u;
        snapshot->relays[index].state = state->desired_on[index];
        snapshot->relays[index].enabled = relays_enabled;
    }
}

void fr_api_assets_manifest_default(fr_assets_manifest_t *manifest)
{
    if (manifest == 0) {
        return;
    }
    manifest->name = "four-relay-admin-hmi";
    manifest->version = "2026-05-18-admin-hmi";
    manifest->asset_root = "/sdcard/www";
    manifest->files[0] = "index.html";
    manifest->files[1] = "styles.css";
    manifest->files[2] = "app.js";
    manifest->files[3] = "manifest.json";
    manifest->file_count = FR_API_ASSET_FILE_COUNT;
}

void fr_api_logs_recent_empty(
    size_t limit,
    const char *type,
    fr_logs_recent_response_t *response
)
{
    if (response == 0) {
        return;
    }
    response->limit = limit;
    response->type = type == 0 ? "all" : type;
    response->item_count = 0u;
    response->truncated = false;
}
