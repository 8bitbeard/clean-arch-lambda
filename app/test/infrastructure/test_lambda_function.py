from unittest.mock import patch, Mock, MagicMock

from src.application.exceptions.failed_get_secret_exception import FailedGetSecretException
from src.application.usecases.impl.fetch_bank_list_impl import FetchBankListUseCaseImpl
from src.infrastructure.entrypoint.dto.lambda_response_dto import LambdaResponseDTO, BodyDTO, DataDTO, ErrorDTO
from src.infrastructure.entrypoint.lambda_function import inject_dependencies, lambda_handler


@patch('src.infrastructure.entrypoint.lambda_function.SecretClientImpl')
@patch('src.infrastructure.entrypoint.lambda_function.AuthorizationClientImpl')
@patch('src.infrastructure.entrypoint.lambda_function.BankClientImpl')
@patch('src.infrastructure.entrypoint.lambda_function.StorageClientImpl')
@patch('src.infrastructure.entrypoint.lambda_function.FetchBankListUseCaseImpl')
def test_inject_dependencies(
        mock_use_case, mock_storage_client, mock_bank_client, mock_authorization_client, mock_secret_client
):
    result = inject_dependencies()

    mock_secret_client.assert_called_once()
    mock_authorization_client.assert_called_once()
    mock_bank_client.assert_called_once()
    mock_storage_client.assert_called_once()
    mock_use_case.assert_called_once()


@patch('src.infrastructure.entrypoint.lambda_function.uuid.uuid4')
@patch('src.infrastructure.entrypoint.lambda_function.os.environ.get')
@patch('src.infrastructure.entrypoint.lambda_function.inject_dependencies')
@patch('src.infrastructure.entrypoint.lambda_function.exception_handler')
def test_lambda_handler_success(mock_exception_handler, mock_inject, mock_env, mock_uuid):
    mock_fetch_bank_list_use_case = MagicMock(spec=FetchBankListUseCaseImpl)

    mock_uuid.side_effect = ["corr_id", "flow_id"]
    mock_env.return_value = "test_flow_id"
    mock_inject.return_value = mock_fetch_bank_list_use_case

    mock_event = Mock()
    mock_context = Mock()

    result = lambda_handler(mock_event, mock_context)

    mock_inject.assert_called_once()
    mock_fetch_bank_list_use_case.execute.assert_called_once_with("corr_id", "test_flow_id")
    mock_uuid.assert_called()
    mock_env.assert_called_once_with("flow_id", "flow_id")

    response = LambdaResponseDTO.model_validate_json(result)
    assert response.status_code == 200
    assert isinstance(response.body, BodyDTO)
    assert isinstance(response.body.data, DataDTO)
    assert response.body.data.status == "SUCCESS"


@patch('src.infrastructure.entrypoint.lambda_function.uuid.uuid4')
@patch('src.infrastructure.entrypoint.lambda_function.os.environ.get')
@patch('src.infrastructure.entrypoint.lambda_function.inject_dependencies')
@patch('src.infrastructure.entrypoint.lambda_function.exception_handler')
def test_lambda_handler_with_exception(mock_exception_handler, mock_inject, mock_env, mock_uuid):
    mock_fetch_bank_list_use_case = MagicMock(spec=FetchBankListUseCaseImpl)

    mock_uuid.return_value = "corr_id"
    mock_env.return_value = "test_flow_id"
    mock_inject.return_value = mock_fetch_bank_list_use_case
    mock_fetch_bank_list_use_case.execute.side_effect = FailedGetSecretException()

    mock_event = Mock()
    mock_context = Mock()

    mock_response = LambdaResponseDTO(
        status_code=500,
        body=BodyDTO(error=ErrorDTO(code="BL_SECRET_FAILURE", message="Failed to get secrets"))
    )
    mock_exception_handler.return_value = lambda e, c: mock_response

    result = lambda_handler(mock_event, mock_context)

    mock_inject.assert_called_once()
    mock_fetch_bank_list_use_case.execute.assert_called_once_with("corr_id", "test_flow_id")
    assert result == mock_response


@patch('src.infrastructure.entrypoint.lambda_function.uuid.uuid4')
@patch('src.infrastructure.entrypoint.lambda_function.inject_dependencies')
@patch('src.infrastructure.entrypoint.lambda_function.exception_handler')
def test_lambda_handler_missing_flow_id(mock_exception_handler, mock_inject, mock_uuid):
    mock_fetch_bank_list_use_case = MagicMock(spec=FetchBankListUseCaseImpl)

    mock_uuid.side_effect = ["corr_id", "flow_id"]
    mock_inject.return_value = mock_fetch_bank_list_use_case

    mock_event = Mock()
    mock_context = Mock()

    result = lambda_handler(mock_event, mock_context)

    mock_fetch_bank_list_use_case.execute.assert_called_once_with("corr_id", "flow_id")
    response = LambdaResponseDTO.model_validate_json(result)
    assert response.status_code == 200
    assert response.body.data.status == "SUCCESS"
