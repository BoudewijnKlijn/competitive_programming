import sys
import os

# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists((file_name := sys.argv[1])):
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__
