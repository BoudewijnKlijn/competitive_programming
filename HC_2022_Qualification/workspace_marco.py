import glob
import os
import time
from copy import copy, deepcopy

import numpy as np
from dataclasses import dataclass

from HC_2022_Qualification.problem_data import ProblemData, Contributor
from HC_2022_Qualification.score import Score
from HC_2022_Qualification.solution import Solution
from HC_2022_Qualification.strategies.base_strategy import BaseStrategy
from valcon.utils import best_score, generate_file_name, get_problem_name, flatten

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class MarcoLessRandomStrategy(BaseStrategy):

    def solve(self, input_data: ProblemData) -> Solution:
        projects = deepcopy(input_data.projects)

        projects = sorted(projects, key=lambda x: x.best_before)

        contributors = deepcopy(input_data.contributors)
        self.rng.shuffle(contributors)

        def get_contributor(contributors, skill_name, level) -> Contributor:
            for contributor in contributors:
                if contributor.skills[skill_name] >= level:
                    return contributor
            return None

        completed_projects = []

        for project in projects:
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
                continue

            completed_projects.append(project)

        return Solution(completed_projects)


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.txt"))

    current_best = best_score(output_directory)

    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        problem = ProblemData(problem_file)

        solver = MarcoLessRandomStrategy()
        scorer = Score(problem)

        start = time.perf_counter()
        solution = solver.solve(problem)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

        out_file = generate_file_name(problem_file, score, solver)

        if score > current_best[problem_name]:
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_directory, out_file))
        else:
            print(f'No improvement for {problem_name}')

        print('\n')

    print(best_score(output_directory))
