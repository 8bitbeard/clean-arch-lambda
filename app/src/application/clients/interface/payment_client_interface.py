from abc import ABC, abstractmethod
from typing import List

from src.domain.models.bank_model import BankModel
from src.domain.models.payment_model import PaymentModel


class PaymentClientInterface(ABC):

    @abstractmethod
    def post_payment(
            self,
            access_token: str,
            app_id: str,
            correlation_id: str,
            flow_id: str,
            certificate_file: str,
            private_key_file: str
    ) -> PaymentModel:
        raise NotImplementedError("Method not implemented")

    def get_payment_details(
            self,
            payment_id: str,
            access_token: str,
            app_id: str,
            correlation_id: str,
            flow_id: str,
            certificate_file: str,
            private_key_file: str
    ) -> PaymentModel:
        raise NotImplementedError("Method not implemented")
