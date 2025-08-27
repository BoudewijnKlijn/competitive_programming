from typing import List


class Solution:
    def countPairs(self, nums: List[int]) -> int:

        def almost_equal(a, b):
            if a == b:
                return True

            a = a.zfill(len(b))
            swaps = list()
            for char1, char2 in zip(a, b):
                if char1 != char2:
                    swaps.append((char1, char2))
            if (
                len(swaps) == 2
                and swaps[0][0] == swaps[1][1]
                and swaps[0][1] == swaps[1][0]
            ):
                return True
            return False

        ans = 0
        nums = list(map(str, sorted(nums)))
        for i, num1 in enumerate(nums):
            for num2 in nums[i + 1 :]:
                if almost_equal(num1, num2):
                    ans += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["countPairs"],
        data_file="leetcode_3265_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
