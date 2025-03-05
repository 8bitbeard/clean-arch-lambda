import pytest
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError
from app.src.application.exceptions.failed_list_banks_exception import FailedListBanksException
from app.src.infrastructure.clients.dto.list_banks_response_dto import ListBanksResponseDTO
from src.infrastructure.clients.impl.bank_client_impl import BankClientImpl


def test_list_banks_successful(
        fixture_bank_client, fixture_list_banks_json_response
):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fixture_list_banks_json_response
    mock_response.raise_for_status.return_value = None

    expected_headers = {
        "Content-Type": "application/json",
        "x-org-appid": "fake_app_id",
        "x-org-correlationID": "fake_correlation_id",
        "x-org-flowID": "fake_flow_id",
        "Authorization": "Bearer fake_access_token"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response

        result = fixture_bank_client.list_banks(
            "fake_access_token", "fake_app_id", "fake_correlation_id", "fake_flow_id"
        )

        assert isinstance(result, ListBanksResponseDTO)
        mock_get.assert_called_once_with(
            url="https://test-banks.com/institutions",
            headers=expected_headers,
            verify=False
        )
        fixture_bank_client._BankClientImpl__logger.error.assert_not_called()


def test_list_banks_http_error(
        fixture_bank_client, fixture_list_banks_json_response
):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = HTTPError("Bad Request")

    expected_headers = {
        "Content-Type": "application/json",
        "x-org-appid": "fake_app_id",
        "x-org-correlationID": "fake_correlation_id",
        "x-org-flowID": "fake_flow_id",
        "Authorization": "Bearer fake_access_token"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response

        with pytest.raises(FailedListBanksException):
            fixture_bank_client.list_banks(
                "fake_access_token", "fake_app_id", "fake_correlation_id", "fake_flow_id"
            )

        mock_get.assert_called_once_with(
            url="https://test-banks.com/institutions",
            headers=expected_headers,
            verify=False
        )
        fixture_bank_client._BankClientImpl__logger.error.assert_called_once()
        call_args = fixture_bank_client._BankClientImpl__logger.error.call_args[0][0]
        assert "Error fetching bank list" in call_args
        assert "https://test-banks.com/institutions" in call_args
        assert "Bad Request" in call_args


def test_list_banks_json_validation_error(
        fixture_bank_client, fixture_list_banks_json_response, fixture_invalid_json_response
):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fixture_invalid_json_response
    mock_response.raise_for_status.return_value = None

    expected_headers = {
        "Content-Type": "application/json",
        "x-org-appid": "fake_app_id",
        "x-org-correlationID": "fake_correlation_id",
        "x-org-flowID": "fake_flow_id",
        "Authorization": "Bearer fake_access_token"
    }

    with patch('requests.get') as mock_get, \
            patch.object(ListBanksResponseDTO, 'model_validate') as mock_validate:
        mock_get.return_value = mock_response
        mock_validate.side_effect = ValueError("Validation error")

        with pytest.raises(FailedListBanksException):
            fixture_bank_client.list_banks(
                "fake_access_token", "fake_app_id", "fake_correlation_id", "fake_flow_id"
            )

        mock_get.assert_called_once_with(
            url="https://test-banks.com/institutions",
            headers=expected_headers,
            verify=False
        )
        fixture_bank_client._BankClientImpl__logger.error.assert_called_once()


def test_list_banks_missing_base_url(
        fixture_bank_client, fixture_list_banks_json_response, fixture_invalid_json_response
):
    with pytest.MonkeyPatch.context() as mp:
        logger = Mock()
        mp.delenv("BANK_LIST_BASE_URL", raising=False)
        bank_client = BankClientImpl(logger)

        with patch('requests.get') as mock_get:
            mock_get.return_value = Mock(status_code=200)
            with pytest.raises(FailedListBanksException):
                bank_client.list_banks(
                    "fake_access_token", "fake_app_id", "fake_correlation_id", "fake_flow_id"
                )
            mock_get.assert_called_once()
