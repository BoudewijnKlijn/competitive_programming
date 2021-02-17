import numpy as np

from assignment import Pizza, Assignment, read_assignment
from vqd.score import score

from itertools import combinations
from functools import lru_cache


def strategy_0(assignment):
    """Eerst 4 pizzas naar alle teams van 4. Daarna 3 naar teams van 3, en dan 2 naar teams van 2."""

    pizzas = [pizza.id for pizza in assignment.pizzas]

    orders = list()

    teams_4 = assignment.n_teams_four

    while len(pizzas) >= 4 and teams_4 > 0:
        new_order = pizzas[:4]
        pizzas = pizzas[4:]
        orders.append((4, new_order))
        teams_4 -= 1

    teams_3 = assignment.n_teams_three

    while len(pizzas) >= 3 and teams_3 > 0:
        new_order = pizzas[:3]
        pizzas = pizzas[3:]
        orders.append((3, new_order))
        teams_3 -= 1

    teams_2 = assignment.n_teams_three

    while len(pizzas) >= 2 and teams_2 > 0:
        new_order = pizzas[:2]
        pizzas = pizzas[2:]
        orders.append((2, new_order))
        teams_2 -= 1

    return orders


def strategy_0_1(assignment):
    """Eerst 4 pizzas naar alle teams van 4. Daarna 3 naar teams van 3, en dan 2 naar teams van 2.
    Sorteer pizzas eerst op aantal ingredienten om."""

    assignment.pizzas.sort(key=lambda x: x.n_ingredients, reverse=True)

    pizzas = [pizza.id for pizza in assignment.pizzas]

    orders = list()

    teams_4 = assignment.n_teams_four

    while len(pizzas) >= 4 and teams_4 > 0:
        new_order = pizzas[:4]
        pizzas = pizzas[4:]
        orders.append((4, new_order))
        teams_4 -= 1

    teams_3 = assignment.n_teams_three

    while len(pizzas) >= 3 and teams_3 > 0:
        new_order = pizzas[:3]
        pizzas = pizzas[3:]
        orders.append((3, new_order))
        teams_3 -= 1

    teams_2 = assignment.n_teams_three

    while len(pizzas) >= 2 and teams_2 > 0:
        new_order = pizzas[:2]
        pizzas = pizzas[2:]
        orders.append((2, new_order))
        teams_2 -= 1

    return orders


def strategy_1(problem, state=42):
    """Eerst pizzas naar alle teams van 4. Daarna naar teams van 3, en dan naar teams van 2.
    Sorteer pizzas eerst op aantal ingredienten om."""

    # assignment.pizzas.sort(key=lambda x: x.n_ingredients, reverse=False)

    np.random.seed(state)

    copy_pizza = assignment.pizzas.copy()

    np.random.shuffle(copy_pizza)

    pizzas = [pizza.id for pizza in copy_pizza]

    orders = list()

    teams_4 = assignment.n_teams_four

    while len(pizzas) >= 4 and teams_4 > 0:
        new_order = pizzas[:4]
        pizzas = pizzas[4:]
        orders.append((4, new_order))
        teams_4 -= 1

    teams_3 = assignment.n_teams_three

    while len(pizzas) >= 3 and teams_3 > 0:
        new_order = pizzas[:3]
        pizzas = pizzas[3:]
        orders.append((3, new_order))
        teams_3 -= 1

    teams_2 = assignment.n_teams_three

    while len(pizzas) >= 2 and teams_2 > 0:
        new_order = pizzas[:2]
        pizzas = pizzas[2:]
        orders.append((2, new_order))
        teams_2 -= 1

    return orders


def strategy_1_2(problem):
    """varieer de random seed van strategy 1"""

    scores = []
    for seed in range(1000):
        output = strategy_1(assignment, seed)
        # print(output)

        with open('temp.out', 'w') as file:

            file.write(f'{len(output)}\n')

            for entry in output:
                file.write(f'{entry[0]} {" ".join([str(x) for x in entry[1]])}\n')
        the_score = score('b_little_bit_of_everything.in', 'temp.out')
        scores.append((seed, the_score))
        print(f"{seed}: {the_score}")

    scores.sort(key=lambda s: s[1], reverse=True)
    print(f'{scores[0]=}')

    return strategy_1(assignment, scores[0][0])


def strategy_2(problem):
    """Pak pizza met meeste ingredienten. Voeg pizza met meeste extra unieke ingredienten toe. Repeat en opnieuw
    Als we direct de meest optimale pizza kiezen, dan krijg je een mogelijk een suboptimale score. Want
    aantal pizzas moet gelijk zijn aan aantal mensen in team.

    TODO: orders beter verdelen over 2,3,4 teams. geen reden om extra pizzas toe te voegen als max punten is bereikt"""

    pizzas = sorted(assignment.pizzas, key=lambda x: x.n_ingredients, reverse=True)
    orders = list()

    def make_order(n_pizzas):
        new_order = [pizzas[0]]
        del pizzas[0]
        already_included_ingredients = new_order[0].ingredients
        for _ in range(n_pizzas-1):
            optimal_pizza = find_optimal_pizza_b(pizzas, already_included_ingredients)
            pizzas.remove(optimal_pizza)
            already_included_ingredients.update(optimal_pizza.ingredients)
            new_order.append(optimal_pizza)
        return new_order

    teams_4 = assignment.n_teams_four
    while len(pizzas) >= 4 and teams_4 > 0:
        new_order = make_order(4)
        orders.append((4, [pizza.id for pizza in new_order]))
        teams_4 -= 1

    teams_3 = assignment.n_teams_three
    while len(pizzas) >= 3 and teams_3 > 0:
        new_order = make_order(3)
        orders.append((3, [pizza.id for pizza in new_order]))
        teams_3 -= 1

    teams_2 = assignment.n_teams_two
    while len(pizzas) >= 2 and teams_2 > 0:
        new_order = make_order(2)
        orders.append((2, [pizza.id for pizza in new_order]))
        teams_2 -= 1

    return orders


