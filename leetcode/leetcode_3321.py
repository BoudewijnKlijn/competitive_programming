import bisect
import heapq
from collections import Counter
from math import prod
from typing import List


class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        return self.pop_insert(nums, k, x)

    def pop_insert(self, nums: List[int], k: int, x: int) -> List[int]:
        """Same as reuse_counter_and_sorted, but uses pop and insert,
            instead of reconstructing new object.

        Create counter object once and reuse it. One items enters window, another is removed.
        Sort once and thereafter use bisect.
        Reuse the prod_sum.
        Accepted. 3898ms Beats 66.67%
        """

        ans = list()
        n = len(nums)
        for i in range(n - k + 1):
            if i == 0:
                # count and sort once.
                count = Counter(nums[i : i + k])
                sorted_count = sorted([(-v, -k) for k, v in count.items()])
                prod_sum = sum(map(prod, sorted_count[:x]))
                ans.append(prod_sum)
            else:
                # decrease count and update removed num
                count_remove_old = count[nums[i - 1]]
                remove_old_idx = bisect.bisect_left(
                    sorted_count, (-count_remove_old, -nums[i - 1])
                )
                sorted_count.pop(remove_old_idx)
                count_remove_new = count_remove_old - 1
                remove_new_idx = bisect.bisect_left(
                    sorted_count, (-count_remove_new, -nums[i - 1])
                )
                sorted_count.insert(remove_new_idx, ((-count_remove_new, -nums[i - 1])))

                # update count
                count[nums[i - 1]] -= 1

                # subtract reduced value from prod_sum
                if remove_old_idx < x:
                    prod_sum -= (count[nums[i - 1]] + 1) * nums[i - 1]
                    if remove_new_idx < x:
                        prod_sum += count[nums[i - 1]] * nums[i - 1]
                    else:
                        prod_sum += prod(sorted_count[x - 1])

                # increase count and update added num
                count_add_old = count[nums[i + k - 1]]
                add_old_idx = bisect.bisect_left(
                    sorted_count, (-count_add_old, -nums[i + k - 1])
                )
                if count_add_old > 0:  # add_old_idx may be incorrect when count==0
                    sorted_count.pop(add_old_idx)
                count_add_new = count_add_old + 1
                add_new_idx = bisect.bisect_left(
                    sorted_count, (-count_add_new, -nums[i + k - 1])
                )
                sorted_count.insert(add_new_idx, (-count_add_new, -nums[i + k - 1]))
                count[nums[i + k - 1]] += 1

                # add increased value to prod_sum
                if add_new_idx < x:
                    if add_old_idx < x:
                        prod_sum += nums[i + k - 1]  # count increased by one.
                    else:
                        prod_sum += count[nums[i + k - 1]] * nums[i + k - 1]
                        prod_sum -= prod(sorted_count[x])
                ans.append(prod_sum)

        return ans

    def reuse_counter_and_sorted(self, nums: List[int], k: int, x: int) -> List[int]:
        """Create counter object once and reuse it. One items enters window, another is removed.
        Sort once and thereafter use bisect.
        Reuse the prod_sum.
        Time Limit Exceeded 779 / 784 testcases passed
        """

        ans = list()
        n = len(nums)
        for i in range(n - k + 1):
            if i == 0:
                # count and sort once.
                count = Counter(nums[i : i + k])
                sorted_count = sorted([(-v, -k) for k, v in count.items()])
                prod_sum = sum(map(prod, sorted_count[:x]))
                ans.append(prod_sum)
            else:
                # decrease count and update removed num
                count_remove_old = count[nums[i - 1]]
                count_remove_new = count_remove_old - 1
                remove_old_idx = bisect.bisect_left(
                    sorted_count, (-count_remove_old, -nums[i - 1])
                )
                remove_new_idx = (
                    bisect.bisect_left(sorted_count, (-count_remove_new, -nums[i - 1]))
                    - 1  # -1, because the old entry will be removed, but is still present here and has a lower idx.
                )
                count[nums[i - 1]] -= 1
                # I assume processing remove and insert at once, is faster than first remove, and then insert.
                # WRONG. uses lot of memory and is slower apparently.
                sorted_count = (
                    sorted_count[:remove_old_idx]
                    + sorted_count[remove_old_idx + 1 : remove_new_idx + 1]
                    + [(-count_remove_new, -nums[i - 1])]
                    + sorted_count[remove_new_idx + 1 :]
                )

                # subtract reduced value from prod_sum
                if remove_old_idx < x:
                    prod_sum -= (count[nums[i - 1]] + 1) * nums[i - 1]
                    if remove_new_idx < x:
                        prod_sum += count[nums[i - 1]] * nums[i - 1]
                    else:
                        prod_sum += prod(sorted_count[x - 1])

                # increase count and update added num
                count_add_old = count[nums[i + k - 1]]
                count_add_new = count_add_old + 1
                add_old_idx = bisect.bisect_left(
                    sorted_count, (-count_add_old, -nums[i + k - 1])
                )
                add_new_idx = bisect.bisect_left(
                    sorted_count, (-count_add_new, -nums[i + k - 1])
                )
                count[nums[i + k - 1]] += 1
                # I assume processing remove and insert at once, is faster than first remove, and then insert.
                # WRONG. uses lot of memory and is slower apparently.
                sorted_count = (
                    sorted_count[:add_new_idx]
                    + [(-count_add_new, -nums[i + k - 1])]
                    + sorted_count[add_new_idx:add_old_idx]
                    + sorted_count[add_old_idx + 1 :]
                )

                # add increased value to prod_sum
                if add_new_idx < x:
                    if add_old_idx < x:
                        prod_sum += nums[i + k - 1]  # count increased by one.
                    else:
                        prod_sum += count[nums[i + k - 1]] * nums[i + k - 1]
                        prod_sum -= prod(sorted_count[x])
                ans.append(prod_sum)

        # import time

        # n = int(time.time())
        # with open(f"{n}.txt", "w") as f:
        #     f.write(str(ans))

        return ans

    def reuse_counter(self, nums: List[int], k: int, x: int) -> List[int]:
        """Exactly the same as 3318.
        Create counter object once and reuse it. One items enters window, another is removed.
        Time Limit Exceeded 776 / 784 testcases passed
        """

        def get_x_sum(count, x):
            top = heapq.nlargest(x, [(c[1], c[0]) for c in count.items()])
            return sum(map(prod, top))

        ans = list()
        n = len(nums)
        for i in range(n - k + 1):
            if i == 0:
                count = Counter(nums[i : i + k])
            else:
                count[nums[i - 1]] -= 1
                count[nums[i + k - 1]] += 1

            ans.append(get_x_sum(count, x))
        return ans


# +----------------------------+--------------+
# |   reuse_counter_and_sorted |   pop_insert |
# |----------------------------+--------------|
# |                   0.000063 |     0.000015 |
# |                   0.000021 |     0.000014 |
# |                   0.000008 |     0.000005 |
# |                   1.216288 |     0.562702 |
# |                   3.272515 |     0.261494 |
# +----------------------------+--------------+

# +-----------------+----------------------------+
# |   reuse_counter |   reuse_counter_and_sorted |
# |-----------------+----------------------------|
# |        0.000071 |                   0.000019 |
# |        0.000021 |                   0.000019 |
# |        0.000007 |                   0.000007 |
# |        0.000007 |                   0.000007 |
# |       21.436963 |                   1.144913 |
# +-----------------+----------------------------+


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3321"
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
        funcs=[
            # "reuse_counter",
            "reuse_counter_and_sorted",
            "pop_insert",
        ],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
