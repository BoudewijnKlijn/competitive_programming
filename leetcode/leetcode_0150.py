from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = list()
        for token in tokens:
            if token in list("+-/*"):
                b = stack.pop()
                a = stack.pop()
                match token:
                    case "-":
                        ans = a - b
                    case "+":
                        ans = a + b
                    case "/":
                        if a * b < 0:
                            ans = -(abs(a) // abs(b))
                        else:
                            ans = a // b
                    case "*":
                        ans = a * b
            else:
                ans = int(token)
            stack.append(ans)
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0150"
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
        funcs=["evalRPN"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
