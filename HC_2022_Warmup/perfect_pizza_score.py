from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import OutputData, InputData
from valcon.scorer import Scorer


class PerfectPizzaScore(Scorer):
    def __init__(self, input_data: PizzaDemands):
        self.pizza_demands = input_data

    def calculate(self, output_data: PerfectPizza) -> int:
        score = 0
        for customer in self.pizza_demands.customers:
            if customer.will_oder(output_data):
                score += 1
        return score
