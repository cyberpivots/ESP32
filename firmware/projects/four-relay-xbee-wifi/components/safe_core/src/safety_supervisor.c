#include "four_relay_core.h"

const char *fr_status_name(fr_status_t status)
{
    switch (status) {
    case FR_OK:
        return "ok";
    case FR_REJECT_ADMIN_REQUIRED:
        return "admin_required";
    case FR_REJECT_SAFETY_LOCKED:
        return "safety_locked";
    case FR_REJECT_RELAY_CONFIG_MISSING:
        return "relay_config_missing";
    case FR_REJECT_RELAY_CHANNEL_INVALID:
        return "relay_channel_invalid";
    case FR_REJECT_PAYLOAD_INVALID:
        return "payload_invalid";
    case FR_REJECT_SEQUENCE_REPLAY:
        return "sequence_replay";
    case FR_REJECT_SOURCE_NOT_ALLOWED:
        return "source_not_allowed";
    case FR_REJECT_XBEE_LINK_UNVERIFIED:
        return "xbee_link_unverified";
    case FR_REJECT_HARDWARE_GATE_OPEN:
        return "hardware_gate_open";
    case FR_REJECT_STORAGE_UNAVAILABLE:
        return "storage_unavailable";
    case FR_REJECT_LOG_APPEND_FAILED:
        return "log_append_failed";
    }
    return "payload_invalid";
}

fr_status_t fr_safety_supervisor_accepts_change(
    const fr_relay_state_t *state,
    const fr_command_context_t *context
)
{
    if (state == 0 || context == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!state->hardware_gate_closed) {
        return FR_REJECT_HARDWARE_GATE_OPEN;
    }
    if (!state->safety_lock_open) {
        return FR_REJECT_SAFETY_LOCKED;
    }
    if (!state->relay_config_valid) {
        return FR_REJECT_RELAY_CONFIG_MISSING;
    }
    if (!context->admin_authenticated) {
        return FR_REJECT_ADMIN_REQUIRED;
    }
    if (!context->source_allowed) {
        return FR_REJECT_SOURCE_NOT_ALLOWED;
    }
    if (!context->xbee_link_verified) {
        return FR_REJECT_XBEE_LINK_UNVERIFIED;
    }
    if (context->sequence != 0 && context->sequence <= state->last_sequence) {
        return FR_REJECT_SEQUENCE_REPLAY;
    }
    return FR_OK;
}
