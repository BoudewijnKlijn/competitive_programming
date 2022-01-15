from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy


class Repeat(Strategy):
    def __init__(self, n_repetitions, strategy):
        """
        Repeat a strategy n_repetitions times.
        :param n_repetitions: number of times to repeat the RandomClients strategy
        :param strategy: strategy to repeat
        """
        super().__init__()
        self.n_repetitions = n_repetitions
        self.strategy = strategy

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        best_score = None
        best_pizza = None
        scorer = PerfectPizzaScore(input_data)
        for _ in range(self.n_repetitions):
            pizza = self.strategy.solve(input_data)
            score = scorer.calculate(pizza)
            if best_score is None or score > best_score:
                best_score = score
                best_pizza = pizza
        return best_pizza
