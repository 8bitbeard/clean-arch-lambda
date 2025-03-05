from abc import ABC, abstractmethod
from typing import List

from src.domain.models.bank_model import BankModel


class BankClientInterface(ABC):

    @abstractmethod
    def list_banks(
            self, access_token: str, app_id: str, correlation_id: str, flow_id: str
    ) -> List[BankModel]:
        raise NotImplementedError("Method not implemented")
