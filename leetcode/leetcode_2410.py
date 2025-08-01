from collections import Counter, deque
from typing import List


class Solution:
    def matchPlayersAndTrainers(self, players: List[int], trainers: List[int]) -> int:
        # return self.using_dicts(players, trainers)
        # return self.using_stack(players, trainers)
        return self.just_sorting_one_pass(players, trainers)

    def just_sorting_one_pass(self, players: List[int], trainers: List[int]) -> int:
        players = sorted(players)
        trainers = sorted(trainers)

        trainer_id = 0
        n = len(trainers)
        ans = 0
        for player in players:
            while trainer_id < n and trainers[trainer_id] < player:
                trainer_id += 1
            if trainer_id < n:
                ans += 1
            else:
                break
            trainer_id += 1
        return ans

    def using_stack(self, players: List[int], trainers: List[int]) -> int:
        count_players = sorted(Counter(players).items())
        count_trainers = deque(sorted(Counter(trainers).items()))

        ans = 0
        for player_level, player_count in count_players:
            while player_count and count_trainers:
                trainer_level, trainer_count = count_trainers.popleft()
                if trainer_level < player_level:
                    continue
                if trainer_count >= player_count:
                    ans += player_count
                    count_trainers.appendleft(
                        (trainer_level, trainer_count - player_count)
                    )
                    player_count = 0
                else:
                    ans += trainer_count
                    player_count -= trainer_count
        return ans

    def using_dicts(self, players: List[int], trainers: List[int]) -> int:
        count_players = dict(sorted(Counter(players).items()))
        count_trainers = dict(sorted(Counter(trainers).items()))

        ans = 0
        for player_level, player_count in count_players.items():
            while count_trainers and player_count:
                remove = set()
                for trainer_level, trainer_count in count_trainers.items():
                    if trainer_level >= player_level:
                        if player_count > trainer_count:
                            ans += trainer_count
                            player_count -= trainer_count
                            count_trainers[trainer_level] = 0
                        else:
                            ans += player_count
                            count_trainers[trainer_level] = trainer_count - player_count
                            player_count = 0
                        if count_trainers[trainer_level] == 0:
                            remove.add(trainer_level)
                        if player_count == 0:
                            break
                    else:
                        remove.add(trainer_level)

                # remove trainers which have no spot left
                for trainer_level in remove:
                    del count_trainers[trainer_level]

        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "matchPlayersAndTrainers",
            "using_stack",
            "using_dicts",
            "using_stack",
            "just_sorting_one_pass",
        ],
        data_file="leetcode_2410_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
