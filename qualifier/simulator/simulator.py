from abc import ABC, abstractmethod

from qualifier.output_data import OutputData


class Simulator(ABC):
    @abstractmethod
    def run(self, output_data: OutputData) -> (int, OutputData):
        raise NotImplementedError()
