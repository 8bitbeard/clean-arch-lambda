import os

import requests
from pydantic.v1 import ValidationError

from app.src.application.clients.interface.bank_client_interface import BankClientInterface
from app.src.application.exceptions.failed_list_banks_exception import (
    FailedListBanksException,
)
from app.src.application.logging.logger_interface import LoggerInterface
from app.src.infrastructure.clients.dto.list_banks_response_dto import (
    ListBanksResponseDTO,
)


class BankClientImpl(BankClientInterface):
    LIST_BANKS_URL = "/institutions"

    def __init__(self, logger: LoggerInterface):
        self.__logger = logger
        self.__base_url = os.environ.get("BANK_LIST_BASE_URL")

    def list_banks(
            self, access_token: str, app_id: str, correlation_id: str, flow_id: str
    ):
        headers = {
            "Content-Type": "application/json",
            "x-org-appid": app_id,
            "x-org-correlationID": correlation_id,
            "x-org-flowID": flow_id,
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(
                url=f"{self.__base_url}{self.LIST_BANKS_URL}",
                headers=headers,
                verify=False,
            )

            response.raise_for_status()

            return ListBanksResponseDTO.model_validate(response.json())
        except (requests.HTTPError, ValueError, ValidationError) as ex:
            self.__logger.error(
                f"[BankClientImpl] Error fetching bank list. URL: {self.__base_url}{self.LIST_BANKS_URL}, "
                f"Headers: {headers}, Exception: {ex}"
            )
            raise FailedListBanksException
