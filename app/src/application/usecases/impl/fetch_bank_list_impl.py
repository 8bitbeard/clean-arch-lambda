from app.src.application.clients.interface.authorization_client_interace import AuthorizationClientInterface
from app.src.application.clients.interface.bank_client_interface import BankClientInterface
from app.src.application.clients.interface.secret_client_interface import SecretClientInterface
from app.src.application.clients.interface.storage_client_interface import StorageClientInterface
from app.src.application.logging.logger_interface import LoggerInterface
from app.src.application.usecases.interface.fetch_bank_list_interface import (
    FetchBankListUseCaseInterface,
)
from app.src.domain.models.metadata_model import MetadataModel


class FetchBankListUseCaseImpl(FetchBankListUseCaseInterface):

    def __init__(
            self,
            logger: LoggerInterface,
            secret_client: SecretClientInterface,
            authorization_client: AuthorizationClientInterface,
            bank_client: BankClientInterface,
            storage_client: StorageClientInterface,
    ):
        self.__logger = logger
        self.__secret_client = secret_client
        self.__authorization_client = authorization_client
        self.__bank_client = bank_client
        self.__storage_client = storage_client

    def execute(self, correlation_id: str, flow_id: str) -> None:
        secret_dto = self.__secret_client.get_secret()
        access_token = self.__authorization_client.get_token(secret_dto)
        app_id = secret_dto.client_id

        bank_model_list = self.__bank_client.list_banks(
            access_token, app_id, correlation_id, flow_id
        )
        metadata_model = MetadataModel()

        self.__storage_client.save_data(metadata_model, bank_model_list)
