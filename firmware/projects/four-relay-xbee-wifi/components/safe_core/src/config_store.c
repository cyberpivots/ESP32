#include "four_relay_core.h"

void fr_config_store_default(fr_config_snapshot_t *config)
{
    if (config == 0) {
        return;
    }
    config->provisioned = false;
    config->relay_config_valid = false;
    config->xbee_allowlist_present = false;
    config->storage_config_valid = false;
}

fr_status_t fr_config_validate_for_relay(const fr_config_snapshot_t *config)
{
    if (config == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!config->provisioned || !config->relay_config_valid) {
        return FR_REJECT_RELAY_CONFIG_MISSING;
    }
    return FR_OK;
}