def find_optimal_pizza_b(pizza_haystack, already_included_ingredients, max_unique_ingredients=10):
    """Select optimal pizza from all remaining pizzas."""
    pizza_scores = list()
    for pizza in pizza_haystack:
        pizza_score = calc_pizza_score(already_included_ingredients, pizza)
        pizza_scores.append((pizza_score, pizza))
        if pizza_score == max_unique_ingredients - len(already_included_ingredients):  # max score achieved
            return pizza

    pizza_scores.sort(key=lambda x: x[0], reverse=True)
    return pizza_scores[0][1]


def calc_pizza_score(already_included_ingredients: set, pizza):
    """Minimize overlap. Maximize extra unique.
    NOTE: Score can become negative if a pizza has 10 ingredients already"""

    overlapping_ingredients = already_included_ingredients.intersection(pizza.ingredients)
    n_overlapping_ingredients = len(overlapping_ingredients)

    n_extra_unique = pizza.n_ingredients - n_overlapping_ingredients

    return n_extra_unique - n_overlapping_ingredients


def strategy_3(problem):
    """Make optimal order. Once optimal serve it to a team and don't add anymore pizzas."""

    pizzas = assignment.pizzas.copy()
    orders = list()

    goal_order_score = 10

    teams_2 = assignment.n_teams_two
    teams_3 = assignment.n_teams_three
    teams_4 = assignment.n_teams_four

    while (teams_2 > 0 and len(pizzas) >= 2) or \
            (teams_3 > 0 and len(pizzas) >= 3) or \
            (teams_4 > 0 and len(pizzas) >= 4):

        pizza_added = True
        while teams_2 > 0 and pizza_added:
            print(len(pizzas), f'{teams_2=}')
            pizza_added = False
            remaining_pizza_ids = [pizza.id for pizza in pizzas]
            potential_orders = combinations(remaining_pizza_ids, 2)

            for potential_order in potential_orders:
                if calc_order_score_adjusted(potential_order) == goal_order_score:
                    orders.append((len(potential_order), list(potential_order)))
                    pizzas = [pizza for pizza in pizzas if pizza.id not in potential_order]
                    pizza_added = True
                    teams_2 -= 1
                    break

        pizza_added = True
        while teams_3 > 0 and pizza_added:
            print(len(pizzas), f'{teams_3=}')
            pizza_added = False
            remaining_pizza_ids = [pizza.id for pizza in pizzas]
            potential_orders = combinations(remaining_pizza_ids, 3)

            for potential_order in potential_orders:
                if calc_order_score_adjusted(potential_order) == goal_order_score:
                    orders.append((len(potential_order), list(potential_order)))
                    pizzas = [pizza for pizza in pizzas if pizza.id not in potential_order]
                    pizza_added = True
                    teams_3 -= 1
                    break

        # too many possibilities with combinations of 4, so we skip the close optimal ones (10 and 9)
        pizza_added = True
        while goal_order_score < 9 and teams_4 > 0 and pizza_added:
            print(len(pizzas), f'{teams_4=}')
            pizza_added = False
            remaining_pizza_ids = [pizza.id for pizza in pizzas]
            potential_orders = combinations(remaining_pizza_ids, 4)

            for potential_order in potential_orders:
                if calc_order_score_adjusted(potential_order) == goal_order_score:
                    orders.append((len(potential_order), list(potential_order)))
                    pizzas = [pizza for pizza in pizzas if pizza.id not in potential_order]
                    pizza_added = True
                    teams_4 -= 1
                    break

        goal_order_score -= 1

    return orders


@lru_cache(maxsize=None)
def calc_order_score_adjusted(pizza_ids_in_order):
    """Score of an order is the number of unique ingredients. Adjusted score subtracts the overlapping ingredients."""

    pizzas_in_order = [assignment.pizzas[pizza_id] for pizza_id in pizza_ids_in_order]
    n_total_ingredients = sum([pizza.n_ingredients for pizza in pizzas_in_order])

    unique_ingredients = set()
    for pizza in pizzas_in_order:
        unique_ingredients.update(pizza.ingredients)
    n_unique_ingredients = len(unique_ingredients)

    n_overlapping_ingredients = n_total_ingredients - n_unique_ingredients

    return n_unique_ingredients - n_overlapping_ingredients


def create_out_file(output, file_out='temp.out'):
    with open(file_out, 'w') as file:

        file.write(f'{len(output)}\n')

        for entry in output:
            file.write(f'{entry[0]} {" ".join([str(x) for x in entry[1]])}\n')


if __name__ == '__main__':
    assignment = read_assignment("b_little_bit_of_everything.in")

    # print(assignment.n_teams_four)

    output = []
    # output = strategy_0(assignment)
    # output = strategy_0_1(assignment)
    # output = strategy_1(assignment)
    # output = strategy_1_2(assignment)
    # output = strategy_2(assignment)
    output = strategy_3(assignment)

    create_out_file(output)

    the_score = score('b_little_bit_of_everything.in', 'temp.out')
    print(f'{the_score=}')
