#include "four_relay_core.h"

void fr_storage_status_default(fr_storage_status_t *status)
{
    if (status == 0) {
        return;
    }
    status->hardware_gate_closed = false;
    status->mounted = false;
    status->writable = false;
    status->assets_available = false;
    status->logs_available = false;
    status->free_kib = 0;
}

fr_status_t fr_storage_require_logs(const fr_storage_status_t *status)
{
    if (status == 0) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (!status->hardware_gate_closed || !status->mounted || !status->writable) {
        return FR_REJECT_STORAGE_UNAVAILABLE;
    }
    if (!status->logs_available) {
        return FR_REJECT_LOG_APPEND_FAILED;
    }
    return FR_OK;
}
