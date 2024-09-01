from typing import List


class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if m * n != len(original):
            return []

        return [original[r * n : (r + 1) * n] for r in range(m)]


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["construct2DArray"],
        data_file="leetcode_2022_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
