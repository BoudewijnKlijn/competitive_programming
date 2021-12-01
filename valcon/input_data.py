from abc import ABC, abstractmethod


class InputData(ABC):
    """ input data abstract class for all hash code events"""

    @abstractmethod
    def load_data(self, file_name: str):
        """ load data from file """
        pass


