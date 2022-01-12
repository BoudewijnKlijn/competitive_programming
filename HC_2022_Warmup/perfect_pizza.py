from valcon import OutputData


class PerfectPizza(OutputData):
    def __init__(self, ingredients: list):
        self.ingredients = set(ingredients)

    def save(self, filename: str):
        with open(filename, 'w') as file:
            list_form = list(self.ingredients)
            sorted(list_form)

            ingredients = ' '.join(list_form)
            count = len(self.ingredients)
            file.write(f'{count} {ingredients}')
