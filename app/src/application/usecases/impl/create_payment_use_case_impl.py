import time

from src.application.clients.interface.authorization_client_interace import AuthorizationClientInterface
from src.application.clients.interface.file_writer_interface import FileWriterInterface
from src.application.clients.interface.payment_client_interface import PaymentClientInterface
from src.application.clients.interface.secret_client_interface import SecretClientInterface
from src.application.logging.logger_interface import LoggerInterface
from src.application.usecases.interface.create_payment_use_case_interface import (
    CreatePaymentUseCaseInterface,
)
from src.domain.services.interface.payment_service_interface import PaymentServiceInterface


class CreatePaymentUseCaseImpl(CreatePaymentUseCaseInterface):

    def __init__(
            self,
            logger: LoggerInterface,
            secret_client: SecretClientInterface,
            file_writer_client: FileWriterInterface,
            authorization_client: AuthorizationClientInterface,
            payment_client: PaymentClientInterface,
            payment_service: PaymentServiceInterface
    ):
        self.__logger = logger
        self.__secret_client = secret_client
        self.__file_writer_client = file_writer_client
        self.__authorization_client = authorization_client
        self.__payment_client = payment_client
        self.__payment_service = payment_service

    def execute(self, correlation_id: str, flow_id: str) -> None:
        secret_dto = self.__secret_client.get_secret()

        certificate_file = self.__file_writer_client.write_certificate_file(secret_dto.certificate)
        private_key_file = self.__file_writer_client.write_private_key_file(secret_dto.private_key)

        access_token = self.__authorization_client.get_token(secret_dto, certificate_file, private_key_file)

        app_id = secret_dto.client_id

        created_payment_model = self.__payment_client.post_payment(
            access_token, app_id, correlation_id, flow_id, certificate_file, private_key_file
        )

        for _ in range(5):
            payment_detail_model = self.__payment_client.get_payment_details(
                created_payment_model.id,
                access_token,
                app_id,
                correlation_id,
                flow_id,
                certificate_file,
                private_key_file
            )
            if self.__payment_service.check_if_payment_is_done(payment_detail_model):
                pass
            time.sleep(1)

        self.__storage_client.write_certificate_file(metadata_model, bank_model_list)
