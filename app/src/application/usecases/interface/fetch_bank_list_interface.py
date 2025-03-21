from abc import ABC, abstractmethod


class FetchBankListUseCaseInterface(ABC):

    @abstractmethod
    def execute(self, correlation_id: str, flow_id: str) -> None:
        raise NotImplementedError("Method not inmplemented")
