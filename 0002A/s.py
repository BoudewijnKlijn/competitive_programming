import sys
import os

# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists((file_name := sys.argv[1])):
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__

n = int(input())

# Init.
player_score = {}
rounds = list()

# Read and store input. Keep track of player scores.
for round_ in range(n):
    # Read and store input.
    player, score = input().split()
    score = int(score)
    rounds.append((player, score))

    # Calculate new score and update dict with player scores.
    prev_score = player_score.get(player, 0)
    new_score = prev_score + score
    player_score[player] = new_score

# Get players with the max score.
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

# Second loop over rounds to see who of players_with_max_score got at least max score first.
player_score = {}
for player, score in rounds:
    if player not in players_with_max_score:
        continue

    # Calculate new score and update dict.
    prev_score = player_score.get(player, 0)
    new_score = prev_score + score
    player_score[player] = new_score

    # If at least the max score, we found the answer.
    if new_score >= max_score:
        print(player)
        break
