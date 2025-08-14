from typing import List


class Solution:
    def minimizeTheDifference(self, mat: List[List[int]], target: int) -> int:
        """First determine minimum and maximum path and subtract minimum within rows.
        If target outside minimum and maximum, min or max is optimum.
            Otherwise determine optimal path.
        Subtract all possibilities from remainder and compare with current best ans.
        Remove negative numbers after checking, those will not improve further."""
        R = len(mat)
        min_result = 0
        max_result = 0
        for row in range(R):
            minimum = min(mat[row])
            maximum = max(mat[row])
            min_result += minimum
            max_result += maximum
            mat[row] = [num - minimum for num in mat[row]]

        remainder = target - min_result
        diff_max_min = max_result - min_result
        # outside bounds if minimum or maximum?
        if remainder <= 0:
            # impossible to reduce total. minimum is optimum
            return abs(remainder)
        elif remainder >= diff_max_min:
            # impossible to increase total. maximum is optimum
            return remainder - diff_max_min

        ans = min(abs(remainder), abs(remainder - diff_max_min))

        # if not outside bounds then determine optimal path for remainder
        # everything added that is less than remainder, reduces remainder (=improvement).
        # can always choose zero if remainder is overshot.
        # the optimum depends on values in all rows. greedy is not optimal.
        # since the maximum number of column is 70, and the numbers are within 1-70, the
        #   the total after some rows will likely be duplicated. useful to reduce states.
        remainders = set([remainder])
        for row in mat:
            remainders = {rem - x for x in row for rem in remainders}
            ans = min(ans, min(map(abs, remainders)))
            if ans == 0:
                # early stopping
                return ans
            # remove negative numbers, those will never improve further
            remainders = {rem for rem in remainders if rem > 0}

        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minimizeTheDifference"],
        data_file="leetcode_1981_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
