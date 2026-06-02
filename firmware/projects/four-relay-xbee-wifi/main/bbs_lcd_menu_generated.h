/* Generated menu header; do not edit. */
#ifndef BBS_LCD_MENU_GENERATED_H
#define BBS_LCD_MENU_GENERATED_H

#include <stdbool.h>
#include <stdint.h>

#define FR_DIAG_FIRMWARE_ID_VALUE "PF0530W"
#define FR_BBS_MENU_XML_SCHEMA "bbs_lcd_menu.v1"
#define FR_BBS_MENU_RENDER_SCHEMA "bbs_lcd_render.v2"
#define FR_BBS_MENU_SOURCE_ID "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02"
#define FR_BBS_MENU_PAGE_COUNT 15u
#define FR_BBS_MENU_ITEM_COUNT 65u
#define FR_BBS_GLYPH_BANK_COUNT 7u
#define FR_BBS_MENU_CONTENT_COLUMNS 19u
#define FR_BBS_MENU_MARQUEE_HOLD_MS 750u
#define FR_BBS_MENU_MARQUEE_STEP_MS 250u
#define FR_BBS_MENU_MARQUEE_GAP 2u

typedef enum {
    FR_BBS_ACTION_PAGE = 0,
    FR_BBS_ACTION_DETAIL,
    FR_BBS_ACTION_EDIT,
    FR_BBS_ACTION_BACK,
} fr_bbs_menu_action_t;

typedef struct {
    const char *id;
    const char *label;
    const char *rows[3];
    uint8_t row_count;
    fr_bbs_menu_action_t action;
    uint8_t target_page;
    bool editable;
    bool table;
} fr_bbs_menu_item_t;

typedef struct {
    const char *id;
    const char *title;
    uint8_t glyph_bank_index;
    uint8_t item_count;
    uint8_t line_count;
    const fr_bbs_menu_item_t *items;
} fr_bbs_menu_page_t;

