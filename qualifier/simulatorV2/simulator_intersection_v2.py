from typing import List

from qualifier.schedule import Schedule
from qualifier.simulatorV2.simulator_street_v2 import SimulatorStreetV2


class SimulatorIntersectionV2:
    def __init__(self, streets: List[SimulatorStreetV2]):
        self.actual_streets = {street.name: street for street in streets}

    def apply_schedule(self, schedule: Schedule):
        start = 0
        end = 0

        duration_data = []
        for street, duration in schedule.street_duration_tuples:
            if duration == 0:
                continue

            end = start + duration
            duration_data.append((street, start, end))
            start = end

        total_duration = end
        for data in duration_data:
            self.actual_streets[data[0]].set_schedule(total_duration, data[1], data[2])
