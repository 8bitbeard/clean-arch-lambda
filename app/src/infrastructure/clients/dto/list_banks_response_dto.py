from typing import List
from pydantic import BaseModel, Field


class Institution(BaseModel):
    institution_id: str = Field(alias="id_instituicao")
    institution_name: str = Field(alias="nome_instituicao")
    institution_short_name: str = Field(alias="nome_instituicao_abreviado")
    ispb: str
    cnpj: str


class BankListResponse(BaseModel):
    items: List[Institution] = Field(alias="itens")


class ListBanksResponseDTO(BaseModel):
    data: BankListResponse
