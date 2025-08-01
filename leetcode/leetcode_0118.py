from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        triangle = [[1]]
        row = 2
        while row <= numRows:
            new_row = [1] + list(map(sum, zip(triangle[-1], triangle[-1][1:]))) + [1]
            triangle.append(new_row)
            row += 1
        return triangle


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["generate"],
        data_file="leetcode_0118_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
