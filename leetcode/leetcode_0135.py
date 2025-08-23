from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        """Rules:
        - each child at least 1 candy.
        - if rating higher than neighbor, also more candy than neighbor.

        Approach:
        - init answer with 1 candy each.
        - Sort ratings, remember original position.
        - Starting from smallest rating, give additional candy if higher rating than neighbor.
        """
        # add max+1 rating on both ends, so that i dont have to check whether within bounds
        MAX = 20_001
        ratings.insert(0, MAX)
        ratings.append(MAX)
        n = len(ratings)
        sorted_rating = sorted(enumerate(ratings), key=lambda x: x[1])
        candy_list = [1] * n
        ans = 0
        for orig_idx, rating in sorted_rating[:-2]:
            if rating > ratings[orig_idx - 1]:
                # more than left neighbor
                candy_list[orig_idx] = candy_list[orig_idx - 1] + 1
            if (
                rating > ratings[orig_idx + 1]
                and candy_list[orig_idx + 1] + 1 > candy_list[orig_idx]
            ):
                # more than right neighbor
                candy_list[orig_idx] = candy_list[orig_idx + 1] + 1
            ans += candy_list[orig_idx]
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["candy"],
        data_file="leetcode_0135_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
