from itertools import accumulate
from typing import List


class Solution:
    def maxFreeTime(
        self, eventTime: int, k: int, startTime: List[int], endTime: List[int]
    ) -> int:
        """Events have to remain non overlapping and order stays the same.
        Then determine largest sum of k consecutive elements."""
        # determine free time between events
        free_time_between = (
            [0]
            + [startTime[0] - 0]
            + [e - s for s, e in zip(endTime[:-1], startTime[1:])]
            + [eventTime - endTime[-1]]
        )

        # determine largest subsum
        running_sum = list(accumulate(free_time_between))
        ans = 0
        for a, b in zip(running_sum, running_sum[k + 1 :]):
            diff = b - a
            ans = max(ans, diff)
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxFreeTime"],
        data_file="leetcode_3439_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
