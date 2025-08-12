from typing import List


class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        return self.store_count(n, x)

    def store_count(self, n: int, x: int) -> int:
        """Use dynamic programming tabulation. Only storing counts.
        Start with 1, then work up to n.
        Add new power to all existing ones. Increase result index with count of existing.
        Much faster because does not calculate duplicates and only stores counts."""
        mod = 1_000_000_000 + 7

        tab = [0] * (n + 1)
        tab[0] = 1  # every number with nothing should increase count by 1
        for base in range(1, n + 1):
            add = base**x
            # early stopping
            if add > n:
                break
            # reverse order to prevent working with adjusted counts
            for j, count in enumerate(tab[::-1]):
                idx = n - j
                if idx + add > n:
                    continue
                tab[idx + add] += count
        return tab[n] % mod

    def store_combinations(self, n: int, x: int) -> int:
        """Use dynamic programming tabulation.
        Start with 1, then work up to n.
        Use frozenset (hashable) to prevent duplicate sets
            (otherwise need sorted tuples and checking if added).
        The mod comment suggests there are going to be many combinations,
            and that I should probably not store all combinations, but just counts"""
        mod = 1_000_000_000 + 7

        tab = [set() for _ in range(n + 1)]  # added 0 index for nicer indexing
        for i in range(1, n + 1):
            if i**x <= n:
                tab[i**x].add(frozenset([i]))

            for idx1, bases1_list in enumerate(tab[:i]):
                # we want to get i. get bases**x that result in idx1 and i-idx1. combine both bases.
                if 2 * idx1 >= i:
                    # do not check the same combinations twice
                    continue
                bases2_list = tab[i - idx1]
                # try all combinations
                for bases1 in bases1_list:
                    for bases2 in bases2_list:
                        # must not have overlapping bases
                        if bases1 & bases2:
                            continue
                        tab[i].add(bases1 | bases2)

        return len(tab[n]) % mod


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["store_combinations", "store_count"],
        data_file="leetcode_2787_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
