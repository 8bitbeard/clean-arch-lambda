from http import HTTPStatus
from unittest.mock import Mock

from src.application.enums.application_code import ApplicationCode
from src.application.exceptions.failed_get_secret_exception import FailedGetSecretException
from src.application.exceptions.failed_get_token_exception import FailedGetTokenException
from src.application.exceptions.failed_list_banks_exception import FailedListBanksException
from src.application.exceptions.failed_save_data_exception import FailedSaveDataException
from src.infrastructure.entrypoint.dto.lambda_response_dto import LambdaResponseDTO, ErrorDTO, BodyDTO
from src.infrastructure.entrypoint.handler.exception_handler import exception_handler


def test_exception_handler_success():
    logger = Mock()
    mock_event = Mock()
    mock_context = Mock()

    def sample_function(event, context):
        return "success"

    decorated_func = exception_handler(logger)(sample_function)

    result = decorated_func(mock_event, mock_context)

    assert result == "success"
    logger.error.assert_not_called()


def test_exception_handler_failed_get_secret_exceptions():
    logger = Mock()
    mock_event = Mock()
    mock_context = Mock()

    def sample_function(event, context):
        raise FailedGetSecretException()

    decorated_func = exception_handler(logger)(sample_function)
    mock_exception = FailedGetSecretException()

    result = decorated_func(mock_event, mock_context)

    assert isinstance(result, LambdaResponseDTO)
    assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(result.body, BodyDTO)
    assert isinstance(result.body.error, ErrorDTO)
    assert result.body.error.code == mock_exception.code.value
    assert result.body.error.message == mock_exception.message

    logger.error.assert_called_once()
    log_message = logger.error.call_args[0][0]
    assert "[exception_handler]: Catched exception" in log_message
    assert str(mock_exception) in log_message


def test_exception_handler_failed_get_token_exceptions():
    logger = Mock()
    mock_event = Mock()
    mock_context = Mock()

    def sample_function(event, context):
        raise FailedGetTokenException()

    decorated_func = exception_handler(logger)(sample_function)
    mock_exception = FailedGetTokenException()

    result = decorated_func(mock_event, mock_context)

    assert isinstance(result, LambdaResponseDTO)
    assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(result.body, BodyDTO)
    assert isinstance(result.body.error, ErrorDTO)
    assert result.body.error.code == mock_exception.code.value
    assert result.body.error.message == mock_exception.message

    logger.error.assert_called_once()
    log_message = logger.error.call_args[0][0]
    assert "[exception_handler]: Catched exception" in log_message
    assert str(mock_exception) in log_message


def test_exception_handler_failed_list_banks_exceptions():
    logger = Mock()
    mock_event = Mock()
    mock_context = Mock()

    def sample_function(event, context):
        raise FailedListBanksException()

    decorated_func = exception_handler(logger)(sample_function)
    mock_exception = FailedListBanksException()

    result = decorated_func(mock_event, mock_context)

    assert isinstance(result, LambdaResponseDTO)
    assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(result.body, BodyDTO)
    assert isinstance(result.body.error, ErrorDTO)
    assert result.body.error.code == mock_exception.code.value
    assert result.body.error.message == mock_exception.message

    logger.error.assert_called_once()
    log_message = logger.error.call_args[0][0]
    assert "[exception_handler]: Catched exception" in log_message
    assert str(mock_exception) in log_message


def test_exception_handler_failed_save_data_exceptions():
    logger = Mock()
    mock_event = Mock()
    mock_context = Mock()

    def sample_function(event, context):
        raise FailedSaveDataException()

    decorated_func = exception_handler(logger)(sample_function)
    mock_exception = FailedSaveDataException()

    result = decorated_func(mock_event, mock_context)

    assert isinstance(result, LambdaResponseDTO)
    assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(result.body, BodyDTO)
    assert isinstance(result.body.error, ErrorDTO)
    assert result.body.error.code == mock_exception.code.value
    assert result.body.error.message == mock_exception.message

    logger.error.assert_called_once()
    log_message = logger.error.call_args[0][0]
    assert "[exception_handler]: Catched exception" in log_message
    assert str(mock_exception) in log_message


def test_exception_handler_generic_exception():
    logger = Mock()
    mock_event = Mock()
    mock_context = Mock()

    def raise_generic_exception(event, context):
        raise ValueError("Generic error")

    decorated_func = exception_handler(logger)(raise_generic_exception)

    result = decorated_func(mock_event, mock_context)

    assert isinstance(result, LambdaResponseDTO)
    assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert isinstance(result.body, BodyDTO)
    assert isinstance(result.body.error, ErrorDTO)
    assert result.body.error.code == ApplicationCode.BL_INTERNAL_SERVER_ERROR.value
    assert result.body.error.message == "Internal server error"

    logger.error.assert_called_once()
    log_message = logger.error.call_args[0][0]
    assert "[exception_handler]: " in log_message
    assert "Generic error" in log_message


def test_exception_handler_preserves_function_metadata():
    logger = Mock()

    def sample_function(event, context):
        return "success"

    decorated_func = exception_handler(logger)(sample_function)

    assert decorated_func.__name__ == "sample_function"
    assert decorated_func.__module__ == sample_function.__module__
