from aocd import get_data

# Get most recent data. Let function determine what that is.
data = get_data()

# Write data to file.
with open('input.txt', 'w') as f:
    f.write(data)
