class Pizza:
    def __init__(self, pizza_id, n_ingredients, ingredients):
        self.id = pizza_id
        self.n_ingredients = n_ingredients
        self.ingredients = set(ingredients)

    def __repr__(self):
        return f'{self.id=} {self.n_ingredients=} {self.ingredients=}\n'


class Assignment:
    def __init__(self, n_pizzas, pizzas, n_teams_two, n_teams_three, n_teams_four, file_in):
        self.n_pizzas = n_pizzas
        self.pizzas = pizzas
        self.n_teams_two = n_teams_two
        self.n_teams_three = n_teams_three
        self.n_teams_four = n_teams_four
        self.file_in = file_in

    def __repr__(self):
        return f'{self.n_pizzas=} {self.n_teams_four=} {self.n_teams_three=} {self.n_teams_two=}'


def read_assignment(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    first_line_input = lines[0].split(" ")
    n_pizzas = int(first_line_input[0])
    n_teams_two = int(first_line_input[1])
    n_teams_three = int(first_line_input[2])
    n_teams_four = int(first_line_input[3])
    pizzas = []

    for i, pizza_line in enumerate(lines[1:], start=0):
        pizza_line_input = pizza_line.replace("\n", "").split(" ")
        pizzas.append(Pizza(pizza_id=i,
                            n_ingredients=int(pizza_line_input[0]),
                            ingredients=pizza_line_input[1:])
                      )

    assert n_pizzas == len(pizzas), "Not all pizzas were created."

    return Assignment(
        n_pizzas=n_pizzas,
        pizzas=pizzas,
        n_teams_two=n_teams_two,
        n_teams_three=n_teams_three,
        n_teams_four=n_teams_four,
        file_in=filename
    )


if __name__ == '__main__':
    assignment = read_assignment("a_example")

    print("Printing pizzas:")
    for pizza in assignment.pizzas:
        print("------------------")
        print(pizza.id)
        print(pizza.n_ingredients)
        print(pizza.ingredients)
    print("#################")
    print("Printing teams of sizes 2, 3, and 4:")
    print(assignment.n_teams_two)
    print(assignment.n_teams_three)
    print(assignment.n_teams_four)
