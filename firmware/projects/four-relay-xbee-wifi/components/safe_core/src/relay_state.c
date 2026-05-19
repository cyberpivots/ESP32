#include "four_relay_core.h"

void fr_relay_state_init(fr_relay_state_t *state)
{
    if (state == 0) {
        return;
    }
    for (size_t index = 0; index < FR_RELAY_CHANNELS; ++index) {
        state->desired_on[index] = false;
    }
    state->hardware_gate_closed = false;
    state->safety_lock_open = false;
    state->relay_config_valid = false;
    state->last_sequence = 0;
}

fr_status_t fr_relay_public_channel_to_index(size_t public_channel, size_t *index)
{
    if (index == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (
        public_channel < FR_RELAY_PUBLIC_MIN_CHANNEL ||
        public_channel > FR_RELAY_PUBLIC_MAX_CHANNEL
    ) {
        return FR_REJECT_RELAY_CHANNEL_INVALID;
    }
    *index = public_channel - 1u;
    return FR_OK;
}

fr_status_t fr_relay_request_set(
    fr_relay_state_t *state,
    size_t channel,
    bool on,
    const fr_command_context_t *context
)
{
    if (state == 0 || context == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (channel >= FR_RELAY_CHANNELS) {
        return FR_REJECT_RELAY_CHANNEL_INVALID;
    }

    fr_status_t accepted = fr_safety_supervisor_accepts_change(state, context);
    if (accepted != FR_OK) {
        return accepted;
    }

    state->desired_on[channel] = on;
    if (context->sequence != 0) {
        state->last_sequence = context->sequence;
    }
    return FR_OK;
}

fr_status_t fr_relay_request_set_public(
    fr_relay_state_t *state,
    size_t public_channel,
    bool on,
    const fr_command_context_t *context
)
{
    size_t index = 0;
    fr_status_t status = fr_relay_public_channel_to_index(public_channel, &index);
    if (status != FR_OK) {
        return status;
    }
    return fr_relay_request_set(state, index, on, context);
}

fr_status_t fr_relay_all_off(
    fr_relay_state_t *state,
    const fr_command_context_t *context
)
{
    if (state == 0 || context == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!context->admin_authenticated) {
        return FR_REJECT_ADMIN_REQUIRED;
    }
    for (size_t index = 0; index < FR_RELAY_CHANNELS; ++index) {
        state->desired_on[index] = false;
    }
    return FR_OK;
}
