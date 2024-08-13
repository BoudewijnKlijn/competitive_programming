from collections import Counter
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        def inner(target, candidates):
            options = []
            for i, candidate in enumerate(candidates):
                new_target = target - candidate
                if new_target == 0:
                    options.append((candidate,))
                elif new_target < 0:
                    continue
                elif sum(candidates[i + 1 :]) < new_target:
                    break
                else:
                    result = inner(new_target, candidates[i + 1 :])
                    for r in result:
                        options.append(tuple(sorted((candidate,) + r)))
            return list(set(options))

        # eliminate candidates that would never be used, because including them would exceed the target
        c = Counter(candidates)
        reduced_candidates = []
        for k, v in c.items():
            reduced_candidates.extend([k] * min(v, target // k))
        reduced_candidates.sort(reverse=True)

        return inner(target, reduced_candidates)


# s = Solution()
# # candidates = [10, 1, 2, 7, 6, 1, 5]
# # target = 8
# # print(s.combinationSum2(candidates, target))

# # candidates = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# # target = 27
# # print(s.combinationSum2(candidates, target))

# candidates = [
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
# ]
# target = 30
# print(s.combinationSum2(candidates, target))
