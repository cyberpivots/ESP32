#include "four_relay_core.h"

#include "driver/gpio.h"
#include "driver/i2c_master.h"
#include "driver/uart.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "soc/gpio_num.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define FR_DIAG_XBEE_BRIDGE_CLOSED 1

#if !FR_DIAG_XBEE_BRIDGE_CLOSED
#define FR_BRIDGE_HOST_UART UART_NUM_0
#define FR_BRIDGE_XBEE_UART UART_NUM_2
#define FR_BRIDGE_HOST_BAUD 115200
#define FR_BRIDGE_XBEE_BAUD 9600
#define FR_BRIDGE_XBEE_TX_GPIO GPIO_NUM_17
#define FR_BRIDGE_XBEE_RX_GPIO GPIO_NUM_16
#define FR_BRIDGE_UART_BUFFER_BYTES 64
#define FR_BRIDGE_UART_RING_BYTES 1024
#endif

#define FR_LCD_I2C_PORT 0
#define FR_LCD_I2C_SDA_GPIO GPIO_NUM_21
#define FR_LCD_I2C_SCL_GPIO GPIO_NUM_22
#define FR_LCD_I2C_SPEED_HZ 100000
#define FR_LCD_I2C_TIMEOUT_MS 50
#define FR_LCD_TASK_STACK_BYTES 4096
#define FR_LCD_TASK_PRIORITY tskIDLE_PRIORITY
#define FR_LCD_COLUMNS 20
#define FR_LCD_ROWS 4
#define FR_MENU_PAGE_COUNT 13
#define FR_MENU_POLL_MS 10
#define FR_MENU_RENDER_POLL_MS 20
#define FR_MENU_IDLE_REFRESH_MS 60000
#define FR_MENU_AUTO_DEMO_MS 7000
#define FR_MENU_ANIMATION_MS 2000
#define FR_MENU_ACK_MS 1500
#define FR_DIAG_FIRMWARE_ID "PF0530L"
#define FR_ENCODER_AB_STABLE_SAMPLES 3
#define FR_ENCODER_SW_GUARD_MS 150
#define FR_MENU_HEARTBEAT_MS 2000
#define FR_MENU_LAST_EVENT_BYTES 20
#define FR_LCD_DIAG_HEARTBEAT_MS 2000
#define FR_MENU_INPUT_TASK_STACK_BYTES 4096
#define FR_MENU_INPUT_TASK_PRIORITY (tskIDLE_PRIORITY + 1)
#define FR_MENU_EDIT_VALUE_MAX 100
#define FR_GLYPH_BANK_COUNT 5
#define FR_GLYPH_SLOTS 8
#define FR_GLYPH_ROWS 8
#define FR_GLYPH_BANK_SWAP_MIN_MS 250

#define FR_LCD_PCF_RS 0x01
#define FR_LCD_PCF_RW 0x02
#define FR_LCD_PCF_ENABLE 0x04
#define FR_LCD_PCF_BACKLIGHT 0x08

#define FR_ENCODER_CLK_GPIO GPIO_NUM_13
#define FR_ENCODER_DT_GPIO GPIO_NUM_14
#define FR_ENCODER_SW_GPIO GPIO_NUM_32
#define FR_ENCODER_TRANSITIONS_PER_STEP 4
#define FR_ENCODER_SW_DEBOUNCE_MS 30
#define FR_ENCODER_LONG_PRESS_MS 800
#define FR_GPIO_SWEEP_COUNT 3
#define FR_ENCODER_EVENT_QUEUE_DEPTH 64
#define FR_ENCODER_IRQ_DRAIN_LIMIT 32

typedef struct {
    i2c_master_bus_handle_t bus;
    i2c_master_dev_handle_t device;
    uint8_t address;
} fr_lcd_context_t;

typedef struct {
    bool valid;
    uint8_t cells[FR_LCD_ROWS][FR_LCD_COLUMNS];
    bool glyph_valid;
    uint8_t glyph_bank_index;
    uint32_t last_glyph_swap_ms;
} fr_lcd_render_cache_t;

typedef struct {
    const char *status;
    const char *stage;
    uint8_t address;
    uint8_t detected_count;
} fr_lcd_diag_state_t;

typedef struct {
    gpio_num_t pin;
    const char *label;
    bool enable_pullup;
} fr_gpio_sweep_pin_t;

static const fr_gpio_sweep_pin_t fr_gpio_sweep_pins[FR_GPIO_SWEEP_COUNT] = {
    {FR_ENCODER_CLK_GPIO, "CLK", true},
    {FR_ENCODER_DT_GPIO, "DT", true},
    {FR_ENCODER_SW_GPIO, "SW", true},
};

static uint32_t fr_menu_now_ms(void);
static const char *fr_bbs_page_name(uint8_t page);

static TickType_t fr_delay_ticks_at_least_one(uint32_t delay_ms)
{
    TickType_t ticks = pdMS_TO_TICKS(delay_ms);
    return ticks == 0 ? 1 : ticks;
}

#if !FR_DIAG_XBEE_BRIDGE_CLOSED
static volatile uint32_t fr_bridge_host_to_xbee_bytes;
static volatile uint32_t fr_bridge_host_to_xbee_chunks;
static volatile uint32_t fr_bridge_xbee_to_host_bytes;
static volatile uint32_t fr_bridge_xbee_to_host_chunks;
#endif

typedef enum {
    FR_MENU_ACK_NONE = 0,
    FR_MENU_ACK_SELECT,
} fr_menu_ack_t;

typedef enum {
    FR_MENU_MODE_PAGE_BROWSE = 0,
    FR_MENU_MODE_ROW_BROWSE,
    FR_MENU_MODE_DETAIL,
    FR_MENU_MODE_EDIT_LAB,
} fr_menu_mode_t;

typedef struct {
    uint8_t page;
    fr_menu_mode_t mode;
    uint8_t selected_row;
    uint8_t edit_value;
    uint8_t cursor_row;
    uint8_t cursor_col;
    uint8_t spinner_frame;
    int32_t position;
    int8_t transition_accumulator;
    uint8_t previous_ab;
    uint8_t raw_a;
    uint8_t raw_b;
    uint8_t raw_sw;
    uint8_t stable_a;
    uint8_t stable_b;
    uint8_t stable_sw;
    uint8_t candidate_a;
    uint8_t candidate_b;
    uint8_t stable_samples_a;
    uint8_t stable_samples_b;
    uint32_t raw_ab_transition_count;
    uint32_t raw_sw_transition_count;
    uint32_t signal_change_count[FR_GPIO_SWEEP_COUNT];
    uint32_t cw_step_count;
    uint32_t ccw_step_count;
    uint32_t invalid_transition_count;
    uint32_t suppressed_transition_count;
    bool switch_stable_pressed;
    bool long_press_handled;
    bool auto_demo_enabled;
    uint32_t switch_changed_ms;
    uint32_t switch_pressed_ms;
    uint32_t switch_guard_until_ms;
    uint32_t last_auto_demo_ms;
    uint32_t last_animation_ms;
    uint32_t button_press_count;
    fr_menu_ack_t ack;
    uint32_t ack_until_ms;
    uint32_t last_heartbeat_ms;
    bool display_dirty;
    char last_event[FR_MENU_LAST_EVENT_BYTES];
} fr_menu_state_t;

typedef struct {
    uint8_t cells[FR_LCD_ROWS][FR_LCD_COLUMNS];
    char log_lines[FR_LCD_ROWS][FR_LCD_COLUMNS + 1];
    uint8_t glyph_bank_index;
    uint8_t cursor_row;
    uint8_t cursor_col;
    uint8_t cursor_ddram;
    const char *focus;
} fr_lcd_frame_t;

typedef struct {
    const char *name;
    uint8_t rows[FR_GLYPH_SLOTS][FR_GLYPH_ROWS];
} fr_lcd_glyph_bank_t;

typedef struct {
    SemaphoreHandle_t lock;
    fr_menu_state_t menu;
    bool lcd_dirty;
    bool stop;
    uint32_t render_request_count;
} fr_menu_runtime_t;

typedef struct {
    uint8_t index;
    uint8_t level;
    TickType_t tick;
} fr_encoder_irq_event_t;

static QueueHandle_t fr_encoder_event_queue;
static volatile uint32_t fr_encoder_irq_drop_count;

static void fr_bridge_init_safe_defaults(void)
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

#if !FR_DIAG_XBEE_BRIDGE_CLOSED
static void fr_bridge_configure_uart(
    uart_port_t port,
    int baud_rate,
    int tx_pin,
    int rx_pin
)
{
    const uart_config_t config = {
        .baud_rate = baud_rate,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .rx_flow_ctrl_thresh = 0,
        .source_clk = UART_SCLK_DEFAULT,
    };

    ESP_ERROR_CHECK(uart_driver_install(
        port,
        FR_BRIDGE_UART_RING_BYTES,
        FR_BRIDGE_UART_RING_BYTES,
        0,
        NULL,
        0
    ));
    ESP_ERROR_CHECK(uart_param_config(port, &config));
    ESP_ERROR_CHECK(uart_set_pin(
        port,
        tx_pin,
        rx_pin,
        UART_PIN_NO_CHANGE,
        UART_PIN_NO_CHANGE
    ));
}

static void fr_bridge_write_all(uart_port_t port, const uint8_t *buffer, size_t length)
{
    size_t offset = 0;
    while (offset < length) {
        int written = uart_write_bytes(
            port,
            (const char *)&buffer[offset],
            length - offset
        );
        if (written <= 0) {
            return;
        }
        offset += (size_t)written;
    }
}

static bool fr_bridge_copy_available(
    uart_port_t source,
    uart_port_t destination,
    TickType_t wait_ticks,
    uint8_t *buffer,
    size_t capacity,
    volatile uint32_t *byte_counter,
    volatile uint32_t *chunk_counter
)
{
    int bytes_read = uart_read_bytes(source, buffer, capacity, wait_ticks);
    if (bytes_read <= 0) {
        return false;
    }

    fr_bridge_write_all(destination, buffer, (size_t)bytes_read);
    *byte_counter += (uint32_t)bytes_read;
    *chunk_counter += 1U;
    return true;
}
#endif

static uint32_t fr_menu_now_ms(void)
{
    return (uint32_t)(xTaskGetTickCount() * portTICK_PERIOD_MS);
}

