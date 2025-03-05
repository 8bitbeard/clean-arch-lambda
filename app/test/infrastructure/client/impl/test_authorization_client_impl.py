from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError

from app.src.application.exceptions.failed_get_secret_exception import FailedGetSecretException
from app.src.infrastructure.clients.dto.get_token_response_dto import GetTokenResponseDTO
from app.src.infrastructure.clients.impl.authorization_client_impl import AuthorizationClientImpl


def test_get_token_successful(fixture_authorization_client, fixture_secret_dto, fixture_get_token_json_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fixture_get_token_json_response
    mock_response.raise_for_status.return_value = None

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response

        token = fixture_authorization_client.get_token(fixture_secret_dto)

        assert token == "fixture_access_token"
        mock_get.assert_called_once_with(
            url="https://test-auth.com/token",
            headers={"Content-Type": "application/json"},
            verify=False
        )
        fixture_authorization_client._AuthorizationClientImpl__logger.error.assert_not_called()


def test_get_token_http_error(fixture_authorization_client, fixture_secret_dto):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = HTTPError("Bad Request")

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response

        with pytest.raises(FailedGetSecretException):
            fixture_authorization_client.get_token(fixture_secret_dto)

        mock_get.assert_called_once_with(
            url="https://test-auth.com/token",
            headers={"Content-Type": "application/json"},
            verify=False
        )
        fixture_authorization_client._AuthorizationClientImpl__logger.error.assert_called_once()
        call_args = fixture_authorization_client._AuthorizationClientImpl__logger.error.call_args[0][0]
        assert "Error fetching bank list" in call_args
        assert "https://test-auth.com/token" in call_args
        assert "Bad Request" in call_args


def test_get_token_json_validation_error(
        fixture_authorization_client, fixture_secret_dto, fixture_invalid_json_response
):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fixture_invalid_json_response
    mock_response.raise_for_status.return_value = None

    with patch('requests.get') as mock_get, \
            patch.object(GetTokenResponseDTO, 'model_validate') as mock_validate:
        mock_get.return_value = mock_response
        mock_validate.side_effect = ValueError("Validation error")

        with pytest.raises(FailedGetSecretException):
            fixture_authorization_client.get_token(fixture_secret_dto)

        mock_get.assert_called_once()
        fixture_authorization_client._AuthorizationClientImpl__logger.error.assert_called_once()


def test_get_token_base_url_missing(fixture_secret_dto):
    logger = Mock()
    with patch('os.environ.get') as mock_env:
        mock_env.return_value = None
        auth_client = AuthorizationClientImpl(logger)
        assert auth_client._AuthorizationClientImpl__base_url is None

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(status_code=200)
            with pytest.raises(FailedGetSecretException):
                auth_client.get_token(fixture_secret_dto)
