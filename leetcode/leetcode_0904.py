from typing import List


class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        """The question is really: what is the longest sub array with at most two unique elements?"""
        # return self.brute_force(fruits)
        return self.two_pointers(fruits)

    def two_pointers(self, fruits: List[int]) -> int:
        """One pass. Use two pointers.
        Increment right pointer, until 3 unique elements, then increment left element, until 2 unique elements.
        Maintain counts."""
        left = 0
        counts = dict()
        ans = 0
        n_unique = 0
        for right, fruit in enumerate(fruits, start=1):
            try:
                counts[fruit] += 1
            except KeyError:
                counts[fruit] = 1
                n_unique += 1

            # increase left as long as more than two unique in window
            while n_unique > 2:
                fruit = fruits[left]
                left += 1
                counts[fruit] -= 1
                if not counts[fruit]:
                    del counts[fruit]
                    n_unique -= 1

            ans = max(ans, right - left)

        return ans

    def brute_force(self, fruits: List[int]) -> int:
        """Try all starting points. Return max result.
        Time Limit Exceeded
        71 / 92 testcases passed"""
        ans = 0
        for start in range(len(fruits)):
            baskets = set()
            n_picked = 0
            for fruit in fruits[start:]:
                baskets.add(fruit)
                n_picked += 1
                if len(baskets) > 2:
                    n_picked -= 1
                    break
                ans = max(ans, n_picked)
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "totalFruit", "brute_force",
            "two_pointers"
        ],
        data_file="leetcode_0904_data.txt",
        exclude_data_lines=None,
        repeat=100,
        check_result=True,
    )
