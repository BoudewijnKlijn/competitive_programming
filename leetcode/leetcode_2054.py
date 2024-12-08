from typing import List


class Solution:
    def maxTwoEvents(self, events: List[List[int]]) -> int:
        sorted_by_from = sorted(events, key=lambda x: (x[0], -x[2]))
        sorted_by_to = sorted(events, key=lambda x: (x[1], -x[2]))

        # loop once in **reverse** over sorted_by_from and record the max value
        #  reached from all the numbers from that value onwards
        # this has to be done in reverse order, since we have to start from the highest from value
        high = 0
        max_values_from = [None] * len(events)
        froms = [None] * len(events)
        for i, (from_, _, value) in enumerate(sorted_by_from[::-1], start=1):
            high = max(high, value)
            max_values_from[-i] = high
            froms[-i] = from_

        # loop once over sorted_by_to and record the max value reached from all numbers up to that to value
        # this can be done in normal order, since to is increasing
        high = 0
        max_values_to = list()
        tos = list()
        for i, (_, to, value) in enumerate(sorted_by_to):
            high = max(high, value)
            max_values_to.append(high)
            tos.append(to)

        # combine, using two pointers
        # increase the from pointer until we find a from value that is greater than the to value
        # then check if both values combined are greater than the maximum answer so far
        # then increase the to index, and repeat.
        ans = max(max_values_to)
        to_index = 0
        from_index = 0
        while to_index < len(events):
            while from_index < len(events) and tos[to_index] >= froms[from_index]:
                from_index += 1

            if from_index < len(events):
                ans = max(ans, max_values_to[to_index] + max_values_from[from_index])
            to_index += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxTwoEvents"],
        data_file="leetcode_2054_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
