import os
import glob
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from HC_2022_Qualification.problem_data import ProblemData

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, '../input')

    input_files = glob.glob(os.path.join(directory, "*.txt"))
    input_files = sorted(input_files)

    input_files = [input_files[1]]
    print(f"Nr of files: {len(input_files)}")
    for problem_file in input_files:
        problem = os.path.basename(problem_file)
        print(f"File: {problem}")
        start = time.perf_counter()
        input_data = ProblemData(problem_file)
        duration = time.perf_counter() - start
        print(f"Parsed file in {duration:0.2f}s")

        projects = input_data.projects
        contributors = input_data.contributors
        print(f"Nr of contributors: {len(contributors)}")
        print(f"Nr of projects: {len(projects)}")

        nr_of_days_per_project = [project.nr_of_days for project in projects]
        sns.histplot(nr_of_days_per_project)

        nr_of_days_per_project = [project.nr_of_days for project in projects]
        sns.histplot(nr_of_days_per_project)

        plt.show()
        break
        print('-------------------------------------------------------------------------------------------------------')