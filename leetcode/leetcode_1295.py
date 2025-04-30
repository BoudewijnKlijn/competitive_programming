from typing import List


class Solution:
    def findNumbers(self, nums: List[int]) -> int:
        ans = 0
        for num in nums:
            even = True
            while num > 0:
                num //= 10
                even = not even
            if even:
                ans += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["findNumbers"],
        data_file="leetcode_1295_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
