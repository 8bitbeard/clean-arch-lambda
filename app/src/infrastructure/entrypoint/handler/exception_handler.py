from functools import wraps
from http import HTTPStatus

from src.application.enums.application_code import ApplicationCode
from src.application.exceptions.failed_get_secret_exception import FailedGetSecretException
from src.application.exceptions.failed_get_token_exception import FailedGetTokenException
from src.application.exceptions.failed_list_banks_exception import FailedListBanksException
from src.application.exceptions.failed_save_data_exception import FailedSaveDataException
from src.application.logging.logger_interface import LoggerInterface
from src.infrastructure.entrypoint.dto.lambda_response_dto import LambdaResponseDTO, ErrorDTO, BodyDTO


def exception_handler(logger: LoggerInterface):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context, *args, **kwargs):
            try:
                return func(event, context, *args, **kwargs)
            except (
                    FailedGetSecretException, FailedGetTokenException, FailedListBanksException, FailedSaveDataException
            ) as ex:
                logger.error(f"[exception_handler]: Catched exception {str(ex)}")
                error_dto = ErrorDTO(
                    code=ex.code,
                    message=ex.message
                )
                body_dto = BodyDTO(error=error_dto)
                return LambdaResponseDTO(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    body=body_dto
                )
            except Exception as e:
                logger.error(f"[exception_handler]: {str(e)}")
                error_dto = ErrorDTO(
                    code=ApplicationCode.BL_INTERNAL_SERVER_ERROR.value,
                    message="Internal server error"
                )
                body_dto = BodyDTO(error=error_dto)
                return LambdaResponseDTO(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    body=body_dto
                )

        return wrapper

    return decorator
