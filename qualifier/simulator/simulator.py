from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from tqdm import tqdm

from qualifier.simulator.simulator_car import SimulatorCar
from qualifier.simulator.simulator_intersection import SimulatorIntersection
from qualifier.simulator.simulator_street import SimulatorStreet


class Simulator:
    def __init__(self, input_data: InputData, verbose: int = 0):
        """

        :type verbose: 0 = nothing, 1=progress bar, 2= debug output
        """

        self.verbose = verbose
        self.bonus = input_data.bonus
        self.duration = input_data.duration

        self.streets = None
        self.intersections = dict()

        self.score = 0
        self.time = -1

        streets_dict = dict()

        for street_name, street in input_data.streets.items():
            streets_dict[street_name] = SimulatorStreet(street.end, street.time, street.name)

        self.streets = streets_dict.values()

        for intersection in input_data.intersections:
            streets = [street for street in self.streets if street.exit_intersection == intersection.index]
            self.intersections[intersection.index] = SimulatorIntersection(intersection.index, streets)

        for car in input_data.cars:
            starting_street = car.path[0]
            simulator_car = SimulatorCar([streets_dict[street.name] for street in car.path])
            streets_dict[starting_street.name].add_car(simulator_car, at_traffic_light=True)

    def setup_run(self, output_data: OutputData):
        for schedule in output_data.schedules:
            self.intersections[schedule.intersection].add_schedule(
                schedule)  # I dont need a dict here I could just scan...

        # want to do this but how to restore the originals?
        # for now I have a check if intersct.schedule_duration == 0 do nothing
        # # clean intersections with only red lights
        # for intersection in list(self.intersections.values()):
        #     if len(intersection.schedule) == 0:
        #         self.intersections.pop(intersection.intersection_number)

    def log(self, message: str):
        if self.verbose >= 2:
            print(message)

    def _score(self, cars):
        for car in cars:
            score = self.bonus + self.duration - self.time
            self.log(f'(time: {self.time}) {str(car[0])} reached destination +{score}')
            self.score += score

    def run(self, output_data: OutputData) -> int:
        self.setup_run(output_data)

        if self.verbose == 1:
            for _ in tqdm(range(self.duration)):
                self._execute_timestep()
        else:
            for _ in range(self.duration):
                self._execute_timestep()

        # I'm not checking yet if they arrive at their destination in their last move...
        # may need to move them a full 1 step when they move from an intersection on to the next road
        self.time += 1  # quite a few hacks here...
        for street in self.streets:
            if len(street.cars) == 0:
                continue

            destination_reached, _ = street.execute_timestep()
            self._score(destination_reached)

        return self.score

    def _execute_timestep(self):
        self.time += 1

        # update lights of each intersection
        for _, intersection in self.intersections.items():
            if intersection.schedule_duration != 0:  # currently we are not yet filtering intersections with no schedule
                intersection.execute_timestep(self.time)

        moving = []

        # update cars and streets
        for street in self.streets:
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
