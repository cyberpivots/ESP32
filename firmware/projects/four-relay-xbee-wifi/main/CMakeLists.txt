idf_component_register(
    SRCS "main.c"
    PRIV_REQUIRES safe_core esp_driver_uart esp_driver_i2c esp_driver_gpio
)
