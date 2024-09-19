import re
from itertools import permutations
from typing import List


class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        # i dont know how to filter out identical expression but created in a different way
        # other than adding parentheses and using a set thereafter
        # i could choose one of the operators. add the numbers on each side. add parenthesis
        # and choose the next operator. try all options
        digit_pattern = r"\d+"
        operator_pattern = r"[\+\-\*]"
        digits = re.findall(pattern=digit_pattern, string=expression)
        operators = re.findall(pattern=operator_pattern, string=expression)
        ans = set()
        for operator_order in permutations(range(len(operators)), len(operators)):
            tmp_digits = digits.copy()
            tmp_operator_order = list(operator_order)
            tmp_operators = operators.copy()
            while tmp_operator_order:
                op_i = tmp_operator_order.pop(0)
                operator = tmp_operators.pop(op_i)
                num_2 = tmp_digits.pop(op_i + 1)
                num_1 = tmp_digits.pop(op_i)
                tmp_digits.insert(op_i, f"({num_1}{operator}{num_2})")
                tmp_operator_order = [
                    x if x < op_i else x - 1 for x in tmp_operator_order
                ]
            ans.add(tmp_digits[0])

        # ordering doesn't matter, so answer check is not working properly
        return list(map(eval, ans))


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["diffWaysToCompute"],
        data_file="leetcode_0241_data.txt",
        exclude_data_lines=None,
        check_result=False,  # ordering doesn't matter, so answer check is not working properly
    )
