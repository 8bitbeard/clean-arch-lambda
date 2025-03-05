from http import HTTPStatus

from src.application.enums.application_code import ApplicationCode


class InvalidLambdaRequestEventException(Exception):
    def __init__(
            self,
            code: ApplicationCode = ApplicationCode.LAMBDA_BAD_REQUEST_ERROR,
            message: str = "Invalid lambda request event",
            status_code: int = HTTPStatus.BAD_REQUEST,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{code}] {message} (Status: {status_code})")
