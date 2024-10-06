class Solution:
    def areSentencesSimilar(self, sentence1: str, sentence2: str) -> bool:
        # always make s1 the shorter sentence
        if len(sentence1) > len(sentence2):
            sentence1, sentence2 = sentence2, sentence1

        splits1 = sentence1.split()
        splits2 = sentence2.split()

        # check insert before sentence1
        if splits2[-len(splits1) :] == splits1:
            return True
        # check insert after sentence1
        if splits2[: len(splits1)] == splits1:
            return True

        # check insert somewhere in the middle of sentence1
        for insert_position in range(1, len(splits1)):
            if (
                splits2[:insert_position] == splits1[:insert_position]
                and splits2[-(len(splits1) - insert_position) :]
                == splits1[-(len(splits1) - insert_position) :]
            ):
                return True

        # otherwise false
        return False


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["areSentencesSimilar"],
        data_file="leetcode_1813_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
