import os

import requests
from pydantic import ValidationError

from src.application.clients.dto.secret_dto import SecretDTO
from src.application.clients.interface.authorization_client_interace import AuthorizationClientInterface
from src.application.exceptions.failed_get_secret_exception import FailedGetSecretException
from src.application.logging.logger_interface import LoggerInterface
from src.infrastructure.clients.dto.get_token_response_dto import GetTokenResponseDTO


class AuthorizationClientImpl(AuthorizationClientInterface):
    TOKEN_URL = "/token"

    def __init__(self, logger: LoggerInterface):
        self.__logger = logger
        self.__base_url = os.environ.get("AUTHORIZATION_CLIENT_BASE_URL")

    def get_token(self, secret: SecretDTO) -> str:
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(
                url=f"{self.__base_url}{self.TOKEN_URL}",
                headers=headers,
                verify=False,
            )

            response.raise_for_status()

            token_dto = GetTokenResponseDTO.model_validate(response.json())

            return token_dto.access_token
        except (requests.HTTPError, ValueError, ValidationError) as ex:
            self.__logger.error(
                f"[BankClientImpl] Error fetching bank list. URL: {self.__base_url}{self.TOKEN_URL}, "
                f"Headers: {headers}, Exception: {ex}"
            )
            raise FailedGetSecretException
