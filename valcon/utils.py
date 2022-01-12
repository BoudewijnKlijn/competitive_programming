import glob
import os


def flatten(t):
    return [item for sublist in t for item in sublist]


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
