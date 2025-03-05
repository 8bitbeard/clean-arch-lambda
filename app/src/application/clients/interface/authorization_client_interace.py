from abc import ABC, abstractmethod

from app.src.application.clients.dto.secret_dto import SecretDTO


class AuthorizationClientInterface(ABC):

    @abstractmethod
    def get_token(self, secret: SecretDTO) -> str:
        raise NotImplementedError("Method not implemented")
