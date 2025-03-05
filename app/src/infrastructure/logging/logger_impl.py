from app.src.application.logging.logger_interface import LoggerInterface


class PowertoolsLogger(LoggerInterface):

    def __init__(self):
        super().__init__()

    def info(self, message: str) -> None:
        pass

    def debug(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass
