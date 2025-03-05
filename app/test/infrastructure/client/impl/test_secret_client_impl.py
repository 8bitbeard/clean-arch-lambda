import pytest
from unittest.mock import patch
from app.src.application.clients.dto.secret_dto import SecretDTO
from app.src.application.exceptions.failed_get_secret_exception import FailedGetSecretException


def test_get_secret_successful(fixture_secret_client):
    mock_env = {
        "CLIENT_ID": "test_client_id",
        "CLIENT_SECRET": "test_client_secret"
    }

    with patch('os.environ', mock_env):
        result = fixture_secret_client.get_secret()

        assert isinstance(result, SecretDTO)
        assert result.client_id == "test_client_id"
        assert result.client_secret == "test_client_secret"
        fixture_secret_client._SecretClientImpl__logger.error.assert_not_called()


def test_get_secret_missing_client_id(fixture_secret_client):
    mock_env = {
        "CLIENT_SECRET": "test_client_secret"
    }

    with patch('os.environ', mock_env):
        with pytest.raises(FailedGetSecretException):
            fixture_secret_client.get_secret()

        fixture_secret_client._SecretClientImpl__logger.error.assert_called_once()
        call_args = fixture_secret_client._SecretClientImpl__logger.error.call_args[0][0]
        assert "Error fetching secrets" in call_args
        assert "CLIENT_ID" in call_args


def test_get_secret_missing_client_secret(fixture_secret_client):
    mock_env = {
        "CLIENT_ID": "test_client_id"
    }

    with patch('os.environ', mock_env):
        with pytest.raises(FailedGetSecretException):
            fixture_secret_client.get_secret()

        fixture_secret_client._SecretClientImpl__logger.error.assert_called_once()
        call_args = fixture_secret_client._SecretClientImpl__logger.error.call_args[0][0]
        assert "Error fetching secrets" in call_args
        assert "CLIENT_SECRET" in call_args


def test_get_secret_missing_all_env_vars(fixture_secret_client):
    mock_env = {}

    with patch('os.environ', mock_env):
        with pytest.raises(FailedGetSecretException):
            fixture_secret_client.get_secret()

        fixture_secret_client._SecretClientImpl__logger.error.assert_called_once()
        call_args = fixture_secret_client._SecretClientImpl__logger.error.call_args[0][0]
        assert "Error fetching secrets" in call_args