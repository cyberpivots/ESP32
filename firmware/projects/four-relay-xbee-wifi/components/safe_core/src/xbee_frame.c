#include "four_relay_core.h"

static bool needs_escape(uint8_t value)
{
    return value == 0x7eu || value == 0x7du || value == 0x11u || value == 0x13u;
}

static fr_status_t append_escaped(
    uint8_t value,
    uint8_t *wire,
    size_t wire_capacity,
    size_t *offset
)
{
    if (needs_escape(value)) {
        if (*offset + 2u > wire_capacity) {
            return FR_REJECT_PAYLOAD_INVALID;
        }
        wire[(*offset)++] = 0x7du;
        wire[(*offset)++] = value ^ 0x20u;
        return FR_OK;
    }
    if (*offset + 1u > wire_capacity) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    wire[(*offset)++] = value;
    return FR_OK;
}

fr_status_t fr_xbee_encode_api2(
    const uint8_t *frame_data,
    size_t frame_len,
    uint8_t *wire,
    size_t wire_capacity,
    size_t *wire_len
)
{
    if (frame_data == 0 || wire == 0 || wire_len == 0 || frame_len > FR_XBEE_MAX_FRAME_DATA) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (wire_capacity < 4u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    size_t offset = 0;
    uint8_t checksum_sum = 0;
    wire[offset++] = 0x7eu;

    fr_status_t status = append_escaped((uint8_t)((frame_len >> 8u) & 0xffu), wire, wire_capacity, &offset);
    if (status != FR_OK) {
        return status;
    }
    status = append_escaped((uint8_t)(frame_len & 0xffu), wire, wire_capacity, &offset);
    if (status != FR_OK) {
        return status;
    }

    for (size_t index = 0; index < frame_len; ++index) {
        checksum_sum = (uint8_t)(checksum_sum + frame_data[index]);
        status = append_escaped(frame_data[index], wire, wire_capacity, &offset);
        if (status != FR_OK) {
            return status;
        }
    }

    status = append_escaped((uint8_t)(0xffu - checksum_sum), wire, wire_capacity, &offset);
    if (status != FR_OK) {
        return status;
    }
    *wire_len = offset;
    return FR_OK;
}

fr_status_t fr_xbee_decode_api2(
    const uint8_t *wire,
    size_t wire_len,
    fr_xbee_frame_t *frame
)
{
    if (wire == 0 || frame == 0 || wire_len < 4u || wire[0] != 0x7eu) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    uint8_t decoded[FR_XBEE_MAX_FRAME_DATA + 3u];
    size_t decoded_len = 0;
    for (size_t index = 1u; index < wire_len; ++index) {
        uint8_t value = wire[index];
        if (value == 0x7du) {
            if (index + 1u >= wire_len) {
                return FR_REJECT_PAYLOAD_INVALID;
            }
            value = wire[++index] ^ 0x20u;
        }
        if (decoded_len >= sizeof(decoded)) {
            return FR_REJECT_PAYLOAD_INVALID;
        }
        decoded[decoded_len++] = value;
    }

    if (decoded_len < 3u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    size_t frame_len = ((size_t)decoded[0] << 8u) | decoded[1];
    if (frame_len > FR_XBEE_MAX_FRAME_DATA || decoded_len != frame_len + 3u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    uint8_t checksum_sum = 0;
    for (size_t index = 0; index < frame_len; ++index) {
        frame->data[index] = decoded[index + 2u];
        checksum_sum = (uint8_t)(checksum_sum + frame->data[index]);
    }
    checksum_sum = (uint8_t)(checksum_sum + decoded[decoded_len - 1u]);
    if (checksum_sum != 0xffu) {
        frame->data_len = 0;
        return FR_REJECT_PAYLOAD_INVALID;
    }

    frame->data_len = frame_len;
    return FR_OK;
}