static uint8_t fr_pin_finder_read_level(size_t index)
{
    return gpio_get_level(fr_gpio_sweep_pins[index].pin) ? 1U : 0U;
}

static void fr_encoder_isr_handler(void *arg)
{
    size_t index = (size_t)(uintptr_t)arg;
    fr_encoder_irq_event_t event = {
        .index = (uint8_t)index,
        .level = fr_pin_finder_read_level(index),
        .tick = xTaskGetTickCountFromISR(),
    };
    BaseType_t higher_priority_task_woken = pdFALSE;

    if (fr_encoder_event_queue == NULL ||
        xQueueSendFromISR(
            fr_encoder_event_queue,
            &event,
            &higher_priority_task_woken
        ) != pdTRUE) {
        fr_encoder_irq_drop_count += 1U;
        return;
    }
    if (higher_priority_task_woken == pdTRUE) {
        portYIELD_FROM_ISR();
    }
}

static bool fr_encoder_configure_input(gpio_num_t pin, bool enable_pullup)
{
    const gpio_config_t config = {
        .pin_bit_mask = 1ULL << pin,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = enable_pullup ? GPIO_PULLUP_ENABLE : GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_ANYEDGE,
    };
    return gpio_config(&config) == ESP_OK;
}

static bool fr_encoder_init(void)
{
    if (fr_encoder_event_queue == NULL) {
        fr_encoder_event_queue = xQueueCreate(
            FR_ENCODER_EVENT_QUEUE_DEPTH,
            sizeof(fr_encoder_irq_event_t)
        );
        if (fr_encoder_event_queue == NULL) {
            return false;
        }
    } else {
        xQueueReset(fr_encoder_event_queue);
    }
    fr_encoder_irq_drop_count = 0;

    for (size_t index = 0; index < FR_GPIO_SWEEP_COUNT; ++index) {
        if (!fr_encoder_configure_input(
                fr_gpio_sweep_pins[index].pin,
                fr_gpio_sweep_pins[index].enable_pullup
            )) {
            return false;
        }
    }

    esp_err_t isr_service_result = gpio_install_isr_service(0);
    if (isr_service_result != ESP_OK &&
        isr_service_result != ESP_ERR_INVALID_STATE) {
        return false;
    }
    for (size_t index = 0; index < FR_GPIO_SWEEP_COUNT; ++index) {
        if (gpio_isr_handler_add(
                fr_gpio_sweep_pins[index].pin,
                fr_encoder_isr_handler,
                (void *)(uintptr_t)index
            ) != ESP_OK) {
            return false;
        }
    }

    return true;
}

static uint8_t fr_menu_stable_ab(const fr_menu_state_t *menu)
{
    return (uint8_t)((menu->stable_a << 1) | menu->stable_b);
}

static uint8_t fr_menu_raw_ab(const fr_menu_state_t *menu)
{
    return (uint8_t)((menu->raw_a << 1) | menu->raw_b);
}

static const char *fr_menu_mode_name(fr_menu_mode_t mode)
{
    switch (mode) {
    case FR_MENU_MODE_PAGE_BROWSE:
        return "page_browse";
    case FR_MENU_MODE_ROW_BROWSE:
        return "row_browse";
    case FR_MENU_MODE_DETAIL:
        return "detail";
    case FR_MENU_MODE_EDIT_LAB:
        return "edit_lab";
    default:
        return "page_browse";
    }
}

static void fr_menu_set_last_event(fr_menu_state_t *menu, const char *event)
{
    snprintf(menu->last_event, sizeof(menu->last_event), "%s", event);
}

static void fr_menu_mark_display_dirty(fr_menu_state_t *menu)
{
    menu->display_dirty = true;
}

static void fr_menu_print_enc_event(
    fr_menu_state_t *menu,
    uint32_t now_ms,
    size_t index,
    uint8_t level
)
{
    menu->signal_change_count[index] += 1U;
    const fr_gpio_sweep_pin_t *pin = &fr_gpio_sweep_pins[index];
    printf(
        "ENC_EV pin=%d label=%s level=%u count=%lu t=%lu\r\n",
        (int)pin->pin,
        pin->label,
        (unsigned int)level,
        (unsigned long)menu->signal_change_count[index],
        (unsigned long)now_ms
    );
}

static void fr_menu_print_raw_event(
    const fr_menu_state_t *menu,
    const char *kind,
    uint32_t now_ms
)
{
    printf(
        "ENC_RAW kind=%s levels=C%uD%uS%u raw_ab=%lu raw_sw=%lu t=%lu\r\n",
        kind,
        (unsigned int)menu->raw_a,
        (unsigned int)menu->raw_b,
        (unsigned int)menu->raw_sw,
        (unsigned long)menu->raw_ab_transition_count,
        (unsigned long)menu->raw_sw_transition_count,
        (unsigned long)now_ms
    );
}

static void fr_menu_print_heartbeat(const fr_menu_state_t *menu, uint32_t now_ms)
{
    printf(
        "BBS_MENU_HB page=%s index=%u pos=%ld levels=C%uD%uS%u steps=%lu/%lu "
        "buttons=%lu invalid=%lu suppressed=%lu irq_drop=%lu t=%lu "
        "mode=%s row=%u value=%u auto_demo=%u\r\n",
        fr_bbs_page_name(menu->page),
        (unsigned int)menu->page,
        (long)menu->position,
        (unsigned int)menu->stable_a,
        (unsigned int)menu->stable_b,
        (unsigned int)menu->stable_sw,
        (unsigned long)menu->cw_step_count,
        (unsigned long)menu->ccw_step_count,
        (unsigned long)menu->button_press_count,
        (unsigned long)menu->invalid_transition_count,
        (unsigned long)menu->suppressed_transition_count,
        (unsigned long)fr_encoder_irq_drop_count,
        (unsigned long)now_ms,
        fr_menu_mode_name(menu->mode),
        (unsigned int)menu->selected_row,
        (unsigned int)menu->edit_value,
        menu->auto_demo_enabled ? 1U : 0U
    );
}

static void fr_menu_step(fr_menu_state_t *menu, int8_t direction, uint32_t now_ms)
{
    menu->auto_demo_enabled = false;
    if (direction > 0) {
        menu->position += 1;
        menu->cw_step_count += 1U;
    } else {
        menu->position -= 1;
        menu->ccw_step_count += 1U;
    }

    switch (menu->mode) {
    case FR_MENU_MODE_ROW_BROWSE:
    case FR_MENU_MODE_DETAIL:
        menu->selected_row = (uint8_t)(
            (menu->selected_row + FR_LCD_ROWS + (direction > 0 ? 1 : -1)) %
            FR_LCD_ROWS
        );
        fr_menu_set_last_event(menu, direction > 0 ? "ROW NEXT" : "ROW PREV");
        break;
    case FR_MENU_MODE_EDIT_LAB:
        if (direction > 0) {
            menu->edit_value = (uint8_t)(
                menu->edit_value >= FR_MENU_EDIT_VALUE_MAX ? 0U : menu->edit_value + 5U
            );
        } else {
            menu->edit_value = (uint8_t)(
                menu->edit_value < 5U ? FR_MENU_EDIT_VALUE_MAX : menu->edit_value - 5U
            );
        }
        fr_menu_set_last_event(menu, "EDIT VALUE");
        break;
    case FR_MENU_MODE_PAGE_BROWSE:
    default:
        if (direction > 0) {
            menu->page = (uint8_t)((menu->page + 1U) % FR_MENU_PAGE_COUNT);
            fr_menu_set_last_event(menu, "STEP CW");
        } else {
            menu->page = (uint8_t)(
                (menu->page + FR_MENU_PAGE_COUNT - 1U) % FR_MENU_PAGE_COUNT
            );
            fr_menu_set_last_event(menu, "STEP CCW");
        }
        menu->selected_row = 0;
        break;
    }
    fr_menu_mark_display_dirty(menu);
    printf(
        "BBS_MENU_STEP dir=%c page=%s index=%u pos=%ld cw=%lu ccw=%lu t=%lu "
        "mode=%s row=%u value=%u\r\n",
        direction > 0 ? '+' : '-',
        fr_bbs_page_name(menu->page),
        (unsigned int)menu->page,
        (long)menu->position,
        (unsigned long)menu->cw_step_count,
        (unsigned long)menu->ccw_step_count,
        (unsigned long)now_ms,
        fr_menu_mode_name(menu->mode),
        (unsigned int)menu->selected_row,
        (unsigned int)menu->edit_value
    );
}

static void fr_menu_handle_rotation(fr_menu_state_t *menu, uint32_t now_ms)
{
    static const int8_t transition_table[16] = {
         0, -1,  1,  0,
         1,  0,  0, -1,
        -1,  0,  0,  1,
         0,  1, -1,  0,
    };

    uint8_t current_ab = fr_menu_stable_ab(menu);
    uint8_t transition = (uint8_t)((menu->previous_ab << 2) | current_ab);
    int8_t delta = transition_table[transition & 0x0fU];

    if (now_ms < menu->switch_guard_until_ms) {
        menu->previous_ab = current_ab;
        menu->transition_accumulator = 0;
        return;
    }

    if (delta == 0 && current_ab != menu->previous_ab) {
        menu->invalid_transition_count += 1U;
        menu->transition_accumulator = 0;
        menu->previous_ab = current_ab;
        fr_menu_set_last_event(menu, "AB INVALID");
        fr_menu_mark_display_dirty(menu);
        printf(
            "AB_INVALID prev=%u curr=%u invalid=%lu t=%lu\r\n",
            (unsigned int)(transition >> 2),
            (unsigned int)current_ab,
            (unsigned long)menu->invalid_transition_count,
            (unsigned long)now_ms
        );
        return;
    }
    menu->previous_ab = current_ab;
    if (delta == 0) {
        return;
    }

    menu->transition_accumulator += delta;
    if (menu->transition_accumulator >= FR_ENCODER_TRANSITIONS_PER_STEP) {
        menu->transition_accumulator = 0;
        fr_menu_step(menu, 1, now_ms);
    } else if (menu->transition_accumulator <= -FR_ENCODER_TRANSITIONS_PER_STEP) {
        menu->transition_accumulator = 0;
        fr_menu_step(menu, -1, now_ms);
    }
}

