from typing import List


class Solution:
    def chalkReplacer(self, chalk: List[int], k: int) -> int:
        per_loop = sum(chalk)
        k %= per_loop

        for student, required in enumerate(chalk):
            k -= required
            if k < 0:
                return student


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["TODO"],
        data_file="leetcode_XXXX_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
