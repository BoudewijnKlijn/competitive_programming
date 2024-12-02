class Solution:
    def isPrefixOfWord(self, sentence: str, searchWord: str) -> int:
        words = sentence.split()
        for i, word in enumerate(words, start=1):
            if word.startswith(searchWord):
                return i
        return -1
