#include "four_relay_core.h"
#include "test_support.h"

#include <string.h>

static void test_api2_codec(void)
{
    const uint8_t frame_data[] = {
        0x90, 0x00, 0x13, 0xa2, 0x00, 0x41, 0x7e, 0x7d, 0x11, 0x13, 0x01
    };
    uint8_t wire[64];
    size_t wire_len = 0;
    fr_xbee_frame_t decoded;

    check(fr_xbee_encode_api2(frame_data, sizeof(frame_data), wire, sizeof(wire), &wire_len) == FR_OK,
          "XBee API2 encode succeeds in memory");
    check(wire_len > sizeof(frame_data), "XBee API2 encoder escapes reserved bytes");
    check(fr_xbee_decode_api2(wire, wire_len, &decoded) == FR_OK,
          "XBee API2 decode succeeds in memory");
    check(decoded.data_len == sizeof(frame_data), "XBee decoded length matches");
    check(memcmp(decoded.data, frame_data, sizeof(frame_data)) == 0,
          "XBee decoded frame matches input");

    wire[wire_len - 1u] ^= 0x01u;
    check(fr_xbee_decode_api2(wire, wire_len, &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee bad checksum rejects");

    const uint8_t status_frame[] = {0x8b, 0x01, 0xff, 0xfe, 0x00, 0x00, 0x00};
    check(fr_xbee_encode_api2(status_frame, sizeof(status_frame), wire, sizeof(wire), &wire_len) == FR_OK,
          "XBee transmit status frame encodes");
    check(fr_xbee_decode_api2(wire, wire_len, &decoded) == FR_OK,
          "XBee transmit status frame decodes");
    check(decoded.data_len == sizeof(status_frame), "XBee status frame decoded length matches");
    check(decoded.data[0] == 0x8b, "XBee status frame type preserved");

    const uint8_t bad_length[] = {0x7e, 0x00, 0x02, 0x90, 0x6f};
    check(fr_xbee_decode_api2(bad_length, sizeof(bad_length), &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee bad length rejects");

    const uint8_t truncated_escape[] = {0x7e, 0x00, 0x01, 0x7d};
    check(fr_xbee_decode_api2(truncated_escape, sizeof(truncated_escape), &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee truncated escape rejects");

    const uint8_t too_short[] = {0x7e, 0x00, 0x01};
    check(fr_xbee_decode_api2(too_short, sizeof(too_short), &decoded) == FR_REJECT_PAYLOAD_INVALID,
          "XBee short frame rejects");
}

static void test_at_response_parser(void)
{
    fr_xbee_frame_t frame;
    fr_xbee_at_response_t response;
    const uint8_t at_response[] = {0x88, 0x01, 'V', 'R', 0x00, 0x22, 0x17};

    memcpy(frame.data, at_response, sizeof(at_response));
    frame.data_len = sizeof(at_response);
    check(fr_xbee_parse_at_response(&frame, &response) == FR_OK,
          "AT response frame parses command");
    check(response.frame_id == 0x01u, "AT response frame preserves frame id");
    check(strcmp(response.command, "VR") == 0, "AT response frame parses command name");
    check(response.command_status == 0x00u, "AT response frame preserves command status");
    check(response.value_len == 2u, "AT response frame preserves value length");

    frame.data[0] = 0x90u;
    check(fr_xbee_parse_at_response(&frame, &response) == FR_REJECT_PAYLOAD_INVALID,
          "AT response parser rejects receive-packet frame");
}

static void test_receive_packet_parser(void)
{
    fr_xbee_frame_t frame;
    fr_xbee_receive_packet_t packet;
    const uint8_t receive_packet[] = {
        0x90,
        0x00, 0x13, 0xa2, 0x00, 0x41, 0x52, 0x53, 0x54,
        0xff, 0xfe,
        0x01,
        'O', 'K'
    };

    memcpy(frame.data, receive_packet, sizeof(receive_packet));
    frame.data_len = sizeof(receive_packet);
    check(fr_xbee_parse_receive_packet(&frame, &packet) == FR_OK,
          "receive-packet payload parses");
    check(packet.source64[0] == 0x00u && packet.source64[7] == 0x54u,
          "receive-packet source64 parses");
    check(packet.source16 == 0xfffeu, "receive-packet source16 parses");
    check(packet.receive_options == 0x01u, "receive-packet options parse");
    check(packet.payload_len == 2u, "receive-packet payload length parses");
    check(packet.payload[0] == 'O' && packet.payload[1] == 'K',
          "receive-packet payload bytes parse");

    frame.data_len = 12u;
    check(fr_xbee_parse_receive_packet(&frame, &packet) == FR_REJECT_PAYLOAD_INVALID,
          "receive-packet parser rejects empty payload");
    frame.data_len = sizeof(receive_packet);
    frame.data[0] = 0x88u;
    check(fr_xbee_parse_receive_packet(&frame, &packet) == FR_REJECT_PAYLOAD_INVALID,
          "receive-packet parser rejects AT response frame");
}

int main(void)
{
    test_api2_codec();
    test_at_response_parser();
    test_receive_packet_parser();
    return finish_tests("test_xbee_frame_codec");
}
