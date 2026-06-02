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
        "PF0530K",
        "PF0530L",
        "PF0530M",
        "PF0530N",
        "PF0530O",
        "PF0530P",
        "PF0530Q",
        "PF0530R",
        "PF0530T",
        "PF0530U",
        "PF0530V",
        "PF0530W",
        "FR_DIAG_XBEE_BRIDGE_CLOSED 1",
        "SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530M-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-SCROLLING-XML-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-REAL-MENU-CAL-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-LIVE-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-DEBOUNCE-CAL-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-LIVE-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-QUIET-CAL-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-LIVE-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530T-RESPONSIVE-2026-06-02",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-RESPONSIVE-V7-2026-06-02",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02",
        "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02",
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
        "PRIV_REQUIRES safe_core esp_driver_uart esp_driver_i2c esp_driver_gpio esp_driver_pcnt",
    ], "UART bridge CMake boundary"))
    return failures


def audit_lcd_test_boundary(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    bridge = (
        (root / UART_BRIDGE_SOURCE).read_text(encoding="utf-8")
        + "\n"
        + (root / "firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h").read_text(encoding="utf-8")
    )
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
        "FR_DIAG_FIRMWARE_ID \"PF0530W\"",
        "FR_DIAG_FIRMWARE_ID_VALUE \"PF0530W\"",
        "FR_GLYPH_BANK_COUNT FR_BBS_GLYPH_BANK_COUNT",
        "FR_BBS_GLYPH_BANK_COUNT 7u",
        "FR_GLYPH_BANK_SWAP_MIN_MS 250",
        "FR_MENU_AUTO_CYCLE_ENABLED 0U",
        "FR_MENU_AUTO_CYCLE_MS 7000",
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
        "irq=pcnt queue=%u",
        "BBS_GLYPH_BANK name=%s index=%u slots=%u rows=%u",
        "BBS_CURSOR row=%u col=%u ddram=0x%02x",
        "BBS_LCD_RENDER page=%s index=%u row0=\\\"%s\\\" row1=\\\"%s\\\"",
        "rows=%u seq=%lu dur_ms=%lu reason=%s",
        "dirty_rows=0x%02x dirty_cells=%u",
        "BBS FIELD STATUS",
        "MESSAGES",
        "PEERS",
        "QUEUE",
        "FILES",
        "MESH",
        "XBEE",
        "DIAG",
        "LOCKS",
        "BARS LINK QUEUE",
        "VERT CHART HISTORY",
        "BIG DIGITS 12:34",
        "GAUGE STATUS",
        "fr_lcd_start_task",
    ], "LCD-only I2C firmware boundary"))
    if "xTaskCreate(\n        fr_lcd_diag_task" in bridge:
        failures.append("LCD task start still targets fr_lcd_diag_task")
    if "xTaskCreate(\n        fr_lcd_bbs_menu_task" not in bridge:
        failures.append("LCD task start does not target fr_lcd_bbs_menu_task")
    return failures


