from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from src.infrastructure.clients.dto.storage_client_request_dto import StorageClientRequestDTO, MetadataDTO, \
    BankItemDTO
from src.infrastructure.mappers.dto_mapper import bank_model_list_and_metadata_to_save_data_request_dto


def test_bank_model_list_and_metadata_to_save_data_request_dto_success(fixture_metadata_model, fixture_bank_model):
    result = bank_model_list_and_metadata_to_save_data_request_dto(fixture_metadata_model, [fixture_bank_model])

    assert isinstance(result, StorageClientRequestDTO)
    assert isinstance(result.metadata, MetadataDTO)
    assert result.metadata.date == "2025-03-04T21:54:00"

    assert len(result.items) == 1
    assert isinstance(result.items[0], BankItemDTO)
    assert result.items[0].id == "fixture_bank_model_id"
    assert result.items[0].name == "fixture_bank_model_name"
    assert result.items[0].ispb == "fixture_bank_model_ispb"


def test_bank_model_list_and_metadata_to_save_data_request_dto_empty_list(fixture_metadata_model):
    result = bank_model_list_and_metadata_to_save_data_request_dto(fixture_metadata_model, [])

    assert isinstance(result, StorageClientRequestDTO)
    assert isinstance(result.metadata, MetadataDTO)
    assert result.metadata.date == "2025-03-04T21:54:00"
    assert len(result.items) == 0
    assert result.items == []


def test_bank_model_list_and_metadata_to_save_data_request_dto_none_values(fixture_metadata_model):
    bank_with_none = Mock()
    bank_with_none.id = None
    bank_with_none.name = None
    bank_with_none.ispb = None
    bank_list = [bank_with_none]

    with pytest.raises(ValidationError):
        result = bank_model_list_and_metadata_to_save_data_request_dto(fixture_metadata_model, bank_list)
