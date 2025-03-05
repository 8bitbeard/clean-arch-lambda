from src.domain.models.bank_model import BankModel


def test_create_new_bank_model_instance():
    test_id = "12345"
    test_name = "fake bank"
    test_ispb = "3982903812"

    sut = BankModel(id=test_id, name=test_name, ispb=test_ispb)

    assert sut.id == test_id
    assert sut.name == test_name
    assert sut.ispb == test_ispb
