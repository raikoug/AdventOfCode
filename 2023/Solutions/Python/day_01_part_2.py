import aoc_utils
from pathlib import Path

day = int(Path(__file__).name.split('_')[1])
input_list = aoc_utils.get_day_input(day)


words = {
    "one" : '1',
    "two" : '2',
    "three" : '3',
    "four" : '4',
    "five" : '5',
    "six" : '6',
    "seven" : '7',
    "eight" : '8',
    "nine" : '9',
}


def is_int(ch):
    try:
        int(ch)
        return True
    except:
        return False

res = 0
for row in input_list:
    # replace words with numbers
    print(row, end=" -> ")
    n = ""

    for i,ch in enumerate(row):
        if is_int(ch):
            n += ch
        for word,value in words.items():
            if row[i:].startswith(word):
                n += value
                break
    print(n, end=" -> ")
    if len(n) == 1:
        value = int(n+n)
    else:
        value = int(n[0]+n[-1])
        
    print(value)

    res += value

print(res)
