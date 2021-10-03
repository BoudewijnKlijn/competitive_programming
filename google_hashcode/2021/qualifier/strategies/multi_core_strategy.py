import multiprocessing
from typing import Callable

from qualifier.input_data import InputData
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
