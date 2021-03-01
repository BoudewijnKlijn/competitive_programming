from typing import List

from qualifier.simulator.simulator_street import SimulatorStreet


class SimulatorCar:
    def __init__(self, path: List[SimulatorStreet]):
        self.path = path
        self.name = f'{path[0].name} to {path[-1].name}'

    def __str__(self):
        return self.name
