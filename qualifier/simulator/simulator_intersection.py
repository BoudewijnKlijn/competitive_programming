from typing import List

from qualifier.input_data import Intersection
from qualifier.schedule import Schedule
from qualifier.simulator.simulator_street import SimulatorStreet


class SimulatorIntersection:
    def __init__(self, intersection: int, streets: List[SimulatorStreet]):
        self.intersection_number = intersection
        self.schedule = []
        self.streets = []
        self.schedule_duration = None
        self.actual_streets = {street.name: street for street in streets}
        self.green = 0

    def add_schedule(self, schedule: Schedule):
        for index, (street, duration) in enumerate(schedule.street_duration_tuples):
            if duration == 0:
                continue

            self.schedule += [index] * duration
            self.streets.append(self.actual_streets[street])

        self.schedule_duration = len(self.schedule)

    def _is_green(self, street, time):
        return street == self.schedule[time % self.schedule_duration]

    def _get_green(self, time):
        return self.schedule[time % self.schedule_duration]

    def execute_timestep(self, time):
        green = self._get_green(time)

        self.streets[self.green].set_green_light(False)
        self.streets[green].set_green_light(True)
        self.green = green
