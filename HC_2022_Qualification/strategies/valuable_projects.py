import random
from copy import deepcopy

import numpy as np

from .base_strategy import BaseStrategy
from ..problem_data import ProblemData
from ..solution import Solution


class ValuableProjectStrategy(BaseStrategy):

    def __init__(self, seed: int = None):
        """
        Initializes a ValuableProjectStrategy which assign contributors to the most valuable projects

        Args:
            seed (int): Seed for random generator
        """
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(0, 999_999_999)
        super().__init__(seed)

    @staticmethod
    def get_project_value(project):
        return project.score / project.duration

    def solve(self, input_data: ProblemData) -> Solution:
        contributors = np.Array(deepcopy(input_data.contributors))
        projects = input_data.projects

         # Sort projects according to their values
        project_values = [self.get_project_value(project) for project in projects]
        projects = [x for _, x in sorted(zip(project_values, projects))]

        # Iterate over all projects
        project_schedules = []
        contributor_idx = 0
        for idx, project in enumerate(projects):
            project_name = project.name
            project_schedule = ProjectSchedule(project_name)

            # Get random contributors
            random_idxs = random.sample(range(len(contributors)), len(project.roles))
            contributors_to_assign = contributors[random_idxs]

            # Assign random contributors to project schedule
            project_schedule.contributors = contributors_to_assign
            project_schedules.append(project_schedule)

            # Delete contributors left
            del contributors[random_idxs]

        return project_schedules
