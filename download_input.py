import datetime
import os
import sys
import requests


YEAR = 2020


# load env vars
with open('.env', 'r') as f:
    var_dict = dict()
    lines = f.read().split('\n')
    for line in lines:
        if line[0] == '#':
            continue
        k, v = map(str.strip, line.split('='))
        var_dict.update({k: v})
os.environ.update(var_dict)


# get day
try:
    day = int(sys.argv[1])
except IndexError:
    print('Missing day input. Using day of month of today.')
    day = datetime.datetime.today().day
except Exception as e:
    print(e)
    day = datetime.datetime.today().day


# download data
link = f'https://adventofcode.com/{YEAR}/day/{day}/input'
cookies = {'session': os.getenv('session')}
r = requests.get(link, cookies=cookies)
contents = r.text
if r.status_code == 200:
    file_name = f'input{day}.txt'
    with open(file_name, 'w') as f:
        contents_written = f.write(contents)
    if contents_written == len(contents):
        exit('Download complete')
exit('Download failed!')
