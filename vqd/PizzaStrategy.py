from abc import ABC, abstractmethod

from vqd.optimizer import PizzaInput, PizzaResult


class PizzaStrategy(ABC):

    @abstractmethod
    def apply(self, input_data: PizzaInput) -> PizzaResult:
        pass
