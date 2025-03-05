from abc import ABC, abstractmethod
from typing import List

from src.domain.models.bank_model import BankModel
from src.domain.models.metadata_model import MetadataModel


class StorageClientInterface(ABC):

    @abstractmethod
    def save_data(self, metadata: MetadataModel, items: List[BankModel]) -> None:
        raise NotImplementedError("Method not implemented")
