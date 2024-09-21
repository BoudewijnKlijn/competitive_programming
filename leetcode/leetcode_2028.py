from typing import List


class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        m = len(rolls)
        total_sum = mean * (m + n)
        current_sum = sum(rolls)

        # the missing rolls are at least n * 1 and at most n * 6
        missing_sum = total_sum - current_sum
        if missing_sum < n or missing_sum > 6 * n:
            # impossible, return empty list
            return []

        # its possible. now just construct the rolls that sum to missing_sum
        div, mod = divmod(missing_sum, n)
        return [div + 1] * mod + [div] * (n - mod)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["missingRolls"],
        data_file="leetcode_2028_data.txt",
        exclude_data_lines=None,
        check_result=True,
        repeat=1000,
    )