static bool fr_menu_sample_ab_channel(
    fr_menu_state_t *menu,
    size_t index,
    uint8_t current_level,
    uint8_t *candidate_level,
    uint8_t *stable_samples,
    uint8_t *stable_level,
    uint32_t now_ms
)
{
    if (current_level == *candidate_level) {
        if (*stable_samples < UINT8_MAX) {
            *stable_samples += 1U;
        }
    } else {
        *candidate_level = current_level;
        *stable_samples = 1U;
    }

    if (*stable_samples < FR_ENCODER_AB_STABLE_SAMPLES ||
        *candidate_level == *stable_level) {
        return false;
    }

    *stable_level = *candidate_level;
    fr_menu_print_enc_event(menu, now_ms, index, *stable_level);
    return true;
}

static void fr_menu_handle_switch_stable(fr_menu_state_t *menu, uint32_t now_ms)
{
    bool pressed = menu->stable_sw == 0U;
    menu->auto_demo_enabled = false;
    menu->switch_guard_until_ms = now_ms + FR_ENCODER_SW_GUARD_MS;
    menu->switch_stable_pressed = pressed;
    menu->transition_accumulator = 0;
    menu->previous_ab = fr_menu_stable_ab(menu);

    if (pressed) {
        menu->switch_pressed_ms = now_ms;
        menu->long_press_handled = false;
        fr_menu_set_last_event(menu, "SW DOWN");
        fr_menu_mark_display_dirty(menu);
        return;
    }

    if (!menu->long_press_handled) {
        switch (menu->mode) {
        case FR_MENU_MODE_PAGE_BROWSE:
            menu->mode = FR_MENU_MODE_ROW_BROWSE;
            menu->selected_row = 0;
            fr_menu_set_last_event(menu, "ROW BROWSE");
            break;
        case FR_MENU_MODE_ROW_BROWSE:
            menu->mode = FR_MENU_MODE_DETAIL;
            fr_menu_set_last_event(menu, "DETAIL");
            break;
        case FR_MENU_MODE_DETAIL:
            menu->mode = FR_MENU_MODE_EDIT_LAB;
            fr_menu_set_last_event(menu, "EDIT LAB");
            break;
        case FR_MENU_MODE_EDIT_LAB:
            menu->mode = FR_MENU_MODE_DETAIL;
            fr_menu_set_last_event(menu, "EDIT SAVE");
            break;
        default:
            menu->mode = FR_MENU_MODE_PAGE_BROWSE;
            fr_menu_set_last_event(menu, "PAGE BROWSE");
            break;
        }
        menu->button_press_count += 1U;
        menu->ack = FR_MENU_ACK_SELECT;
        menu->ack_until_ms = now_ms + FR_MENU_ACK_MS;
        fr_menu_mark_display_dirty(menu);
        printf(
            "BBS_MENU_SELECT buttons=%lu page=%s index=%u kind=short t=%lu "
            "mode=%s row=%u value=%u\r\n",
            (unsigned long)menu->button_press_count,
            fr_bbs_page_name(menu->page),
            (unsigned int)menu->page,
            (unsigned long)now_ms,
            fr_menu_mode_name(menu->mode),
            (unsigned int)menu->selected_row,
            (unsigned int)menu->edit_value
        );
    }
}

static void fr_menu_handle_long_press(fr_menu_state_t *menu, uint32_t now_ms)
{
    if (!menu->switch_stable_pressed || menu->long_press_handled) {
        return;
    }
    if ((now_ms - menu->switch_pressed_ms) < FR_ENCODER_LONG_PRESS_MS) {
        return;
    }
    menu->auto_demo_enabled = false;
    if (menu->mode == FR_MENU_MODE_EDIT_LAB) {
        menu->mode = FR_MENU_MODE_DETAIL;
        fr_menu_set_last_event(menu, "BACK DETAIL");
    } else if (menu->mode == FR_MENU_MODE_DETAIL) {
        menu->mode = FR_MENU_MODE_ROW_BROWSE;
        fr_menu_set_last_event(menu, "BACK ROW");
    } else if (menu->mode == FR_MENU_MODE_ROW_BROWSE) {
        menu->mode = FR_MENU_MODE_PAGE_BROWSE;
        fr_menu_set_last_event(menu, "BACK PAGE");
    } else {
        menu->page = 0;
        menu->selected_row = 0;
        fr_menu_set_last_event(menu, "LONG HOME");
    }
    menu->button_press_count += 1U;
    menu->ack = FR_MENU_ACK_SELECT;
    menu->ack_until_ms = now_ms + FR_MENU_ACK_MS;
    menu->long_press_handled = true;
    fr_menu_mark_display_dirty(menu);
    printf(
        "BBS_MENU_SELECT buttons=%lu page=%s index=%u kind=long t=%lu "
        "mode=%s row=%u value=%u\r\n",
        (unsigned long)menu->button_press_count,
        fr_bbs_page_name(menu->page),
        (unsigned int)menu->page,
        (unsigned long)now_ms,
        fr_menu_mode_name(menu->mode),
        (unsigned int)menu->selected_row,
        (unsigned int)menu->edit_value
    );
}

static void fr_menu_process_levels(
    fr_menu_state_t *menu,
    uint8_t current_a,
    uint8_t current_b,
    uint8_t current_sw,
    uint32_t now_ms
)
{
    uint8_t previous_raw_ab = fr_menu_raw_ab(menu);
    uint8_t previous_raw_sw = menu->raw_sw;
    uint8_t current_raw_ab = (uint8_t)((current_a << 1) | current_b);
    bool raw_ab_changed = current_raw_ab != previous_raw_ab;
    bool raw_sw_changed = current_sw != previous_raw_sw;

    if (raw_ab_changed) {
        menu->raw_ab_transition_count += 1U;
        if (now_ms < menu->switch_guard_until_ms) {
            menu->suppressed_transition_count += 1U;
            fr_menu_set_last_event(menu, "AB SUPPRESS");
            printf(
                "AB_SUPPRESS raw=%u levels=C%uD%uS%u suppressed=%lu t=%lu\r\n",
                (unsigned int)current_raw_ab,
                (unsigned int)current_a,
                (unsigned int)current_b,
                (unsigned int)current_sw,
                (unsigned long)menu->suppressed_transition_count,
                (unsigned long)now_ms
            );
        }
    }
    if (raw_sw_changed) {
        menu->raw_sw_transition_count += 1U;
        menu->switch_changed_ms = now_ms;
    }

    menu->raw_a = current_a;
    menu->raw_b = current_b;
    menu->raw_sw = current_sw;
    if (raw_ab_changed) {
        fr_menu_print_raw_event(menu, "ab", now_ms);
        fr_menu_handle_rotation(menu, now_ms);
    }
    if (raw_sw_changed) {
        fr_menu_print_raw_event(menu, "sw", now_ms);
    }

    bool ab_changed = false;
    ab_changed |= fr_menu_sample_ab_channel(
        menu,
        0,
        current_a,
        &menu->candidate_a,
        &menu->stable_samples_a,
        &menu->stable_a,
        now_ms
    );
    ab_changed |= fr_menu_sample_ab_channel(
        menu,
        1,
        current_b,
        &menu->candidate_b,
        &menu->stable_samples_b,
        &menu->stable_b,
        now_ms
    );
    (void)ab_changed;

    if (current_sw != menu->stable_sw &&
        (now_ms - menu->switch_changed_ms) >= FR_ENCODER_SW_DEBOUNCE_MS) {
        menu->stable_sw = current_sw;
        fr_menu_print_enc_event(menu, now_ms, 2, menu->stable_sw);
        fr_menu_handle_switch_stable(menu, now_ms);
    }
}

static void fr_menu_sample_inputs(fr_menu_state_t *menu, uint32_t now_ms)
{
    fr_encoder_irq_event_t event;
    uint32_t drained_count = 0;

    while (fr_encoder_event_queue != NULL &&
           drained_count < FR_ENCODER_IRQ_DRAIN_LIMIT &&
           xQueueReceive(fr_encoder_event_queue, &event, 0) == pdTRUE) {
        uint8_t event_a = menu->raw_a;
        uint8_t event_b = menu->raw_b;
        uint8_t event_sw = menu->raw_sw;
        uint32_t event_ms = (uint32_t)(event.tick * portTICK_PERIOD_MS);

        if (event.index == 0U) {
            event_a = event.level;
        } else if (event.index == 1U) {
            event_b = event.level;
        } else if (event.index == 2U) {
            event_sw = event.level;
        }
        fr_menu_process_levels(menu, event_a, event_b, event_sw, event_ms);
        drained_count += 1U;
    }

    fr_menu_process_levels(
        menu,
        fr_pin_finder_read_level(0),
        fr_pin_finder_read_level(1),
        fr_pin_finder_read_level(2),
        now_ms
    );
}

static bool fr_menu_poll(fr_menu_state_t *menu)
{
    uint32_t now_ms = fr_menu_now_ms();
    menu->display_dirty = false;
    fr_menu_sample_inputs(menu, now_ms);
    fr_menu_handle_long_press(menu, now_ms);
    if (menu->auto_demo_enabled &&
        (now_ms - menu->last_auto_demo_ms) >= FR_MENU_AUTO_DEMO_MS) {
        menu->page = (uint8_t)((menu->page + 1U) % FR_MENU_PAGE_COUNT);
        menu->mode = FR_MENU_MODE_PAGE_BROWSE;
        menu->selected_row = 0;
        menu->position += 1;
        menu->last_auto_demo_ms = now_ms;
        fr_menu_set_last_event(menu, "AUTO DEMO");
        fr_menu_mark_display_dirty(menu);
        printf(
            "BBS_MENU_AUTO page=%s index=%u interval_ms=%u t=%lu\r\n",
            fr_bbs_page_name(menu->page),
            (unsigned int)menu->page,
            (unsigned int)FR_MENU_AUTO_DEMO_MS,
            (unsigned long)now_ms
        );
    }
    if ((now_ms - menu->last_animation_ms) >= FR_MENU_ANIMATION_MS) {
        menu->spinner_frame = (uint8_t)((menu->spinner_frame + 1U) % 4U);
        menu->last_animation_ms = now_ms;
        fr_menu_mark_display_dirty(menu);
    }
    if (menu->ack != FR_MENU_ACK_NONE && now_ms >= menu->ack_until_ms) {
        menu->ack = FR_MENU_ACK_NONE;
        fr_menu_set_last_event(menu, "ACK CLEAR");
        fr_menu_mark_display_dirty(menu);
    }
    if ((now_ms - menu->last_heartbeat_ms) >= FR_MENU_HEARTBEAT_MS) {
        menu->last_heartbeat_ms = now_ms;
        fr_menu_print_heartbeat(menu, now_ms);
    }
    return menu->display_dirty;
}

