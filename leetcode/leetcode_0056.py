from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        return self.sort_and_one_pass(intervals)

    def sort_and_one_pass(self, intervals: List[List[int]]) -> List[List[int]]:
        """Sort intervals from low to high.
        Then combine intervals if next start is less than or equal to prev end."""
        intervals.sort()
        ans = [intervals[0]]
        for start, end in intervals[1:]:
            if end <= ans[-1][1]:
                # encapsulated, no improvement. continue with next.
                continue

            if start <= ans[-1][1]:
                # extend last interval
                ans[-1][1] = end
            else:
                # start comes after last end. create new interval
                ans.append([start, end])

        return ans

    def bool_list(self, intervals: List[List[int]]) -> List[List[int]]:
        """Range is small <= 10**4.
        Track which numbers are covered. Then reconstruct intervals.
        """
        numbers_present = [False] * 10_001
        ends = [False] * 10_001
        for start, end in intervals:
            for i in range(start, end + 1):
                numbers_present[i] = True
                if i < end:
                    ends[i] = True

        # reconstruct intervals
        prev = None
        intervals_out = list()
        for idx, (is_present, end_is_present) in enumerate(zip(numbers_present, ends)):
            if not prev and is_present:
                # create new interval
                intervals_out.append([idx, idx])
            elif is_present:
                # increase end of interval
                intervals_out[-1][1] = idx
            prev = end_is_present

        return intervals_out


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["bool_list", "sort_and_one_pass"],
        data_file="leetcode_0056_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
