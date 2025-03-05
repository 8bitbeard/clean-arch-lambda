from unittest.mock import patch, Mock

import pytest
from botocore.exceptions import ClientError

from src.application.exceptions.failed_save_data_exception import FailedSaveDataException


@patch('src.infrastructure.clients.impl.storage_client_impl.boto3.client')
@patch('src.infrastructure.clients.impl.storage_client_impl.bank_model_list_and_metadata_to_save_data_request_dto')
def test_save_data_successful(
        mock_mapper, mock_boto3_client, fixture_storage_client, fixture_metadata_model, fixture_bank_model
):
    mock_request_dto = Mock()
    mock_request_dto.model_dump_json.return_value = '{"data": "test"}'

    mock_s3_client = Mock()
    mock_s3_client.put_object.return_value = None

    mock_metadata = fixture_metadata_model
    mock_bank_list = [fixture_bank_model]

    mock_boto3_client.return_value = mock_s3_client
    mock_mapper.return_value = mock_request_dto

    fixture_storage_client.save_data(mock_metadata, mock_bank_list)

    mock_boto3_client.assert_called_once_with('s3')
    mock_mapper.assert_called_once_with(mock_metadata, mock_bank_list)
    mock_request_dto.model_dump_json.assert_called_once()
    mock_s3_client.put_object.assert_called_once_with(
        Bucket="my-bucket-name",
        Key="BankList/data.json",
        Body='{"data": "test"}',
        ContentType="application/json"
    )
    fixture_storage_client._StorageClientImpl__logger.error.assert_not_called()


@patch('src.infrastructure.clients.impl.storage_client_impl.boto3.client')
@patch('src.infrastructure.clients.impl.storage_client_impl.bank_model_list_and_metadata_to_save_data_request_dto')
def test_save_data_client_error(
        mock_mapper, mock_boto3_client, fixture_storage_client, fixture_metadata_model, fixture_bank_model
):
    mock_request_dto = Mock()
    mock_request_dto.model_dump_json.return_value = '{"data": "test"}'

    mock_metadata = fixture_metadata_model
    mock_bank_list = [fixture_bank_model]

    mock_s3_client = Mock()
    mock_s3_client.put_object.side_effect = ClientError(
        {'Error': {'Code': 'TestError', 'Message': 'Test Error'}},
        'put_object'
    )

    mock_boto3_client.return_value = mock_s3_client
    mock_mapper.return_value = mock_request_dto

    with pytest.raises(FailedSaveDataException):
        fixture_storage_client.save_data(mock_metadata, mock_bank_list)

    mock_boto3_client.assert_called_once_with('s3')
    mock_mapper.assert_called_once_with(mock_metadata, mock_bank_list)
    mock_request_dto.model_dump_json.assert_called_once()
    mock_s3_client.put_object.assert_called_once_with(
        Bucket="my-bucket-name",
        Key="BankList/data.json",
        Body='{"data": "test"}',
        ContentType="application/json"
    )
    fixture_storage_client._StorageClientImpl__logger.error.assert_called_once()
    call_args = fixture_storage_client._StorageClientImpl__logger.error.call_args[0][0]
    assert "Error saving data to s3 bucket" in call_args
    assert "TestError" in call_args


@patch('src.infrastructure.clients.impl.storage_client_impl.boto3.client')
@patch('src.infrastructure.clients.impl.storage_client_impl.bank_model_list_and_metadata_to_save_data_request_dto')
def test_save_data_mapper_error(
        mock_mapper, mock_boto3_client, fixture_storage_client, fixture_metadata_model, fixture_bank_model
):
    mock_mapper.side_effect = ValueError("Mapping error")
    mock_s3_client = Mock()
    mock_boto3_client.return_value = mock_s3_client

    mock_metadata = fixture_metadata_model
    mock_bank_list = [fixture_bank_model]

    with pytest.raises(FailedSaveDataException):
        fixture_storage_client.save_data(mock_metadata, mock_bank_list)

    mock_mapper.assert_called_once_with(mock_metadata, mock_bank_list)
    mock_boto3_client.assert_not_called()
    fixture_storage_client._StorageClientImpl__logger.error.assert_called_once()
    call_args = fixture_storage_client._StorageClientImpl__logger.error.call_args[0][0]
    assert "Error saving data to s3 bucket" in call_args
    assert "Mapping error" in call_args
