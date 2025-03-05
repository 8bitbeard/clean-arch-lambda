import re

import pytest
from pydantic import ValidationError

from app.src.domain.models.metadata_model import MetadataModel


def test_create_new_metadata_model_instance_with_default_value():
    sut = MetadataModel()

    assert sut.date is not None
    assert re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$', sut.date)


def test_create_new_metadata_model_instance_with_custom_value():
    custom_date = "2025-03-01T21:59:59"
    sut = MetadataModel(date=custom_date)

    assert sut.date == custom_date


def test_create_new_metadata_model_instance_raises_exception_with_wrong_value():
    custom_date = "wrong_value"

    with pytest.raises(ValidationError):
        sut = MetadataModel(date=custom_date)
