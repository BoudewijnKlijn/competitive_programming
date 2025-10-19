from collections import deque


class Solution:
    def findLexSmallestString(self, s: str, a: int, b: int) -> str:
        return self.bruteforce(s, a, b)

    def bruteforce(self, s: str, a: int, b: int) -> str:
        """I suspect the number of unique possibilities is quite limited.
        s <= 100 and each position can be 0-9.
        However, order is relatively fixed,
            and all odd position numbers are changed simultaneously.
        Create all possibilities and return minimum.
        """
        mapping = {str(i): str((i + a) % 10) for i in range(10)}

        def operation_one(string):
            """Replace odd position with new value."""
            odd = False
            new_string = ""
            for char in string:
                if odd:
                    char = mapping[char]
                new_string += char
                odd = not odd
            return new_string

        def operation_two(string):
            """Shift b positions right."""
            return string[-b:] + string[:-b]

        seen = set()
        queue = deque([s])
        while queue:
            string = queue.popleft()
            if string in seen:
                continue
            seen.add(string)
            # apply operation one and two and add to queue
            for f in [operation_one, operation_two]:
                new = f(string)
                queue.append(new)
        return min(seen)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1625"
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
        funcs=["findLexSmallestString"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
