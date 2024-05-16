import re
from math import prod


def is_part_accepted(workflows, rating):
    workflow_name = "in"
    while workflow_name not in ["A", "R"]:
        workflow = workflows[workflow_name]
        n_steps = workflow.count(",") + 1
        for i, step in enumerate(workflow.split(","), start=1):
            if i == n_steps:
                workflow_name = step
                break

            pattern = r"(?P<attribute>\w+)(?P<operator>[<>])(?P<value>\d+):(?P<new_workflow_name>\w+)"
            result = re.search(pattern, step)
            result = dict(result.groupdict())
            code = f'rating.get("{result.get("attribute")}") {result.get("operator")} {result.get("value")}'
            if eval(code):
                workflow_name = result["new_workflow_name"]
                break

    if workflow_name == "A":
        return True
    return False


def part1(content):
    workflows, ratings = content.strip().split("\n\n")
    workflows = workflows.split("\n")
    workflows = {
        workflow.split("{")[0]: workflow[:-1].split("{")[1] for workflow in workflows
    }

    ratings = ratings.split("\n")

    ans = 0
    for rating in ratings:
        rating = eval("dict(" + rating[1:-1] + ")")
        if is_part_accepted(workflows, rating):
            ans += sum(rating.values())

    return ans


def part2(content):
    """Each rating has 4 attributes and each can have values from 1 to 4000.
    In total there are 4000 ** 4 possible ratings = 256_000_000_000_000 combinations.
    Obviously I cannot test all of them.

    We don't need to test all of them. We need to construct the binary tree, until each leave is A or R.
    Then we traverse the tree, and remember the splits that we pass.
    Instead of a single rating we test a range of ratings."""
    workflows, _ = content.strip().split("\n\n")
    workflows = workflows.split("\n")
    workflows = {
        workflow.split("{")[0]: workflow[:-1].split("{")[1] for workflow in workflows
    }

    true_conditions = list()
    false_conditions = list()
    ans = traverse(workflows, "in", true_conditions, false_conditions)

    return ans


def traverse(workflows, workflow_name, true_conditions, false_conditions):
    if workflow_name == "A":
        return calculate_combinations_based_on_conditions(
            true_conditions, false_conditions
        )
    elif workflow_name == "R":
        return 0

    workflow = workflows[workflow_name]
    steps = workflow.split(",")
    n_steps = len(steps)
    ans = 0
    for i, step in enumerate(steps, start=1):
        if i == n_steps:
            # the last step in the workflow is only a name; it has no conditions
            new_workflow_name = step
            ans += traverse(
                workflows, new_workflow_name, true_conditions, false_conditions.copy()
            )
            continue

        pattern = r"(?P<attribute>\w+)(?P<operator>[<>])(?P<value>\d+):(?P<new_workflow_name>\w+)"
        result = re.search(pattern, step)
        result = dict(result.groupdict())
        for boolean in [True, False]:
            condition = (
                result.get("attribute"),
                result.get("operator"),
                result.get("value"),
            )
            if boolean:
                ans += traverse(
                    workflows,
                    result["new_workflow_name"],
                    true_conditions + [condition],
                    false_conditions.copy(),
                )
            else:
                false_conditions = false_conditions.copy() + [condition]

    return ans


def calculate_combinations_based_on_conditions(true_conditions, false_conditions):
    combinations = list()
    for letter in "xmas":
        valid = set(range(1, 4001))
        # keep the values that correspond with the true conditions
        for condition_letter, operator, value in true_conditions:
            if letter != condition_letter:
                continue
            if operator == "<":
                valid = valid.intersection(set(range(1, int(value))))
            else:
                valid = valid.intersection(set(range(int(value) + 1, 4001)))
        # remove the values that correspond with the false conditions
        for condition_letter, operator, value in false_conditions:
            if letter != condition_letter:
                continue
            if operator == "<":
                valid = valid.difference(set(range(1, int(value))))
            else:
                valid = valid.difference(set(range(int(value) + 1, 4001)))

        combinations.append(len(valid))

    return prod(combinations)


if __name__ == "__main__":
    SAMPLE = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

    assert part1(SAMPLE) == 19114

    CONTENT = open("day19.txt").read().strip()

    print(part1(CONTENT))

    assert calculate_combinations_based_on_conditions([], []) == 4000**4
    assert (
        calculate_combinations_based_on_conditions([("x", "<", "3001")], [])
        == 4000**3 * 3000
    )
    assert (
        calculate_combinations_based_on_conditions(
            [("x", "<", "3001")], [("x", "<", "1001")]
        )
        == 4000**3 * 2000
    )

    assert part2(SAMPLE) == 167409079868000

    print(part2(CONTENT))