def audit_encoder_menu_boundary(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    bridge = (
        (root / UART_BRIDGE_SOURCE).read_text(encoding="utf-8")
        + "\n"
        + (root / "firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h").read_text(encoding="utf-8")
    )
    failures.extend(require_markers(bridge, [
        "#include \"driver/gpio.h\"",
        "FR_ENCODER_CLK_GPIO GPIO_NUM_13",
        "FR_ENCODER_DT_GPIO GPIO_NUM_14",
        "FR_ENCODER_SW_GPIO GPIO_NUM_32",
        "FR_ENCODER_TRANSITIONS_PER_STEP 1",
        "FR_ENCODER_SW_DEBOUNCE_MS 30",
        "FR_ENCODER_AB_STABLE_SAMPLES 1",
        "FR_ENCODER_AB_DEBOUNCE_MS 1",
        "FR_ENCODER_AB_QUIET_MS 0",
        "FR_ENCODER_DETENT_AB 3U",
        "FR_ENCODER_STEP_LOCKOUT_MS 25",
        "FR_ENCODER_SW_GUARD_MS 40",
        "FR_ENCODER_PCNT_LOW_LIMIT -32767",
        "FR_ENCODER_PCNT_HIGH_LIMIT 32767",
        "FR_ENCODER_PCNT_RECENTER_LIMIT 30000",
        "FR_ENCODER_PCNT_GLITCH_NS 1000",
        "FR_ENCODER_PCNT_COUNTS_PER_STEP 4",
        "FR_ENCODER_PCNT_MAX_STEPS_PER_POLL 4",
        "FR_ENCODER_PCNT_DIR_SIGN 1",
        "FR_ENCODER_LONG_PRESS_MS 650",
        "FR_ENCODER_RAW_HEARTBEAT_MS 1000",
        "FR_ENCODER_RAW_EVENT_LOG_ENABLED 0U",
        "FR_ENCODER_INTERRUPT_TELEMETRY 0U",
        "FR_ENCODER_DETENT_GATED 1U",
        "FR_GPIO_SWEEP_COUNT 3",
        "FR_MENU_POLL_MS 2",
        "FR_MENU_PAGE_COUNT FR_BBS_MENU_PAGE_COUNT",
        "FR_BBS_MENU_PAGE_COUNT 15u",
        "FR_MENU_HEARTBEAT_MS 2000",
        "FR_MENU_AUTO_CYCLE_ENABLED 0U",
        "FR_MENU_AUTO_CYCLE_MS 7000",
        "FR_MENU_ANIMATION_MS 2000",
        "FR_ENCODER_EVENT_QUEUE_DEPTH 0",
        "FR_ENCODER_IRQ_DRAIN_LIMIT 0",
        "FR_DIAG_FIRMWARE_ID \"PF0530W\"",
        "FR_DIAG_FIRMWARE_ID_VALUE \"PF0530W\"",
        "FR_DIAG_XBEE_BRIDGE_CLOSED 1",
        "FR_GLYPH_BANK_COUNT FR_BBS_GLYPH_BANK_COUNT",
        "FR_BBS_GLYPH_BANK_COUNT 7u",
        "FR_GLYPH_SLOTS 8",
        "FR_GLYPH_ROWS 8",
        "FR_GLYPH_BANK_SWAP_MIN_MS 250",
        "FR_MENU_RENDER_POLL_MS 20",
        "FR_MENU_IDLE_REFRESH_MS 60000",
        "FR_MENU_INPUT_TASK_PRIORITY (tskIDLE_PRIORITY + 1)",
        "FR_MENU_MODE_PAGE_BROWSE",
        "FR_MENU_MODE_ROW_BROWSE",
        "FR_MENU_MODE_DETAIL",
        "FR_MENU_MODE_EDIT_LAB",
        "fr_delay_ticks_at_least_one",
        "fr_encoder_irq_count",
        "fr_encoder_pin_mask",
        "gpio_config(&config)",
        "gpio_dump_io_configuration(stdout, fr_encoder_pin_mask())",
        ".mode = GPIO_MODE_INPUT",
        ".pull_up_en = enable_pullup ? GPIO_PULLUP_ENABLE : GPIO_PULLUP_DISABLE",
        ".pull_down_en = GPIO_PULLDOWN_DISABLE",
        ".intr_type = FR_ENCODER_INTERRUPT_TELEMETRY != 0U",
        ": GPIO_INTR_DISABLE",
        "BBS_LCD_READY gpio=13/14/32 pullups=on lcd=21/22 addr=0x%02x",
        "BBS_INPUT_READY task=split poll_ms=%u render=dirty idle_ms=%u ",
        "irq=pcnt queue=%u",
        "modes=scroll,detail,edit actions=page,detail,edit,back",
        "step=%u stable=%u sw_debounce_ms=%u sw_guard_ms=%u long_ms=%u drain=%u",
        "cal=pcnt-v1",
        "decoder=pcnt sw=poll pcnt=1 counts_per_step=%u",
        "max_steps=%u glitch_ns=%u dir=%d recenter=%d",
        "ab_ms=%u quiet_ms=%u step_lockout_ms=%u",
        "detent=%u detent_gate=%u raw_hb_ms=%u gpio_cfg=1 poll_raw=1 ",
        "raw_log=%u poll_decoder=0 source=%s",
        "ENC_BASE levels=C%uD%uS%u raw_ab=%u pcnt_count=%ld t=%lu",
        "ENC_GPIO_CONFIG pin=%d label=%s mode=input pullup=%s",
        "ENC_PCNT_READY result=ok",
        "ENC_LEVEL_HB levels=C%uD%uS%u raw_ab=%u stable=C%uD%u",
        "ENC_PCNT_HB count=%ld delta=%ld residual=%ld steps=%lu",
        "FR_BBS_MENU_XML_SCHEMA",
        "FR_BBS_MENU_RENDER_SCHEMA",
        "FR_BBS_MENU_MARQUEE_HOLD_MS 750u",
        "FR_BBS_MENU_MARQUEE_STEP_MS 250u",
        "fr_bbs_generated_pages",
        "fr_bbs_sync_menu_view",
        "fr_bbs_render_generated_frame",
        ".name = \"table\"",
        "NODE |RSSI|Q",
        "ROUTES",
        "ENC_RAW kind=%s levels=C%uD%uS%u raw_ab=%lu raw_sw=%lu ",
        "gap_ms=%lu burst=%lu t=%lu",
        "ENC_EV pin=%d label=%s level=%u count=%lu t=%lu",
        "BBS_MENU_STEP dir=%c page=%s index=%u pos=%ld cw=%lu ccw=%lu t=%lu",
        "BBS_MENU_SELECT buttons=%lu page=%s index=%u kind=short held_ms=%lu t=%lu",
        "BBS_MENU_SELECT buttons=%lu page=%s index=%u kind=long held_ms=%lu t=%lu",
        "AB_SUPPRESS raw=%u levels=C%uD%uS%u suppressed=%lu t=%lu",
        "AB_INVALID prev=%u curr=%u invalid=%lu t=%lu",
        "ENC_FILTER reason=%s prev=%u curr=%u levels=C%uD%uS%u",
        "\"ab_debounce\"",
        "\"ab_quiet\"",
        "\"step_lockout\"",
        "\"detent_partial\"",
        "\"invalid\"",
        "\"sw_guard\"",
        "BBS_MENU_HB page=%s index=%u pos=%ld levels=C%uD%uS%u steps=%lu/%lu",
        "ab_hold=%lu ab_quiet=%lu stable_ab=%lu detent=%lu detent_step=%lu partial=%lu",
        "step_lockout=%lu invalid=%lu suppressed=%lu",
        "raw_burst=%lu gap_ms=%lu",
        "BBS_MENU_AUTO_CYCLE page=%s index=%u interval_ms=%u t=%lu",
        "irq_drop=%lu",
        "queue_drop=%lu",
        "raw_levels=C%uD%uS%u raw_ab=%u candidate=C%uD%u",
        "isr=C%luD%luS%lu queue_rx=%lu poll=%lu",
        "BBS_GLYPH_BANK name=%s index=%u slots=%u rows=%u",
        ".name = \"core_status\"",
        ".name = \"horizontal_bar\"",
        ".name = \"vertical_chart\"",
        ".name = \"big_digits\"",
        ".name = \"gauge\"",
        ".name = \"art_panel\"",
        "FR_BBS_ART_GLYPH_BANK_INDEX 6U",
        "fr_bbs_art_panel_slots",
        "ART Pixel Gallery",
        "ART",
        "fr_lcd_load_glyph_bank",
        "BBS_CURSOR row=%u col=%u ddram=0x%02x focus=%s mode=%s",
        "BBS_LCD_RENDER page=%s index=%u row0=\\\"%s\\\" row1=\\\"%s\\\"",
        "rows=%u seq=%lu dur_ms=%lu reason=%s",
        "dirty_rows=0x%02x dirty_cells=%u",
        "fr_menu_input_task",
        "fr_lcd_render_cache_t",
        "render_cache.valid",
        "runtime.lcd_dirty",
        "#include \"driver/pulse_cnt.h\"",
        "pcnt_new_unit",
        "pcnt_unit_set_glitch_filter",
        "pcnt_new_channel",
        "pcnt_channel_set_edge_action",
        "pcnt_channel_set_level_action",
        "pcnt_unit_enable",
        "pcnt_unit_clear_count",
        "pcnt_unit_start",
        "pcnt_unit_get_count",
        "fr_encoder_pcnt_accumulate_steps",
        "fr_menu_process_pcnt",
        "fr_menu_resync_pcnt",
        "FR_ENCODER_DETENT_AB",
        "raw_ab_transition_count",
        "raw_sw_transition_count",
        "poll_count",
        "queue_receive_count",
        "signal_change_count",
        "cw_step_count",
        "ccw_step_count",
        "pcnt_last_count",
        "pcnt_last_delta",
        "pcnt_residual",
        "pcnt_step_count",
        "pcnt_capped_poll_count",
        "pcnt_direction_flip_count",
        "pcnt_guard_reset_count",
        "pcnt_suppressed_delta_count",
        "pcnt_recenter_count",
        "ab_debounce_hold_count",
        "ab_quiet_hold_count",
        "accepted_stable_ab_transition_count",
        "detent_return_count",
        "detent_step_count",
        "detent_partial_count",
        "step_lockout_count",
        "raw_ab_burst_count",
        "last_raw_ab_gap_ms",
        "last_ab_held_ms",
        "last_ab_quiet_ms",
        "invalid_transition_count",
        "suppressed_transition_count",
        "switch_guard_until_ms",
        "candidate_changed_ms_a",
        "candidate_changed_ms_b",
        "last_step_ms",
        "last_heartbeat_ms",
        "last_level_heartbeat_ms",
        "{FR_ENCODER_CLK_GPIO, \"CLK\", true}",
        "{FR_ENCODER_DT_GPIO, \"DT\", true}",
        "{FR_ENCODER_SW_GPIO, \"SW\", true}",
        "fr_gpio_sweep_pins[index].enable_pullup",
        "fr_menu_sample_ab_pair",
        "fr_menu_ab_a",
        "fr_menu_ab_b",
        "fr_menu_raw_ab",
        "fr_menu_process_levels",
        "fr_menu_handle_switch_stable",
        "fr_menu_handle_long_press",
        "fr_menu_sample_inputs",
        "fr_diag_short_display_count",
        "fr_diag_short_position_magnitude",
        "fr_bbs_page_name",
        "BBS FIELD STATUS",
        "fr_menu_level_char",
        "MSG NEW:01 IN:12",
        "PEERS ACTIVE 2/3",
        "QUEUE P:2 F:0",
        "FILES Q:1 D:3",
        "MESH runtime",
        "BRIDGE LOCAL CLOSED",
        "DIAG ERRORS:0",
        "Flash:LOCK Ser:LOCK",
        "BARS LINK QUEUE",
        "VERT CHART HISTORY",
        "BIG DIGITS 12:34",
        "GAUGE STATUS",
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
