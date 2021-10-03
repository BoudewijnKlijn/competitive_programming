import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy
from qualifier.util import save_output

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_street_points(input):

    # First compute average route duration.
    route_durations = []
    for car in input.cars:
        route_durations.append(car.get_total_time())
    avg_route_duration = sum(route_durations) / len(route_durations)

    logging.info(f"Average route duration is {avg_route_duration}.")
    logging.info(f"Start computing street points for {len(input.streets.keys())} streets.")

    # Then create relevance score of street.
    street_points = dict()  # Dict from street name to relevance score of street
    for street_name in input.streets.keys():
        street_points[street_name] = 0  # Give each street 0 points to begin with.

    for car in input.cars:
        for street in car.path:
            # Street points are based on number of cars passing this street + whether car has short route duration.
            street_points[street.name] = street_points[street.name] + (avg_route_duration / car.get_total_time())

    logger.info("Computed street points.")
    return street_points


def norm(l):
    return [float(i)/sum(l) for i in l]


def compute_total_seconds_cycle(input_problem, intersection):
    """
    Compute total seconds that a cycle can take.
    """
    logger.info(f"Duration: {input_problem.duration}")
    logger.info(f"Number of incoming streets: {len(intersection.incoming_streets)}")
    result = len(intersection.incoming_streets) + 5
    logger.info(f"Total seconds for intersection cycle: {result}")
    return result


def compute_seconds_distribution(input_problem, street_points, intersection):
    total_seconds_cycle = compute_total_seconds_cycle(input_problem, intersection)
    incoming_streets = list(intersection.incoming_streets)
    raw_distribution = [street_points[street.name] for street in incoming_streets]

    # If no street has points for this intersection, return False.
    if all(street_points[street.name] == 0 for street in incoming_streets):
        return False

    norm_distribution = norm(raw_distribution)
    return {s.name: round(total_seconds_cycle * d) for d, s in zip(norm_distribution, incoming_streets)}


class FixedPeriods(Strategy):

    def solve(self, input):
        logger.info("Start solving problem.")
        street_points = get_street_points(input)

        logger.info("Start computing schedules.")
        schedules = []
        for intersection in input.intersections:

            distr = compute_seconds_distribution(input, street_points, intersection)

            if distr:
                trafic_lights = []
                for street_name, seconds in distr.items():
                    if seconds > 0:
                        trafic_lights.append((street_name, seconds))
                schedule = Schedule(intersection.index, trafic_lights)
                schedules.append(schedule)
        logger.info("Done computing schedules.")
        return OutputData(schedules)


if __name__ == '__main__':

    directory = os.path.join('inputs')
    for file_name in os.listdir(directory):
        logger.info(f"Looking at file {file_name}")
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = FixedPeriods()

        output = my_strategy.solve(input_data)

        logger.info(f"Start calculating score.")
        score = calculate_score(output)
        logger.info("Saving output.")
        save_output(output, file_name, score, 'diede')