static void fr_lcd_cleanup(fr_lcd_context_t *lcd)
{
    if (lcd->device != NULL) {
        (void)i2c_master_bus_rm_device(lcd->device);
        lcd->device = NULL;
    }
    if (lcd->bus != NULL) {
        (void)i2c_del_master_bus(lcd->bus);
        lcd->bus = NULL;
    }
}

static void fr_lcd_diag_set(
    fr_lcd_diag_state_t *diag,
    const char *status,
    const char *stage
)
{
    diag->status = status;
    diag->stage = stage;
}

static void fr_lcd_diag_print_heartbeat(
    const fr_lcd_diag_state_t *diag,
    uint32_t count
)
{
    printf(
        "LCD_DIAG_HB status=%s count=%lu addr=0x%02x stage=%s devices=%u\r\n",
        diag->status,
        (unsigned long)count,
        diag->address,
        diag->stage,
        diag->detected_count
    );
}

static bool fr_lcd_probe_range(
    i2c_master_bus_handle_t bus,
    uint8_t first_address,
    uint8_t last_address,
    uint8_t *detected_address,
    uint8_t *detected_count
)
{
    for (uint8_t address = first_address; address <= last_address; ++address) {
        esp_err_t result = i2c_master_probe(bus, address, FR_LCD_I2C_TIMEOUT_MS);
        if (result == ESP_OK) {
            *detected_address = address;
            *detected_count += 1U;
            continue;
        }
        if (result != ESP_ERR_NOT_FOUND) {
            return false;
        }
    }
    return true;
}

static bool fr_lcd_diag_probe_range(
    i2c_master_bus_handle_t bus,
    uint8_t first_address,
    uint8_t last_address,
    uint8_t *detected_address,
    uint8_t *detected_count
)
{
    for (uint8_t address = first_address; address <= last_address; ++address) {
        esp_err_t result = i2c_master_probe(bus, address, FR_LCD_I2C_TIMEOUT_MS);
        if (result == ESP_OK) {
            *detected_address = address;
            *detected_count += 1U;
            printf(
                "LCD_PROBE addr=0x%02x result=ack err=%s\r\n",
                address,
                esp_err_to_name(result)
            );
            continue;
        }
        if (result == ESP_ERR_NOT_FOUND) {
            printf(
                "LCD_PROBE addr=0x%02x result=nack err=%s\r\n",
                address,
                esp_err_to_name(result)
            );
            continue;
        }
        printf(
            "LCD_PROBE addr=0x%02x result=err err=%s\r\n",
            address,
            esp_err_to_name(result)
        );
        return false;
    }
    return true;
}

static bool fr_lcd_diag_init_i2c(fr_lcd_context_t *lcd, fr_lcd_diag_state_t *diag)
{
    uint8_t detected_address = 0;
    uint8_t detected_count = 0;
    const i2c_master_bus_config_t bus_config = {
        .i2c_port = FR_LCD_I2C_PORT,
        .sda_io_num = FR_LCD_I2C_SDA_GPIO,
        .scl_io_num = FR_LCD_I2C_SCL_GPIO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = false,
    };

    esp_err_t result = i2c_new_master_bus(&bus_config, &lcd->bus);
    if (result != ESP_OK) {
        printf("LCD_BUS result=fail err=%s\r\n", esp_err_to_name(result));
        printf("LCD_INIT_FAIL stage=bus detail=%s\r\n", esp_err_to_name(result));
        fr_lcd_diag_set(diag, "fail", "bus");
        return false;
    }
    printf("LCD_BUS result=ok err=%s\r\n", esp_err_to_name(result));

    bool probe_ok =
        fr_lcd_diag_probe_range(lcd->bus, 0x20, 0x27, &detected_address, &detected_count) &&
        fr_lcd_diag_probe_range(lcd->bus, 0x38, 0x3f, &detected_address, &detected_count);
    diag->address = detected_address;
    diag->detected_count = detected_count;
    printf(
        "LCD_PROBE_SUMMARY count=%u selected=0x%02x\r\n",
        detected_count,
        detected_address
    );
    if (!probe_ok) {
        printf("LCD_INIT_FAIL stage=probe detail=scan-error\r\n");
        fr_lcd_diag_set(diag, "fail", "probe");
        fr_lcd_cleanup(lcd);
        return false;
    }
    if (detected_count != 1U) {
        printf("LCD_INIT_FAIL stage=probe detail=count-%u\r\n", detected_count);
        fr_lcd_diag_set(diag, "fail", "probe");
        fr_lcd_cleanup(lcd);
        return false;
    }

    const i2c_device_config_t device_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = detected_address,
        .scl_speed_hz = FR_LCD_I2C_SPEED_HZ,
    };
    result = i2c_master_bus_add_device(lcd->bus, &device_config, &lcd->device);
    if (result != ESP_OK) {
        printf(
            "LCD_DEVICE result=fail addr=0x%02x err=%s\r\n",
            detected_address,
            esp_err_to_name(result)
        );
        printf("LCD_INIT_FAIL stage=device detail=%s\r\n", esp_err_to_name(result));
        fr_lcd_diag_set(diag, "fail", "device");
        fr_lcd_cleanup(lcd);
        return false;
    }

    lcd->address = detected_address;
    diag->address = detected_address;
    printf(
        "LCD_DEVICE result=ok addr=0x%02x err=%s\r\n",
        detected_address,
        esp_err_to_name(result)
    );
    fr_lcd_diag_set(diag, "probe-ok", "device");
    return true;
}

static bool __attribute__((unused)) fr_lcd_init_i2c(fr_lcd_context_t *lcd)
{
    uint8_t detected_address = 0;
    uint8_t detected_count = 0;
    const i2c_master_bus_config_t bus_config = {
        .i2c_port = FR_LCD_I2C_PORT,
        .sda_io_num = FR_LCD_I2C_SDA_GPIO,
        .scl_io_num = FR_LCD_I2C_SCL_GPIO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = false,
    };

    if (i2c_new_master_bus(&bus_config, &lcd->bus) != ESP_OK) {
        return false;
    }

    if (!fr_lcd_probe_range(lcd->bus, 0x20, 0x27, &detected_address, &detected_count) ||
        !fr_lcd_probe_range(lcd->bus, 0x38, 0x3f, &detected_address, &detected_count) ||
        detected_count != 1U) {
        fr_lcd_cleanup(lcd);
        return false;
    }

    const i2c_device_config_t device_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = detected_address,
        .scl_speed_hz = FR_LCD_I2C_SPEED_HZ,
    };
    if (i2c_master_bus_add_device(lcd->bus, &device_config, &lcd->device) != ESP_OK) {
        fr_lcd_cleanup(lcd);
        return false;
    }

    lcd->address = detected_address;
    return true;
}

static bool __attribute__((unused)) fr_lcd_write_pcf(
    fr_lcd_context_t *lcd,
    uint8_t value
)
{
    return i2c_master_transmit(
        lcd->device,
        &value,
        sizeof(value),
        FR_LCD_I2C_TIMEOUT_MS
    ) == ESP_OK;
}

static bool fr_lcd_transmit_pcf(
    fr_lcd_context_t *lcd,
    const uint8_t *values,
    size_t value_count
)
{
    return i2c_master_transmit(
        lcd->device,
        values,
        value_count,
        FR_LCD_I2C_TIMEOUT_MS
    ) == ESP_OK;
}

static uint8_t fr_lcd_nibble_value(uint8_t nibble, bool data_mode)
{
    uint8_t value = (uint8_t)((nibble & 0x0fU) << 4);
    value |= FR_LCD_PCF_BACKLIGHT;
    if (data_mode) {
        value |= FR_LCD_PCF_RS;
    }
    value &= (uint8_t)~FR_LCD_PCF_RW;
    return value;
}

static bool fr_lcd_write_nibble(fr_lcd_context_t *lcd, uint8_t nibble, bool data_mode)
{
    uint8_t value = fr_lcd_nibble_value(nibble, data_mode);
    uint8_t sequence[3] = {
        value,
        (uint8_t)(value | FR_LCD_PCF_ENABLE),
        (uint8_t)(value & (uint8_t)~FR_LCD_PCF_ENABLE),
    };

    if (!fr_lcd_transmit_pcf(lcd, sequence, sizeof(sequence))) {
        return false;
    }
    esp_rom_delay_us(50);
    return true;
}

static bool fr_lcd_write_byte(fr_lcd_context_t *lcd, uint8_t value, bool data_mode)
{
    uint8_t high = fr_lcd_nibble_value((uint8_t)(value >> 4), data_mode);
    uint8_t low = fr_lcd_nibble_value(value, data_mode);
    uint8_t sequence[6] = {
        high,
        (uint8_t)(high | FR_LCD_PCF_ENABLE),
        (uint8_t)(high & (uint8_t)~FR_LCD_PCF_ENABLE),
        low,
        (uint8_t)(low | FR_LCD_PCF_ENABLE),
        (uint8_t)(low & (uint8_t)~FR_LCD_PCF_ENABLE),
    };

    if (!fr_lcd_transmit_pcf(lcd, sequence, sizeof(sequence))) {
        return false;
    }
    esp_rom_delay_us((value == 0x01U || value == 0x02U) ? 2000 : 50);
    return true;
}

static bool fr_lcd_command(fr_lcd_context_t *lcd, uint8_t command)
{
    return fr_lcd_write_byte(lcd, command, false);
}

static bool fr_lcd_write_char(fr_lcd_context_t *lcd, char character)
{
    return fr_lcd_write_byte(lcd, (uint8_t)character, true);
}

