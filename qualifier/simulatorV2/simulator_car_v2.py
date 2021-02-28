from typing import List

from qualifier.simulatorV2.simulator_street_v2 import SimulatorStreetV2


class SimulatorCarV2:
    def __init__(self, path: List[SimulatorStreetV2]):
        self.path = path
        self.name = f'{path[0].name} to {path[-1].name}'

    def __str__(self):
        return self.name
