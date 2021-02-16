from abc import ABC, abstractmethod


class PizzaInput:
    pass

class PizzaResult:
    pass

class PizzaStrategy(ABC):

    @abstractmethod
    def apply(self, input_data: PizzaInput)->PizzaResult:
        pass

class PizzaOptimizer:
    def __init__(self, strategy: PizzaStrategy):
        self.strategy = strategy

    def optimize(self, input_data: PizzaInput):
        result = self.strategy.apply(input_data)
