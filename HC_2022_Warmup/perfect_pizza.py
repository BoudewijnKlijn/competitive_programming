from valcon import OutputData


class PerfectPizza(OutputData):
    def __init__(self, ingredients: list):
        self.ingredients = set(ingredients)

    def save(self, filename: str):
        with open(filename, 'w') as file:
            ingredients = ' '.join(self.ingredients)
            count = len(self.ingredients)
            file.write(f'{count} {ingredients}')