static bool __attribute__((unused)) fr_lcd_init_hd44780(fr_lcd_context_t *lcd)
{
    vTaskDelay(pdMS_TO_TICKS(50));
    if (!fr_lcd_write_nibble(lcd, 0x03, false)) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(5));
    if (!fr_lcd_write_nibble(lcd, 0x03, false)) {
        return false;
    }
    esp_rom_delay_us(150);
    if (!fr_lcd_write_nibble(lcd, 0x03, false)) {
        return false;
    }
    esp_rom_delay_us(150);
    if (!fr_lcd_write_nibble(lcd, 0x02, false)) {
        return false;
    }
    esp_rom_delay_us(150);

    return fr_lcd_command(lcd, 0x28) &&
           fr_lcd_command(lcd, 0x08) &&
           fr_lcd_command(lcd, 0x01) &&
           fr_lcd_command(lcd, 0x06) &&
           fr_lcd_command(lcd, 0x0c);
}

static bool fr_lcd_diag_hd44780_step(
    fr_lcd_context_t *lcd,
    const char *step,
    bool ok,
    const char **failed_step
)
{
    printf(
        "LCD_HD44780 step=%s result=%s err=%s\r\n",
        step,
        ok ? "ok" : "fail",
        ok ? "ESP_OK" : "transmit"
    );
    if (!ok) {
        *failed_step = step;
    }
    return ok;
}

static bool fr_lcd_init_hd44780_diag(fr_lcd_context_t *lcd, const char **failed_step)
{
    vTaskDelay(pdMS_TO_TICKS(50));
    if (!fr_lcd_diag_hd44780_step(
            lcd,
            "wake1",
            fr_lcd_write_nibble(lcd, 0x03, false),
            failed_step
        )) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(5));
    if (!fr_lcd_diag_hd44780_step(
            lcd,
            "wake2",
            fr_lcd_write_nibble(lcd, 0x03, false),
            failed_step
        )) {
        return false;
    }
    esp_rom_delay_us(150);
    if (!fr_lcd_diag_hd44780_step(
            lcd,
            "wake3",
            fr_lcd_write_nibble(lcd, 0x03, false),
            failed_step
        )) {
        return false;
    }
    esp_rom_delay_us(150);
    if (!fr_lcd_diag_hd44780_step(
            lcd,
            "4bit",
            fr_lcd_write_nibble(lcd, 0x02, false),
            failed_step
        )) {
        return false;
    }
    esp_rom_delay_us(150);

    return fr_lcd_diag_hd44780_step(
               lcd,
               "function-set",
               fr_lcd_command(lcd, 0x28),
               failed_step
           ) &&
           fr_lcd_diag_hd44780_step(
               lcd,
               "display-off",
               fr_lcd_command(lcd, 0x08),
               failed_step
           ) &&
           fr_lcd_diag_hd44780_step(
               lcd,
               "clear",
               fr_lcd_command(lcd, 0x01),
               failed_step
           ) &&
           fr_lcd_diag_hd44780_step(
               lcd,
               "entry",
               fr_lcd_command(lcd, 0x06),
               failed_step
           ) &&
           fr_lcd_diag_hd44780_step(
               lcd,
               "display-on",
               fr_lcd_command(lcd, 0x0c),
               failed_step
           );
}

static const uint8_t fr_lcd_row_offsets[FR_LCD_ROWS] = {0x00, 0x40, 0x14, 0x54};

static uint8_t fr_lcd_ddram_address(uint8_t row, uint8_t column)
{
    if (row >= FR_LCD_ROWS || column >= FR_LCD_COLUMNS) {
        return 0;
    }
    return (uint8_t)(fr_lcd_row_offsets[row] + column);
}

static bool fr_lcd_set_cursor_at(fr_lcd_context_t *lcd, uint8_t row, uint8_t column)
{
    if (row >= FR_LCD_ROWS) {
        return false;
    }
    if (column >= FR_LCD_COLUMNS) {
        column = FR_LCD_COLUMNS - 1U;
    }
    return fr_lcd_command(
        lcd,
        (uint8_t)(0x80U | fr_lcd_ddram_address(row, column))
    );
}

static bool fr_lcd_set_cursor(fr_lcd_context_t *lcd, uint8_t row)
{
    return fr_lcd_set_cursor_at(lcd, row, 0);
}

static bool fr_lcd_write_line(fr_lcd_context_t *lcd, uint8_t row, const char *text)
{
    if (!fr_lcd_set_cursor(lcd, row)) {
        return false;
    }
    const char *cursor = text;
    for (size_t column = 0; column < FR_LCD_COLUMNS; ++column) {
        char character = ' ';
        if (*cursor != '\0') {
            character = *cursor;
            cursor += 1;
        }
        if (!fr_lcd_write_char(lcd, character)) {
            return false;
        }
    }
    return true;
}

static bool fr_lcd_write_page(
    fr_lcd_context_t *lcd,
    const char *line0,
    const char *line1,
    const char *line2,
    const char *line3
)
{
    return fr_lcd_write_line(lcd, 0, line0) &&
           fr_lcd_write_line(lcd, 1, line1) &&
           fr_lcd_write_line(lcd, 2, line2) &&
           fr_lcd_write_line(lcd, 3, line3);
}

static unsigned long __attribute__((unused)) fr_diag_short_display_count(uint32_t count)
{
    return (unsigned long)(count % 1000U);
}

static unsigned long __attribute__((unused)) fr_diag_short_position_magnitude(int32_t position)
{
    int32_t short_position = position % 1000;
    if (short_position < 0) {
        short_position = -short_position;
    }
    return (unsigned long)short_position;
}

static char fr_menu_level_char(uint8_t level)
{
    return level == 0U ? '0' : '1';
}

static const fr_lcd_glyph_bank_t fr_lcd_glyph_banks[FR_GLYPH_BANK_COUNT] = {
    {
        .name = "core_status",
        .rows = {
            {0x0e, 0x11, 0x11, 0x1f, 0x1b, 0x1b, 0x1f, 0x00},
            {0x00, 0x1f, 0x11, 0x0a, 0x04, 0x0a, 0x11, 0x1f},
            {0x1f, 0x11, 0x1f, 0x00, 0x1f, 0x11, 0x1f, 0x00},
            {0x04, 0x0e, 0x04, 0x0e, 0x15, 0x04, 0x0a, 0x00},
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01},
            {0x00, 0x00, 0x00, 0x00, 0x04, 0x05, 0x05, 0x05},
            {0x00, 0x00, 0x10, 0x10, 0x14, 0x15, 0x15, 0x15},
            {0x04, 0x0e, 0x15, 0x04, 0x15, 0x0e, 0x04, 0x00},
        },
    },
    {
        .name = "horizontal_bar",
        .rows = {
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},
            {0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10},
            {0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18},
            {0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c},
            {0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e},
            {0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f},
            {0x1f, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1f},
            {0x1f, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x1f},
        },
    },
    {
        .name = "vertical_chart",
        .rows = {
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f},
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f},
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1f},
            {0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1f, 0x1f},
            {0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f},
            {0x00, 0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f},
            {0x00, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f, 0x1f},
        },
    },
    {
        .name = "big_digits",
        .rows = {
            {0x0e, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0e, 0x00},
            {0x04, 0x0c, 0x04, 0x04, 0x04, 0x04, 0x0e, 0x00},
            {0x0e, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1f, 0x00},
            {0x1f, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0e, 0x00},
            {0x02, 0x06, 0x0a, 0x12, 0x1f, 0x02, 0x02, 0x00},
            {0x1f, 0x10, 0x1e, 0x01, 0x01, 0x11, 0x0e, 0x00},
            {0x0e, 0x10, 0x1e, 0x11, 0x11, 0x11, 0x0e, 0x00},
            {0x1f, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08, 0x00},
        },
    },
    {
        .name = "gauge_demo",
        .rows = {
            {0x00, 0x00, 0x01, 0x03, 0x07, 0x0f, 0x1f, 0x00},
            {0x00, 0x04, 0x0e, 0x15, 0x04, 0x04, 0x04, 0x00},
            {0x00, 0x00, 0x10, 0x18, 0x1c, 0x1e, 0x1f, 0x00},
            {0x00, 0x0e, 0x11, 0x04, 0x04, 0x04, 0x04, 0x00},
            {0x00, 0x0e, 0x11, 0x01, 0x02, 0x04, 0x04, 0x00},
            {0x00, 0x0e, 0x11, 0x10, 0x08, 0x04, 0x04, 0x00},
            {0x00, 0x04, 0x0e, 0x15, 0x1f, 0x0e, 0x04, 0x00},
            {0x00, 0x04, 0x04, 0x0e, 0x0e, 0x1f, 0x1f, 0x00},
        },
    },
};

static const char *fr_bbs_page_name(uint8_t page)
{
    static const char *const page_names[FR_MENU_PAGE_COUNT] = {
        "HOME",
        "MESSAGES",
        "PEERS",
        "QUEUE",
        "FILES",
        "MESH",
        "XBEE",
        "DIAG",
        "LOCKS",
        "BARS",
        "CHART",
        "DIGITS",
        "GAUGE",
    };

    if (page >= FR_MENU_PAGE_COUNT) {
        return "HOME";
    }
    return page_names[page];
}

static uint8_t fr_bbs_page_glyph_bank_index(uint8_t page)
{
    switch (page) {
    case 9:
        return 1;
    case 10:
        return 2;
    case 11:
        return 3;
    case 12:
        return 4;
    default:
        return 0;
    }
}

static const char *fr_lcd_glyph_bank_name(uint8_t index)
{
    if (index >= FR_GLYPH_BANK_COUNT) {
        index = 0;
    }
    return fr_lcd_glyph_banks[index].name;
}

static void fr_lcd_frame_clear(fr_lcd_frame_t *frame)
{
    memset(frame, 0, sizeof(*frame));
    for (size_t row = 0; row < FR_LCD_ROWS; ++row) {
        for (size_t column = 0; column < FR_LCD_COLUMNS; ++column) {
            frame->cells[row][column] = ' ';
            frame->log_lines[row][column] = ' ';
        }
        frame->log_lines[row][FR_LCD_COLUMNS] = '\0';
    }
    frame->focus = "page_browse";
}

static void fr_lcd_frame_set_line(fr_lcd_frame_t *frame, uint8_t row, const char *text)
{
    if (row >= FR_LCD_ROWS) {
        return;
    }
    size_t source_offset = 0;
    for (size_t column = 0; column < FR_LCD_COLUMNS; ++column) {
        char character = ' ';
        if (text != NULL && text[source_offset] != '\0') {
            character = text[source_offset];
            source_offset += 1U;
            if (character < 32 || character > 126) {
                character = '?';
            }
        }
        frame->cells[row][column] = (uint8_t)character;
        frame->log_lines[row][column] = character;
    }
    frame->log_lines[row][FR_LCD_COLUMNS] = '\0';
}

