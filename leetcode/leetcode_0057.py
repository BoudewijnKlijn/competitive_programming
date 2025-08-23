from typing import List


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        def search(array, val):
            """Binary search."""
            if val > array[-1][1]:
                return 2 * len(array)

            left, right = 0, 2 * len(array) - 1
            while left < right:
                div, mod = divmod((left + right) // 2, 2)
                if val < array[div][mod]:
                    right = div * 2 + mod
                else:
                    left = div * 2 + mod + 1
            return left

        if not intervals:
            return [newInterval]

        start_insert = search(intervals, newInterval[0])
        end_insert = search(intervals, newInterval[1])

        # parts that come before and after merging intervals
        prefix = intervals[: start_insert // 2]
        suffix = intervals[(end_insert + 1) // 2 :]

        # define the start and end of the merged intervals
        start = newInterval[0]
        # skip if start is larger than all elements in intervals
        if start_insert < 2 * len(intervals):
            # take min of start new_interval and existing start
            start = min(start, intervals[start_insert // 2][0])
        end = newInterval[1]

        # skip if end is smaller than all elements in intervals
        if end_insert > 0:
            # take max of end new_interval and existing end
            end = max(end, intervals[(end_insert - 1) // 2][1])
        intermediate = [[start, end]]

        # combine with parts before and after.
        if prefix and prefix[-1][1] == intermediate[0][0]:
            # merge if equal start and end.
            intermediate[0][0] = prefix[-1][0]
            del prefix[-1]
        if suffix and suffix[0][0] == intermediate[0][1]:
            # merge if equal end and start.
            intermediate[0][1] = suffix[0][1]
            del suffix[0]

        ans = prefix + intermediate + suffix
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["insert"],
        data_file="leetcode_0057_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
