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


def get_max_asleep(df):
    guard_ids = df['id'].value_counts().to_dict()

    max_asleep = 0
    guard_id_max_asleep = None
    for guard_id, rows in guard_ids.items():
        temp = df[df['id'] == guard_id]
        asleep = temp[temp == 0].count().sum()

        if asleep >= max_asleep:
            max_asleep, guard_id_max_asleep = asleep, guard_id

    return max_asleep, guard_id_max_asleep


def get_max_minute_asleep(df, guard_id):
    temp = df[df['id'] == guard_id]
    return temp[temp == 0].count().idxmax(axis=1)


def main():
    contents = read_file('input.txt')[:-1]  # remove last item since it is empty
    ordered_contents = order_contents(contents)
    df = count_minutes_asleep(ordered_contents)

    max_asleep, guard_id_max_asleep = get_max_asleep(df)
    print(f"Max asleep is guard {guard_id_max_asleep}.")

    minute_most_asleep = get_max_minute_asleep(df, guard_id_max_asleep)
    print(f"Guard {guard_id_max_asleep} is most asleep at minute {minute_most_asleep}.")

    answer = minute_most_asleep * guard_id_max_asleep
    print(f"Answer: {answer}")
    print("minute 37 and 39 are both the same. 39 is the correct answer for some reason. 39 * 2441 = 95199")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
