from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.simulator.simulator import Simulator
from qualifier.simulatorV4.simulator_v4 import SimulatorV4
from qualifier.strategy import Strategy


class RandomStrategy(Strategy):
    def __init__(self, strategy, seed=27, tries=100):
        super().__init__(seed)
        self.tries = tries
        self._strategy = strategy
        self.name = f'RandomStrategy on {strategy.name}'

    def solve(self, input: InputData) -> OutputData:
        best_score = 0
        best_result = None
        best_seed = None

        for i in range(1, self.tries + 1):
            seed = self.random.randint(0, 1_000_000)

            strategy = self._strategy(seed=seed)
            result = strategy.solve(input)
            score = SimulatorV4(input).run(result)  # still a bug in v4 with reruns...
            print(f'Score try {i}/{self.tries}:{score}')
            if score > best_score:
                best_score = score
                best_seed = seed
                best_result = result
                result.save(f'intermediate_random_result_{score:09}.out')

        print(f""" Best seed: {best_seed}
        Best score: {best_score}
        Best result: {best_result}
        """)

        return best_result
