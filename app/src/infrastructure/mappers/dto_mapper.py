from typing import List

from app.src.domain.models.bank_model import BankModel
from app.src.domain.models.metadata_model import MetadataModel
from app.src.infrastructure.clients.dto.storage_client_request_dto import StorageClientRequestDTO, MetadataDTO, \
    BankItemDTO


def bank_model_list_and_metadata_to_save_data_request_dto(
        metadata_model: MetadataModel,
        bank_model_list: List[BankModel]
) -> StorageClientRequestDTO:
    return StorageClientRequestDTO(
        metadados=MetadataDTO(
            data=metadata_model.date
        ),
        itens=[
            BankItemDTO(
                codigo=bank_model.id,
                nome=bank_model.name,
                ispb=bank_model.ispb
            ) for bank_model in bank_model_list
        ]
    )