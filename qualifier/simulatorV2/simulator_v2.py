from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from tqdm import tqdm

from qualifier.simulatorV2.simulator_car_v2 import SimulatorCarV2
from qualifier.simulatorV2.simulator_intersection_v2 import SimulatorIntersectionV2
from qualifier.simulatorV2.simulator_street_v2 import SimulatorStreetV2


class SimulatorV2:
    def __init__(self, input_data: InputData, verbose: int = 0):

        self.verbose = verbose
        self.bonus = input_data.bonus
        self.duration = input_data.duration
        self.cars = input_data.cars

        self.streets = dict()
        self.intersections = dict()

        self.score = 0
        self.time = -1

        for street_name, street in input_data.streets.items():
            self.streets[street_name] = SimulatorStreetV2(street.end, street.time, street.name)

        for intersection in input_data.intersections:
            streets = [street for street in self.streets.values() if street.exit_intersection == intersection.index]
            self.intersections[intersection.index] = SimulatorIntersectionV2(streets)

    def init_run(self, output_data: OutputData):
        self.score = 0
        self.time = -1

        # clear the streets
        for street in self.streets.values():
            street.cars.clear()

        # set the new schedule
        for schedule in output_data.schedules:
            self.intersections[schedule.intersection].apply_schedule(
                schedule)  # I dont need a dict here I could just scan...

        # populate with the cars
        for car in self.cars:
            starting_street = car.path[0]
            simulator_car = SimulatorCarV2([street.name for street in car.path])
            self.streets[starting_street.name].add_car(simulator_car, at_traffic_light=True)

        # want to do this but how to restore the originals?
        # for now I have a check if intersct.schedule_duration == 0 do nothing
        # # clean intersections with only red lights
        # for intersection in list(self.intersections.values()):
        #     if len(intersection.schedule) == 0:
        #         self.intersections.pop(intersection.intersection_number)

    def log(self, message: str):
        if self.verbose >= 2:
            print(message)

    def run(self, output_data: OutputData) -> int:
        self.init_run(output_data)

        # Main loop
        if self.verbose == 1:
            for _ in tqdm(range(self.duration)):
                self._execute_timestep()
        else:
            for _ in range(self.duration):
                self._execute_timestep()

        # I'm not checking yet if they arrive at their destination in their last move...
        # may need to move them a full 1 step when they move from an intersection on to the next road
        # self.time += 1  # quite a few hacks here...
        # for street in self.streets.values():
        #     if len(street.cars) == 0:
        #         continue
        #
        #     destination_reached, _ = street.execute_timestep(self.time)
        #     self._score(destination_reached, self.time)

        return self.score

    def _score(self, cars, time):
        for car in cars:
            time_points = self.duration - time
            if time_points >= 0:
                score = self.bonus + time_points
                self.log(f'(time: {time}) {str(car)} reached destination +{score}')
                self.score += score

    def _execute_timestep(self):
        self.time += 1

        moving = []

        # update cars and streets
        for street in self.streets.values():
            if len(street.cars) == 0:
                continue

            destination_reached, moving_to_next_street = street.execute_timestep(self.time)
            self._score(destination_reached, self.time)
            if moving_to_next_street is not None:
                moving.append((street, moving_to_next_street))

                # now that all streets have been processed we can move the cars (we dont want to move them twice in 1 timestep)
        for street, car in moving:
            self.log(f'(time: {self.time}) {car}:\n\t\tmoving onto {car.path[0]}')
            if len(car.path) == 1:
                self._score([car], self.time + self.streets[car.path[0]].length)
            else:
                street = car.path[0]
                self.streets[street].add_car(car)
