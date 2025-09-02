from collections import deque


class Solution:
    def isValid(self, s: str) -> bool:
        """Use last in first out queue."""
        if len(s) % 2:
            return False
        counterparts = {"]": "[", "}": "{", ")": "("}
        queue = deque()
        for char in s:
            if char not in counterparts:
                queue.append(char)
            elif not queue:
                # queue cannot be empty
                return False
            elif queue.pop() == counterparts[char]:
                continue
            else:
                return False
        if queue:
            # queue must be empty
            return False
        return True


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0020"
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
        funcs=["isValid"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
