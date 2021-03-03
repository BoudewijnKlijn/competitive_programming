from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class AtleastOneCar(Strategy):
    name = 'AtleastOneCar'

    def solve(self, input_data):

        streets_with_cars = self.streets_with_car_at_light(input_data)

        schedules = []
        for intersection in input_data.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                if street.name in streets_with_cars:
                    trafic_lights.append((street.name, 1))

            schedule = Schedule(intersection.index, tuple(trafic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))
