import re
from itertools import cycle


def read_input(content):
    instructions, other = content.split("\n\n")

    mapping = dict()
    for line in other.split("\n"):
        key, value = line.split(" = ")
        mapping[key] = re.findall(r"\w+", value)

    return instructions, mapping


def do_step(node, instruction, mapping):
    if instruction == "L":
        return mapping[node][0]
    else:
        return mapping[node][1]


def part1(content):
    instructions, mapping = read_input(content)

    node = "AAA"
    for steps, instruction in enumerate(cycle(instructions), start=1):
        node = do_step(node, instruction, mapping)

        if node == "ZZZ":
            return steps


def part2_naive(content):
    instructions, mapping = read_input(content)

    nodes = [n for n in mapping.keys() if n.endswith("A")]
    for steps, instruction in enumerate(cycle(instructions), start=1):
        tmp = list()
        for node in nodes:
            tmp.append(do_step(node, instruction, mapping))
        nodes = tmp

        if all(n.endswith("Z") for n in nodes):
            return steps


def part2(content):
    """Solve for each starting node individually.
    Then find the least common multiple of all the steps.

    Only six starting nodes:
    - First node repeats every 18157 steps.
    - Second node repeats every 14363 steps.
    - Third node repeats every 19783 steps.
    - Fourth node repeats every 15989 steps.
    - Fifth node repeats every 19241 steps.
    - Sixth node repeats every 12737 steps.
    """
    instructions, mapping = read_input(content)
    print(len(instructions))

    starting_nodes = [n for n in mapping.keys() if n.endswith("A")]
    print(
        len(starting_nodes)
    )  # only 6 starting nodes, so we can do this partly manually

    for node_i, node in enumerate(starting_nodes):
        if node_i < 6:
            continue

        for steps, instruction in enumerate(cycle(instructions), start=1):
            node = do_step(node, instruction, mapping)

            if node.endswith("Z"):
                print(steps, "ends on Z")
                input()

    # Find the least common multiple of all the steps
    primes = get_primes_below_n(20000)
    cycles = [18157, 14363, 19783, 15989, 19241, 12737]
    for c in cycles:
        divisors = get_divisors(c, primes)
        print(c, divisors)

    # 18157 [67, 271]
    # 14363 [53, 271]
    # 19783 [73, 271]
    # 15989 [59, 271]
    # 19241 [71, 271]
    # 12737 [47, 271]

    # Every 'divisors' includes 271, so only need 271 once. Multiply 271 with all unique divisors.
    return 271 * 67 * 53 * 73 * 59 * 71 * 47


def get_divisors(n, primes):
    divisors = []
    for p in primes:
        while n % p == 0:
            n /= p
            divisors.append(p)
    return divisors


def get_primes_below_n(n):
    primes = [2]
    for i in range(3, n + 1, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)
    return primes


if __name__ == "__main__":
    SAMPLE = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

    assert part1(SAMPLE) == 2

    SAMPLE2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    assert part1(SAMPLE2) == 6

    with open("day8.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))

    SAMPLE3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    assert part2_naive(SAMPLE3) == 6

    # print(part2_naive(CONTENT))  # too slow

    print(part2(CONTENT))
