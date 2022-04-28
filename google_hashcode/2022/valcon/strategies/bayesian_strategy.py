from typing import Callable

from valcon import Strategy, InputData, OutputData
from bayes_opt import BayesianOptimization

from valcon.scorer import Scorer


class BayesianStrategy(Strategy):

    def __init__(self, seed, strategy: Callable, parameter_bounds: dict, scorer: Scorer):
        super().__init__(seed)

        self.scorer = scorer
        self.strategy = strategy
        self.parameter_bounds = parameter_bounds

        self.input_data = None

    def _black_box(self, **kwargs):
        strategy = self.strategy(**kwargs)
        solution = strategy.solve(self.input_data)
        return self.scorer.calculate(solution)

    def solve(self, input_data: InputData) -> OutputData:
        self.input_data = input_data

        optimizer = BayesianOptimization(
            f=self._black_box,
            pbounds=self.parameter_bounds,
            random_state=self.seed,
        )

        optimizer.maximize(n_iter=100)

        print(optimizer.max)
        best = self.strategy(**optimizer.max['params'])
        return best.solve(input_data)
