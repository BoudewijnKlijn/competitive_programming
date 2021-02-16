from vqd.PizzaStrategy import PizzaStrategy


class PizzaInput:
    pass


class PizzaResult:
    pass


class MyOptimizer(PizzaStrategy):
    pass


class PizzaOptimizer:
    def __init__(self, strategy: PizzaStrategy):
        self.strategy = strategy

    def optimize(self, input_data: PizzaInput):
        result = self.strategy.apply(input_data)
