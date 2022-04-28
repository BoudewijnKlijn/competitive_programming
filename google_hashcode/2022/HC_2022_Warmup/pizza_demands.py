from collections import Counter
from dataclasses import dataclass

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from valcon import InputData


@dataclass
class Customer:
    likes: set
    dislikes: set

    def will_order(self, pizza: PerfectPizza):
        if len(pizza.ingredients & self.likes) == len(self.likes) and len(pizza.ingredients & self.dislikes) == 0:
            return True
        return False


class PizzaDemands(InputData):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            number, *lines = file.readlines()

        number = int(number)

        self.customers = []
        self.unique_likes = set()
        self.count_likes = Counter()
        self.count_dislikes = Counter()

        for _ in range(number):
            likes_count, *likes = lines.pop(0).strip().split(' ')
            dislikes_count, *dislikes = lines.pop(0).strip().split(' ')
            self.customers.append(Customer(set(likes), set(dislikes)))
            self.unique_likes.update(likes)
            self.count_likes.update(likes)
            self.count_dislikes.update(dislikes)
