import glob
import os

from . import Strategy


def flatten(t):
    return [item for sublist in t for item in sublist]


def generate_file_name(problem_file: str, score: int, solver: Strategy):
    return f'{os.path.basename(problem_file)[0]}-{score:06d}-{solver.name}.txt'


def get_problem_name(file_name: str):
    return os.path.basename(file_name)[0]


def best_score(directory: str):
    problems = ['a', 'b', 'c', 'd', 'e']

    solutions = glob.glob(os.path.join(directory, '*.txt'))
    file_names = [os.path.basename(f) for f in solutions]
    split = [f.split('-') for f in file_names]

    best_scores = dict()

    for problem in problems:
        scores = [int(s[1]) for s in split if s[0] == problem in s]
        best_scores[problem] = max(scores) if scores else 0
    return best_scores
