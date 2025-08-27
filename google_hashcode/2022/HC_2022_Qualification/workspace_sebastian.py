import glob
import os
import time
from copy import deepcopy

from HC_2022_Qualification.problem_data import ProblemData, Contributor
from HC_2022_Qualification.score import Score
from HC_2022_Qualification.solution import Solution
from HC_2022_Qualification.strategies.base_strategy import BaseStrategy
from HC_2022_Qualification.strategies.baseline_strategy_v2 import BaselineStrategy
from valcon.utils import best_score, get_problem_name, generate_file_name

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class SebasLessRandomStrategy(BaseStrategy):
    @staticmethod
    def get_contributor(contributors, skill_name, level) -> Contributor:
        for contributor in contributors:
            if contributor.skills[skill_name] >= level:
                return contributor
        return None

    def solve(self, input_data: ProblemData) -> Solution:
        projects = deepcopy(input_data.projects)
        projects = sorted(projects, key=lambda x: x.best_before)
        contributors = deepcopy(input_data.contributors)
        self.rng.shuffle(contributors)

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

                    contributor = self.get_contributor(contributors, role.name, skill_needed)
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


def solve_with_strategy(strategy, files, output_dir):
    current_best = best_score(output_dir)
    print(f"Nr of files {len(files)}")
    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        problem = ProblemData(problem_file)

        solver = strategy

        scorer = Score(problem)

        start = time.perf_counter()
        solution = solver.solve(problem)
        # print(f"Solution: {solution}")
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        out_file = generate_file_name(problem_file, score, solver)

        if score > current_best[problem_name]:
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_dir, out_file))
        else:
            print(f'No improvement for {problem_name}')

        print('\n')

    print(best_score(output_directory))


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    input_files = glob.glob(os.path.join(directory, "*.txt"))
    input_files = sorted(input_files)

    solve_with_strategy(BaselineStrategy(), input_files, output_directory)
    # solve_with_strategy(RandomStrategy(), input_files, output_directory)
    # solve_with_strategy(ValuableProjectStrategy(), input_files, output_directory)
    # solve_with_strategy(SebasLessRandomStrategy(), input_files, output_directory)
