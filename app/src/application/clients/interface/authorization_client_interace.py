from abc import ABC, abstractmethod

from src.application.clients.dto.secret_dto import SecretDTO


class AuthorizationClientInterface(ABC):

    @abstractmethod
    def get_token(self, secret: SecretDTO, certificate_file: str, private_key_file: str) -> str:
        raise NotImplementedError("Method not implemented")
