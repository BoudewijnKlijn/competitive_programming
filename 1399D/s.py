import sys
import os

# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1]
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


def main():
    t = int(input())
    for _ in range(t):
        _ = int(input())
        s = input().strip()
        streaks = make_streaks(s)
        removed_streaks = remove_and_combine(streaks)
        print(len(removed_streaks))
        out = [0] * len(s)
        for i, streak in enumerate(removed_streaks, start=1):
            for id in streak.ids:
                out[id] = i
        print(' '.join(map(str, out)))


class Streak2:
    def __init__(self, id, ids, chars, before, after):
        self.id = id
        self.ids = ids
        self.chars = chars
        self.length = len(chars)
        self.before = before
        self.after = after

    def __repr__(self):
        return f'{self.ids=}, {self.chars=}, {self.length=}'


def make_streaks(s):
    this_id = 0
    before_id = -1
    after_id = 1
    streaks = dict()
    streak_ids = [0]
    streak_values = [s[0]]
    for i, char in enumerate(s[1:], start=1):
        same_char = char == streak_values[-1]
        if not same_char:
            streak_values.append(char)
            streak_ids.append(i)
            continue

        streaks[this_id] = Streak2(id=this_id, ids=streak_ids, chars=streak_values, before=before_id, after=after_id)
        streak_ids = [i]
        streak_values = [char]
        this_id += 1
        before_id += 1
        after_id += 1

    # end of sequence append
    streaks[this_id] = Streak2(id=this_id, ids=streak_ids, chars=streak_values, before=before_id, after=after_id)

    return streaks


def remove_and_combine(streaks):
    # removing streaks with an even length will combine the ones on the sides.
    removed_streaks = list()
    removed = True
    while removed:
        removed = False
        for i, streak in streaks.items():
            if streak.length % 2 == 0 and streaks.get(streak.before) is not None and streaks.get(streak.after):
                removed_streaks.append(streak)
                del streaks[i]
                removed = True

                # combine
                streak_before = streaks.get(streak.before)
                streak_after = streaks.get(streak.after)
                # if streak_before is not None and streak_after is not None:
                # Combine before and after streak.
                streaks[streak_before.id] = Streak2(
                    id=streak_before.id,
                    ids=streak_before.ids + streak_after.ids,
                    chars=streak_before.chars + streak_after.chars,
                    before=streak_before.before,
                    after=streak_after.after,
                )
                del streaks[streak_after.id]

                # Update the streak after streak after.
                streak_after_after = streaks.get(streak_after.after)
                if streak_after_after is not None:
                    streaks[streak_after_after.id] = Streak2(
                        id=streak_after_after.id,
                        ids=streak_after_after.ids,
                        chars=streak_after_after.chars,
                        before=streak_before.id,  # only update which streak is before
                        after=streak_after_after.after,
                    )

                break

    for _, streak in streaks.items():
        removed_streaks.append(streak)

    return removed_streaks


if __name__ == '__main__':
    main()
