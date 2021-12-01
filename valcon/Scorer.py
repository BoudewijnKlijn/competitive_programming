from abc import abstractmethod, ABC

from valcon import OutputData, InputData


class Scorer(ABC):

    @abstractmethod
    def __init__(self, input_data: InputData):
        pass

    @abstractmethod
    def calculate(self, output_data: OutputData)->int:
        """ calculates score of the output data """
        pass