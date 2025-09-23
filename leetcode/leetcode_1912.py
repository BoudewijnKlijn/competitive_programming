import bisect
from collections import defaultdict
from typing import List


class MovieRentingSystem:
    def __init__(self, n: int, entries: List[List[int]]):
        """Determine ranking of cheapest shops per movie once. Skip rented later.
        Continuously update ranking of cheapest rented movies.

        232ms Beats 99.19%
        """
        self.cheapest_rented = list()
        self.rented = set()
        self.prices = dict()
        self.cheapest_shops = defaultdict(list)
        for shop, movie, price in entries:
            self.prices[(shop, movie)] = price
            self.cheapest_shops[movie].append((price, shop))

        # sort after adding all movies is faster than sort after individual inserts.
        for movie in self.cheapest_shops.keys():
            self.cheapest_shops[movie].sort()

    def search(self, movie: int) -> List[int]:
        """Cheapest shops are always the same.
        If movie is rented out, the shop is skipped."""
        out = list()
        i = 0
        for _, shop in self.cheapest_shops[movie]:
            if (movie, shop) in self.rented:
                continue
            out.append(shop)
            i += 1
            if i == 5:
                break
        return out

    def rent(self, shop: int, movie: int) -> None:
        price = self.prices[(shop, movie)]
        self.rented.add((movie, shop))
        bisect.insort_right(self.cheapest_rented, (price, shop, movie))

    def drop(self, shop: int, movie: int) -> None:
        price = self.prices[(shop, movie)]
        idx = bisect.bisect(self.cheapest_rented, (price, shop, movie))
        del self.cheapest_rented[idx - 1]
        self.rented.remove((movie, shop))

    def report(self) -> List[List[int]]:
        return [(shop, movie) for _, shop, movie in self.cheapest_rented[:5]]


# Your MovieRentingSystem object will be instantiated and called as such:
# obj = MovieRentingSystem(n, entries)
# param_1 = obj.search(movie)
# obj.rent(shop,movie)
# obj.drop(shop,movie)
# param_4 = obj.report()
# param_4 = obj.report()
