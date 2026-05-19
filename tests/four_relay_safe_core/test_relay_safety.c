#include "four_relay_core.h"
#include "test_support.h"

#include <string.h>

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

    fr_relay_state_init(&state);
    fr_config_store_default(&config);

    check(!state.hardware_gate_closed, "relay hardware gate defaults open");
    check(!state.safety_lock_open, "safety lock defaults closed");
    check(!state.relay_config_valid, "relay config defaults invalid");
    for (size_t index = 0; index < FR_RELAY_CHANNELS; ++index) {
        check(!state.desired_on[index], "relay desired state defaults off");
    }
    check(fr_config_validate_for_relay(&config) == FR_REJECT_RELAY_CONFIG_MISSING,
          "default config rejects relay use");
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

int main(void)
{
    test_safe_defaults();
    test_relay_gates();
    return finish_tests("test_relay_safety");
}
