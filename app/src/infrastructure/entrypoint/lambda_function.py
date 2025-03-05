import os
import uuid

from src.application.usecases.impl.fetch_bank_list_impl import FetchBankListUseCaseImpl
from src.infrastructure.clients.impl.authorization_client_impl import AuthorizationClientImpl
from src.infrastructure.clients.impl.bank_client_impl import BankClientImpl
from src.infrastructure.clients.impl.secret_client_impl import SecretClientImpl
from src.infrastructure.clients.impl.storage_client_impl import StorageClientImpl
from src.infrastructure.entrypoint.handler.exception_handler import exception_handler
from src.infrastructure.logging.logger_impl import PowertoolsLogger
from src.infrastructure.entrypoint.dto.lambda_response_dto import LambdaResponseDTO, BodyDTO, DataDTO

logger = PowertoolsLogger()


def inject_dependencies():
    secret_client = SecretClientImpl(logger)
    authorization_client = AuthorizationClientImpl(logger)
    bank_client = BankClientImpl(logger)
    storage_client = StorageClientImpl(logger)

    return FetchBankListUseCaseImpl(logger, secret_client, authorization_client, bank_client, storage_client)


@exception_handler(logger)
# @logger.inject_lambda_context()
def lambda_handler(event, context):
    correlation_id = str(uuid.uuid4())
    flow_id = os.environ.get("flow_id", str(uuid.uuid4()))

    fetch_bank_list_use_case = inject_dependencies()
    fetch_bank_list_use_case.execute(correlation_id, flow_id)

    response = LambdaResponseDTO(
        status_code=200,
        body=BodyDTO(
            data=DataDTO(
                status="SUCCESS"
            )
        )
    )

    return response.model_dump_json()