static void fr_lcd_frame_set_glyph(
    fr_lcd_frame_t *frame,
    uint8_t row,
    uint8_t column,
    uint8_t slot,
    char fallback
)
{
    if (row >= FR_LCD_ROWS || column >= FR_LCD_COLUMNS || slot >= FR_GLYPH_SLOTS) {
        return;
    }
    frame->cells[row][column] = slot;
    frame->log_lines[row][column] =
        (fallback >= 32 && fallback <= 126) ? fallback : '?';
}

static void fr_lcd_frame_put_bar(
    fr_lcd_frame_t *frame,
    uint8_t row,
    uint8_t column,
    uint8_t width,
    uint8_t percent
)
{
    static const char fallback[6] = {' ', '.', ':', '-', '=', '#'};
    if (percent > 100U) {
        percent = 100U;
    }
    uint16_t total_segments = (uint16_t)((uint32_t)percent * width * 5U / 100U);
    for (uint8_t index = 0; index < width; ++index) {
        int16_t remaining = (int16_t)total_segments - (int16_t)(index * 5U);
        uint8_t fill = 0;
        if (remaining >= 5) {
            fill = 5;
        } else if (remaining > 0) {
            fill = (uint8_t)remaining;
        }
        fr_lcd_frame_set_glyph(
            frame,
            row,
            (uint8_t)(column + index),
            fill,
            fallback[fill]
        );
    }
}

static void fr_lcd_frame_put_chart(
    fr_lcd_frame_t *frame,
    uint8_t row,
    uint8_t column,
    const uint8_t *values,
    uint8_t count
)
{
    static const char fallback[8] = {' ', '.', ':', '-', '=', '+', '#', '@'};
    for (uint8_t index = 0; index < count; ++index) {
        uint8_t slot = values[index] > 7U ? 7U : values[index];
        fr_lcd_frame_set_glyph(
            frame,
            row,
            (uint8_t)(column + index),
            slot,
            fallback[slot]
        );
    }
}

static const char *fr_bbs_last_event(const fr_menu_state_t *menu, uint32_t now_ms)
{
    if (menu->ack == FR_MENU_ACK_SELECT && now_ms < menu->ack_until_ms) {
        return "ACK local";
    }
    return menu->last_event[0] == '\0' ? "?" : menu->last_event;
}

static void fr_bbs_format_uptime(char *buffer, size_t buffer_size, uint32_t now_ms)
{
    uint32_t seconds = now_ms / 1000U;
    uint32_t minutes = seconds / 60U;
    uint32_t hours = minutes / 60U;
    seconds %= 60U;
    minutes %= 60U;

    if (hours > 0U) {
        snprintf(buffer, buffer_size, "%luh%02lum",
            (unsigned long)hours,
            (unsigned long)minutes
        );
        return;
    }
    snprintf(buffer, buffer_size, "%lum%02lus",
        (unsigned long)minutes,
        (unsigned long)seconds
    );
}

static void fr_bbs_render_frame(
    const fr_menu_state_t *menu,
    uint8_t lcd_address,
    uint32_t now_ms,
    fr_lcd_frame_t *frame
)
{
    char raw[FR_LCD_ROWS][64];
    char uptime[16];
    const char *last_event = fr_bbs_last_event(menu, now_ms);
    uint8_t glyph_bank_index = fr_bbs_page_glyph_bank_index(menu->page);
    uint8_t bar_value = menu->edit_value;
    uint8_t chart_values[8] = {1, 3, 2, 6, 4, 7, 5, 3};

    fr_lcd_frame_clear(frame);
    frame->glyph_bank_index = glyph_bank_index;
    frame->cursor_row = menu->selected_row;
    frame->cursor_col = 0;
    frame->focus = fr_menu_mode_name(menu->mode);

    for (size_t row = 0; row < FR_LCD_ROWS; ++row) {
        raw[row][0] = '\0';
    }

    switch (menu->page) {
    case 0:
        snprintf(raw[0], sizeof(raw[0]), " BBS FIELD UX READY");
        snprintf(raw[1], sizeof(raw[1]), "Peers:3 Queue:2");
        snprintf(raw[2], sizeof(raw[2]), "Cust:OPCON");
        snprintf(raw[3], sizeof(raw[3]), "Last:%s", last_event);
        break;
    case 1:
        snprintf(raw[0], sizeof(raw[0]), " MSG N:1 IN:12");
        snprintf(raw[1], sizeof(raw[1]), "OUT:4 ACK:12");
        snprintf(raw[2], sizeof(raw[2]), "Custody:ACKED");
        snprintf(raw[3], sizeof(raw[3]), "Last:%s", last_event);
        break;
    case 2:
        snprintf(raw[0], sizeof(raw[0]), "PEERS 2/3");
        snprintf(raw[1], sizeof(raw[1]), "Link:OK RSSI:-67");
        snprintf(raw[2], sizeof(raw[2]), "ACK:7 Dup:0");
        snprintf(raw[3], sizeof(raw[3]), "Mesh:coord01");
        break;
    case 3:
        snprintf(raw[0], sizeof(raw[0]), "QUEUE P:2 F:0");
        snprintf(raw[1], sizeof(raw[1]), "Retry:1");
        snprintf(raw[2], sizeof(raw[2]), "Cust:ACKED");
        snprintf(raw[3], sizeof(raw[3]), "Control:CLOSED");
        break;
    case 4:
        snprintf(raw[0], sizeof(raw[0]), "FILES Q:1 D:3");
        snprintf(raw[1], sizeof(raw[1]), "Bytes:4096");
        snprintf(raw[2], sizeof(raw[2]), "Names:CLOSED");
        snprintf(raw[3], sizeof(raw[3]), "Transfer:CLOSED");
        break;
    case 5:
        snprintf(raw[0], sizeof(raw[0]), "MESH sim");
        snprintf(raw[1], sizeof(raw[1]), "Root:coord01");
        snprintf(raw[2], sizeof(raw[2]), "Hops:2 Heal:1");
        snprintf(raw[3], sizeof(raw[3]), "Live:CLOSED");
        break;
    case 6:
        snprintf(raw[0], sizeof(raw[0]), "XBEE CLOSED");
        snprintf(raw[1], sizeof(raw[1]), "UART:CLOSED");
        snprintf(raw[2], sizeof(raw[2]), "NP:?");
        snprintf(raw[3], sizeof(raw[3]), "TX CLOSED");
        break;
    case 7:
        fr_bbs_format_uptime(uptime, sizeof(uptime), now_ms);
        snprintf(raw[0], sizeof(raw[0]), "DIAG FIELD");
        snprintf(raw[1], sizeof(raw[1]), "Up:%s", uptime);
        snprintf(raw[2], sizeof(raw[2]), "LCD:0x%02x C%cD%cS%c",
            lcd_address,
            fr_menu_level_char(menu->stable_a),
            fr_menu_level_char(menu->stable_b),
            fr_menu_level_char(menu->stable_sw)
        );
        snprintf(raw[3], sizeof(raw[3]), "Event:%s", last_event);
        break;
    case 8:
        snprintf(raw[0], sizeof(raw[0]), "LOCKS");
        snprintf(raw[1], sizeof(raw[1]), "Relay:LOCK");
        snprintf(raw[2], sizeof(raw[2]), "XBee:LOCK");
        snprintf(raw[3], sizeof(raw[3]), "Flash:LOCK Ser:LOCK");
        break;
    case 9:
        snprintf(raw[0], sizeof(raw[0]), "BARS LINK QUEUE");
        snprintf(raw[1], sizeof(raw[1]), "LNK");
        snprintf(raw[2], sizeof(raw[2]), "QUE");
        snprintf(raw[3], sizeof(raw[3]), "EDIT %3u%%", (unsigned int)bar_value);
        break;
    case 10:
        chart_values[0] = (uint8_t)(1U + (menu->spinner_frame % 3U));
        chart_values[4] = (uint8_t)(4U + (menu->spinner_frame % 4U));
        snprintf(raw[0], sizeof(raw[0]), "VERT CHART HISTORY");
        snprintf(raw[1], sizeof(raw[1]), "RSSI");
        snprintf(raw[2], sizeof(raw[2]), "ACK ");
        snprintf(raw[3], sizeof(raw[3]), "SPARK local only");
        break;
    case 11:
        snprintf(raw[0], sizeof(raw[0]), "BIG DIGITS 12:34");
        snprintf(raw[1], sizeof(raw[1]), "      NET TIME");
        snprintf(raw[2], sizeof(raw[2]), "      Q%02u ACK%02u",
            (unsigned int)(2U + menu->spinner_frame),
            (unsigned int)12U
        );
        snprintf(raw[3], sizeof(raw[3]), "No clock writes");
        break;
    default:
        snprintf(raw[0], sizeof(raw[0]), "GAUGE DEMO");
        snprintf(raw[1], sizeof(raw[1]), "Signal local %3u%%", (unsigned int)bar_value);
        snprintf(raw[2], sizeof(raw[2]), "    SAFE LOAD OFF");
        snprintf(raw[3], sizeof(raw[3]), "Relay/RF CLOSED");
        break;
    }

    for (size_t row = 0; row < FR_LCD_ROWS; ++row) {
        fr_lcd_frame_set_line(frame, (uint8_t)row, raw[row]);
    }

    switch (menu->page) {
    case 0:
        fr_lcd_frame_set_glyph(frame, 0, 0, 6, '^');
        fr_lcd_frame_set_glyph(frame, 1, 8, 3, 'P');
        fr_lcd_frame_set_glyph(frame, 1, 16, 2, 'Q');
        break;
    case 1:
        fr_lcd_frame_set_glyph(frame, 0, 0, 1, 'M');
        fr_lcd_frame_set_glyph(frame, 2, 0, 2, 'C');
        break;
    case 2:
        fr_lcd_frame_set_glyph(frame, 0, 0, 3, 'P');
        fr_lcd_frame_set_glyph(frame, 1, 8, 5, '|');
        fr_lcd_frame_set_glyph(frame, 1, 9, 6, '|');
        break;
    case 6:
    case 8:
        fr_lcd_frame_set_glyph(frame, 0, 0, 0, 'L');
        break;
    case 9:
        fr_lcd_frame_put_bar(frame, 1, 4, 12, 72);
        fr_lcd_frame_put_bar(frame, 2, 4, 12, 45);
        fr_lcd_frame_put_bar(frame, 3, 8, 10, bar_value);
        break;
    case 10:
        fr_lcd_frame_put_chart(frame, 1, 6, chart_values, 8);
        fr_lcd_frame_put_chart(frame, 2, 6, &chart_values[0], 8);
        break;
    case 11:
        fr_lcd_frame_set_glyph(frame, 1, 0, 1, '1');
        fr_lcd_frame_set_glyph(frame, 1, 1, 2, '2');
        fr_lcd_frame_set_glyph(frame, 1, 3, 3, '3');
        fr_lcd_frame_set_glyph(frame, 1, 4, 4, '4');
        fr_lcd_frame_set_glyph(frame, 2, 0, 5, '5');
        fr_lcd_frame_set_glyph(frame, 2, 1, 6, '6');
        break;
    case 12:
        fr_lcd_frame_set_glyph(frame, 2, 0, 0, '[');
        fr_lcd_frame_set_glyph(frame, 2, 1, 1, '|');
        fr_lcd_frame_set_glyph(frame, 2, 2, 2, ']');
        fr_lcd_frame_set_glyph(frame, 2, 9, (uint8_t)(3U + menu->spinner_frame), '^');
        break;
    default:
        break;
    }

    if (menu->ack == FR_MENU_ACK_SELECT && now_ms < menu->ack_until_ms) {
        fr_lcd_frame_set_line(frame, FR_LCD_ROWS - 1, "ACK local");
    }

    if (menu->mode != FR_MENU_MODE_PAGE_BROWSE) {
        fr_lcd_frame_set_glyph(
            frame,
            menu->selected_row,
            0,
            glyph_bank_index == 0U ? 7U : 5U,
            '>'
        );
    }
    if (menu->mode == FR_MENU_MODE_EDIT_LAB) {
        frame->cursor_col = 18;
    } else if (menu->mode == FR_MENU_MODE_DETAIL) {
        frame->cursor_col = 1;
    } else {
        frame->cursor_col = 0;
    }
    frame->cursor_row = menu->mode == FR_MENU_MODE_PAGE_BROWSE ?
        0U : menu->selected_row;
    frame->cursor_ddram = fr_lcd_ddram_address(frame->cursor_row, frame->cursor_col);
}

