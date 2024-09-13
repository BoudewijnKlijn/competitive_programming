from functools import cache
from typing import List


class Solution:
    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        # naive solution
        self.arr = arr
        ans = [self.xor_query(left, right) for left, right in queries]
        self.xor_query.cache_clear()
        return ans

    @cache
    def xor_query(self, left, right):
        num = self.arr[left]
        for num2 in self.arr[left + 1 : right + 1]:
            num ^= num2
        return num


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["xorQueries"],
        data_file="leetcode_1310_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
