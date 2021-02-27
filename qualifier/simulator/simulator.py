from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from tqdm import tqdm

from qualifier.simulator.simulator_car import SimulatorCar
from qualifier.simulator.simulator_intersection import SimulatorIntersection
from qualifier.simulator.simulator_street import SimulatorStreet


class Simulator:
    def __init__(self, input_data: InputData, output_data: OutputData, verbose=False):
        """

        :type verbose: object
        """
        self.output_data = output_data
        self.input_data = input_data
        self.verbose = verbose

        self.streets = dict()
        self.intersections = dict()

        self.score = 0
        self.time = -1

        for street_name, street in input_data.streets.items():
            self.streets[street_name] = SimulatorStreet(street.end, street.time, street.name)

        for intersection in self.input_data.intersections:
            streets = [street for street in self.streets.values() if street.exit_intersection == intersection.index]
            self.intersections[intersection.index] = SimulatorIntersection(intersection.index, streets)

        for car in input_data.cars:
            starting_street = car.path[0]
            simulator_car = SimulatorCar([self.streets[street.name] for street in car.path])
            self.streets[starting_street.name].add_car(simulator_car, at_traffic_light=True)

        for schedule in output_data.schedules:
            self.intersections[schedule.intersection].add_schedule(schedule)

        # clean intersections with only red lights
        for intersection in list(self.intersections.values()):
            if len(intersection.schedule) == 0:
                self.intersections.pop(intersection.intersection_number)

    def log(self, message: str):
        if self.verbose:
            print(message)

    def _score(self, cars):
        for car in cars:
            score = self.input_data.bonus + self.input_data.duration - self.time  # WARNING MIGHT BE OFF BY 1
            self.log(f'(time: {self.time}) {str(car[0])} reached destination +{score}')
            self.score += score

    def run(self) -> int:
        for _ in tqdm(range(self.input_data.duration)):
            self._execute_timestep()

        # I'm not checking yet if they arrive at their destination in their last move...
        # may need to move them a full 1 step when they move from an intersection on to the next road
        self.time += 1  # quite a few hacks here...
        for _, street in self.streets.items():
            if len(street.cars) == 0:
                continue

            destination_reached, _ = street.execute_timestep()
            self._score(destination_reached)

        return self.score

    def _execute_timestep(self):
        self.time += 1

        # update lights of each intersection
        for _, intersection in self.intersections.items():
            intersection.execute_timestep(self.time)

        moving = []

        # update cars and streets
        for _, street in self.streets.items():
            if len(street.cars) == 0:
                continue

            destination_reached, moving_to_next_street = street.execute_timestep()
            self._score(destination_reached)
            if moving_to_next_street is not None:
                moving.append(moving_to_next_street)

                # now that all streets have been processed we can move the cars (we dont want to move them twice in 1 timestep)
        for car in moving:
            self.log(f'(time: {self.time}) {car}:\n\t\tmoving onto {car.path[0].name}')
            street = car.path[0]
            street.add_car(car)