static bool fr_lcd_load_glyph_bank(
    fr_lcd_context_t *lcd,
    fr_lcd_render_cache_t *cache,
    uint8_t bank_index,
    uint32_t now_ms
)
{
    if (bank_index >= FR_GLYPH_BANK_COUNT) {
        bank_index = 0;
    }
    if (cache->glyph_valid && cache->glyph_bank_index == bank_index) {
        return true;
    }
    if (cache->glyph_valid &&
        (now_ms - cache->last_glyph_swap_ms) < FR_GLYPH_BANK_SWAP_MIN_MS) {
        uint32_t wait_ms =
            FR_GLYPH_BANK_SWAP_MIN_MS - (now_ms - cache->last_glyph_swap_ms);
        vTaskDelay(fr_delay_ticks_at_least_one(wait_ms));
        now_ms = fr_menu_now_ms();
    }

    const fr_lcd_glyph_bank_t *bank = &fr_lcd_glyph_banks[bank_index];
    for (uint8_t slot = 0; slot < FR_GLYPH_SLOTS; ++slot) {
        if (!fr_lcd_command(lcd, (uint8_t)(0x40U | (slot << 3)))) {
            return false;
        }
        for (uint8_t row = 0; row < FR_GLYPH_ROWS; ++row) {
            if (!fr_lcd_write_byte(lcd, bank->rows[slot][row], true)) {
                return false;
            }
        }
    }

    cache->glyph_valid = true;
    cache->glyph_bank_index = bank_index;
    cache->last_glyph_swap_ms = now_ms;
    cache->valid = false;
    printf(
        "BBS_GLYPH_BANK name=%s index=%u slots=%u rows=%u min_swap_ms=%u t=%lu\r\n",
        bank->name,
        (unsigned int)bank_index,
        (unsigned int)FR_GLYPH_SLOTS,
        (unsigned int)FR_GLYPH_ROWS,
        (unsigned int)FR_GLYPH_BANK_SWAP_MIN_MS,
        (unsigned long)now_ms
    );
    return true;
}

static bool fr_lcd_write_cell_line(
    fr_lcd_context_t *lcd,
    uint8_t row,
    const uint8_t cells[FR_LCD_COLUMNS]
)
{
    if (!fr_lcd_set_cursor(lcd, row)) {
        return false;
    }
    for (size_t column = 0; column < FR_LCD_COLUMNS; ++column) {
        if (!fr_lcd_write_byte(lcd, cells[column], true)) {
            return false;
        }
    }
    return true;
}

static bool fr_lcd_render_bbs_page(
    fr_lcd_context_t *lcd,
    const fr_menu_state_t *menu,
    fr_lcd_render_cache_t *cache,
    uint32_t sequence,
    const char *reason
)
{
    uint32_t start_ms = fr_menu_now_ms();
    fr_lcd_frame_t frame;
    fr_bbs_render_frame(menu, lcd->address, start_ms, &frame);
    uint8_t rows_written = 0;
    uint8_t dirty_row_mask = 0;
    uint16_t dirty_cells = 0;

    if (!fr_lcd_load_glyph_bank(lcd, cache, frame.glyph_bank_index, start_ms)) {
        return false;
    }

    for (size_t row = 0; row < FR_LCD_ROWS; ++row) {
        bool row_dirty = !cache->valid;
        if (cache->valid) {
            for (size_t column = 0; column < FR_LCD_COLUMNS; ++column) {
                if (cache->cells[row][column] != frame.cells[row][column]) {
                    dirty_cells += 1U;
                    row_dirty = true;
                }
            }
        } else {
            dirty_cells += FR_LCD_COLUMNS;
        }
        if (!row_dirty) {
            continue;
        }
        if (!fr_lcd_write_cell_line(lcd, (uint8_t)row, frame.cells[row])) {
            return false;
        }
        memcpy(cache->cells[row], frame.cells[row], FR_LCD_COLUMNS);
        rows_written += 1U;
        dirty_row_mask |= (uint8_t)(1U << row);
    }
    cache->valid = true;
    if (!fr_lcd_set_cursor_at(lcd, frame.cursor_row, frame.cursor_col)) {
        return false;
    }
    uint32_t end_ms = fr_menu_now_ms();

    printf(
        "BBS_CURSOR row=%u col=%u ddram=0x%02x focus=%s mode=%s\r\n",
        (unsigned int)frame.cursor_row,
        (unsigned int)frame.cursor_col,
        (unsigned int)frame.cursor_ddram,
        frame.focus,
        fr_menu_mode_name(menu->mode)
    );
    printf(
        "BBS_LCD_RENDER page=%s index=%u row0=\"%s\" row1=\"%s\" "
        "row2=\"%s\" row3=\"%s\" rows=%u seq=%lu dur_ms=%lu reason=%s "
        "mode=%s focus=%s bank=%s cursor=%u,%u ddram=0x%02x "
        "dirty_rows=0x%02x dirty_cells=%u\r\n",
        fr_bbs_page_name(menu->page),
        (unsigned int)menu->page,
        frame.log_lines[0],
        frame.log_lines[1],
        frame.log_lines[2],
        frame.log_lines[3],
        (unsigned int)rows_written,
        (unsigned long)sequence,
        (unsigned long)(end_ms - start_ms),
        reason,
        fr_menu_mode_name(menu->mode),
        frame.focus,
        fr_lcd_glyph_bank_name(frame.glyph_bank_index),
        (unsigned int)frame.cursor_row,
        (unsigned int)frame.cursor_col,
        (unsigned int)frame.cursor_ddram,
        (unsigned int)dirty_row_mask,
        (unsigned int)dirty_cells
    );
    return true;
}

static void fr_menu_init_state(fr_menu_state_t *menu)
{
    menu->raw_a = fr_pin_finder_read_level(0);
    menu->raw_b = fr_pin_finder_read_level(1);
    menu->raw_sw = fr_pin_finder_read_level(2);
    menu->stable_a = menu->raw_a;
    menu->stable_b = menu->raw_b;
    menu->stable_sw = menu->raw_sw;
    menu->candidate_a = menu->raw_a;
    menu->candidate_b = menu->raw_b;
    menu->stable_samples_a = FR_ENCODER_AB_STABLE_SAMPLES;
    menu->stable_samples_b = FR_ENCODER_AB_STABLE_SAMPLES;
    menu->previous_ab = fr_menu_stable_ab(menu);
    menu->switch_stable_pressed = menu->stable_sw == 0U;
    menu->switch_changed_ms = fr_menu_now_ms();
    menu->last_heartbeat_ms = menu->switch_changed_ms;
    menu->last_auto_demo_ms = menu->switch_changed_ms;
    menu->last_animation_ms = menu->switch_changed_ms;
    menu->auto_demo_enabled = true;
    menu->mode = FR_MENU_MODE_PAGE_BROWSE;
    menu->selected_row = 0;
    menu->edit_value = 50;
    menu->cursor_row = 0;
    menu->cursor_col = 0;
    menu->display_dirty = true;
    fr_menu_set_last_event(menu, "BOOT");
    if (menu->switch_stable_pressed) {
        menu->switch_pressed_ms = menu->switch_changed_ms;
    }
}

static void fr_menu_runtime_stop(fr_menu_runtime_t *runtime)
{
    if (runtime->lock == NULL) {
        return;
    }
    if (xSemaphoreTake(runtime->lock, portMAX_DELAY) == pdTRUE) {
        runtime->stop = true;
        xSemaphoreGive(runtime->lock);
    }
}

static void fr_menu_input_task(void *context)
{
    fr_menu_runtime_t *runtime = (fr_menu_runtime_t *)context;

    for (;;) {
        bool stop = false;
        if (xSemaphoreTake(runtime->lock, portMAX_DELAY) == pdTRUE) {
            stop = runtime->stop;
            if (!stop && fr_menu_poll(&runtime->menu)) {
                runtime->lcd_dirty = true;
                runtime->render_request_count += 1U;
            }
            xSemaphoreGive(runtime->lock);
        }
        if (stop) {
            break;
        }
        vTaskDelay(fr_delay_ticks_at_least_one(FR_MENU_POLL_MS));
    }

    vTaskDelete(NULL);
}

