from assignment import Pizza, Assignment, read_assignment


def strategy_0(assignment):
    """Eerst 4 pizzas naar alle teams van 4. Daarna 3 naar teams van 3, en dan 2 naar teams van 2."""

    pizzas = assignment.pizzas

    orders = list()

    for _ in range(assignment.n_teams_four):
        new_order = pizzas[:4]
        pizzas = pizzas[4:]
        orders.append(new_order)

    for _ in range(assignment.n_teams_three):
        new_order = pizzas[:3]
        pizzas = pizzas[3:]
        orders.append(new_order)

    for _ in range(assignment.n_teams_two):
        new_order = pizzas[:2]
        pizzas = pizzas[2:]
        orders.append(new_order)

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
    assignment = read_assignment("a_example")

    print(assignment.n_teams_four)

    print(strategy_0(assignment))
