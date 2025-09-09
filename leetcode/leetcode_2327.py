from collections import deque


class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        """There are only a few different states.
        Use deque with count of people in each state."""
        queue = deque([0] * forget)
        queue[0] = 1
        total = queue[0]
        sharing = 0
        for _ in range(1, n):
            minus = queue.pop()
            sharing += queue[delay - 1] - minus
            queue.appendleft(sharing)
            total += sharing - minus
        return total % (10**9 + 7)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2327"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["peopleAwareOfSecret"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
