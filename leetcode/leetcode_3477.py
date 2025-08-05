from typing import List


class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        used = set()
        ans = 0
        for fruit in fruits:
            for basket_i, size in enumerate(baskets):
                if fruit <= size and basket_i not in used:
                    used.add(basket_i)
                    break
            else:
                ans += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["numOfUnplacedFruits"],
        data_file="leetcode_3477_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
