from typing import List


class Solution:
    def maxTotalFruits(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        return self.two_pointers(fruits, startPos, k)

    def two_pointers(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        """Use two pointers.
        Loop over fruits (to increase right pointer) and increase cumulative sum.
        If the steps is larger than k, increase left pointer.
        Subtract values which disappear from window.
        Make sure left pointer never passes right pointer."""
        fruit_id_left = 0
        cumsum = 0
        ans = 0
        for fruit_id_right, (position_right, amount) in enumerate(fruits):
            cumsum += amount
            # increase left pointer until steps is at most k again.
            # regardless of where left and right are, you always move from left to right,
            # in addition to minimum between startpos and left or startpos and right
            while (
                position_right
                - fruits[fruit_id_left][0]
                + min(
                    abs(startPos - fruits[fruit_id_left][0]),
                    abs(position_right - startPos),
                )
            ) > k:
                # if steps not valid, remove left most amount, and increase left pointer
                cumsum -= fruits[fruit_id_left][1]
                fruit_id_left += 1
                if fruit_id_left > fruit_id_right:
                    # left pointer must not pass right pointer
                    break

            ans = max(ans, cumsum)

        return ans

    def slow(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        """Switching directions twice is never usefull.
        Max is achieved by either walking left or right all the time, or switching directions once.
        Determine score over all intervals in clever way and then take max.
        Possible optimization:
            - It only makes sense to walk to a fruit and then switch. Never turn on empty index.
        """
        max_idx = 2 * 10**5
        # index of cumsum is shifted one. cumsum[0] is sum of zero elements.
        # cumsum[1] is sum of one element. the element at index[0]
        # cumsum[2] - cumsum[1] is sum of two elements at index[0] and index[1] minus element at index[1]
        #   so index[1]
        # to get sum from element[a] to element[b], use cumsum[b+1] - cumsum[a]
        cum_sum = [0] * (max_idx + 2)
        prev_idx = 1
        prev_sum = 0
        for idx, amount in fruits:
            idx += 1
            cum_sum[prev_idx:idx] = [prev_sum] * (idx - prev_idx)
            prev_idx = idx
            prev_sum += amount
        cum_sum[prev_idx:] = [prev_sum] * (max_idx - prev_idx + 2)

        # the area covered is either:
        #   - all the way to the left. So [startPos-k:startPos] (inclusive) [start:end]
        #   - first one step right, and then all the way to the left: [startPos-2-k:startPos+1]
        #   - frist two steps right, and then all the way to the left: [startPos-4-k:startPos+2]
        #   - frist x steps right, and then all the way to the left: [startPos-2*x-k:startPos+x]
        # where start is at least zero, and end is at most 2*10**5
        ans = 0
        for direction1 in range(0, k + 1):
            direction2 = max(0, k - 2 * direction1)
            # first left then right
            start = max(0, startPos - direction1)
            end = min(max_idx, startPos + direction2)
            ans = max(ans, cum_sum[end + 1] - cum_sum[start])

            # first right then left
            start = max(0, startPos - direction2)
            end = min(max_idx, startPos + direction1)
            ans = max(ans, cum_sum[end + 1] - cum_sum[start])
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxTotalFruits"],
        data_file="leetcode_2106_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
