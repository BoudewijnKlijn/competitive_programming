import bisect
from collections import defaultdict
from typing import List


class FoodRatings:
    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.food = dict()
        self.sorting = defaultdict(list)
        for item in zip(foods, cuisines, ratings):
            self.add(*item)

    def add(self, food, cuisine, rating):
        self.food[food] = (rating, cuisine)
        bisect.insort(self.sorting[cuisine], (-rating, food))

    def changeRating(self, food: str, newRating: int) -> None:
        # remove current rating
        rating, cuisine = self.food[food]
        idx = bisect.bisect(self.sorting[cuisine], (-rating, food))
        del self.sorting[cuisine][idx - 1]
        # add new rating
        self.add(food, cuisine, newRating)

    def highestRated(self, cuisine: str) -> str:
        _, food = self.sorting[cuisine][0]
        return food


# Your FoodRatings object will be instantiated and called as such:
# obj = FoodRatings(foods, cuisines, ratings)
# obj.changeRating(food,newRating)
# param_2 = obj.highestRated(cuisine)
