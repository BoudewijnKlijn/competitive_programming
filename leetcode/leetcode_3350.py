from typing import List


class Solution:
    def maxIncreasingSubarrays(self, nums: List[int]) -> int:
        """Follow up of 3349.
        Need to find maximum value of k.
        k is at least 1.
        """
        return self.single_loop(nums)

    def single_loop(self, nums: List[int]) -> int:
        """1267ms Beats 99.35%"""
        prev = nums[0]
        streak = 1
        first_half = 0
        best = 1
        for num in nums[1:]:
            if num > prev:
                streak += 1
            else:
                first_half = streak
                streak = 1

            if streak > 2 * best:
                best = streak // 2
            elif first_half > best and streak > best:
                # min(first_half, streak)
                # can only improve 1 at most
                best += 1

            prev = num

        return best

    def bruteforce(self, nums: List[int]) -> int:
        """Bruteforce: increase k until no longer True.

        Time Limit Exceeded 1103 / 1111 testcases passed
        """

        def leetcode_3349(k):
            """Single loop over nums.
            Check if num increases.
            If 2*k increases in a row, return True.
            If interrupted by a single non-increase where the first and second half
                have at least k increases, also return True.
            """
            prev = nums[0]
            streak = 1
            first_half = False
            for num in nums[1:]:
                if num > prev:
                    streak += 1
                else:
                    if streak >= k:
                        first_half = True
                    else:
                        first_half = False
                    streak = 1

                if streak >= 2 * k:
                    return True
                elif first_half and streak >= k:
                    return True

                prev = num

            return False

        k = 1
        while leetcode_3349(k + 1):
            k += 1
        return k


# +--------------+---------------+
# |   bruteforce |   single_loop |
# |--------------+---------------|
# |     0.000009 |      0.000005 |
# |     0.000003 |      0.000002 |
# |    17.383235 |      0.003376 |
# +--------------+---------------+


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3350"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["bruteforce", "single_loop"],
        data_file=data_file,
        exclude_data_lines=[2],
        check_result=True,
    )
