from abc import ABC, abstractmethod


class FileWriterInterface(ABC):

    @abstractmethod
    def write_certificate_file(self, content: str) -> str:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def write_private_key_file(self, content: str) -> str:
        raise NotImplementedError("Method not implemented")
