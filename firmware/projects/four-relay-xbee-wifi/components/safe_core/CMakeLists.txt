idf_component_register(
    SRCS
        "src/api_contract.c"
        "src/api_model.c"
        "src/config_store.c"
        "src/relay_state.c"
        "src/safety_supervisor.c"
        "src/storage_status.c"
        "src/xbee_frame.c"
    INCLUDE_DIRS "include"
)
