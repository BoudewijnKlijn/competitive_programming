from abc import abstractmethod, ABC
from typing import Iterable

from valcon import OutputData, InputData


class Scorer(ABC):

    @abstractmethod
    def __init__(self, input_data: InputData):
        pass

    @abstractmethod
    def calculate(self, output_data: OutputData) -> int:
        """ calculates score of the output data """
        pass

    @abstractmethod
    def calculate_multi(self, multi_output_data: Iterable[OutputData]) -> Iterable[int]:
        """Calculate score multiple times, once for each output data."""
        raise NotImplementedError
