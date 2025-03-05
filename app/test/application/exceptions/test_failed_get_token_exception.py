from http import HTTPStatus

from src.application.enums.application_code import ApplicationCode
from src.application.exceptions.failed_get_token_exception import FailedGetTokenException


def test_failed_get_token_exception_with_default_values():
    sut = FailedGetTokenException()

    assert sut.code == ApplicationCode.BL_TOKEN_FAILURE
    assert sut.message == "Failed to get authorization token"
    assert sut.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_failed_get_token_exception_with_custom_values():
    code = ApplicationCode.BL_INTERNAL_SERVER_ERROR
    message = "Custom exception message"
    status_code = HTTPStatus.BAD_GATEWAY

    sut = FailedGetTokenException(code, message, status_code)

    assert sut.code == code
    assert sut.message == message
    assert sut.status_code == status_code
