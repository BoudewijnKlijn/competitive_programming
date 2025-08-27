from collections import deque


def is_ordered_correctly(update, ordering_rules_set):
    n = len(update)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if (
                f"{update[i]}|{update[j]}" not in ordering_rules_set
                or f"{update[j]}|{update[i]}" in ordering_rules_set
            ):
                return False
    return True


def part1(contents):
    ordering_rules, updates = contents.split("\n\n")
    ordering_rules_set = set(ordering_rules.split("\n"))
    ordering_rules = [
        (int(before), int(after))
        for before, after in map(lambda x: x.split("|"), ordering_rules.split("\n"))
    ]
    updates = [list(map(int, line.split(","))) for line in updates.split("\n")]

    ans = 0
    for update in updates:
        if is_ordered_correctly(update, ordering_rules_set):
            ans += update[len(update) // 2]
    return ans


def order(relevant_rules, ordering_rules_set):
    """Loop over the rules that are in some update.
    If number is smaller than a number, insert it.
    Double check if not larger than any number that comes after it."""
    queue = deque(relevant_rules)
    all_sorted = list()
    while queue:
        before, after = queue.popleft()
        if not all_sorted:
            all_sorted.append(before)
            all_sorted.append(after)
            continue
        if before in all_sorted:
            pass
        else:
            for i, other in enumerate(all_sorted):
                if f"{before}|{other}" in ordering_rules_set:
                    # double check if in accordance with other rules
                    for other2 in all_sorted[i + 1 :]:
                        assert (
                            f"{other2}|{before}" not in ordering_rules_set
                        ), f"{other2}|{before} not correct"
                    all_sorted.insert(i, before)
                    break
            if before not in all_sorted:
                all_sorted.append(before)
        if after in all_sorted:
            pass
        else:
            for i, other in enumerate(all_sorted):
                if f"{after}|{other}" in ordering_rules_set:
                    # double check if in accordance with other rules
                    for other2 in all_sorted[i + 1 :]:
                        assert (
                            f"{other2}|{after}" not in ordering_rules_set
                        ), f"{other2}|{after} not correct"
                    all_sorted.insert(i, after)
                    break
            if after not in all_sorted:
                all_sorted.append(after)

    assert is_ordered_correctly(all_sorted, ordering_rules_set)
    return all_sorted


def part2(contents):
    ordering_rules, updates = contents.split("\n\n")
    ordering_rules_set = set(ordering_rules.split("\n"))
    ordering_rules = [
        (int(before), int(after))
        for before, after in map(lambda x: x.split("|"), ordering_rules.split("\n"))
    ]
    updates = [list(map(int, line.split(","))) for line in updates.split("\n")]

    # dont seem to be able to sort all updates at once
    # sort only the number of one specific update that is not correctly ordered
    ans = 0
    for update in updates:
        if not is_ordered_correctly(update, ordering_rules_set):
            sorted_correctly = order(
                ((a, b) for a, b in ordering_rules if a in update and b in update),
                ordering_rules_set,
            )
            ans += sorted_correctly[len(sorted_correctly) // 2]
    return ans


if __name__ == "__main__":

    sample = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    assert part1(sample) == 143

    with open("2024/day5.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 123

    ans2 = part2(contents)
    print(ans2)
