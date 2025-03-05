from app.src.application.enums.application_code import ApplicationCode


def test_bl_storage_failure_value():
    assert ApplicationCode.BL_STORAGE_FAILURE.value == "BL_STORAGE_FAILURE"


def test_bl_secret_failure_value():
    assert ApplicationCode.BL_SECRET_FAILURE.value == "BL_SECRET_FAILURE"


def test_bl_list_banks_failure_value():
    assert ApplicationCode.BL_LIST_BANKS_FAILURE.value == "BL_LIST_BANKS_FAILURE"


def test_bl_token_failure_value():
    assert ApplicationCode.BL_TOKEN_FAILURE.value == "BL_TOKEN_FAILURE"


def test_bl_internal_server_error_value():
    assert ApplicationCode.BL_INTERNAL_SERVER_ERROR.value == "BL_INTERNAL_SERVER_ERROR"
