file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day9\\input.txt'
handle = open(file, 'r')
content = handle.read()

good_content = ''
good_chars = '{},'
garbage_state = False
ignore_state = False

# to debug
count_deleted = 0
ignore_list = []
garbage_list = []
good_but_meaningless = ''

# only keep the non-garbage content
for char in content:
    if ignore_state:
        ignore_state = False
        count_deleted += 1
        ignore_list[-1] += char
        continue

    if char == '!':
        ignore_state = True
        count_deleted += 1
        ignore_list.append('!')
        continue

    if garbage_state:
        garbage_list[-1] += char
        if char != '>':
            count_deleted += 1
            continue
        else:
            garbage_state = False

    if char == '<':
        garbage_state = True
        count_deleted += 1
        garbage_list.append('<')
        continue

    if char not in good_chars:
        count_deleted += 1
        good_but_meaningless += char
        continue

    good_content += char


assert good_content.count('{') == good_content.count('}'), "Mismatch between '{' and '}'"
assert len(content) - count_deleted - len(good_content) == 0, "Some characters unaccounted for"

score = 0
group_score = 1
for char in good_content:
    if char == '}':
        group_score -= 1
        continue
    elif char == '{':
        score += group_score
        group_score += 1

print("Answer:", score)
