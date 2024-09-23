from typing import List


class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        """first simplify dictionary terms. (terms are unique but can overlap)
        if a longer term can be constructed of smaller terms, thats always better
        which is funny, because its the same problem but with zero characters leftover
        --> nice thought but it slows script down!
        remove terms that don't appear in string

        check if string starts with one of terms in dictionary
        if so, cut that part from the string, and solve the remainder
        if not, remove one character: increase answer with 1, and solve remainder

        tried different versions to optimize speed
        """
        # # simplify dict
        # remove = set()

        # for i, term in enumerate(dictionary):

        #     # # remove terms which can be reconstructed from other parts (without leftovers)
        #     # self.cache = {"": 0}
        #     # n_leftover = self.inner(term, dictionary[:i] + dictionary[i + 1 :])
        #     # if n_leftover == 0:
        #     #     remove.add(term)

        #     # remove terms that don't appear in string
        #     if not term in s:
        #         remove.add(term)

        # for x in remove:
        #     dictionary.remove(x)

        # faster to create new list with terms present than to remove terms
        self.dictionary = []
        for term in dictionary:
            if term in s:
                self.dictionary.append(term)
        self.dictionary.sort(key=len)  # faster to use the short terms first

        self.cache = {"": 0}
        # for length in range(1, len(s) + 1):
        #     self.inner(s[-length:])
        # return self.cache[s]
        return self.inner(s)

    def inner(self, s):
        if s in self.cache:
            return self.cache[s]

        ans = 1 + self.inner(s[1:])
        for term in self.dictionary:
            if s.startswith(term):
                n_leftover = self.inner(s[len(term) :])
                ans = min(ans, n_leftover)
                if ans == 0:
                    # early stopping: cannot improve further
                    break
        self.cache[s] = ans
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minExtraChar"],
        data_file="leetcode_2707_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
