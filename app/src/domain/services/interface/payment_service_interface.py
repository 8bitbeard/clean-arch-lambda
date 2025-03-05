from abc import abstractmethod, ABC
from decimal import Decimal

from src.domain.models.payment_model import PaymentModel


class PaymentServiceInterface(ABC):

    @abstractmethod
    def check_if_payment_value_is_eligible(self, amount: Decimal) -> bool:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def check_if_payment_is_done(self, payment: PaymentModel) -> bool:
        raise NotImplementedError("Method not implemented")