static void fr_lcd_bbs_menu_task(void *context)
{
    (void)context;
    fr_lcd_context_t lcd = {0};
    fr_lcd_diag_state_t diag = {
        .status = "boot",
        .stage = "start",
        .address = 0,
        .detected_count = 0,
    };
    fr_menu_runtime_t runtime = {0};
    fr_lcd_render_cache_t render_cache = {0};
    TaskHandle_t input_task = NULL;
    uint32_t heartbeat_count = 0;
    uint32_t last_render_ms = 0;
    uint32_t render_sequence = 0;

    printf(
        "%s LCD_DIAG_READY gpio=21/22 speed=%d pullups=external "
        "xbee=closed relay=closed\r\n",
        FR_DIAG_FIRMWARE_ID,
        FR_LCD_I2C_SPEED_HZ
    );

    if (!fr_lcd_diag_init_i2c(&lcd, &diag)) {
        goto heartbeat_loop;
    }

    const char *failed_step = "none";
    if (!fr_lcd_init_hd44780_diag(&lcd, &failed_step)) {
        printf("LCD_INIT_FAIL stage=hd44780 detail=%s\r\n", failed_step);
        fr_lcd_diag_set(&diag, "fail", "hd44780");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }

    if (!fr_encoder_init()) {
        printf("%s GPIO_CONFIG_FAILED gpio=13/14/32\r\n", FR_DIAG_FIRMWARE_ID);
        fr_lcd_diag_set(&diag, "fail", "encoder");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }
    runtime.lock = xSemaphoreCreateMutex();
    if (runtime.lock == NULL) {
        printf("%s INPUT_RUNTIME_FAILED detail=mutex\r\n", FR_DIAG_FIRMWARE_ID);
        fr_lcd_diag_set(&diag, "fail", "runtime");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }
    if (xSemaphoreTake(runtime.lock, portMAX_DELAY) != pdTRUE) {
        printf("%s INPUT_RUNTIME_FAILED detail=lock\r\n", FR_DIAG_FIRMWARE_ID);
        fr_lcd_diag_set(&diag, "fail", "runtime");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }
    fr_menu_init_state(&runtime.menu);
    runtime.lcd_dirty = true;
    runtime.render_request_count = 1U;
    xSemaphoreGive(runtime.lock);
    if (xTaskCreate(
            fr_menu_input_task,
            "fr_menu_input",
            FR_MENU_INPUT_TASK_STACK_BYTES,
            &runtime,
            FR_MENU_INPUT_TASK_PRIORITY,
            &input_task
        ) != pdPASS) {
        printf("%s INPUT_TASK_FAILED\r\n", FR_DIAG_FIRMWARE_ID);
        fr_menu_runtime_stop(&runtime);
        fr_lcd_diag_set(&diag, "fail", "input-task");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }

    fr_lcd_diag_set(&diag, "ok", "menu");
    printf("LCD_INIT_OK addr=0x%02x\r\n", lcd.address);
    printf(
        "%s BBS_LCD_READY gpio=13/14/32 pullups=on lcd=21/22 addr=0x%02x "
        "pages=%u xbee=closed relay=closed input=split render=dirty "
        "glyph_banks=%u cursor=software auto_demo_ms=%u\r\n",
        FR_DIAG_FIRMWARE_ID,
        lcd.address,
        (unsigned int)FR_MENU_PAGE_COUNT,
        (unsigned int)FR_GLYPH_BANK_COUNT,
        (unsigned int)FR_MENU_AUTO_DEMO_MS
    );
    printf(
        "%s BBS_INPUT_READY task=split poll_ms=%u render=dirty idle_ms=%u "
        "irq=anyedge queue=%u modes=page,row,detail,edit\r\n",
        FR_DIAG_FIRMWARE_ID,
        (unsigned int)FR_MENU_POLL_MS,
        (unsigned int)FR_MENU_IDLE_REFRESH_MS,
        (unsigned int)FR_ENCODER_EVENT_QUEUE_DEPTH
    );

    for (;;) {
        fr_menu_state_t snapshot = {0};
        bool render_now = false;
        bool stop = false;
        const char *render_reason = "none";
        uint32_t now_ms = fr_menu_now_ms();

        if (xSemaphoreTake(runtime.lock, portMAX_DELAY) == pdTRUE) {
            bool dirty = runtime.lcd_dirty;
            bool idle_refresh =
                render_cache.valid &&
                (now_ms - last_render_ms) >= FR_MENU_IDLE_REFRESH_MS;
            stop = runtime.stop;
            if (!stop && (!render_cache.valid || dirty || idle_refresh)) {
                snapshot = runtime.menu;
                runtime.lcd_dirty = false;
                render_now = true;
                if (!render_cache.valid) {
                    render_reason = "initial";
                } else if (dirty) {
                    render_reason = "event";
                } else {
                    render_reason = "idle";
                }
            }
            xSemaphoreGive(runtime.lock);
        }

        if (stop) {
            break;
        }
        if (render_now) {
            if (!fr_lcd_render_bbs_page(
                    &lcd,
                    &snapshot,
                    &render_cache,
                    render_sequence,
                    render_reason
                )) {
                printf("LCD_INIT_FAIL stage=display detail=render\r\n");
                fr_menu_runtime_stop(&runtime);
                fr_lcd_diag_set(&diag, "fail", "display");
                fr_lcd_cleanup(&lcd);
                goto heartbeat_loop;
            }
            last_render_ms = fr_menu_now_ms();
            render_sequence += 1U;
            continue;
        }

        vTaskDelay(fr_delay_ticks_at_least_one(FR_MENU_RENDER_POLL_MS));
    }

heartbeat_loop:
    for (;;) {
        fr_lcd_diag_print_heartbeat(&diag, heartbeat_count);
        heartbeat_count += 1U;
        vTaskDelay(pdMS_TO_TICKS(FR_LCD_DIAG_HEARTBEAT_MS));
    }
}

static void __attribute__((unused)) fr_lcd_diag_task(void *context)
{
    (void)context;
    fr_lcd_context_t lcd = {0};
    fr_lcd_diag_state_t diag = {
        .status = "boot",
        .stage = "start",
        .address = 0,
        .detected_count = 0,
    };
    uint32_t heartbeat_count = 0;

    printf(
        "%s LCD_DIAG_READY gpio=21/22 speed=%d pullups=external "
        "xbee=closed relay=closed\r\n",
        FR_DIAG_FIRMWARE_ID,
        FR_LCD_I2C_SPEED_HZ
    );

    if (!fr_lcd_diag_init_i2c(&lcd, &diag)) {
        goto heartbeat_loop;
    }

    const char *failed_step = "none";
    if (!fr_lcd_init_hd44780_diag(&lcd, &failed_step)) {
        printf("LCD_INIT_FAIL stage=hd44780 detail=%s\r\n", failed_step);
        fr_lcd_diag_set(&diag, "fail", "hd44780");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }

    char line2[FR_LCD_COLUMNS + 1];
    (void)snprintf(line2, sizeof(line2), "ADDR 0x%02x INIT OK", lcd.address);
    if (!fr_lcd_write_page(
            &lcd,
            FR_DIAG_FIRMWARE_ID " LCD DIAG",
            "I2C 21/22 100k",
            line2,
            "SAFE SURF CLOSED"
        )) {
        printf("LCD_INIT_FAIL stage=display detail=write\r\n");
        fr_lcd_diag_set(&diag, "fail", "display");
        fr_lcd_cleanup(&lcd);
        goto heartbeat_loop;
    }

    fr_lcd_diag_set(&diag, "ok", "ready");
    printf("LCD_INIT_OK addr=0x%02x\r\n", lcd.address);

heartbeat_loop:
    for (;;) {
        fr_lcd_diag_print_heartbeat(&diag, heartbeat_count);
        heartbeat_count += 1U;
        vTaskDelay(pdMS_TO_TICKS(FR_LCD_DIAG_HEARTBEAT_MS));
    }
}

static void fr_lcd_start_task(void)
{
    (void)xTaskCreate(
        fr_lcd_bbs_menu_task,
        "fr_lcd_bbs",
        FR_LCD_TASK_STACK_BYTES,
        NULL,
        FR_LCD_TASK_PRIORITY,
        NULL
    );
}

void app_main(void)
{
#if !FR_DIAG_XBEE_BRIDGE_CLOSED
    uint8_t host_to_xbee[FR_BRIDGE_UART_BUFFER_BYTES];
    uint8_t xbee_to_host[FR_BRIDGE_UART_BUFFER_BYTES];
#endif

    fr_bridge_init_safe_defaults();
    setvbuf(stdout, NULL, _IONBF, 0);
    esp_log_level_set("*", ESP_LOG_NONE);

#if !FR_DIAG_XBEE_BRIDGE_CLOSED
    fr_bridge_configure_uart(
        FR_BRIDGE_HOST_UART,
        FR_BRIDGE_HOST_BAUD,
        UART_PIN_NO_CHANGE,
        UART_PIN_NO_CHANGE
    );
    fr_bridge_configure_uart(
        FR_BRIDGE_XBEE_UART,
        FR_BRIDGE_XBEE_BAUD,
        FR_BRIDGE_XBEE_TX_GPIO,
        FR_BRIDGE_XBEE_RX_GPIO
    );
    fr_lcd_start_task();

    for (;;) {
        bool copied = false;
        copied |= fr_bridge_copy_available(
            FR_BRIDGE_HOST_UART,
            FR_BRIDGE_XBEE_UART,
            0,
            host_to_xbee,
            sizeof(host_to_xbee),
            &fr_bridge_host_to_xbee_bytes,
            &fr_bridge_host_to_xbee_chunks
        );
        copied |= fr_bridge_copy_available(
            FR_BRIDGE_XBEE_UART,
            FR_BRIDGE_HOST_UART,
            pdMS_TO_TICKS(2),
            xbee_to_host,
            sizeof(xbee_to_host),
            &fr_bridge_xbee_to_host_bytes,
            &fr_bridge_xbee_to_host_chunks
        );
        if (!copied) {
            vTaskDelay(pdMS_TO_TICKS(1));
        }
    }
#else
    fr_lcd_start_task();

    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
#endif
}
