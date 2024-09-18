from typing import List


class Solution:
    def findMinDifference(self, timePoints: List[str]) -> int:
        # first sort all times
        # then calculate the difference between each subsequent times. only n comparisons
        timePoints.sort()
        ans = 12 * 60  # maximum distance, because circular
        for t1, t2 in zip(timePoints, timePoints[1:] + [timePoints[0]]):
            diff = self.timediff(t1, t2)
            ans = min(ans, diff)
        return ans

    def timediff(self, t1, t2):
        # how many minutes do we need to add to t1 to get to t2
        # would have been clearer if I converted everything to just minutes...
        if t1 == t2:
            return 0
        diff = 0
        t1_mins = int(t1[-2:])
        t2_mins = int(t2[-2:])
        t1_hrs = int(t1[:2])
        t2_hrs = int(t2[:2])
        mins_diff = t2_mins - t1_mins
        if mins_diff < 0:
            mins_diff += 60
            t1_hrs += 1
        diff += mins_diff
        hrs_diff = t2_hrs - t1_hrs
        if hrs_diff < 0:
            hrs_diff += 24
        diff += hrs_diff * 60
        one_day = 24 * 60
        return min(diff, one_day - diff)  # circular, so what if t2 is smaller than t1


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["findMinDifference"],
        data_file="leetcode_0539_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
