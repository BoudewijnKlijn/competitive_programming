def strategy_0(problem):

    pizzas = list(range(100))

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
