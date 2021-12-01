from abc import ABC, abstractmethod

from valcon import OutputData, InputData


class Strategy(ABC):

    @abstractmethod
    def solve(self, input: InputData) -> OutputData:
        pass