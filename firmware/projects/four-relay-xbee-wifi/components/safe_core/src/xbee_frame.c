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

fr_status_t fr_xbee_parse_at_response(
    const fr_xbee_frame_t *frame,
    fr_xbee_at_response_t *response
)
{
    if (frame == 0 || response == 0 || frame->data_len < 5u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (frame->data[0] != 0x88u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    size_t value_len = frame->data_len - 5u;
    if (value_len > FR_XBEE_AT_VALUE_MAX) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    response->frame_id = frame->data[1];
    response->command[0] = (char)frame->data[2];
    response->command[1] = (char)frame->data[3];
    response->command[2] = '\0';
    response->command_status = frame->data[4];
    response->value_len = value_len;
    for (size_t index = 0; index < value_len; ++index) {
        response->value[index] = frame->data[index + 5u];
    }
    return FR_OK;
}

fr_status_t fr_xbee_parse_receive_packet(
    const fr_xbee_frame_t *frame,
    fr_xbee_receive_packet_t *packet
)
{
    if (frame == 0 || packet == 0 || frame->data_len <= 12u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    if (frame->data[0] != 0x90u) {
        return FR_REJECT_PAYLOAD_INVALID;
    }

    for (size_t index = 0; index < 8u; ++index) {
        packet->source64[index] = frame->data[index + 1u];
    }
    packet->source16 = ((uint16_t)frame->data[9] << 8u) | frame->data[10];
    packet->receive_options = frame->data[11];

    packet->payload_len = frame->data_len - 12u;
    if (packet->payload_len > FR_XBEE_MAX_FRAME_DATA) {
        return FR_REJECT_PAYLOAD_INVALID;
    }
    for (size_t index = 0; index < packet->payload_len; ++index) {
        packet->payload[index] = frame->data[index + 12u];
    }
    return FR_OK;
}
