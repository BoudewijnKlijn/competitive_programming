from typing import List


class Solution:
    """Only use the min and max of each array. Alrady sorted so index 0 and -1."""

    def maxDistance(self, arrays: List[List[int]]) -> int:
        return self.only_extremes(arrays)

    def only_extremes(self, arrays: List[List[int]]) -> int:
        """The distance between the max of all maxes and the min of all mins almost yields the correct result.
        Only exception is when they are both in the same array.
        Then we need to use the 2nd lowest or the 2nd highest.
        Use the one that has the smallest distance to the optimum."""
        MAX = 1e4
        low_ultimate = MAX
        high_ultimate = -MAX
        low_index = None
        high_index = None
        low_alternative = MAX
        high_alternative = -MAX

        for i, arr in enumerate(arrays):
            low, high = arr[0], arr[-1]
            if low < low_ultimate:
                low_ultimate, low_alternative = low, low_ultimate
                low_index = i
            elif low < low_alternative:
                low_alternative = low
            if high > high_ultimate:
                high_ultimate, high_alternative = high, high_ultimate
                high_index = i
            elif high > high_alternative:
                high_alternative = high

        ans = high_ultimate - low_ultimate
        if low_index != high_index:
            return ans
        adjustment = min(
            high_ultimate - high_alternative, low_alternative - low_ultimate
        )
        return ans - adjustment

    def lows_highs_sorted(self, arrays: List[List[int]]) -> int:
        """Same idea as only_extremes but with sorted lists, hence slower."""
        lows = sorted([(arr[0], i) for i, arr in enumerate(arrays)])
        highs = sorted([(arr[-1], i) for i, arr in enumerate(arrays)])

        ans = highs[-1][0] - lows[0][0]
        if highs[-1][1] != lows[0][1]:
            return ans
        adjustment = min(highs[-1][0] - highs[-2][0], lows[1][0] - lows[0][0])
        return ans - adjustment

    def naive(self, arrays: List[List[int]]) -> int:
        """Reduce arrays to min and max. Remove duplicates.
        Compare all pairs of min and max values.
        Time limit exceeded."""
        from collections import Counter

        unique_low_high = Counter((arr[0], arr[-1]) for arr in arrays)

        max_distance = 0
        dict_items = list(unique_low_high.items())
        for i, ((low, high), count) in enumerate(dict_items):
            if count > 1:
                candidate = abs(high - low)
                if candidate > max_distance:
                    max_distance = candidate

            for (low2, high2), _ in dict_items[i + 1 :]:
                candidate = max(abs(high - low2), abs(high2 - low))
                if candidate > max_distance:
                    max_distance = candidate
        return max_distance


if __name__ == "__main__":
    from timing import timing

    timing(
        data_file="leetcode_0624_data.txt",
        funcs=["only_extremes", "maxDistance", "lows_highs_sorted", "naive"],
        solution=Solution(),
    )
