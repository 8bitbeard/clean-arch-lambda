from unittest.mock import Mock

import pytest

from src.application.usecases.impl.create_payment_use_case_impl import CreatePaymentUseCaseImpl


def test_secret_client_raises_exception():
    logger = Mock()
    secret_client = Mock()
    secret_client.get_secret.side_effect = Exception("Test Exception")
    authorization_client = Mock()
    bank_client = Mock()
    storage_client = Mock()

    sut = CreatePaymentUseCaseImpl(logger, secret_client, authorization_client, bank_client, storage_client)

    with pytest.raises(Exception):
        sut.execute("fake_correlation_id", "fake_flow_id")

    secret_client.get_secret.assert_called_once()
    authorization_client.get_token.assert_not_called()
    bank_client.list_banks.assert_not_called()
    storage_client.save_data.assert_not_called()


def test_authorization_client_raises_exception():
    logger = Mock()
    secret_client = Mock()
    authorization_client = Mock()
    authorization_client.get_token.side_effect = Exception("Test Exception")
    bank_client = Mock()
    storage_client = Mock()

    sut = CreatePaymentUseCaseImpl(logger, secret_client, authorization_client, bank_client, storage_client)

    with pytest.raises(Exception):
        sut.execute("fake_correlation_id", "fake_flow_id")

    secret_client.get_secret.assert_called_once()
    authorization_client.get_token.assert_called_once()
    bank_client.list_banks.assert_not_called()
    storage_client.save_data.assert_not_called()


def test_bank_client_raises_exception():
    logger = Mock()
    secret_client = Mock()
    authorization_client = Mock()
    bank_client = Mock()
    bank_client.list_banks.side_effect = Exception("Test Exception")
    storage_client = Mock()

    sut = CreatePaymentUseCaseImpl(logger, secret_client, authorization_client, bank_client, storage_client)

    with pytest.raises(Exception):
        sut.execute("fake_correlation_id", "fake_flow_id")

    secret_client.get_secret.assert_called_once()
    authorization_client.get_token.assert_called_once()
    bank_client.list_banks.assert_called_once()
    storage_client.save_data.assert_not_called()


def test_storage_client_raises_exception():
    logger = Mock()
    secret_client = Mock()
    authorization_client = Mock()
    bank_client = Mock()
    storage_client = Mock()
    storage_client.save_data.side_effect = Exception("Test Exception")

    sut = CreatePaymentUseCaseImpl(logger, secret_client, authorization_client, bank_client, storage_client)

    with pytest.raises(Exception):
        sut.execute("fake_correlation_id", "fake_flow_id")

    secret_client.get_secret.assert_called_once()
    authorization_client.get_token.assert_called_once()
    bank_client.list_banks.assert_called_once()
    storage_client.save_data.assert_called_once()
