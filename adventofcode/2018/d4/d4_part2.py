import time
import re
import pandas as pd


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


def time_component(line_item):
    return line_item[:18]


def get_time(line_item):
    return int(line_item[15:17])


def get_date(line_item):
    return line_item[1:11]


def order_contents(contents):
    """Bubble sort"""
    for runs in range(len(contents)-1):
        for position in range(0, len(contents)-runs-1):
            if time_component(contents[position]) > time_component(contents[position+1]):
                contents[position], contents[position+1] = contents[position+1], contents[position]
    return contents


def count_minutes_asleep(contents):
    df = pd.DataFrame(columns=['id'] + list(range(60)))

    for line_item in contents:
        if 'Guard' in line_item:
            guard = int(re.findall('[\d]+', line_item[18:])[0])
            index_date = get_date(line_item)
            new_df = pd.DataFrame([[guard] + [1]*60], index=[index_date], columns=['id'] + list(range(60)))
            df = df.append(new_df)

        elif 'asleep' in line_item:
            current_time = get_time(line_item)
            df.loc[index_date, current_time+1:] = 0

        elif 'wakes' in line_item:
            current_time = get_time(line_item)
            df.loc[index_date, current_time+1:] = 1
    return df


def count_most_asleep_specific_minute(df):
    guard_ids = df['id'].value_counts().to_dict()

    most_asleep_guard, most_asleep_minute, minute = None, 0, None
    for guard_id in guard_ids:
        temp = df[df['id'] == guard_id]
        most_asleep = temp[temp == 0].count().max()
        minute = temp[temp == 0].count().idxmax()

        if most_asleep > most_asleep_minute:
            most_asleep_minute = most_asleep
            most_asleep_guard = guard_id
            most_asleep_minute = minute

    return most_asleep_minute, most_asleep_guard


def main():
    contents = read_file('input.txt')[:-1]  # remove last item since it is empty
    ordered_contents = order_contents(contents)
    df = count_minutes_asleep(ordered_contents)

    minute, most_asleep_guard = count_most_asleep_specific_minute(df)

    answer = minute* most_asleep_guard
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
