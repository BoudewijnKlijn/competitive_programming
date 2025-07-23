from typing import List


class Solution:
    def maximumGain(self, s: str, x: int, y: int) -> int:
        """It's always best to remove the high value pair first."""
        # return self.too_slow(s, x, y)
        return self.faster(s, x, y)

    def faster(self, s, x, y):
        """Remove all occurences of most, until not present anymore, then remove least.
        Accepted
        77 / 77 testcases passed"""
        if x >= y:
            most = "ab"
            least = "ba"
        else:
            most = "ba"
            least = "ab"

        def remove_fast(array, substring, p):
            """remove instances of substring from array
            All instances are removed in one sweep.
            effectively uses a stack"""
            extra_points = 0
            new_array = list()
            for char in array:
                if char == substring[1] and new_array and new_array[-1] == substring[0]:
                    new_array.pop(-1)
                    extra_points += p
                    continue
                new_array.append(char)

            return new_array, extra_points

        s = list(s)
        total = 0

        s, points = remove_fast(s, most, max(x, y))
        total += points
        s, points = remove_fast(s, least, min(x, y))
        total += points

        return total

    def too_slow(self, s: str, x: int, y: int) -> int:
        """Remove all occurences of most, until not present anymore, then remove least, and try again.
        Time Limit Exceeded
        63 / 77 testcases passed"""
        if x >= y:
            most = "ab"
            least = "ba"
        else:
            most = "ba"
            least = "ab"

        def remove(array, substring, p):
            """remove instances of substring from array"""
            extra_points = 0
            prev = None
            new_array = list()
            for char in array:
                if char == substring[1] and prev == substring[0]:
                    prev = None
                    extra_points += p
                    continue
                if prev:
                    new_array.append(prev)
                prev = char
            if prev:
                new_array.append(prev)
            return new_array, extra_points

        s = list(s)
        total = 0

        while True:
            s, points = remove(s, most, max(x, y))
            total += points
            if points == 0:
                s, points = remove(s, least, min(x, y))
                total += points
                if points == 0:
                    break

        return total


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maximumGain"],
        data_file="leetcode_1717_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
