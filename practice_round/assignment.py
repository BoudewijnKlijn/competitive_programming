

class Pizza:

    n_ingredients = None
    ingredients = []

    def __init__(self, n_ingredients, ingredients):
        self.n_ingredients = n_ingredients
        self.ingredients = ingredients


class Assignment:

    pizzas = []
    n_teams_two = None
    n_teams_three = None
    n_teams_four = None

    def __init__(self, pizzas, n_teams_two, n_teams_three, n_teams_four):
        self.pizzas = pizzas
        self.n_teams_two = n_teams_two
        self.n_teams_three = n_teams_three
        self.n_teams_four = n_teams_four


def read_assignment(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    first_line_input = lines[0].split(" ")
    n_pizzas = int(first_line_input[0])
    n_teams_two = int(first_line_input[1])
    n_teams_three = int(first_line_input[2])
    n_teams_four = int(first_line_input[3])
    pizzas = []

    for pizza_line in lines[1:]:
        pizza_line_input = pizza_line.replace("\n", "").split(" ")
        pizzas.append(Pizza(n_ingredients=pizza_line_input[0],
                            ingredients=pizza_line_input[1:])
        )

    assert n_pizzas == len(pizzas), "Not all pizzas were created."

    return Assignment(
        pizzas=pizzas,
        n_teams_two=n_teams_two,
        n_teams_three=n_teams_three,
        n_teams_four=n_teams_four
    )


if __name__ == '__main__':
    assignment = read_assignment("a_example")

    print("Printing pizzas:")
    for pizza in assignment.pizzas:
        print("------------------")
        print(pizza.n_ingredients)
        print(pizza.ingredients)
    print("#################")
    print("Printing teams of sizes 2, 3, and 4:")
    print(assignment.n_teams_two)
    print(assignment.n_teams_three)
    print(assignment.n_teams_four)
