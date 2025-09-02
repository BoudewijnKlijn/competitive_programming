from itertools import product
from typing import List


class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        # return self.bruteforce(points)
        return self.sort_first(points)

    def sort_first(self, points):
        """Sorting first, prevents checks on x and only try C between A and B."""
        points.sort(key=lambda x: (x[0], -x[1]))
        ans = 0
        for i, (_, yA) in enumerate(points):
            for j, (_, yB) in enumerate(points[i + 1 :], start=i + 1):
                if yA < yB:
                    # A must be upper left of B
                    continue

                # smaller than A (i) or larger than B (j) are definitely not inside rectangle
                for _, yC in points[i + 1 : j]:
                    if yB <= yC <= yA:
                        # C must not be contained in rectangle of A and B
                        break
                else:
                    ans += 1

        return ans

    def bruteforce(self, points: List[List[int]]) -> int:
        """Only 50 points, so can just check everything with everything. 50**3=125_000"""
        ans = 0
        for (xA, yA), (xB, yB) in product(points, repeat=2):
            if (xA, yA) == (xB, yB):
                continue
            if not (xA <= xB and yA >= yB):
                # A must be upper left of B: <= x and >= y
                continue

            for xC, yC in points:
                if (xA, yA) == (xC, yC) or (xB, yB) == (xC, yC):
                    continue
                elif xA <= xC <= xB and yB <= yC <= yA:
                    # C must not be contained in rectangle of A and B
                    break
            else:
                ans += 1

        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3025"
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
        funcs=["bruteforce", "sort_first"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
