from abc import abstractmethod, ABC

from src.application.clients.dto.secret_dto import SecretDTO


class SecretClientInterface(ABC):

    @abstractmethod
    def get_secret(self) -> SecretDTO:
        raise NotImplementedError("Method not implemented")
