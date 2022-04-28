from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands, Customer
from valcon import Strategy

from tqdm import tqdm


class EasyCustomers(Strategy):
    def __init__(self, scorer, seed=None, forward_selection=True):
        super().__init__(seed)
        self.scorer = scorer
        self.forward_selection = forward_selection

    def _get_easy_customers(self, customers: [Customer]):
        customers = sorted(customers, key=lambda customer: len(customer.dislikes))

        if self.forward_selection:
            return customers
        else:
            return reversed(customers)

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        if self.forward_selection:
            return self.solve_forward(input_data)
        else:
            return self.solve_backward(input_data)

    def solve_forward(self, input_data: PizzaDemands) -> PerfectPizza:
        easy_customers = self._get_easy_customers(input_data.customers)
        # print(f"Ingredient values: {valuable_ingredients}")
        highest_score = 0
        highest_score_ingredients = []
        current_ingredients = []
        for customer in tqdm(easy_customers):
            current_ingredients = highest_score_ingredients
            current_ingredients += customer.likes
            score = self.scorer.calculate(PerfectPizza(current_ingredients))
            if score > highest_score:
                highest_score = score
                highest_score_ingredients = current_ingredients

        return PerfectPizza(current_ingredients)

    def solve_backward(self, input_data: PizzaDemands) -> PerfectPizza:
        raise NotImplementedError()
