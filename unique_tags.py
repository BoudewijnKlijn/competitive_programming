import os
import re

file_path = os.path.join('HC_2019_Qualification', 'input', 'b_lovely_landscapes.txt')

with open(file_path, 'r') as f:
    file_contents = f.read()

unique_tags = set(re.findall(r'(t[a-z\d]+)', file_contents))

print(unique_tags)
print(len(unique_tags))
