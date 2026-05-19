#include "four_relay_core.h"

#include <string.h>

static fr_http_method_t parse_method(const char *method)
{
    if (method == 0) {
        return FR_HTTP_METHOD_UNSUPPORTED;
    }
    if (strcmp(method, "GET") == 0) {
        return FR_HTTP_METHOD_GET;
    }
    if (strcmp(method, "POST") == 0) {
        return FR_HTTP_METHOD_POST;
    }
    return FR_HTTP_METHOD_UNSUPPORTED;
}

static bool parse_relay_channel(const char *path, int *channel)
{
    const char prefix[] = "/api/relay/";
    size_t prefix_len = sizeof(prefix) - 1u;
    if (strncmp(path, prefix, prefix_len) != 0) {
        return false;
    }
    char value = path[prefix_len];
    if (value < '1' || value > '4' || path[prefix_len + 1u] != '\0') {
        return false;
    }
    *channel = value - '0';
    return true;
}

fr_http_route_t fr_http_classify_route(const char *method, const char *path)
{
    fr_http_route_t route;
    route.method = parse_method(method);
    route.endpoint = FR_HTTP_ENDPOINT_UNKNOWN;
    route.state_changing = false;
    route.relay_channel = -1;

    if (path == 0 || route.method == FR_HTTP_METHOD_UNSUPPORTED) {
        return route;
    }

    if (route.method == FR_HTTP_METHOD_GET && strcmp(path, "/api/state") == 0) {
        route.endpoint = FR_HTTP_ENDPOINT_STATE;
        return route;
    }
    if (route.method == FR_HTTP_METHOD_GET && strcmp(path, "/api/storage/status") == 0) {
        route.endpoint = FR_HTTP_ENDPOINT_STORAGE_STATUS;
        return route;
    }
    if (route.method == FR_HTTP_METHOD_GET && strcmp(path, "/api/assets/manifest") == 0) {
        route.endpoint = FR_HTTP_ENDPOINT_ASSETS_MANIFEST;
        return route;
    }
    if (route.method == FR_HTTP_METHOD_GET && strcmp(path, "/api/logs/recent") == 0) {
        route.endpoint = FR_HTTP_ENDPOINT_LOGS_RECENT;
        return route;
    }
    if (route.method == FR_HTTP_METHOD_POST && strcmp(path, "/api/all-off") == 0) {
        route.endpoint = FR_HTTP_ENDPOINT_ALL_OFF;
        route.state_changing = true;
        return route;
    }
    if (route.method == FR_HTTP_METHOD_POST && strcmp(path, "/api/safety-lock") == 0) {
        route.endpoint = FR_HTTP_ENDPOINT_SAFETY_LOCK;
        route.state_changing = true;
        return route;
    }
    if (route.method == FR_HTTP_METHOD_POST && parse_relay_channel(path, &route.relay_channel)) {
        route.endpoint = FR_HTTP_ENDPOINT_RELAY;
        route.state_changing = true;
        return route;
    }

    return route;
}
