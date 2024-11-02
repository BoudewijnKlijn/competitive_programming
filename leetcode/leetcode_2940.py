class Solution:
    def isCircularSentence(self, sentence: str) -> bool:
        words = sentence.split()
        for word1, word2 in zip(words[-1:] + words[:-1], words):
            if word1[-1] != word2[0]:
                return False
        return True
