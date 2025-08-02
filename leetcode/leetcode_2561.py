import heapq
from collections import Counter
from typing import List


class Solution:
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        """Can be made equal if counts of both baskets combined of each number is even.
        Ordering is done afterwards, so indices do not matter.
        Swap minimum key with maximum key (a pair) to minimize cost.
        Alternatively, if 2*smallest value in goal < min(pair) to be swapped,
            then swap that smallest value back and forth.
            Increases cost with 2*smallest value instead of min(pair)."""
        count1 = Counter(basket1)
        count2 = Counter(basket2)
        combined = count1 + count2
        if not all(v % 2 == 0 for v in combined.values()):
            return -1

        goal = Counter({k: v // 2 for k, v in combined.items()})
        min_key = min(goal.keys())
        too_much1 = count1 - goal
        too_much2 = count2 - goal
        all_swaps = too_much1 + too_much2
        remaining_swaps = sum(all_swaps.values())
        swaps = sorted(all_swaps.items())
        cost = 0
        # keys are ordered, so we pick the minimum automatically
        for k, v in swaps:
            # swap minimum value back and forth if values to swap are >2*larger
            if k > 2 * min_key:
                cost += remaining_swaps * min_key
                break

            # 2*v values swapped at cost of min of both
            # make sure not to overshoot and precisely end at 0 remaining swaps
            if remaining_swaps <= 2 * v:
                cost += k * remaining_swaps // 2
                break
            cost += k * v
            remaining_swaps -= 2 * v

        return cost


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minCost"],
        data_file="leetcode_2561_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
