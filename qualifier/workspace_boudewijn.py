import time
import os
from collections import defaultdict
import numpy as np

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy
from qualifier.strategies.RandomPeriods import RandomPeriods
from qualifier.strategies.FixedPeriods import FixedPeriods
from qualifier.util import save_output
from qualifier.simulatorV4.simulator_v4 import SimulatorV4
from qualifier.simulatorV2.simulator_v2 import SimulatorV2
from qualifier.simulator.simulatorv1 import SimulatorV1
from qualifier.strategies.PlanV4 import PlanV4

from qualifier.zero_delay_schedule import get_zero_delay_schedule

THIS_PATH = os.path.realpath(__file__)


def load_schedule_from_output():
    file_name = 'd_002488632_b_and_m-RandomStrategy on PlanV4.out'
    with open(file_name, 'r') as file:
        lines = file.readlines()

    schedules = []

    intersections = int(lines.pop(0))
    current_intersections = []
    while (lines):
        intersection = int(lines.pop(0).strip())
        current_intersections.append(intersection)
        schedule_count = int(lines.pop(0).strip())
        street_durations = []
        for _ in range(schedule_count):
            street, duration = lines.pop(0).split(' ')
            street_durations.append((street, int(duration.strip())))

        schedules.append(Schedule(intersection, tuple(street_durations)))

    return OutputData(tuple(schedules))


if __name__ == '__main__':

    directory = os.path.join('inputs')
    single_file = 'd.txt'  # 'e.txt'  # file_name or None
    for file_name in os.listdir(directory):
        if single_file is not None:
            file_name = single_file
        input_data = InputData(os.path.join(directory, file_name)) # 'qualifier',

        my_strategy = PlanV4(seed=2)  # FixedPeriods()

        # output = my_strategy.solve(input_data)

        output = load_schedule_from_output()

        sims = [SimulatorV4]  # Simulator, SimulatorV2,
        for sim in sims:
            score, _, streets = sim(input_data, verbose=0).run(output)
            print(f'{sim.__name__=}, {score=}')
            save_output(output, file_name, score, f'boudewijn_{sim.__name__}')

        if single_file is not None:
            break

    street_arrival_times = {street_name: value.arrival_times_car_at_light for street_name, value in streets.items()}
    # print(street_arrival_times)

    # result = list()
    # for i, intersection in enumerate(input_data.intersections):
    #     print(i)
    #     arrivals = list()
    #     # print('number of incoming streets', len(intersection.incoming_streets))
    #     for street in intersection.incoming_streets:
    #         if street_arrival_times[street.name]:
    #             arrivals.append(street_arrival_times[street.name])
    #
    #     # print(arrivals)
    #     if arrivals:
    #         if get_zero_delay_schedule(arrivals) is not None:
    #             result.append((len(intersection.incoming_streets), True))
    #         else:
    #             result.append((len(intersection.incoming_streets), False))
    # print(result)

    # adjust output of small intersections
    new_schedules = list()
    for schedule in output.schedules:
        intersection_id = schedule.intersection
        number_of_scheduled_streets = len(schedule.street_duration_tuples)
        arrivals = list()
        street_name_of_arrivals = list()
        if number_of_scheduled_streets < 8:
            # gather the arrival times of all streets at the intersection
            for intersection in input_data.intersections:
                if intersection.index != intersection_id:
                    continue

                for street in intersection.incoming_streets:
                    if street_arrival_times[street.name]:
                        arrivals.append(street_arrival_times[street.name])
                        street_name_of_arrivals.append(street.name)

        if arrivals and (zero_delay_schedule := get_zero_delay_schedule(arrivals)) is not None:
            # adjust schedule
            street_name_arrival_dict = dict(enumerate(street_name_of_arrivals))
            schedule_with_correct_street_names = tuple([(street_name_arrival_dict[int(street_name_int)], duration)
                                                        for street_name_int, duration in zero_delay_schedule])
            new_schedules.append(Schedule(intersection_id, schedule_with_correct_street_names))
        else:
            new_schedules.append(schedule)

    new_output = OutputData(tuple(new_schedules))

    score, _, _ = SimulatorV4(input_data, verbose=0).run(new_output)
    print(f'{SimulatorV4.__name__=}, {score=}')
    save_output(new_output, file_name, score, f'boudewijn_zero_{SimulatorV4.__name__}')

