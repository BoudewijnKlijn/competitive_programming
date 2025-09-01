import heapq
from typing import List


class Solution:
    def maxAverageRatio(self, classes: List[List[int]], extraStudents: int) -> float:
        """Sort clases in heapq, based on most benefit (store negative).
        Pop from heapq, update avg passing rate, update new benefit, insert back again.
        Adding a function with cache to calculate benefit makes it slower."""
        benefit = list()
        n = len(classes)
        passing_rates = list()
        for passing, total in classes:
            benefit_class = (passing + 1) / (total + 1) - passing / total
            passing_rates.append(passing / total)
            benefit.append((-benefit_class, passing + 1, total + 1))

        heapq.heapify(benefit)

        avg_passing_rate_times_n = sum(
            passing_rates
        )  # faster than dividing by n all the time

        for _ in range(extraStudents):
            neg_benefit, passing, total = benefit[0]
            avg_passing_rate_times_n -= (
                neg_benefit  # faster than dividing by n all the time
            )
            benefit_class = (passing + 1) / (total + 1) - passing / total
            heapq.heapreplace(
                benefit, (-benefit_class, passing + 1, total + 1)
            )  # faster than heappop followed by heappush

        return round(avg_passing_rate_times_n / n, 5)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1792"
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
        funcs=["maxAverageRatio"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
