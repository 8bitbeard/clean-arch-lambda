from pydantic import BaseModel

from src.domain.enums.payment_status import PaymentStatus


class PaymentModel(BaseModel):
    id: str
    status: PaymentStatus
    date: str
