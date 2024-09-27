class MyCalendarTwoNaive:
    """First find parts which are double booked.
    Within the double booked intervals, check if parts are triple booked."""

    def __init__(self):
        self.intervals = list()

    def overlap(self, start, end, existing: list) -> bool:
        overlap_list = list()
        for s, e in existing:
            if start < e and end > s:
                overlap_list.append((max(start, s), min(e, end)))
        return overlap_list

    def book(self, start: int, end: int) -> bool:
        # check for double bookings
        # only store the overlapping part
        double_booked = self.overlap(start, end, self.intervals)

        # check double booked for triple bookings
        for i, (s, e) in enumerate(double_booked):
            if self.overlap(s, e, double_booked[:i] + double_booked[i + 1 :]):
                return False
        self.intervals.append((start, end))
        return True


class MyCalendarTwo(MyCalendarTwoNaive):

    def __init__(self):
        super().__init__()


class Solution:
    # Your MyCalendarTwo object will be instantiated and called as such:
    # obj = MyCalendarTwo()
    # param_1 = obj.book(start,end)

    def __init__(self):
        pass

    def naive(self, data):
        my_calendar = MyCalendarTwoNaive()
        ans = [my_calendar.book(*dat) for dat in data]
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["naive"],
        data_file="leetcode_0731_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
