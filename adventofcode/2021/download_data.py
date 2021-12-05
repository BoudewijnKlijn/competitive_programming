from aocd import get_data
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Get most recent data. Let function determine what that is.
data = get_data()

# Write data to file.
with open('input.txt', 'w') as f:
    f.write(data)
