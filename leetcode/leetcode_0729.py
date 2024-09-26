import bisect


class MyCalendar:
    """maintain list with all start and end times
    to insert new start and end time, determine the insertion indices
    start and end need to have the same index and be even

    start has to come AFTER another end, hence bisect RIGHT
    end has to come BEFORE another start, hence bisect LEFT

    its faster to check if end suffices based on the start index
    (instead of another bisect_left call)
    we know already it needs to have the same insertion index"""

    def __init__(self):
        self.times = list()

    def book(self, start: int, end: int) -> bool:
        start_index = bisect.bisect_right(self.times, start)
        # end_index = bisect.bisect_left(self.times, end, lo=start_index)
        # if start_index == end_index and start_index % 2 == 0:
        if start_index % 2 == 0 and (
            (start_index == len(self.times)) or (end <= self.times[start_index])
        ):
            self.times.insert(start_index, end)
            self.times.insert(start_index, start)
            return True
        return False


class MyCalendarTuples:
    """Only needs one insertion instead of two."""

    def __init__(self):
        self.times = list()

    def book(self, start: int, end: int) -> bool:
        index = bisect.bisect_right(self.times, (start, end))
        if (index == 0 or (index > 0 and self.times[index - 1][1] <= start)) and (
            (index == len(self.times))
            or (index < len(self.times) and end <= self.times[index][0])
        ):
            self.times.insert(index, (start, end))
            return True
        return False


class MyCalendarNaive:

    def __init__(self):
        self.intervals = list()

    def overlap(self, start2, end2):
        for start1, end1 in self.intervals:
            if min(end1, end2) > max(start1, start2):
                return True
        return False

    def book(self, start: int, end: int) -> bool:
        overlap = self.overlap(start, end)
        if not overlap:
            self.intervals.append((start, end))
        return not overlap


class Solution:
    # Your MyCalendar object will be instantiated and called as such:
    # obj = MyCalendar()
    # param_1 = obj.book(start,end)

    def __init__(self):
        pass

    def naive(self, data):
        my_calendar = MyCalendarNaive()
        ans = [my_calendar.book(*dat) for dat in data]
        return ans

    def bisect(self, data):
        my_calendar = MyCalendar()
        ans = [my_calendar.book(*dat) for dat in data]
        return ans

    def bisect_tuples(self, data):
        my_calendar = MyCalendarTuples()
        ans = [my_calendar.book(*dat) for dat in data]
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["naive", "bisect", "bisect_tuples"],
        data_file="leetcode_0729_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
