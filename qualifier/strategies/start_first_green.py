from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class StartFirstGreen(Strategy):
    """ Streets where cars start get green light first"""
    name = 'StartFirstGreen'

    def solve(self, input_data: InputData):
        streets_with_cars = self.streets_with_car_at_light(input_data)

        streets_where_cars_start = {car.path[0].name for car in input_data.cars}

        schedules = []

        for intersection in input_data.intersections:

            schedule = []
            streets = list(intersection.incoming_streets)
            self.random.shuffle(streets)
            for street in streets:
                if street.name in streets_where_cars_start:
                    schedule.insert(0, (street.name, 1))
                elif street.name in streets_with_cars:
                    schedule.append((street.name, 1))

            schedules.append(Schedule(intersection.index, tuple(schedule)))

        return OutputData(tuple(schedules))
