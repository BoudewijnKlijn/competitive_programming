import os
import re

file_path = os.path.join('HC_2019_Qualification', 'input', 'b_lovely_landscapes.txt')

with open(file_path, 'r') as f:
    file_contents = f.read()

# Generator implementation (maybe better for larger inputs).
regex_group_iterator = re.finditer(r'(t[a-z\d]+)', file_contents)
tags = map(lambda x: x.group(1), regex_group_iterator)
unique_tags = set(tags)

# unique_tags = set(re.findall(r'(t[a-z\d]+)', file_contents))

print(unique_tags)
print(len(unique_tags))
