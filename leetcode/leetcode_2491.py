from collections import Counter
from math import prod
from typing import List


class Solution:
    def dividePlayers(self, skill: List[int]) -> int:
        counts = Counter(skill)

        n_players = len(skill)
        n_teams = n_players // 2
        sum_skill = sum(
            map(prod, counts.items())
        )  # same as sum(skill), but maybe faster for large inputs
        team_skill, remainder = divmod(sum_skill, n_teams)
        if remainder != 0:
            return -1
        if any(player_skill >= team_skill for player_skill in counts):
            return -1

        chemistry_sum = 0
        while counts:
            key, value = counts.popitem()
            # If key is half of team_skill then it should appear even times in skills.
            if 2 * key == team_skill and value % 2 == 0:
                chemistry_sum += key * key * value // 2
                continue
            # Get counterpart, and remove that as well.
            elif counts.get(team_skill - key) == value:
                counts.pop(team_skill - key)
                chemistry_sum += (team_skill - key) * key * value
                continue
            # Otherwise, not possible.
            return -1
        return chemistry_sum


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["dividePlayers"],
        data_file="leetcode_2491_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
