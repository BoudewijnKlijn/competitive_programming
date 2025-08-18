from itertools import permutations, product
from operator import add, mul, sub, truediv
from typing import List


class Solution:
    def judgePoint24(self, cards: List[int]) -> bool:
        return self.bruteforce(cards)

    def bruteforce(self, cards: List[int]) -> bool:
        """Try all combinations.
        Cards have 4*3*2*1 = 24 options.
        Operators (4) can be repeated in 3 positions, so 4**3 = 64 options.
        Order of operations is 3*2*1 = 6 options.
        Total = 24 * 64 * 6 = 9216 options.
        Ugly solution."""
        card_options = permutations(cards, len(cards))
        operators = [add, mul, sub, truediv]
        operator_options = product(operators, repeat=3)
        order_of_operations = permutations(range(3), 3)

        for card_option, operator_option, order in product(
            card_options, operator_options, order_of_operations
        ):
            try:
                match order:
                    case (0, 1, 2):
                        result = operator_option[2](
                            operator_option[1](
                                operator_option[0](card_option[0], card_option[1]),
                                card_option[2],
                            ),
                            card_option[3],
                        )
                    case (0, 2, 1):
                        result = operator_option[1](
                            operator_option[0](card_option[0], card_option[1]),
                            operator_option[2](card_option[2], card_option[3]),
                        )
                    case (1, 0, 2):
                        result = operator_option[2](
                            operator_option[0](
                                card_option[0],
                                operator_option[1](card_option[1], card_option[2]),
                            ),
                            card_option[3],
                        )
                    case (1, 2, 0):
                        result = operator_option[1](
                            operator_option[0](card_option[0], card_option[1]),
                            operator_option[2](card_option[2], card_option[3]),
                        )
                    case (2, 0, 1):
                        result = operator_option[0](
                            card_option[0],
                            operator_option[2](
                                operator_option[1](card_option[1], card_option[2]),
                                card_option[3],
                            ),
                        )
                    case (2, 1, 0):
                        result = operator_option[0](
                            card_option[0],
                            operator_option[1](
                                card_option[1],
                                operator_option[2](card_option[2], card_option[3]),
                            ),
                        )

                if round(result, 5) == 24:
                    return True
            except ZeroDivisionError:
                pass
        return False


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["judgePoint24"],
        data_file="leetcode_0679_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
