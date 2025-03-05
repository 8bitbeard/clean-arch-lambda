import os

from app.src.application.clients.dto.secret_dto import SecretDTO
from app.src.application.clients.interface.secret_client_interface import SecretClientInterface
from app.src.application.exceptions.failed_get_secret_exception import (
    FailedGetSecretException,
)
from app.src.application.logging.logger_interface import LoggerInterface


class SecretClientImpl(SecretClientInterface):

    def __init__(self, logger: LoggerInterface):
        self.__logger = logger

    def get_secret(self) -> SecretDTO:
        try:
            client_id = os.environ["CLIENT_ID"]
            client_secret = os.environ["CLIENT_SECRET"]

            return SecretDTO(client_id=client_id, client_secret=client_secret)
        except KeyError as ex:
            self.__logger.error(
                f"[SecretClientImpl] Error fetching secrets. Exception: {ex}"
            )
            raise FailedGetSecretException
