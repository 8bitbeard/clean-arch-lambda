from decimal import Decimal

from src.domain.enums.payment_status import PaymentStatus
from src.domain.models.payment_model import PaymentModel
from src.domain.services.interface.payment_service_interface import PaymentServiceInterface


class PaymentServiceImpl(PaymentServiceInterface):

    PAYMENT_LIMIT_AMOUNT = Decimal("3000.0")

    def __init__(self):
        pass

    def check_if_payment_value_is_eligible(self, amount: Decimal) -> bool:
        return amount <= self.PAYMENT_LIMIT_AMOUNT

    def check_if_payment_is_done(self, payment: PaymentModel) -> bool:
        return payment.status == PaymentStatus.SUCCEEDED