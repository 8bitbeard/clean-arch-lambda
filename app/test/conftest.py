from unittest.mock import patch, Mock

import pytest

from src.application.clients.dto.secret_dto import SecretDTO
from src.domain.models.bank_model import BankModel
from src.domain.models.metadata_model import MetadataModel
from src.infrastructure.clients.impl.authorization_client_impl import AuthorizationClientImpl
from src.infrastructure.clients.impl.bank_client_impl import BankClientImpl
from src.infrastructure.clients.impl.secret_client_impl import SecretClientImpl
from src.infrastructure.clients.impl.storage_client_impl import StorageClientImpl


@pytest.fixture
def fixture_authorization_client():
    with patch('os.environ.get') as mock_env:
        logger = Mock()
        mock_env.return_value = "https://test-auth.com"
        return AuthorizationClientImpl(logger)


@pytest.fixture
def fixture_bank_client():
    with patch('os.environ.get') as mock_env:
        logger = Mock()
        mock_env.return_value = "https://test-banks.com"
        return BankClientImpl(logger)


@pytest.fixture
def fixture_secret_client():
    logger = Mock()
    return SecretClientImpl(logger)


@pytest.fixture
def fixture_storage_client():
    logger = Mock()
    return StorageClientImpl(logger)


@pytest.fixture()
def fixture_metadata_model() -> MetadataModel:
    return MetadataModel(
        date="2025-03-04T21:54:00"
    )


@pytest.fixture()
def fixture_bank_model() -> BankModel:
    return BankModel(
        id="fixture_bank_model_id",
        name="fixture_bank_model_name",
        ispb="fixture_bank_model_ispb"
    )


@pytest.fixture
def fixture_secret_dto():
    return SecretDTO(
        client_id="fixture_client_id",
        client_secret="fixture_client_secret"
    )


@pytest.fixture()
def fixture_get_token_json_response() -> dict:
    return {
        "access_token": "fixture_access_token",
        "refresh_token": "fixture_refresh_token",
        "expires_in": 100,
        "type": "fixture_type",
        "scopes": "fixture_scopes"
    }


@pytest.fixture()
def fixture_list_banks_json_response() -> dict:
    return {
        "data": {
            "itens": [
                {
                    "id_instituicao": "fixture_institution_id",
                    "nome_instituicao": "fixture_institution_name",
                    "nome_instituicao_abreviado": "fixture_institution_short_name",
                    "ispb": "fixture_ispb",
                    "cnpj": "fixture_cnpj"
                }
            ]
        }
    }


@pytest.fixture()
def fixture_invalid_json_response() -> dict:
    return {
        "invalid": "invalid"
    }
