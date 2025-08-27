import os
import glob
import time

import matplotlib.pyplot as plt
import seaborn as sns

from HC_2022_Qualification.problem_data import ProblemData

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, '../input')

    input_files = glob.glob(os.path.join(directory, "*.txt"))
    input_files = sorted(input_files)

    #input_files = [input_files[4]]
    print(f"Nr of files: {len(input_files)}")
    for problem_file in input_files:
        problem = os.path.basename(problem_file).split('.')[0]
        print(f"File: {problem}")
        start = time.perf_counter()
        input_data = ProblemData(problem_file)
        duration = time.perf_counter() - start
        print(f"Parsed file in {duration:0.2f}s")

        projects = input_data.projects
        contributors = input_data.contributors
        print(f"Nr of contributors: {len(contributors)}")
        print(f"Nr of projects: {len(projects)}")

        # incorrect because it does not take into consideration the time dimension
        #max_contributors_needed = sum([len(project.roles) for project in projects])
        #avg_nr_roles_per_project = max_contributors_needed / len(projects)
        #print(f"Avg nr of roles per project: {avg_nr_roles_per_project:0.0f}")
        #print(f"Max contributors needed: {max_contributors_needed:0.0f}")

        nr_of_days_per_project = [project.nr_of_days for project in projects]
        ax = sns.histplot(nr_of_days_per_project)
        output_path = os.path.join("histogram_nr_of_days", problem + '.png')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        ax.figure.savefig(output_path)
        plt.clf()

        nr_of_roles_per_project = [len(project.roles) for project in projects]
        sns.histplot(nr_of_roles_per_project)
        plt.title('Histogram: nr of roles')
        output_path = os.path.join("histogram_nr_of_roles", problem + '.png')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        ax.figure.savefig(output_path)
        plt.clf()

        score_per_project = [project.score for project in projects]
        sns.histplot(score_per_project)
        plt.title('Histogram: score')
        output_path = os.path.join("histogram_score_per_project", problem + '.png')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        ax.figure.savefig(output_path)
        plt.clf()


        sns.scatterplot(nr_of_days_per_project, score_per_project)
        plt.title('Histogram: score')
        output_path = os.path.join("scatterplot_score_vs_days", problem + '.png')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        ax.figure.savefig(output_path)
        plt.clf()

        plt.show()
        print('-------------------------------------------------------------------------------------------------------')