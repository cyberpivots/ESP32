#include "four_relay_core.h"

void app_main(void)
{
    fr_relay_state_t relay_state;
    fr_config_snapshot_t config;
    fr_storage_status_t storage;

    fr_relay_state_init(&relay_state);
    fr_config_store_default(&config);
    fr_storage_status_default(&storage);

    (void)relay_state;
    (void)config;
    (void)storage;
}
