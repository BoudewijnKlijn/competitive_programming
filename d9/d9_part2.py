import time


def play_game(players, last_marble):
    board = [0]*last_marble
    players_scores = {p: 0 for p in range(1, players+1)}
    current_position = 0
    current_player = 0

    size = 1

    for marble in range(1, last_marble+1):
        current_player += 1
        if current_player > players:
            current_player = 1

        if marble % 23 == 0:
            current_position = current_position - 7
            if current_position < 0:
                current_position += size

            removed_marble = board[current_position]
            size -= 1
            board = board[:current_position] + board[current_position+1:] + [0]*(last_marble+1 - size)
            players_scores[current_player] += marble + removed_marble

        else:
            insert_position = (current_position + 2) % size
            if insert_position == 0:
                insert_position = size
            board = board[:insert_position] + [marble] + board[insert_position:size] + [0]*(last_marble+1 - size)
            size += 1
            current_position = insert_position

    return max(players_scores.values())


def main():
    # Examples:
    # high_score = play_game(players=9, last_marble=25)
    # high_score = play_game(players=10, last_marble=1618)
    high_score = play_game(players=13, last_marble=7999)
    # high_score = play_game(players=17, last_marble=1104)
    # high_score = play_game(players=21, last_marble=6111)
    # high_score = play_game(players=30, last_marble=5807)

    # part1
    # high_score = play_game(players=464, last_marble=71730)

    # part2
    # high_score = play_game(players=464, last_marble=7173000)

    answer = high_score
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))