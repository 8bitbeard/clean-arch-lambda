from typing import List

from pydantic import BaseModel, Field


class CustomConfigBaseModel(BaseModel):
    class Config:
        populate_by_name = True


class MetadataDTO(CustomConfigBaseModel):
    date: str = Field(..., alias="data")


class BankItemDTO(CustomConfigBaseModel):
    id: str = Field(..., alias="codigo")
    name: str = Field(..., alias="nome")
    ispb: str = Field(..., alias="ispb")


class StorageClientRequestDTO(CustomConfigBaseModel):
    metadata: MetadataDTO = Field(..., alias="metadados")
    items: List[BankItemDTO] = Field(..., alias="itens")
