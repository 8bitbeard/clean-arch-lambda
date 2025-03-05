from pydantic import ValidationError

from src.application.exceptions.invalid_lambda_request_event_exception import InvalidLambdaRequestEventException
from src.application.usecases.impl.create_payment_use_case_impl import CreatePaymentUseCaseImpl
from src.infrastructure.clients.impl.authorization_client_impl import AuthorizationClientImpl
from src.infrastructure.clients.impl.bank_client_impl import PaymentClientImpl
from src.infrastructure.clients.impl.secret_client_impl import SecretClientImpl
from src.infrastructure.clients.impl.storage_client_impl import FileWriterImpl
from src.infrastructure.entrypoint.dto.lambda_request_dto import LambdaRequestDTO
from src.infrastructure.entrypoint.dto.lambda_response_dto import LambdaResponseDTO, BodyDTO, DataDTO
from src.infrastructure.entrypoint.handler.exception_handler import exception_handler
from src.infrastructure.logging.logger_impl import PowertoolsLogger

logger = PowertoolsLogger()


def inject_dependencies():
    secret_client = SecretClientImpl(logger)
    authorization_client = AuthorizationClientImpl(logger)
    bank_client = PaymentClientImpl(logger)
    storage_client = FileWriterImpl(logger)

    return CreatePaymentUseCaseImpl(logger, secret_client, authorization_client, bank_client, storage_client)


@exception_handler(logger)
# @logger.inject_lambda_context()
def lambda_handler(event: dict, context):
    try:
        lambda_request_dto = LambdaRequestDTO.model_validate(event)

        create_payment_use_case = inject_dependencies()
        create_payment_use_case.execute(lambda_request_dto.headers.correlation_id, lambda_request_dto.headers.flow_id)

        response = LambdaResponseDTO(
            status_code=200,
            body=BodyDTO(
                data=DataDTO(
                    status="SUCCESS"
                )
            )
        )

        return response.model_dump_json()
    except ValidationError as ex:
        raise InvalidLambdaRequestEventException()
