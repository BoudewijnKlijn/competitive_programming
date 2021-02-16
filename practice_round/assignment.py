

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
