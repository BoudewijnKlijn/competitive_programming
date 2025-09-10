from typing import List


class Solution:
    def minimumTeachings(
        self, n: int, languages: List[List[int]], friendships: List[List[int]]
    ) -> int:
        """All connected people (friendships) need to have a common language.
        That does not mean every person needs to speak the same language.
        If they already have a common language, no need to learn another language.
        Constraints are small, so can probably bruteforce.
        """
        languages = [set()] + [set(lang) for lang in languages]
        option_for_lesson = set()
        for friend_a, friend_b in friendships:
            if languages[friend_a] & languages[friend_b]:
                # friends can already communicate. no need to add language.
                continue
            option_for_lesson.add(friend_a)
            option_for_lesson.add(friend_b)

        # find best language to teach. minimum lessons.
        # everyone that cannot commmunicate needs to learn the language if they cannot already.
        best = len(option_for_lesson)
        for language in range(1, n + 1):
            n_lessons = 0
            for student in option_for_lesson:
                if language not in languages[student]:
                    n_lessons += 1
            if n_lessons < best:
                best = n_lessons
        return best


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1733"
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
        funcs=["minimumTeachings"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
