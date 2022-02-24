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
        contributors_available_from = {contributor.name: 0 for contributor in contributors}
        projects = input_data.projects
        # just assume contributors cannot improve
        unique_skills = {skill for contributor in contributors for skill in contributor.skills}

        contributors_with_skill = dict()
        for skill in unique_skills:
            contributors_with_skill[skill] = {contributor for contributor in contributors if skill in contributor.skills}

        projects = sorted(projects, key=lambda x: x.score / x.nr_of_days, reverse=True)

        for project in projects:
            # Iterate over all roles needed for that project
            earliest_contributors = []
            valid_team = True
            for role in project.roles:
                # Assign the contributor that has the required skill and is first available
                earliest_valid_contributor = None
                for contributor in contributors_with_skill[role.name]:
                    if contributor in earliest_contributors:
                        # Contributor can only have 1 role
                        continue
                    if contributor.skills[role.name] >= role.level:
                        if earliest_valid_contributor is None or \
                                contributors_available_from[contributor.name] < contributors_available_from[earliest_valid_contributor.name]:
                            earliest_valid_contributor = contributor

                if earliest_valid_contributor is not None:
                    earliest_contributors.append(earliest_valid_contributor)
                else:
                    # No contributor found for this role.
                    valid_team = False

            if valid_team:
                # update the earliest available time for all contributors
                project_start_time = max([contributors_available_from[contributor.name] for contributor in earliest_contributors])
                for contributor in earliest_contributors:
                    contributors_available_from[contributor.name] = project_start_time + project.nr_of_days

                project.contributors = earliest_contributors

        # Filter projects that have no contributors
        executed_projects = [project for project in projects if len(project.contributors) == len(project.roles)]

        return Solution(executed_projects)
