class Solution:
    def numTeams(self, rating: list[int]) -> int:
        # iterate with a mid point and determine how many are smaller and to the left,
        # and how many are larger and to the right. then multiply them
        # same logic, but then larger and to the left, and smaller and to the right
        # smaller_left + larger_left = n_left
        n = len(rating)
        sorted_rating = sorted(rating)
        # rank_dict might be slightly faster than calling .index
        rank_dict = {rating: rank for rank, rating in enumerate(sorted_rating)}
        left = set()
        rank = rank_dict.get(rating[0])  # sorted_rating.index(rating[0])
        smaller_left = 0
        larger_left = 0
        larger_right = n - 1 - rank
        smaller_right = n - 1 - rank
        ans = 0
        for n_left, mid in enumerate(rating[1:-1], start=1):
            left.add(rating[n_left - 1])
            rank_prev = rank
            rank = rank_dict.get(mid)  # sorted_rating.index(mid)
            if rank > rank_prev:  # rank increased
                # include rank_prev, include rank
                for rating_in_between in sorted_rating[rank_prev : rank + 1]:
                    if rating_in_between in left:
                        smaller_left += 1
                    else:
                        larger_right -= 1
            else:  # rank decreased
                # exclude rank, exclude rank_prev
                for rating_in_between in sorted_rating[rank + 1 : rank_prev]:
                    if rating_in_between in left:
                        smaller_left -= 1
                    else:
                        larger_right += 1

            larger_left = n_left - smaller_left
            smaller_right = n - 1 - n_left - larger_right
            ans += smaller_left * larger_right + larger_left * smaller_right

        return ans


s = Solution()
print(s.numTeams([2, 5, 3, 4, 1]))  # 3
