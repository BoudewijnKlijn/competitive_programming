from abc import ABC, abstractmethod


class OutputData(ABC):

    @abstractmethod
    def save(self, filename: str):
        """ saves file ready for submission """
        pass
