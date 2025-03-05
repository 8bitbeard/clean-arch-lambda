from abc import ABC, abstractmethod


class LoggerInterface(ABC):

    @abstractmethod
    def info(self, message: str) -> None:
        raise NotImplemented("Method not implemented")

    @abstractmethod
    def debug(self, message: str) -> None:
        raise NotImplemented("Method not implemented")

    @abstractmethod
    def error(self, message: str) -> None:
        raise NotImplemented("Method not implemented")
