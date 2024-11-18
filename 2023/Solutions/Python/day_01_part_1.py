from icecream import ic
import aoc_utils
from pathlib import Path

day = int(Path(__file__).name.split('_')[1])
input_list = aoc_utils.get_day_input(day)

def is_int(ch):
    try:
        int(ch)
        return True
    except:
        return False

res = 0
for row in input_list:
    n = ""
    for ch in row:
        if is_int(ch):
            n += ch
    if len(n) == 1:
        value = int(n+n)
    else:
        value = int(n[0]+n[-1])

    res += value

print(res)
