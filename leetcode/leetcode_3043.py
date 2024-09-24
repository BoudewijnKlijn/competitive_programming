from typing import List


class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        return self.tree(arr1, arr2)

    def tree(self, arr1: List[int], arr2: List[int]) -> int:
        root = dict()
        for n in map(str, arr1):
            node = root
            for level, char in enumerate(n, start=1):
                if char not in node:
                    node[char] = dict()
                node = node[char]

        ans = 0
        for n in map(str, arr2):
            node = root
            for level, char in enumerate(n, start=1):
                if char in node:
                    node = node[char]
                    if ans < level:
                        ans = level
                else:
                    break
        return ans

    def naive_faster(self, arr1: List[int], arr2: List[int]) -> int:
        ans = 0
        for prefix_length in range(1, 9):
            if ans < prefix_length - 1:
                break
            prefix_set1 = self.gen_prefixes(arr1, prefix_length)
            prefix_set2 = self.gen_prefixes(arr2, prefix_length)
            for pref1 in prefix_set1:
                if pref1 in prefix_set2:
                    ans = prefix_length
                    break
        return ans

    def naive(self, arr1: List[int], arr2: List[int]) -> int:
        from itertools import product

        ans = 0
        for prefix_length in range(1, 9):
            if ans < prefix_length - 1:
                break
            prefix_set1 = self.gen_prefixes(arr1, prefix_length)
            prefix_set2 = self.gen_prefixes(arr2, prefix_length)
            for pref1, pref2 in product(prefix_set1, prefix_set2):
                if pref1 == pref2:
                    ans = prefix_length
                    break
        return ans

    def gen_prefixes(self, arr, prefix_length):
        prefix_set = set()
        minimum = 10 ** (prefix_length - 1)
        for n in arr:
            if n < minimum:
                continue
            n_prefix = self.gen_prefix(n, prefix_length)
            prefix_set.add(n_prefix)
        return prefix_set

    def gen_prefix(self, number, length):
        while number >= 10**length:
            number //= 10
        return number


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["tree", "naive", "naive_faster"],
        data_file="leetcode_3043_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
