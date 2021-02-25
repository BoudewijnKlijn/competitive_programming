from qualifier.output_data import OutputData
from qualifier.input_data import InputData, Street, Car, Intersection
from typing import Dict, List, Optional
from qualifier.schedule import Schedule


class CarLocation:
    def __init__(
        self,
        current_start_intersection: int,
        current_end_intersection: int,
        current_street: str,
        sec_on_street: int,
        duration_current_street: int,
        remaining_itinerary: List[str],
        moving: bool = False,
    ):
        self.current_start_intersection = current_start_intersection
        self.current_end_intersection = current_end_intersection
        self.current_street = (current_street,)
        self.sec_on_street = sec_on_street
        self.duration_current_street = duration_current_street
        self.remaining_itinerary = remaining_itinerary
        self.moving = moving
        self.status = None

    def continue_on_street(self):
        self.sec_on_street += 1

    def update_intersections(self, new_destination, new_duration):
        self.current_start_intersection = self.current_end_intersection
        self.current_street = self.remaining_itinerary[0]
        self.remaining_itinerary.pop()

        if len(self.remaining_itinerary) == 0:
            self.status = "DONE"
            self.sec_on_street = -1

        self.duration_current_street = new_duration
        self.current_end_intersection = new_destination
        self.sec_on_street = 0


def validate_output(output: OutputData) -> bool:
    return True


def calculate_score(input: InputData, solution: OutputData) -> int:
    if not validate_output(solution):
        raise ValueError("Not valid output")

    car2location = get_initial_locations(input)
    score = 0

    for moment in range(input.duration):
        for car in input.cars:
            car_location = car2location[car]

            # Car is already done
            if car_location.sec_on_street < 1:
                score += 1
            if car_location.sec_on_street == car_location.duration_current_street:
                next_street = car_location.remaining_itinerary[0]
                car_location.update_intersections(
                    new_destination=next_street.end, new_duration=next_street.time
                )

                if car_location.status == "DONE":
                    score += input.bonus

            # Just drive
            if 0 < car_location.sec_on_street < car_location.duration_current_street:
                car_location.continue_on_street()

            if car_location.sec_on_street == 0:
                # TODO: check if there is a queue
                no_queue = True

                current_intersection = car_location.current_start_intersection
                intersection_schedule = solution.schedules[
                    current_intersection
                ]

                light_green = False
                cycle_length = sum(t[1] for t in intersection_schedule.street_duration_tuples)
                modulo_moment = moment % cycle_length

                cumulative_schedule = []
                time = 0
                for t in intersection_schedule.street_duration_tuples:
                    time = time + t[1]
                    cumulative_schedule.append((t[0], time))
                    if modulo_moment < time:
                        if t[0] == current_intersection:
                            light_green = True
                        else:
                            break

                if light_green and no_queue:
                    car_location.continue_on_street()

                else:
                    # Wait
                    pass

    return score


def get_initial_locations(input: InputData) -> Dict[Car, CarLocation]:
    locations = dict()
    for car in input.cars:

        first_street = car.path[0]
        start_intersection = first_street.begin

        second_street = car.path[1]
        end_intersection = second_street.end
        total_street_duration = second_street.time

        full_itinerary = car.path
        remaining_destinations = full_itinerary[1:]

        location_car = CarLocation(
            current_start_intersection=start_intersection,
            current_end_intersection=end_intersection,
            sec_on_street=first_street.time,
            duration_current_street=total_street_duration,
            remaining_itinerary=remaining_destinations,
            current_street=first_street,
        )

        locations[car] = location_car

    return locations


def get_end_intersection(street):
    pass


sample_input = InputData(
    "/Users/mathijs/Documents/code/2021-google-hash-code/qualifier/inputs/a.txt"
)

schedules = [
    Schedule(intersection=1, street_duration_tuples=[("rue-d-athenes", 2)]),
    Schedule(intersection=0, street_duration_tuples=[("rue-de-londres", 2)]),
    Schedule(intersection=2, street_duration_tuples=[("rue-de-moscou", 1)])
]
sample_output = OutputData(schedules=schedules)
s = calculate_score(sample_input, sample_output)
print(s)