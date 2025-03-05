from http import HTTPStatus

from src.application.enums.application_code import ApplicationCode
from src.application.exceptions.failed_get_secret_exception import FailedGetSecretException


def test_failed_get_secret_exception_with_default_values():
    sut = FailedGetSecretException()

    assert sut.code == ApplicationCode.BL_SECRET_FAILURE
    assert sut.message == "Failed to get secrets"
    assert sut.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_failed_get_secret_exception_with_custom_values():
    code = ApplicationCode.BL_INTERNAL_SERVER_ERROR
    message = "Custom exception message"
    status_code = HTTPStatus.BAD_GATEWAY

    sut = FailedGetSecretException(code, message, status_code)

    assert sut.code == code
    assert sut.message == message
    assert sut.status_code == status_code
