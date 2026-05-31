#!/usr/bin/env python3
"""Firmware skeleton and safe-core contract audits."""

from __future__ import annotations

from pathlib import Path

from scaffold_audit_data import (
    FIRMWARE_SOURCE_SCAN_ROOT,
    FORBIDDEN_FIRMWARE_MARKERS,
    ROOT,
)
from scaffold_audit_docs import require_markers

UART_BRIDGE_SOURCE = "firmware/projects/four-relay-xbee-wifi/main/main.c"


def audit_firmware_readme(root: Path = ROOT) -> list[str]:
    firmware_readme = (
        root / "firmware/projects/four-relay-xbee-wifi/README.md"
    ).read_text(encoding="utf-8")
    return require_markers(firmware_readme, [
        "## Verified facts",
        "## Assumptions",
        "## Unknowns",
        "## Hard gates",
        "No GPIO writes",
        "Encoder GPIO reads are allowed only for this input-only menu/diagnostic work",
        "No expander writes",
        "No XBee setting writes",
        "UART bridge writes are allowed only for the normal bridge feature",
        "LCD I2C writes are allowed only for this display-only menu feature",
        "No flash or monitor step",
        "No live bench mutation outside accepted named gates",
        "encoder menu gate,",
        "completed COM6-only write/verify",
        "PF0530F",
        "PF0530G",
        "PF0530H",
        "PF0530I",
        "PF0530J",
        "FR_DIAG_XBEE_BRIDGE_CLOSED 1",
        "SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31",
        "pure-C API payload validation",
        "normalized state snapshots",
        "split host-test binaries",
        "SRC-ESP-IDF-STABLE-ESP32",
        "SRC-ESP-IDF-I2C",
        "SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30",
        "page-0 raw levels and transition",
        "pin-finder",
        "SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19",
    ], "firmware skeleton README")


def audit_safe_core_contract(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    core_header = (
        root
        / "firmware/projects/four-relay-xbee-wifi/components/safe_core/include/four_relay_core.h"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(core_header, [
        "FR_REJECT_HARDWARE_GATE_OPEN",
        "fr_relay_request_set",
        "fr_relay_request_set_public",
        "fr_relay_public_channel_to_index",
        "fr_safety_supervisor_accepts_change",
        "fr_config_store_default",
        "fr_http_classify_route",
        "fr_api_validate_relay_payload",
        "fr_api_build_state_snapshot",
        "fr_api_assets_manifest_default",
        "fr_api_logs_recent_empty",
        "fr_storage_status_default",
        "fr_xbee_encode_api2",
        "fr_xbee_decode_api2",
        "fr_xbee_parse_at_response",
        "fr_xbee_parse_receive_packet",
    ], "safe core header"))

    host_test_runner = (
        root / "tests/four_relay_safe_core/run_host_tests.py"
    ).read_text(encoding="utf-8")
    host_test_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((root / "tests/four_relay_safe_core").glob("test_*.c"))
    )
    failures.extend(require_markers(host_test_text, [
        "hardware_gate_open",
        "public relay channel zero route rejects",
        "public relay channel 4 maps to internal index three",
        "GET /api/state response snapshot includes storage",
        "POST /api/all-off payload contract accepts sequence",
        "GET /api/assets/manifest response exposes file list",
        "GET /api/logs/recent response defaults empty",
        "XBee API2 encode succeeds in memory",
        "bad checksum rejects",
        "XBee truncated escape rejects",
        "AT response frame parses command",
        "receive-packet payload parses",
    ], "safe core host tests"))
    for marker in ["-Werror", "test_relay_safety", "safe_core"]:
        if marker not in host_test_runner:
            failures.append(f"safe core test runner missing marker: {marker}")
    return failures


