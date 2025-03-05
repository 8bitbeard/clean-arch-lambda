from http import HTTPStatus

from app.src.application.enums.application_code import ApplicationCode
from app.src.application.exceptions.failed_list_banks_exception import FailedListBanksException


def test_failed_list_banks_exception_with_default_values():
    sut = FailedListBanksException()

    assert sut.code == ApplicationCode.BL_LIST_BANKS_FAILURE
    assert sut.message == "Failed to get the list of banks"
    assert sut.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_failed_list_banks_exception_with_custom_values():
    code = ApplicationCode.BL_INTERNAL_SERVER_ERROR
    message = "Custom exception message"
    status_code = HTTPStatus.BAD_GATEWAY

    sut = FailedListBanksException(code, message, status_code)

    assert sut.code == code
    assert sut.message == message
    assert sut.status_code == status_code
