from typing import List


class Solution:
    def largestTriangleArea(self, points: List[List[int]]) -> float:
        """n<=50, so brute force is fine."""

        def get_area(a, b, c):
            """Heron's formula."""
            s = (a + b + c) / 2
            if a > s or b > s or c > s:
                # this is not a triangle. one side is longer than the sum of other two.
                return 0
            return (s * (s - a) * (s - b) * (s - c)) ** 0.5

        def get_length(a, b):
            x1, y1 = a
            x2, y2 = b
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        n = len(points)
        ans = 0
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    a = get_length(points[i], points[j])
                    b = get_length(points[i], points[k])
                    c = get_length(points[j], points[k])
                    area = get_area(a, b, c)
                    if area > ans:
                        ans = area
        return round(ans, 5)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0812"
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
        funcs=["largestTriangleArea"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
