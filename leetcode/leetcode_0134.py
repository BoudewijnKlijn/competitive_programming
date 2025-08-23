from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        """First determine the net gain for each station: gas - cost.
        Then determine running total of gas in the tank starting from first station.
        From problem statement: If there is a solution, it is unique.
        Therefore the best station is the one after we reach the minimum tank value.
        Store index of minimum. Then increase index with 1 to find the best starting position.
        Best starting position is only good enough if the gain from minimum to final value is
        more than the loss from the start to the minimum value.
        Hence, valid solution if final tank - minimum > 0 - minimum, which is tank >= 0.
        """
        n = len(gas)
        tank = 0
        minimum = None
        min_idx = None
        for i in range(n):
            net_gain = gas[i] - cost[i]
            tank += net_gain
            if minimum is None or tank < minimum:
                minimum = tank
                min_idx = i

        best_idx = (min_idx + 1) % n
        if tank >= 0:
            return best_idx
        return -1


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["canCompleteCircuit"],
        data_file="leetcode_0134_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
