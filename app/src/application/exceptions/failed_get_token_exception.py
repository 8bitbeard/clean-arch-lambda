from http import HTTPStatus

from src.application.enums.application_code import ApplicationCode


class FailedGetTokenException(Exception):
    def __init__(
            self,
            code: ApplicationCode = ApplicationCode.BL_TOKEN_FAILURE,
            message: str = "Failed to get authorization token",
            status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{code}] {message} (Status: {status_code})")
