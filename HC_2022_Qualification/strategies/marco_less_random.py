from copy import deepcopy
from random import randint

from HC_2022_Qualification.problem_data import ProblemData, Contributor
from HC_2022_Qualification.solution import Solution
from HC_2022_Qualification.strategies.base_strategy import BaseStrategy
from HC_2022_Qualification.strategies.baseline_strategy import BaselineStrategy


class MarcoLessRandomStrategy(BaseStrategy):

    def __init__(self, seed: int = None):
        if seed is not None:
            self.seed = seed
        else:
            self.seed = randint(0, 999_999_999)

        super().__init__(self.seed)

    def solve(self, input_data: ProblemData) -> Solution:
        projects = deepcopy(input_data.projects)

        # projects = sorted(projects, key=lambda x: x.score - x.best_before, reverse=True)
        self.rng.shuffle(projects)

        contributors = deepcopy(input_data.contributors)
        self.rng.shuffle(contributors)

        def get_contributor(contributors, skill_name, level) -> Contributor:
            for contributor in contributors:
                if contributor.skills[skill_name] >= level:
                    return contributor
            return None

        completed_projects = []

        timeline = [[] for _ in range(max([p.best_before + p.score for p in projects]))]

        timeline[0] = contributors

        available_contributors = []

        max_end_time = len(timeline) - 1

        for t in range(len(timeline)):
            available_contributors.extend(timeline[t])
            # self.rng.shuffle(available_contributors)

            not_executed = []
            while projects:
                project = projects.pop(0)
                if project.best_before + project.score > max_end_time:
                    continue  # permanent removal

                project_failed = False

                for role in project.roles:
                    has_mentor = project.has_mentor(role)
                    skill_needed = role.level
                    if has_mentor:
                        skill_needed -= 1

                    contributor = get_contributor(contributors, role.name, skill_needed)
                    if contributor is None:
                        project_failed = True
                        break

                    contributors.remove(contributor)
                    project.contributors.append(contributor)

                if project_failed:
                    contributors.extend(project.contributors)
                    project.contributors = []
                    not_executed.append(project)
                    continue

                completed_projects.append(project)
                timeline[t + project.nr_of_days].extend(project.contributors)
                project.level_contributors()

        return Solution(completed_projects)