static const fr_bbs_menu_item_t fr_bbs_menu_items_home[] = {
    {"home-status", "BBS Ready {link.status}", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"home-messages", "Messages Custody", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 1u, false, false},
    {"home-peers", "Peers RSSI", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 2u, false, false},
    {"home-queue", "Queue Files", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 3u, false, false},
    {"home-mesh", "Routes Mesh", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 13u, false, false},
    {"home-diag", "Diag Locks", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 7u, false, false},
    {"home-widgets", "Widget Lab", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 9u, false, false},
    {"home-art", "ART Pixel Gallery", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 14u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_messages[] = {
    {"msg-new", "New inbox messages", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"msg-outbox", "Outbox pending acknowledgements", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"msg-custody", "Custody ACKED local only", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"msg-last", "Last event ACK peer01 with long scroll text", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"msg-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_peers[] = {
    {"peer-count", "Active peers 2 of 3", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"peer-rssi", "RSSI -67 ACK 07", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"peer-root", "Root coord01 hops 2", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"peer-dup", "Duplicate count zero", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"peer-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_queue[] = {
    {"queue-pending", "Pending messages 02", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"queue-retry", "Retry queue 01", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"queue-files", "Files queued 01 done 03", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 4u, false, false},
    {"queue-control", "Control bridge CLOSED", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"queue-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_files[] = {
    {"files-counts", "Files queued 01 done 03", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"files-bytes", "Bytes staged 4096", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"files-names", "File names closed surface", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"files-back", "Back queue", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 3u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_mesh[] = {
    {"mesh-mode", "Mesh runtime mode", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"mesh-root", "Root coordinator coord01", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"mesh-heal", "Heal events 01", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"mesh-routes", "Open route table", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 13u, false, false},
    {"mesh-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_xbee[] = {
    {"xbee-closed", "Bridge local CLOSED", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"xbee-host", "Host UART0 115200", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"xbee-radio", "XBee UART2 9600 closed", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"xbee-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_diag[] = {
    {"diag-errors", "Diagnostics errors zero", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"diag-uptime", "Uptime host snapshot", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"diag-lcd", "LCD GPIO21 GPIO22 display only", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"diag-locks", "Locks relay xbee flash serial", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 8u, false, false},
    {"diag-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_locks[] = {
    {"lock-relay", "Relay LOCK", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"lock-xbee", "XBee LOCK", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"lock-flash", "Flash LOCK", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"lock-serial", "Serial write LOCK", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"lock-back", "Back diagnostics", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 7u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_bars[] = {
    {"bars-link", "Link level local bar", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"bars-queue", "Queue level local bar", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"bars-edit", "Adjust local value", {"", "", ""}, 1u, FR_BBS_ACTION_EDIT, 0u, true, false},
    {"bars-chart", "Open chart page", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 10u, false, false},
    {"bars-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 0u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_chart[] = {
    {"chart-history", "Vertical chart history", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"chart-spark", "Sparkline local only", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"chart-digits", "Open digits page", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 11u, false, false},
    {"chart-back", "Back bars", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 9u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_digits[] = {
    {"digits-status", "Big digits status", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"digits-clock", "No clock writes", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"digits-gauge", "Open gauge page", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 12u, false, false},
    {"digits-back", "Back chart", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 10u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_gauge[] = {
    {"gauge-signal", "Signal local gauge", {"", "", ""}, 1u, FR_BBS_ACTION_EDIT, 0u, true, false},
    {"gauge-load", "Safe load off", {"", "", ""}, 1u, FR_BBS_ACTION_DETAIL, 0u, false, false},
    {"gauge-back", "Back widgets", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 9u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_routes[] = {
    {"routes-table", "NODE |RSSI|Q", {"coord01|-67 |2", "peer02 |-71 |0", "peer03 |-82 |1"}, 4u, FR_BBS_ACTION_DETAIL, 0u, false, true},
    {"routes-back", "Back mesh", {"", "", ""}, 1u, FR_BBS_ACTION_PAGE, 5u, false, false},
};

static const fr_bbs_menu_item_t fr_bbs_menu_items_art[] = {
    {"art-back", "Back home", {"", "", ""}, 1u, FR_BBS_ACTION_BACK, 0u, false, false},
};

static const fr_bbs_menu_page_t fr_bbs_generated_pages[FR_BBS_MENU_PAGE_COUNT] = {
    {"HOME", "BBS Field", 0u, 8u, 8u, fr_bbs_menu_items_home},
    {"MESSAGES", "Messages", 0u, 5u, 5u, fr_bbs_menu_items_messages},
    {"PEERS", "Peers", 0u, 5u, 5u, fr_bbs_menu_items_peers},
    {"QUEUE", "Queue", 0u, 5u, 5u, fr_bbs_menu_items_queue},
    {"FILES", "Files", 0u, 4u, 4u, fr_bbs_menu_items_files},
    {"MESH", "Mesh", 0u, 5u, 5u, fr_bbs_menu_items_mesh},
    {"XBEE", "XBee Bridge", 0u, 4u, 4u, fr_bbs_menu_items_xbee},
    {"DIAG", "Diagnostics", 0u, 5u, 5u, fr_bbs_menu_items_diag},
    {"LOCKS", "Locks", 0u, 5u, 5u, fr_bbs_menu_items_locks},
    {"BARS", "Bars", 1u, 5u, 5u, fr_bbs_menu_items_bars},
    {"CHART", "Chart", 2u, 4u, 4u, fr_bbs_menu_items_chart},
    {"DIGITS", "Digits", 3u, 4u, 4u, fr_bbs_menu_items_digits},
    {"GAUGE", "Gauge", 4u, 3u, 3u, fr_bbs_menu_items_gauge},
    {"ROUTES", "Routes", 5u, 2u, 5u, fr_bbs_menu_items_routes},
    {"ART", "Art Panel", 6u, 1u, 1u, fr_bbs_menu_items_art},
};

#endif /* BBS_LCD_MENU_GENERATED_H */
