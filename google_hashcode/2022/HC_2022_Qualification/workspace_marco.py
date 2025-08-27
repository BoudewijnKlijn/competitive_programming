import glob
import os
import time
from copy import deepcopy
from random import randint


from HC_2022_Qualification.problem_data import ProblemData, Contributor, Project, Role
from HC_2022_Qualification.score import Score
from HC_2022_Qualification.solution import Solution
from HC_2022_Qualification.strategies.base_strategy import BaseStrategy
from valcon.utils import best_score, generate_file_name, get_problem_name

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class MarcoLessRandomStrategy2(BaseStrategy):
    def __init__(self, seed: int = None):
        if seed is not None:
            self.seed = seed
        else:
            self.seed = randint(0, 999_999_999)

        super().__init__(self.seed)

    def solve(self, input_data: ProblemData) -> Solution:
        projects = deepcopy(input_data.projects)

        def project_score(project):
            level_required = sum([x.level for x in project.roles])
            return project.score - level_required * 2

        projects = sorted(projects, key=lambda x: project_score(x), reverse=True)
        # self.rng.shuffle(projects)

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


class ProbabilityStrategy(BaseStrategy):
    def __init__(self, seed: int = None, score_project: callable = None, score_contributor: callable = None):
        if seed is not None:
            self.seed = seed
        else:
            self.seed = randint(0, 999_999_999)

        super().__init__(self.seed)

    @staticmethod
    def _score_project(project: Project, time_step: int) -> float:
        max_score = max(project.score + min(project.best_before - (time_step + project.nr_of_days), 0), 0)

        # score per day per person
        score = max_score / project.nr_of_days / len(project.roles)

        return score

    @staticmethod
    def _score_contributor(project: Project, role: Role, contributor: Contributor) -> float:
        # assumes only valid contributors are passed

        score = 10  # dont want negative scores start with a nice offset knowning that we normalize the scores lateron

        # can do the given role 1.0 (perfect fit) and  -0.x for each level over qualified
        score += 1 - (contributor.skills[role.name] - role.level) * 0.1

        # can mentor open slots + .2 per mentor slot
        unfilled_roles = project.unfilled_roles()
        can_mentor = [role for role in unfilled_roles if contributor.skills[role.name] >= role.level]
        score += len(can_mentor) * 0.2

        # has many more skills than needed (might have mentored more people on other projects - .1 per skill not used
        # TODO

        return max(score, 0)

    def _get_probable_best(self, list_of_things: list, scores: list = None, score_function: callable = None) -> object:
        """Gets the best of the list using the score as a probability"""

        if len(list_of_things) == 1:
            return list_of_things[0]

        if score_function:
            scores = [score_function(thing) for thing in list_of_things]

        assert scores, 'Need either a list of scores or a score function to get a score for each thing'

        sum_scores = sum(scores)

        if sum_scores == 0:
            # does not matter anymore no project will score any points.
            return list_of_things[0]

        normalized_scores = [x / sum_scores for x in scores]

        probable = self.rng.choice(list_of_things, p=normalized_scores)
        assert probable is not None, 'by now we sould always have a probable best'
        return probable

    def solve(self, input_data: ProblemData) -> Solution:
        timeline = [[] for _ in range(max([p.best_before + p.score for p in input_data.projects]))]

        timeline[0] = input_data.contributors

        unexecuted_projects = input_data.projects
        for project in unexecuted_projects:
            project.contributors = [None] * len(project.roles)

        completed_projects = []

        max_time = len(timeline) - 1

        available_contributors = []

        for time_step in range(max_time + 1):
            available_contributors.extend(timeline[time_step])

            available_projects = unexecuted_projects
            unexecuted_projects = []

            # only need to recalculate this if the timestep changes
            project_scores = [self._score_project(x, time_step) for x in available_projects]

            while available_projects:
                project = self._get_probable_best(available_projects, project_scores)

                project_scores.pop(available_projects.index(project))
                available_projects.remove(project)

                if time_step + project.nr_of_days >= project.best_before + project.score:
                    continue  # permanent removal

                project_failed = False

                role_indices = list(range(len(project.roles)))
                self.rng.shuffle(role_indices)

                for i in role_indices:
                    role = project.roles[i]
                    has_mentor = project.has_mentor(role)
                    skill_needed = role.level
                    if has_mentor:
                        skill_needed -= 1

                    candidates = [c for c in available_contributors if c.skills[role.name] >= skill_needed]

                    if not candidates:
                        project_failed = True
                        break

                    contributor = self._get_probable_best(
                        candidates,
                        score_function=lambda x: self._score_contributor(project, role, x))

                    available_contributors.remove(contributor)
                    project.contributors[i] = contributor

                if project_failed:
                    available_contributors.extend([c for c in project.contributors if c])
                    project.contributors = [None] * len(project.roles)
                    unexecuted_projects.append(project)
                    continue

                completed_projects.append(project)
                timeline[time_step + project.nr_of_days].extend(project.contributors)
                project.level_contributors()

        return Solution(completed_projects)


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.txt"))

    current_best = best_score(output_directory)

    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        if problem_name in [
            'a',
            # 'b',
            'c',
            'd',
            'e',
            'f'
        ]:
            continue

        problem = ProblemData(problem_file)

        solver = ProbabilityStrategy()
        scorer = Score(problem)

        start = time.perf_counter()
        solution = solver.solve(problem)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

        out_file = generate_file_name(problem_file, score, solver)

        if score > current_best[problem_name] or score == 0:
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_directory, out_file))
        else:
            print(f'{score} is not an improvement for {problem_name} {current_best[problem_name]}')

        print('\n')

    print(best_score(output_directory))
