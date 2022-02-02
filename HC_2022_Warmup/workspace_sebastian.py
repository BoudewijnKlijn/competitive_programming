import glob
import os
import time

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies import RandomIngredients
from HC_2022_Warmup.strategies.genetic_solver import GeneticStrategy
from HC_2022_Warmup.strategies.valuable_ingredients import ValuableIngredients
from valcon.utils import best_score

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


def valuable_ingredients_approach():
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.txt"))
    files = sorted(files)

    current_best = best_score(output_directory)

    # files = ['e_elaborate.in.txt']
    # Forward selection
    for problem_file in files:
        problem = os.path.basename(problem_file)[0]
        print(f"Trying to solve file (FORWARD): {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        scorer = PerfectPizzaScore(demands)
        strategy = ValuableIngredients(scorer, seed=27)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        print("----------------------")

        if current_best[problem] < score:
            out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-{strategy.name}.txt'
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_directory, out_file))

    print("----------------------")
    print("----------------------")
    print()

    """
    for problem_file in files:
        print(f"Trying to solve file (BACKWARD): {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        scorer = PerfectPizzaScore(demands)
        strategy = ValuableIngredients(scorer, forward_selection=False, seed=27)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        print("----------------------")
    """


def genetic_solver_approach():
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    # files = glob.glob(os.path.join(directory, "*.txt"))
    # files = sorted(files)
    files = ['e_elaborate.in.txt']
    # files = ['a_an_example.in.txt']

    current_best = best_score(output_directory)

    # Forward selection
    for problem_file in files:
        problem = os.path.basename(problem_file)[0]
        print(f"Trying to solve file: {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        scorer = PerfectPizzaScore(demands)
        strategy = GeneticStrategy(scorer, max_generations=1000, population_size=10, nr_tournament_candidates=3,
                                   seed=27)
        # strategy = ValuableIngredients(scorer, seed=27)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        print("----------------------")

        if current_best[problem] < score:
            out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-{strategy.name}.txt'
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_directory, out_file))


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    # files = glob.glob(os.path.join(directory, "*.txt"))
    # files = sorted(files)
    #files = ['a_an_example.in.txt']
    #files = ['e_elaborate.in.txt']
    files = ['d_difficult.in.txt']

    current_best = best_score(output_directory)

    NR_EXAMPLES = 10000
    for problem_file in files:
        problem = os.path.basename(problem_file)[0]
        print(f"Trying to solve file: {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        # 1. Generate a lot of examples and calculate their score
        score = 0
        scorer = PerfectPizzaScore(demands)
        strategy = RandomIngredients(seed=27)
        start = time.perf_counter()

        solutions = []
        scores = []
        for _ in tqdm(range(0, NR_EXAMPLES)):
            solution = strategy.solve(demands)
            score = scorer.calculate(solution)
            solution_dict = {}
            for ingredient in solution.ingredients:
                solution_dict[ingredient] = 1
            solutions.append(solution_dict)
            scores.append(score)

        # 2. Train an ML model
        df = pd.DataFrame(solutions)
        columns = list(df.columns)
        df = df.fillna(0)
        features = df.copy()
        df['target'] = scores
        labels = df['target']

        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25,
                                                                                    random_state=42)
        print('Training Features Shape:', train_features.shape)
        print('Training Labels Shape:', train_labels.shape)
        print('Testing Features Shape:', test_features.shape)
        print('Testing Labels Shape:', test_labels.shape)

        print("Training model...")
        rf = RandomForestRegressor(n_estimators=10, random_state=42)  # Train the model on training data
        rf.fit(train_features, train_labels)
        print("Done training model...")
        print("Feature importances:")
        importances = rf.feature_importances_
        print(importances)

        fig, ax = plt.subplots()
        forest_importances = pd.Series(importances, index=columns)
        forest_importances = forest_importances.sort_values(ascending=False)
        forest_importances[:10].plot.bar(ax=ax)
        ax.set_title("Feature importances")
        ax.set_ylabel("Importance")
        fig.tight_layout()
        plt.show()

        for i in range(0, len(forest_importances)):
            ingredients = list(forest_importances.index[:i])
            solution = PerfectPizza(ingredients)
            duration = time.perf_counter() - start

            score = scorer.calculate(solution)

            print(f'{problem_file} Score: {score} in iteration {i}')

            if current_best[problem] < score:
                print(f'HIGHER SCORE!!!!  {problem_file} Score: {score}')

                out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-{strategy.name}.txt'
                print(f'Writing {out_file}')
                solution.save(os.path.join(output_directory, out_file))
