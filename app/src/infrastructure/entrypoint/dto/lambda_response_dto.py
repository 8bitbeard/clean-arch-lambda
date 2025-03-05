from typing import Optional

from pydantic import BaseModel


class DataDTO(BaseModel):
    status: str


class ErrorDTO(BaseModel):
    code: str
    message: str


class BodyDTO(BaseModel):
    data: Optional[DataDTO] = None
    error: Optional[ErrorDTO] = None


class LambdaResponseDTO(BaseModel):
    status_code: int
    body: BodyDTO
