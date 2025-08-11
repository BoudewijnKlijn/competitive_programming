import os


def solve():
    n = int(input())
    player_score = {}
    rounds = list()
    for round_ in range(n):
        player, score = input().split()
        score = int(score)
        rounds.append((player, score))
        prev_score = player_score.get(player, 0)
        new_score = prev_score + score
        player_score[player] = new_score
    max_score = None
    players_with_max_score = None
    for player, score in player_score.items():
        if max_score is None:
            max_score = score
            players_with_max_score = [player]
        elif score > max_score:
            max_score = score
            players_with_max_score = [player]
        elif score == max_score:
            players_with_max_score.append(player)
    player_score = {}
    for player, score in rounds:
        if player not in players_with_max_score:
            continue
        prev_score = player_score.get(player, 0)
        new_score = prev_score + score
        player_score[player] = new_score
        if new_score >= max_score:
            print(player)
            break


if __name__ == "__main__":
    MULTIPLE_TESTS = False
    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())
        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
