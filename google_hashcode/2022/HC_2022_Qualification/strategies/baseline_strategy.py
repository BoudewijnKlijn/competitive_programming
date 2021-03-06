import random

from .base_strategy import BaseStrategy
from ..problem_data import ProblemData
from ..solution import Solution


class BaselineStrategy(BaseStrategy):
    def __init__(self, seed: int = None):
        """
        Initializes a BaseLineStrategy which simply assigns every contributor to a project based on first come (in list)
        first served (only if it has the required skill)

        Args:
            seed (int): Seed for random generator
        """
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(0, 999_999_999)
        super().__init__(self.seed)

    def solve(self, input_data: ProblemData) -> Solution:
        contributors = input_data.contributors
        projects = input_data.projects

        # Iterate over all projects
        contributor_idx = 0
        for idx, project in enumerate(projects):
            # Iterate over all roles needed for that project
            for role in project.roles:
                # Simply assign the first/next contributor to that role if contributor has that skill at the required level
                for contributor in contributors:
                    if contributor.skills[role.name] >= role.level:
                        project.contributors.append(contributor)
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
