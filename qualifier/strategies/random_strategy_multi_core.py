import multiprocessing
from collections import Callable

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.strategy import Strategy


class MultiCoreStrategy(Strategy):
    SIMULATORS = dict()

    @classmethod
    def _worker_initializer(cls, simulator: Callable, input_data):
        worker_name = multiprocessing.current_process().name
        cls.SIMULATORS[worker_name] = simulator(input_data=input_data)

    @classmethod
    def _worker_func(cls, work):
        worker_name = multiprocessing.current_process().name
        return cls.SIMULATORS[worker_name].run(work)

    def __init__(self, simulator_class: Callable, input_data: InputData, seed=27, jobs=6):
        super().__init__(seed=seed)
        self.jobs = jobs
        self.pool = multiprocessing.Pool(self.jobs, initializer=MultiCoreStrategy._worker_initializer,
                                         initargs=(simulator_class, input_data))

    def __del__(self):
        self.pool.close()


class RandomStrategyMultiCore(MultiCoreStrategy):
    def __init__(self, strategy, simulator, input_data, seed=27, tries=100):
        super().__init__(simulator, input_data, seed=seed)
        self.tries = tries
        self._strategy = strategy
        self._simulator = simulator
        self.name = f'RandomStrategy on {strategy.name}'

    def solve(self, input: InputData) -> OutputData:
        results = []

        print(f'Making solutions (1 job)')
        for _ in range(self.tries):
            seed = self.random.randint(0, 100_000_000)
            strategy = self._strategy(seed=seed)
            results.append((strategy.solve(input), seed))

        outputs = [result[0] for result in results]

        print(f'Simulationg soltions ({self.jobs} jobs)')
        simulation_results = self.pool.map(RandomStrategyMultiCore._worker_func, outputs)
        scores = [score for score, output in simulation_results]
        final_results = list(zip(results, scores))
        final_results.sort(key=lambda x: x[1], reverse=True)

        print(f'best seed: {final_results[0][0][1]}\nScore: {final_results[0][1]}')

        return final_results[0][0][0]
