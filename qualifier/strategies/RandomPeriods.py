from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class RandomPeriods(Strategy):
    name = 'RandomPeriods'

    def solve(self, input):
        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                trafic_lights.append((street.name, self.random.randint(1, 3)))
            schedule = Schedule(intersection.index, trafic_lights)
            schedules.append(schedule)

        return OutputData(tuple(schedules))