def audit_firmware_forbidden_markers(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    scan_root = root / FIRMWARE_SOURCE_SCAN_ROOT.relative_to(ROOT)
    for source_file in sorted(scan_root.rglob("*")):
        if source_file.suffix not in {".c", ".h", ".txt"} and source_file.name != "CMakeLists.txt":
            continue
        text = source_file.read_text(encoding="utf-8")
        rel = source_file.relative_to(root).as_posix()
        for forbidden in FORBIDDEN_FIRMWARE_MARKERS:
            if forbidden == "uart_write_bytes" and rel == UART_BRIDGE_SOURCE:
                continue
            if forbidden == "gpio_config" and rel == UART_BRIDGE_SOURCE:
                continue
            if forbidden == "i2c_master_transmit" and rel == UART_BRIDGE_SOURCE:
                continue
            if forbidden in text:
                failures.append(f"firmware skeleton contains forbidden marker {forbidden}: {rel}")
    return failures


def audit_uart_bridge_boundary(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    bridge = (root / UART_BRIDGE_SOURCE).read_text(encoding="utf-8")
    failures.extend(require_markers(bridge, [
        "FR_BRIDGE_HOST_UART UART_NUM_0",
        "FR_BRIDGE_XBEE_UART UART_NUM_2",
        "FR_BRIDGE_HOST_BAUD 115200",
        "FR_BRIDGE_XBEE_BAUD 9600",
        "FR_BRIDGE_XBEE_TX_GPIO GPIO_NUM_17",
        "FR_BRIDGE_XBEE_RX_GPIO GPIO_NUM_16",
        "UART_HW_FLOWCTRL_DISABLE",
        "esp_log_level_set(\"*\", ESP_LOG_NONE)",
        "uart_write_bytes",
        "uart_read_bytes",
        "fr_relay_state_init",
        "fr_config_store_default",
        "fr_storage_status_default",
    ], "UART bridge firmware boundary"))
    for forbidden in [
        "\"WR\"",
        "\"AC\"",
        "\"KY\"",
        "esp_wifi_start",
        "esp_vfs_fat",
        "gpio_set_level",
    ]:
        if forbidden in bridge:
            failures.append(f"UART bridge source contains forbidden marker: {forbidden}")

    main_cmake = (
        root / "firmware/projects/four-relay-xbee-wifi/main/CMakeLists.txt"
    ).read_text(encoding="utf-8")
    failures.extend(require_markers(main_cmake, [
        "PRIV_REQUIRES safe_core esp_driver_uart esp_driver_i2c esp_driver_gpio",
    ], "UART bridge CMake boundary"))
    return failures


def audit_lcd_test_boundary(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    bridge = (root / UART_BRIDGE_SOURCE).read_text(encoding="utf-8")
    failures.extend(require_markers(bridge, [
        "FR_LCD_I2C_PORT 0",
        "FR_LCD_I2C_SDA_GPIO GPIO_NUM_21",
        "FR_LCD_I2C_SCL_GPIO GPIO_NUM_22",
        "FR_LCD_I2C_SPEED_HZ 100000",
        "FR_LCD_TASK_PRIORITY tskIDLE_PRIORITY",
        ".flags.enable_internal_pullup = false",
        "i2c_master_probe",
        "fr_lcd_probe_range(lcd->bus, 0x20, 0x27",
        "fr_lcd_probe_range(lcd->bus, 0x38, 0x3f",
        "i2c_master_transmit",
        "FR_DIAG_XBEE_BRIDGE_CLOSED 1",
        "FR_DIAG_FIRMWARE_ID \"PF0530K\"",
        "LCD_DIAG_READY gpio=21/22 speed=%d pullups=external",
        "LCD_BUS result=ok",
        "LCD_PROBE addr=0x%02x result=ack",
        "LCD_PROBE_SUMMARY count=%u selected=0x%02x",
        "LCD_DEVICE result=ok addr=0x%02x",
        "LCD_HD44780 step=%s result=%s err=%s",
        "LCD_INIT_OK addr=0x%02x",
        "LCD_INIT_FAIL stage=",
        "LCD_DIAG_HB status=%s count=%lu addr=0x%02x stage=%s devices=%u",
        "fr_lcd_bbs_menu_task",
        "BBS_LCD_READY gpio=13/14/32 pullups=on lcd=21/22 addr=0x%02x",
        "BBS_INPUT_READY task=split poll_ms=%u render=dirty idle_ms=%u ",
        "irq=anyedge queue=%u",
        "BBS_LCD_RENDER page=%s index=%u row0=\\\"%s\\\" row1=\\\"%s\\\"",
        "rows=%u seq=%lu dur_ms=%lu reason=%s",
        "BBS FIELD LINK:OK",
        "MESSAGES",
        "PEERS",
        "QUEUE",
        "FILES",
        "MESH",
        "XBEE",
        "DIAG",
        "LOCKS",
        "fr_lcd_start_task",
    ], "LCD-only I2C firmware boundary"))
    if "xTaskCreate(\n        fr_lcd_diag_task" in bridge:
        failures.append("LCD task start still targets fr_lcd_diag_task")
    if "xTaskCreate(\n        fr_lcd_bbs_menu_task" not in bridge:
        failures.append("LCD task start does not target fr_lcd_bbs_menu_task")
    return failures


def audit_encoder_menu_boundary(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    bridge = (root / UART_BRIDGE_SOURCE).read_text(encoding="utf-8")
    failures.extend(require_markers(bridge, [
        "#include \"driver/gpio.h\"",
        "#include \"freertos/queue.h\"",
        "FR_ENCODER_CLK_GPIO GPIO_NUM_13",
        "FR_ENCODER_DT_GPIO GPIO_NUM_14",
        "FR_ENCODER_SW_GPIO GPIO_NUM_32",
        "FR_ENCODER_TRANSITIONS_PER_STEP 4",
        "FR_ENCODER_SW_DEBOUNCE_MS 30",
        "FR_ENCODER_SW_GUARD_MS 150",
        "FR_ENCODER_LONG_PRESS_MS 800",
        "FR_ENCODER_AB_STABLE_SAMPLES 3",
        "FR_GPIO_SWEEP_COUNT 3",
        "FR_MENU_POLL_MS 10",
        "FR_MENU_PAGE_COUNT 9",
        "FR_MENU_HEARTBEAT_MS 2000",
        "FR_ENCODER_EVENT_QUEUE_DEPTH 64",
        "FR_ENCODER_IRQ_DRAIN_LIMIT 32",
        "FR_DIAG_FIRMWARE_ID \"PF0530K\"",
        "FR_DIAG_XBEE_BRIDGE_CLOSED 1",
        "FR_MENU_RENDER_POLL_MS 20",
        "FR_MENU_IDLE_REFRESH_MS 60000",
        "FR_MENU_INPUT_TASK_PRIORITY (tskIDLE_PRIORITY + 1)",
        "fr_delay_ticks_at_least_one",
        "fr_encoder_irq_event_t",
        "fr_encoder_event_queue",
        "fr_encoder_isr_handler",
        "xQueueCreate(",
        "xQueueSendFromISR(",
        "xQueueReceive(fr_encoder_event_queue",
        "gpio_install_isr_service(0)",
        "gpio_isr_handler_add(",
        "gpio_config(&config)",
        ".mode = GPIO_MODE_INPUT",
        ".pull_up_en = enable_pullup ? GPIO_PULLUP_ENABLE : GPIO_PULLUP_DISABLE",
        ".pull_down_en = GPIO_PULLDOWN_DISABLE",
        ".intr_type = GPIO_INTR_ANYEDGE",
        "BBS_LCD_READY gpio=13/14/32 pullups=on lcd=21/22 addr=0x%02x",
        "BBS_INPUT_READY task=split poll_ms=%u render=dirty idle_ms=%u ",
        "irq=anyedge queue=%u",
        "ENC_RAW kind=%s levels=C%uD%uS%u raw_ab=%lu raw_sw=%lu t=%lu",
        "ENC_EV pin=%d label=%s level=%u count=%lu t=%lu",
        "BBS_MENU_STEP dir=%c page=%s index=%u pos=%ld cw=%lu ccw=%lu t=%lu",
        "BBS_MENU_SELECT buttons=%lu page=%s index=%u kind=short t=%lu",
        "BBS_MENU_SELECT buttons=%lu page=%s index=%u kind=long t=%lu",
        "AB_SUPPRESS raw=%u levels=C%uD%uS%u suppressed=%lu t=%lu",
        "AB_INVALID prev=%u curr=%u invalid=%lu t=%lu",
        "BBS_MENU_HB page=%s index=%u pos=%ld levels=C%uD%uS%u steps=%lu/%lu",
        "irq_drop=%lu",
        "BBS_LCD_RENDER page=%s index=%u row0=\\\"%s\\\" row1=\\\"%s\\\"",
        "rows=%u seq=%lu dur_ms=%lu reason=%s",
        "fr_menu_input_task",
        "fr_lcd_render_cache_t",
        "render_cache.valid",
        "runtime.lcd_dirty",
        "static const int8_t transition_table[16]",
        "fr_menu_step(menu, 1, now_ms)",
        "fr_menu_step(menu, -1, now_ms)",
        "raw_ab_transition_count",
        "raw_sw_transition_count",
        "signal_change_count",
        "cw_step_count",
        "ccw_step_count",
        "invalid_transition_count",
        "suppressed_transition_count",
        "switch_guard_until_ms",
        "last_heartbeat_ms",
        "{FR_ENCODER_CLK_GPIO, \"CLK\", true}",
        "{FR_ENCODER_DT_GPIO, \"DT\", true}",
        "{FR_ENCODER_SW_GPIO, \"SW\", true}",
        "fr_gpio_sweep_pins[index].enable_pullup",
        "fr_menu_sample_ab_channel",
        "fr_menu_raw_ab",
        "fr_menu_process_levels",
        "fr_menu_handle_switch_stable",
        "fr_menu_handle_long_press",
        "fr_menu_sample_inputs",
        "fr_diag_short_display_count",
        "fr_diag_short_position_magnitude",
        "fr_bbs_page_name",
        "BBS FIELD LINK:OK",
        "fr_menu_level_char",
        "MSG N:1 IN:12",
        "PEERS 2/3",
        "QUEUE P:2 F:0",
        "FILES Q:1 D:3",
        "MESH sim",
        "XBEE CLOSED",
        "DIAG FIELD",
        "Flash:LOCK Ser:LOCK",
    ], "encoder LCD menu firmware boundary"))
    for forbidden in [
        "FR_DIAG_SERIAL_PINTRACE 1",
        "SERIAL_PINTRACE READY",
        "fr_serial_pintrace_start_task",
        "fr_serial_pintrace_run();",
        "    menu->page = 0;\n    if (menu->ack",
        "gpio_pullup_en(pins[index])",
        "FR_ENCODER_CLK_GPIO GPIO_NUM_34",
        "FR_ENCODER_DT_GPIO GPIO_NUM_35",
        "FR_ENCODER_SW_GPIO GPIO_NUM_13",
        "{FR_GPIO_SWEEP_GPIO32, \"32\", false}",
        "FR_GPIO_SWEEP_GPIO16",
        "FR_GPIO_SWEEP_GPIO17",
        "FR_GPIO_SWEEP_GPIO21",
        "FR_GPIO_SWEEP_GPIO22",
        "FR_GPIO_SWEEP_GPIO25",
        "FR_GPIO_SWEEP_GPIO26",
        "FR_GPIO_SWEEP_GPIO27",
        "FR_GPIO_SWEEP_GPIO33",
        "gpio_set_level",
        "esp_partition_erase",
        "esp_wifi_start",
        "httpd_start",
        "esp_vfs_fat",
    ]:
        if forbidden in bridge:
            failures.append(f"encoder menu source contains forbidden marker: {forbidden}")
    return failures


def audit_firmware(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(audit_firmware_readme(root))
    failures.extend(audit_safe_core_contract(root))
    failures.extend(audit_firmware_forbidden_markers(root))
    failures.extend(audit_uart_bridge_boundary(root))
    failures.extend(audit_lcd_test_boundary(root))
    failures.extend(audit_encoder_menu_boundary(root))
    return failures
