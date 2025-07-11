import heapq
from typing import List


class Solution:
    def maxFreeTime(
        self, eventTime: int, startTime: List[int], endTime: List[int]
    ) -> int:
        """Move just one meeting. Ordering is allowed to change.
        Determine sum of free time before and after meeting, which is first guess.
        Determine if order can be changed to improve further.
        """
        time_between_meetings = (
            [startTime[0] - 0]
            + [
                start_next - end_prev
                for end_prev, start_next in zip(endTime, startTime[1:])
            ]
            + [eventTime - endTime[-1]]
        )

        all_times = [-t for t in time_between_meetings]
        heapq.heapify(all_times)

        ans = 0
        for time_before, time_after, start, end in zip(
            time_between_meetings, time_between_meetings[1:], startTime, endTime
        ):
            # assuming order cannot be changed
            ans = max(ans, time_before + time_after)

            # verifying if order can be changed. remove before and after times from available spots
            removed = []
            if all_times[0] == min(-time_before, -time_after):
                removed.append(heapq.heappop(all_times))
                if all_times[0] == max(-time_before, -time_after):
                    removed.append(heapq.heappop(all_times))
            if start - end >= all_times[0]:
                # yes, order can be changed
                ans = max(ans, time_before + time_after + end - start)

            for r in removed:
                heapq.heappush(all_times, r)

        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxFreeTime"],
        data_file="leetcode_3440_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
