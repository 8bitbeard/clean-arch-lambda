from http import HTTPStatus
from app.src.application.enums.application_code import ApplicationCode


class FailedListBanksException(Exception):
    def __init__(
        self,
        code: ApplicationCode = ApplicationCode.BL_LIST_BANKS_FAILURE,
        message: str = "Failed to get the list of banks",
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{code}] {message} (Status: {status_code})")
