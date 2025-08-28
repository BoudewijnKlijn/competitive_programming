import os
from collections import defaultdict


def solve():
    """We start with an empty sequence, length 0.
    At every step we can either take or not take the new number.
    If we take it and it is different from the last number we had in the sequence, we can
        remove that last character because that cannot become a block anymore.
        Unless it is 1, but then we could have squashed it.
    If we take the number and it is equal, it can or is already a block. In that case
        we remove the numbers and increase ans. This way we hopefully get overlapping cases
        and use DP."""
    _ = int(input())
    a = list(map(int, input().split()))

    sequences = defaultdict(int)
    sequences[(0, 0)] = 0
    for aa in a:
        new_sequences = defaultdict(int)
        added = dict()
        for (seq_num, num_count), ans in sequences.items():
            options = list()
            # if seq_num == 0, always better to take the number

            # take the number and adjust existing sequences
            if (aa == 1 and seq_num == 0) or (
                aa == seq_num and num_count == seq_num - 1
            ):
                # always better to complete a sequence.
                # we cannot become worse from completing a block sooner rather than later.
                # adding number completes the block. no sequence left over. update ans.
                new_sequences[(0, 0)] = max(new_sequences[(0, 0)], ans + aa)
                continue

            if aa == seq_num:
                options.append((seq_num, num_count + 1, ans))
                # # adding number, but block not complete. ans does not change.
                # # only add if maybe better than what is already added
                # if (seq_num, ans) not in added or num_count + 1 > added[(seq_num, ans)]:
                #     # if we have (3,1)=2 and (3,2)=2, then there is no need to keep (3,1). it cannot become better
                #     # not sure if the lower answer, but higher count, will complete, so keep both.
                #     new_sequences[key] = max(new_sequences[key], ans)
                #     added[(seq_num, ans)] = num_count
            else:
                options.append((aa, 1, ans))
                options.append((seq_num, num_count, ans))
                # # only in this case can it be better to not take the number
                # # block is not complete. start with new number. ans does not change.
                # key = (aa, 1)
                # new_sequences[key] = max(new_sequences[key], ans)
                # # or do not take the number and keep existing sequence
                # key = (seq_num, num_count)
                # if (seq_num, ans) not in added or num_count > added[(seq_num, ans)]:
                #     # if we have (3,1)=2 and (3,2)=2, then there is no need to keep (3,1). it cannot become better
                #     # not sure if the lower answer, but higher count will complete, so keep both.
                #     new_sequences[key] = max(new_sequences[key], ans)
                #     added[(seq_num, ans)] = num_count
            for seq_num, new_num_count, ans in options:
                if (seq_num, ans) not in added or new_num_count > added[(seq_num, ans)]:
                    key = (seq_num, new_num_count)
                    new_sequences[key] = max(new_sequences[key], ans)
                    added[(seq_num, ans)] = new_num_count

        sequences = new_sequences
    print(max(sequences.values()))


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
