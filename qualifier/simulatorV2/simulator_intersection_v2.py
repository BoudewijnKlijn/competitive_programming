from typing import List

from qualifier.schedule import Schedule
from qualifier.simulatorV2.simulator_street_v2 import SimulatorStreetV2


class SimulatorIntersectionV2:
    def __init__(self, intersection: int, streets: List[SimulatorStreetV2]):
        self.intersection_number = intersection
        self.schedule = []
        self.streets = []
        self.schedule_duration = 0
        self.actual_streets = {street.name: street for street in streets}
        self.green = 0

    def apply_schedule(self, schedule: Schedule):
        start = 0
        end = 0
        duration_data = []
        for index, (street, duration) in enumerate(schedule.street_duration_tuples):
            end = start + duration
            start = end
            duration_data.append((street, start, end))

        total_duration = end
        for data in duration_data:
            self.actual_streets[data[0]].set_schedule(total_duration, data[1], data[2])

    def _get_green(self, time):
        return self.schedule[time % self.schedule_duration]

    def execute_timestep(self, time):
        green = self._get_green(time)

        self.streets[self.green].set_green_light(False)
        self.streets[green].set_green_light(True)
        self.green = green
