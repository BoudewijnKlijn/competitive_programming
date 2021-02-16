from assignment import Pizza, Assignment, read_assignment
from vqd.score import score


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


def strategy_1(problem):
    """Eerst pizzas naar alle teams van 4. Daarna naar teams van 3, en dan naar teams van 2.
    Sorteer pizzas eerst op aantal ingredienten om."""

    pizzas = sorted(list(range(100)), reverse=True)

    orders = list()

    for _ in range(problem.T4):
        new_order = pizzas[:4]
        pizzas = pizzas[4:]
        orders.append(new_order)

    for _ in range(problem.T3):
        new_order = pizzas[:3]
        pizzas = pizzas[3:]
        orders.append(new_order)

    for _ in range(problem.T2):
        new_order = pizzas[:2]
        pizzas = pizzas[2:]
        orders.append(new_order)

    return orders


if __name__ == '__main__':
    assignment = read_assignment("b_little_bit_of_everything.in")

    print(assignment.n_teams_four)

    output = strategy_0(assignment)
    print(output)

    with open('temp.out', 'w') as file:

        file.write(f'{len(output)}\n')

        for entry in output:
            file.write(f'{entry[0]} {" ".join([str(x) for x in entry[1]])}\n')

    print(score("b_little_bit_of_everything.in", 'temp.out'))
