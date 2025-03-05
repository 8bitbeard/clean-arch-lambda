from decimal import Decimal

from pydantic import BaseModel


class LambdaHeadersRequestDTO(BaseModel):
    correlation_id: str
    flow_id: str


class PaymentRequestDTO(BaseModel):
    amount: Decimal


class BankAccountRequestDTO(BaseModel):
    id: str
    name: str
    ispb: str


class LambdaBodyRequestDTO(BaseModel):
    payment: PaymentRequestDTO
    account: BankAccountRequestDTO


class LambdaRequestDTO(BaseModel):
    headers: LambdaHeadersRequestDTO
    body: LambdaBodyRequestDTO
