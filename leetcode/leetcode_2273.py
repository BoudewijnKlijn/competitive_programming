from typing import List


class Solution:
    def removeAnagrams(self, words: List[str]) -> List[str]:
        ans = list()
        sorted_ans = list()
        for word in words:
            sorted_word = "".join(sorted(word))
            if sorted_ans and sorted_word == sorted_ans[-1]:
                continue
            else:
                ans.append(word)
                sorted_ans.append(sorted_word)
        return ans
