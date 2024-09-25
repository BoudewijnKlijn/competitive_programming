from collections import Counter
from typing import List


class Solution:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        """first create a tree, like the previous day (3043)
        walk the tree with the complete word and sum the scores along the way
        Counter is small optimization for duplicates in words"""
        self.tree = self.generate_tree(words)
        ans = [self.calc_score(word) for word in words]
        return ans

    def generate_tree(self, words) -> dict:
        """Use key=0 to record the count."""
        root = dict()
        for word, multiplier in Counter(words).items():
            node = root
            for char in word:
                if char not in node:
                    node[char] = {0: 0}
                node[char][0] += multiplier
                node = node[char]
        return root

    def calc_score(self, word):
        score = 0
        node = self.tree
        for char in word:
            if char in node:
                score += node[char][0]
                node = node[char]
            else:
                break
        return score


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["sumPrefixScores"],
        data_file="leetcode_2416_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
