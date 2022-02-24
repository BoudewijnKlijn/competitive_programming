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
        return int(project.score) / int(project.nr_of_days)

    def solve(self, input_data: ProblemData) -> Solution:
        contributors = np.array(deepcopy(input_data.contributors))
        projects = input_data.projects

        # Sort projects according to their values
        project_values = [self.get_project_value(project) for project in projects]
        projects = [x for _, x in sorted(zip(project_values, projects))]

        # Iterate over all projects
        contributor_idx = 0
        for idx, project in enumerate(projects):
            # Iterate over all roles needed for that project
            for role in project.roles:
                # Simply assign the first/next contributor to that role if contributor has that skill at the required level
                for contributor in contributors:
                    if role.name in [skill.name for skill in contributor.skills]:
                        relevant_skill = [skill for skill in contributor.skills if role.name == skill.name][0]
                        if relevant_skill.level >= role.level:
                            project.contributors.append(contributors[contributor_idx])
                            contributor_idx += 1

                    # todo: fix ugly multiple breaks
                    if contributor_idx >= len(contributors):
                        print("No more contributors left")
                        break
                if contributor_idx >= len(contributors):
                    break
            if contributor_idx >= len(contributors):
                break

        # Filter projects that have no contributors
        executed_projects = [project for project in projects if len(project.contributors) == len(project.roles)]

        return Solution(executed_projects)
