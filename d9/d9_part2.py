import time


class LinkedList(object):

    def __init__(self, first_node_value):
        self.node_values = [first_node_value]
        self.next_nodes = [0]
        self.previous_nodes = [0]
        self.node_index = 0
        self.size = 1

    def move_forward(self, steps):
        for _ in range(steps):
            self.node_index = self.next_nodes[self.node_index]

    def move_backward(self, steps):
        for _ in range(steps):
            self.node_index = self.previous_nodes[self.node_index]

    def insert_node(self, value):
        """
        (1)->(2)->(3)
        1 = node before inserted node (before_node)
        2 = inserted node
        3 = node after inserted node (after_node)
        """

        # Store index of before and after node to be inserted.
        node_index_before_node = self.node_index
        node_index_after_node = self.next_nodes[self.node_index]

        # Create the node to be inserted.
        self.node_values.append(value)
        self.next_nodes.append(node_index_after_node)
        self.previous_nodes.append(node_index_before_node)
        self.size += 1

        # Adjust the next_nodes of the before node.
        self.next_nodes[node_index_before_node] = self.size - 1

        # Adjust the previous_nodes of the after_node.
        self.previous_nodes[node_index_after_node] = self.size - 1

    def remove_node(self):
        """
        (1)->(2)->(3)
        1 = node before removed node (before_node)
        2 = removed node
        3 = node after removed node (after_node)
        """

        # Store index of before and after node to be inserted.
        node_index_before_node = self.node_index
        node_index_removed_node = self.next_nodes[self.node_index]
        node_index_after_node = self.next_nodes[node_index_removed_node]

        # We don't really remove the node, we just adjust the next_nodes and previous_node of the nodes around it.
        removed_value = self.node_values[node_index_removed_node]

        # Adjust the next_nodes of the before_node.
        self.next_nodes[node_index_before_node] = node_index_after_node

        # Adjust the previous_nodes of the after_node.
        self.previous_nodes[node_index_after_node] = node_index_before_node

        return removed_value

    def show_order(self, current_node=0):
        printed = []
        while current_node not in printed:
            print(self.node_values[current_node], end=', ')
            printed.append(current_node)
            current_node = self.next_nodes[current_node]


def play_game(players, last_marble):
    board = LinkedList(0)
    players_scores = {p: 0 for p in range(1, players + 1)}
    current_player = 0

    for marble in range(1, last_marble + 1):

        current_player += 1
        if current_player > players:
            current_player = 1

        if marble % 23 == 0:
            board.move_backward(7+1)
            removed_marble = board.remove_node()
            board.move_forward(1)
            players_scores[current_player] += marble + removed_marble

        else:
            board.move_forward(1)
            board.insert_node(marble)
            board.move_forward(1)

    # board.show_order(0)
    return max(players_scores.values())


def main():
    # Examples:
    # high_score = play_game(players=9, last_marble=25)
    # high_score = play_game(players=10, last_marble=1618)
    # high_score = play_game(players=13, last_marble=7999)
    # high_score = play_game(players=17, last_marble=1104)
    # high_score = play_game(players=21, last_marble=6111)
    # high_score = play_game(players=30, last_marble=5807)

    # part1
    # high_score = play_game(players=464, last_marble=71730)

    # part2
    high_score = play_game(players=464, last_marble=7173000)

    answer = high_score
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))